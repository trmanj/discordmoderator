import discord
from discord import app_commands
import os
import subprocess
import sys
from flask import Flask
from threading import Thread
from datetime import datetime

# ========== RENDER UYANIK TUTMA ==========
app = Flask('')

@app.route('/')
def home():
    return "🟢 Seedloaf Discord Bot Aktif!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_web, daemon=True).start()

# ========== DISCORD BOT ==========
class SeedloafBot(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        await self.tree.sync()
        print(f"✅ Bot hazır! Giriş: {self.user}")

bot = SeedloafBot()

# ========== KOMUTLAR ==========

@bot.tree.command(name="baslat", description="🟢 Minecraft sunucusunu başlat")
@app_commands.checks.cooldown(1, 60)
async def baslat(interaction: discord.Interaction):
    await interaction.response.defer()

    # Check if credentials are set
    username = os.getenv("SEEDLOAF_EMAIL")
    password = os.getenv("SEEDLOAF_PASSWORD")

    if not username or not password:
        await interaction.followup.send(
            "⚠️ **Seedloaf giriş bilgileri eksik!**\n"
            "Render Environment Variables'a şunları ekle:\n"
            "- `SEEDLOAF_EMAIL`\n"
            "- `SEEDLOAF_PASSWORD`",
            ephemeral=True
        )
        return

    await interaction.followup.send("🟢 **Sunucu başlatılıyor...** Bu 1-2 dakika sürebilir.")

    try:
        # Run the Selenium script
        result = subprocess.run(
            [sys.executable, "seedloaf_start.py"],
            capture_output=True,
            text=True,
            timeout=120
        )

        output = result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout

        if "Clicked start" in output or "Stop button found" in output:
            await interaction.followup.send("✅ **Sunucu başlatıldı!** 🎮")
        elif "Password is incorrect" in output:
            await interaction.followup.send("🔴 **Şifre yanlış!** Lütfen SEEDLOAF_PASSWORD kontrol et.")
        elif "Username is incorrect" in output:
            await interaction.followup.send("🔴 **Email yanlış!** Lütfen SEEDLOAF_EMAIL kontrol et.")
        else:
            await interaction.followup.send(
                f"⚠️ **Durum belirsiz.** Log:\n```{output[-500:]}```"
            )

    except subprocess.TimeoutExpired:
        await interaction.followup.send("⏱️ **Zaman aşımı!** İşlem çok uzun sürdü.")
    except Exception as e:
        await interaction.followup.send(f"💥 **Hata:** `{str(e)}`")

@bot.tree.command(name="durdur", description="🔴 Minecraft sunucusunu durdur")
@app_commands.checks.cooldown(1, 60)
async def durdur(interaction: discord.Interaction):
    await interaction.response.defer()

    username = os.getenv("SEEDLOAF_EMAIL")
    password = os.getenv("SEEDLOAF_PASSWORD")

    if not username or not password:
        await interaction.followup.send("⚠️ Giriş bilgileri eksik!", ephemeral=True)
        return

    await interaction.followup.send("🔴 **Sunucu durduruluyor...**")

    try:
        result = subprocess.run(
            [sys.executable, "seedloaf_stop.py"],
            capture_output=True,
            text=True,
            timeout=120
        )

        output = result.stdout[-1500:] if len(result.stdout) > 1500 else result.stdout

        if "Clicked stop" in output or "Start button found" in output:
            await interaction.followup.send("✅ **Sunucu durduruldu!**")
        else:
            await interaction.followup.send(
                f"⚠️ **Durum belirsiz.** Log:\n```{output[-500:]}```"
            )

    except Exception as e:
        await interaction.followup.send(f"💥 **Hata:** `{str(e)}`")

@bot.tree.command(name="durum", description="📊 Bot durumunu kontrol et")
async def durum(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📊 Seedloaf Bot Durumu",
        color=discord.Color.green(),
        timestamp=datetime.now()
    )

    embed.add_field(
        name="🤖 Bot",
        value=f"🟢 Çevrimiçi\n👤 `{bot.user}`",
        inline=True
    )

    username = os.getenv("SEEDLOAF_EMAIL")
    if username:
        embed.add_field(
            name="🔗 Seedloaf",
            value=f"🟢 Yapılandırıldı\n📧 `{username[:3]}...`",
            inline=True
        )
    else:
        embed.add_field(
            name="🔗 Seedloaf",
            value="🔴 Yapılandırılmamış!",
            inline=True
        )

    embed.add_field(
        name="📋 Komutlar",
        value="`/baslat` - Sunucuyu başlat\n`/durdur` - Sunucuyu durdur\n`/durum` - Durumu göster",
        inline=False
    )

    await interaction.response.send_message(embed=embed)

@baslat.error
async def baslat_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(
            f"⏳ **Cooldown!** `{error.retry_after:.1f}` saniye bekle.",
            ephemeral=True
        )

@durdur.error  
async def durdur_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(
            f"⏳ **Cooldown!** `{error.retry_after:.1f}` saniye bekle.",
            ephemeral=True
        )

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    print("❌ DISCORD_TOKEN bulunamadı!")
else:
    bot.run(TOKEN)

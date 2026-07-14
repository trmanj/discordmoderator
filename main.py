
# Shell paralıymış. O zaman log'ları daha detaylı yazdıralım.
# main.py'yi güncelleyelim - her şeyi log'a yazsın

main_py = '''import discord
from discord import app_commands
import os
import subprocess
import sys
from flask import Flask
from threading import Thread
from datetime import datetime
import logging

# Log ayarları
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
        logger.info(f"✅ Bot hazır! Giriş: {self.user}")

bot = SeedloafBot()

# ========== KOMUTLAR ==========

@bot.tree.command(name="baslat", description="🟢 Minecraft sunucusunu başlat")
@app_commands.checks.cooldown(1, 60)
async def baslat(interaction: discord.Interaction):
    await interaction.response.defer()
    
    username = os.getenv("SEEDLOAF_EMAIL")
    password = os.getenv("SEEDLOAF_PASSWORD")
    
    if not username or not password:
        await interaction.followup.send(
            "⚠️ **Seedloaf giriş bilgileri eksik!**\\n"
            "Render Environment Variables'a ekle:\\n"
            "- `SEEDLOAF_EMAIL`\\n"
            "- `SEEDLOAF_PASSWORD`",
            ephemeral=True
        )
        return
    
    await interaction.followup.send("🟢 **Sunucu başlatılıyor...** Bu 1-2 dakika sürebilir.")
    
    try:
        logger.info("seedloaf_start.py çalıştırılıyor...")
        result = subprocess.run(
            [sys.executable, "seedloaf_start.py"],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        stdout = result.stdout or "(boş)"
        stderr = result.stderr or "(boş)"
        returncode = result.returncode
        
        logger.info(f"Return code: {returncode}")
        logger.info(f"STDOUT: {stdout[:2000]}")
        logger.info(f"STDERR: {stderr[:2000]}")
        
        # Her durumda log'ları göster
        log_summary = f"Return: {returncode}\\nSTDOUT: {stdout[-800:]}\\nSTDERR: {stderr[-800:]}"
        
        if "tıklandı" in stdout or "tıklandı" in stderr:
            await interaction.followup.send("✅ **Sunucu başlatıldı!** 🎮")
        elif "zaten çalışıyor" in stdout or "zaten çalışıyor" in stderr:
            await interaction.followup.send("✅ **Sunucu zaten çalışıyor!**")
        elif "Giriş başarısız" in stdout or "Giriş başarısız" in stderr:
            await interaction.followup.send("🔴 **Giriş başarısız!** Email/şifre yanlış.")
        elif returncode != 0:
            await interaction.followup.send(
                f"❌ **Script hata verdi!** (code: {returncode})\\n```\\n{log_summary}\\n```"
            )
        else:
            await interaction.followup.send(
                f"⚠️ **Durum belirsiz.**\\n```\\n{log_summary}\\n```"
            )
            
    except subprocess.TimeoutExpired:
        logger.error("Zaman aşımı!")
        await interaction.followup.send("⏱️ **Zaman aşımı!** İşlem çok uzun sürdü.")
    except Exception as e:
        logger.error(f"Beklenmeyen hata: {e}")
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
        
        stdout = result.stdout or "(boş)"
        stderr = result.stderr or "(boş)"
        
        if "tıklandı" in stdout or "tıklandı" in stderr:
            await interaction.followup.send("✅ **Sunucu durduruldu!**")
        elif "zaten durmuş" in stdout or "zaten durmuş" in stderr:
            await interaction.followup.send("✅ **Sunucu zaten durmuş!**")
        else:
            await interaction.followup.send(
                f"⚠️ **Durum belirsiz.**\\n```\\n{stdout[-800:]}\\n{stderr[-800:]}\\n```"
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
        value=f"🟢 Çevrimiçi\\n👤 `{bot.user}`",
        inline=True
    )
    
    username = os.getenv("SEEDLOAF_EMAIL")
    if username:
        embed.add_field(
            name="🔗 Seedloaf",
            value=f"🟢 Yapılandırıldı\\n📧 `{username[:3]}...`",
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
        value="`/baslat` - Sunucuyu başlat\\n`/durdur` - Sunucuyu durdur\\n`/durum` - Durumu göster",
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
    logger.error("DISCORD_TOKEN bulunamadı!")
else:
    bot.run(TOKEN)
'''

with open('/mnt/agents/output/main.py', 'w') as f:
    f.write(main_py)

print("✅ main.py güncellendi!")
print("Şimdi GitHub'a push et ve Render'da redeploy yap.")
print("Yeni log'lar Discord'da gösterilecek.")

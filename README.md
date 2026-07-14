# 🎮 Seedloaf Discord Bot

Seedloaf Minecraft sunucusunu Discord'dan başlatma/durdurma botu.
**Seedloaf'ın public API'si olmadığı için Selenium ile tarayıcı otomasyonu kullanıyor.**

## 🚀 Kurulum

### 1. Discord Bot Oluştur
- [Discord Developer Portal](https://discord.com/developers/applications) git
- Yeni Application oluştur → Bot ekle
- Token'ı kopyala
- OAuth2 URL Generator:
  - Scopes: `bot`, `applications.commands`
  - Bot Permissions: `Send Messages`, `Use Slash Commands`
  - URL'yi aç, sunucuna ekle

### 2. Render'a Deploy
1. Bu repo'yu **GitHub'a yükle**
2. [Render.com](https://render.com) → New Web Service → GitHub repo
3. **Environment Variables** ekle:
   - `DISCORD_TOKEN` = Discord bot token
   - `SEEDLOAF_EMAIL` = Seedloaf hesap email
   - `SEEDLOAF_PASSWORD` = Seedloaf hesap şifre
4. Deploy et!

## 📋 Komutlar

| Komut | Açıklama |
|-------|----------|
| `/baslat` | Minecraft sunucusunu başlat |
| `/durdur` | Minecraft sunucusunu durdur |
| `/durum` | Bot durumunu göster |

## ⚠️ Önemli Notlar

- Her komutta 60 saniye cooldown var
- Render ücretsiz plan 15 dk idle sonra uyur → [UptimeRobot](https://uptimerobot.com) ile ping at
- Selenium ile tarayıcı açıldığı için işlem 1-2 dk sürebilir

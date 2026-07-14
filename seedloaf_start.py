import os
import sys
import asyncio
from playwright.async_api import async_playwright

async def start_server():
    email = os.getenv("SEEDLOAF_EMAIL")
    password = os.getenv("SEEDLOAF_PASSWORD")
    
    if not email or not password:
        print("SEEDLOAF_EMAIL ve SEEDLOAF_PASSWORD gerekli!")
        return False
    
    async with async_playwright() as p:
        # RENDER İÇİN: headless-shell kullan (daha hafif)
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )
        
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            print("Seedloaf'a gidiliyor...")
            await page.goto("https://accounts.seedloaf.com/sign-in")
            await page.wait_for_load_state("networkidle")
            
            print("Email giriliyor...")
            await page.fill("#identifier-field", email)
            await page.press("#identifier-field", "Enter")
            await page.wait_for_timeout(3000)
            
            print("Password giriliyor...")
            await page.fill("#password-field", password)
            await page.press("#password-field", "Enter")
            await page.wait_for_timeout(5000)
            
            if "dashboard" not in page.url:
                print(f"Giriş başarısız! URL: {page.url}")
                await browser.close()
                return False
            
            print("Dashboard'a girildi!")
            
            # Start World butonunu bekle ve tıkla
            try:
                await page.click("button.btn-primary", timeout=15000)
                print("✅ Start World butonuna tıklandı!")
                await page.wait_for_timeout(5000)
                await browser.close()
                return True
            except Exception as e:
                print(f"Buton bulunamadı: {e}")
                print("Sunucu zaten çalışıyor olabilir")
                await browser.close()
                return True
                
        except Exception as e:
            print(f"❌ Hata: {e}")
            await browser.close()
            return False

if __name__ == "__main__":
    result = asyncio.run(start_server())
    sys.exit(0 if result else 1)

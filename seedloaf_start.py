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
        # Chromium'u indir ve başlat
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        try:
            # Seedloaf'a git
            await page.goto("https://accounts.seedloaf.com/sign-in")
            await page.wait_for_load_state("networkidle")
            
            # Giriş yap
            await page.fill("#identifier-field", email)
            await page.press("#identifier-field", "Enter")
            await page.wait_for_timeout(3000)
            
            await page.fill("#password-field", password)
            await page.press("#password-field", "Enter")
            await page.wait_for_timeout(5000)
            
            # Dashboard'a yönlendirildi mi kontrol et
            if "dashboard" not in page.url:
                print("Giriş başarısız!")
                await browser.close()
                return False
            
            # Start World butonuna tıkla
            try:
                await page.click("button.btn-primary", timeout=10000)
                print("Start World butonuna tıklandı!")
                await page.wait_for_timeout(3000)
                await browser.close()
                return True
            except:
                # Buton yoksa, zaten çalışıyor olabilir
                print("Start butonu bulunamadı - sunucu zaten çalışıyor olabilir")
                await browser.close()
                return True
                
        except Exception as e:
            print(f"Hata: {e}")
            await browser.close()
            return False

if __name__ == "__main__":
    result = asyncio.run(start_server())
    sys.exit(0 if result else 1)

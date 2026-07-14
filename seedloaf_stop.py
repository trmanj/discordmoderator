import os
import sys
import asyncio
from playwright.async_api import async_playwright

async def stop_server():
    email = os.getenv("SEEDLOAF_EMAIL")
    password = os.getenv("SEEDLOAF_PASSWORD")
    
    if not email or not password:
        print("SEEDLOAF_EMAIL ve SEEDLOAF_PASSWORD gerekli!")
        return False
    
    async with async_playwright() as p:
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
            await page.goto("https://accounts.seedloaf.com/sign-in")
            await page.wait_for_load_state("networkidle")
            
            await page.fill("#identifier-field", email)
            await page.press("#identifier-field", "Enter")
            await page.wait_for_timeout(3000)
            
            await page.fill("#password-field", password)
            await page.press("#password-field", "Enter")
            await page.wait_for_timeout(5000)
            
            if "dashboard" not in page.url:
                print("Giriş başarısız!")
                await browser.close()
                return False
            
            try:
                await page.click("button.btn-error", timeout=15000)
                print("✅ Stop World butonuna tıklandı!")
                await page.wait_for_timeout(5000)
                await browser.close()
                return True
            except Exception as e:
                print(f"Stop butonu bulunamadı: {e}")
                print("Sunucu zaten durmuş olabilir")
                await browser.close()
                return True
                
        except Exception as e:
            print(f"❌ Hata: {e}")
            await browser.close()
            return False

if __name__ == "__main__":
    result = asyncio.run(stop_server())
    sys.exit(0 if result else 1)

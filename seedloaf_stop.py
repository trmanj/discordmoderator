import os
import sys
import asyncio
from playwright.async_api import async_playwright

async def stop_server():
    email = os.getenv("SEEDLOAF_EMAIL")
    password = os.getenv("SEEDLOAF_PASSWORD")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
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
            
            # Stop World butonuna tıkla (kırmızı buton)
            try:
                await page.click("button.btn-error", timeout=10000)
                print("Stop World butonuna tıklandı!")
                await page.wait_for_timeout(3000)
                await browser.close()
                return True
            except:
                print("Stop butonu bulunamadı - sunucu zaten durmuş olabilir")
                await browser.close()
                return True
                
        except Exception as e:
            print(f"Hata: {e}")
            await browser.close()
            return False

if __name__ == "__main__":
    result = asyncio.run(stop_server())
    sys.exit(0 if result else 1)

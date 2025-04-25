import asyncio
from playwright.async_api import async_playwright
import json
import os
import random

USERNAME = "solomonaspire2323"
PASSWORD = "Password1234scrapy"
LOGIN_URL = "https://breachforums.st/member?action=login"

# จะเก็บ cookies ไว้ตรงนี้
COOKIES_FILE = os.path.join(os.path.dirname(__file__), "..", "cookies.json")

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            viewport={"width": 1280, "height": 800},
            java_script_enabled=True,
            ignore_https_errors=True
        )
        page = await context.new_page()

        # เข้าหน้า Login โดยไม่ต้อง retry หลายรอบแล้ว
        try:
            print("🌐 เข้าหน้า Login ...")
            await page.goto(LOGIN_URL, wait_until="networkidle", timeout=60000)
        except Exception as e:
            print(f"⚠️ โหลดไม่สำเร็จ: {e}")
            return

        # กรอกข้อมูลและ CAPTCHA ครั้งเดียว
        print(f"\n🔁 Attempt 1/1")
        await page.mouse.move(500, 400)
        await asyncio.sleep(random.uniform(0.5, 1.5))

        await page.click('input[name="username"]')
        await page.keyboard.type(USERNAME, delay=random.randint(50, 150))
        await asyncio.sleep(random.uniform(0.3, 0.8))

        await page.click('input[name="password"]')
        await page.keyboard.type(PASSWORD, delay=random.randint(50, 150))
        await asyncio.sleep(random.uniform(1.2, 2.5))

        await page.wait_for_selector('img[src*="captcha"]')
        captcha_img = await page.query_selector('img[src*="captcha"]')
        captcha_bytes = await captcha_img.screenshot()

        with open(f"captcha_debug_attempt1.png", "wb") as f:
            f.write(captcha_bytes)
        print(f"📸 Saved CAPTCHA: captcha_debug_attempt1.png")

        # กรอก CAPTCHA เองที่นี่
        captcha_text = input("📥 กรุณากรอก CAPTCHA จากภาพ captcha_debug_attempt1.png: ").strip()

        if not captcha_text or len(captcha_text) < 3:
            print("⚠️ CAPTCHA อ่านไม่ได้หรือสั้นเกินไป")
            captcha_text = "invalid"

        await page.fill('input#imagestring', captcha_text)
        await asyncio.sleep(random.uniform(1.0, 2.0))
        await page.click('input[type="submit"]')
        await page.wait_for_load_state("networkidle")

        title = await page.title()
        if "Login" not in title:
            print(f"🎉 Login successful! Page title: {title}")

            # ✅ บันทึก cookies
            cookies = await context.cookies()
            with open(COOKIES_FILE, "w") as f:
                json.dump(cookies, f, indent=2)
            print(f"🍪 Cookies ถูกบันทึกไว้ที่: {COOKIES_FILE}")

        else:
            print("❌ CAPTCHA incorrect or login failed.")

        print("\n🖥️ Browser จะเปิดค้างไว้เพื่อดูผลลัพธ์")
        input("📌 กด Enter เพื่อปิด browser และออกจากโปรแกรม...")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())

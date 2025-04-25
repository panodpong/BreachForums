import subprocess
import sys
import os

# 1. Login with Playwright to get cookies
print("🔐 Starting Playwright login to get cookies...")
playwright_process = subprocess.Popen([sys.executable, "playwright_login/login.py"])
playwright_process.communicate()

# 2. Check if cookies.json was created successfully
cookies_path = os.path.join(os.getcwd(), "cookies.json")
if not os.path.exists(cookies_path):
    print("⚠️ Error: cookies.json not found! Make sure Playwright login was successful.")
    sys.exit(1)

# 3. Crawl with Scrapy after login (using cookies from Playwright)
print("🕷️ Starting Scrapy spider...")
scrapy_process = subprocess.Popen([sys.executable, "-m", "scrapy", "crawl", "forum_search"], cwd="scrapy_spider")
scrapy_process.communicate()

print("✅ Process completed successfully!")

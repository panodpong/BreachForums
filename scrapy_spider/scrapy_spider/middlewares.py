import json
import os

class CookieInjectorMiddleware:
    def __init__(self):
        cookies_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../cookies.json"))
        if not os.path.exists(cookies_path):
            raise FileNotFoundError(f"ไม่พบไฟล์ cookies.json ที่ {cookies_path}")

        with open(cookies_path, "r") as f:
            raw_cookies = json.load(f)
            self.cookies = {cookie["name"]: cookie["value"] for cookie in raw_cookies}

    def process_request(self, request, spider):
        request.cookies = self.cookies

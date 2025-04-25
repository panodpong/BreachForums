import scrapy

class ForumSearchSpider(scrapy.Spider):
    name = "forum_search"
    allowed_domains = ["breachforums.st"]
    start_urls = [
        "https://breachforums.st/Forum-Cracked-Accounts?page=1"
    ]

    def parse(self, response):
        current_page = response.url.split("page=")[-1] if "page=" in response.url else "1"
        self.logger.info(f"📄 กำลังดึง Search Results หน้า {current_page}")

        # ดึงลิงก์ทั้งหมด
        # links = response.xpath('//a/@href').getall()
        links = response.xpath('//a').extract()
        filename = f"search-page{current_page}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            for link in links:
                f.write(link + "\n")

        # หาปุ่ม Next
        next_page = response.xpath('//a[contains(@class, "pagination_next")]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            self.logger.info(f"➡️ ไปต่อที่หน้า: {next_page_url}")
            yield scrapy.Request(next_page_url, callback=self.parse)
        else:
            self.logger.info("🏁 ถึงหน้าสุดท้ายแล้ว")
# import scrapy

# class ForumSearchSpider(scrapy.Spider):
#     name = "forum_search"
#     allowed_domains = ["breachforums.st"]
#     start_urls = [
#         "https://breachforums.st/Forum-Databases?page=1"
#     ]

#     def parse(self, response):
#         current_page = response.url.split("page=")[-1] if "page=" in response.url else "1"
#         self.logger.info(f"📄 กำลังดึง Search Results หน้า {current_page}")

#         # ดึงลิงก์ทั้งหมด พร้อมข้อความจาก <a> 
#         links = response.xpath('//a')
        
#         filename = f"search-page{current_page}.txt"
#         with open(filename, "w", encoding="utf-8") as f:
#             for link in links:
#                 # ดึง href และข้อความในแท็ก <a>
#                 href = link.xpath('@href').get()  # ดึง href attribute
#                 text = link.xpath('text()').get()  # ดึงข้อความในแท็ก <a>

#                 # เช็คว่า href และข้อความมีค่าหรือไม่
#                 if href and text:
#                     f.write(f"{{{href}}}{{{text}}}\n")

#         # หาปุ่ม Next
#         next_page = response.xpath('//a[contains(@class, "pagination_next")]/@href').get()
#         if next_page:
#             next_page_url = response.urljoin(next_page)
#             self.logger.info(f"➡️ ไปต่อที่หน้า: {next_page_url}")
#             yield scrapy.Request(next_page_url, callback=self.parse)
#         else:
#             self.logger.info("🏁 ถึงหน้าสุดท้ายแล้ว")

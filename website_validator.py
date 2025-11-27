import os
import requests
from bs4 import BeautifulSoup
import time

class WebsiteValidator:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.results = {
            'passed': [],
            'warnings': [],
            'errors': []
        }
    
    def log_result(self, category, message):
        self.results[category].append(message)
        status = "PASS" if category == 'passed' else "WARN" if category == 'warnings' else "FAIL"
        print(f"[{status}] {message}")
    
    def check_page_load(self, url):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return True, response.text
            else:
                return False, f"Status code: {response.status_code}"
        except Exception as e:
            return False, str(e)
    
    def validate_seo_metadata(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        
        # Check title
        title = soup.find('title')
        if title:
            title_text = title.get_text().strip()
            title_len = len(title_text)
            if 40 <= title_len <= 60:
                self.log_result('passed', f"Title length OK: {title_len} chars")
            else:
                self.log_result('warnings', f"Title length {title_len} chars (should be 40-60)")
        
        # Check meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            desc = meta_desc.get('content', '').strip()
            desc_len = len(desc)
            if 120 <= desc_len <= 160:
                self.log_result('passed', f"Description length OK: {desc_len} chars")
            else:
                self.log_result('warnings', f"Description length {desc_len} chars (should be 120-160)")
        else:
            self.log_result('errors', "No meta description found")
    
    def validate_images(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        images = soup.find_all('img')
        
        broken_images = 0
        for img in images:
            src = img.get('src', '')
            if src and not src.startswith(('http', '//')):
                img_path = src.lstrip('/')
                if not os.path.exists(img_path):
                    broken_images += 1
                    self.log_result('errors', f"Broken image: {src}")
        
        if broken_images == 0:
            self.log_result('passed', "All images loaded correctly")
    
    def validate_phone_links(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        phone_links = soup.find_all('a', href=lambda x: x and 'tel:' in x)
        
        if phone_links:
            self.log_result('passed', f"Phone links found: {len(phone_links)}")
        else:
            self.log_result('warnings', "No phone links found")
    
    def run_basic_test(self):
        test_pages = [
            "",
            "services.html",
            "services/ada-compliant-showers.html"
        ]
        
        print("BASIC WEBSITE VALIDATION")
        print("=" * 50)
        
        for page in test_pages:
            url = f"{self.base_url}/{page}" if page else self.base_url
            print(f"\nTesting: {url}")
            print("-" * 40)
            
            success, html = self.check_page_load(url)
            if success:
                self.log_result('passed', f"Page loads successfully")
                self.validate_seo_metadata(url, html)
                self.validate_images(url, html)
                self.validate_phone_links(html)
            else:
                self.log_result('errors', f"Page failed to load")
            
            time.sleep(0.5)
        
        # Print summary
        print("\n" + "=" * 50)
        print("VALIDATION SUMMARY")
        print("=" * 50)
        print(f"PASSED: {len(self.results['passed'])}")
        print(f"WARNINGS: {len(self.results['warnings'])}")
        print(f"ERRORS: {len(self.results['errors'])}")
        
        if self.results['errors']:
            print("\nCRITICAL ERRORS NEED FIXING:")
            for error in self.results['errors']:
                print(f"  - {error}")

if __name__ == "__main__":
    validator = WebsiteValidator()
    validator.run_basic_test()
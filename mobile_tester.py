import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_mobile_responsiveness():
    """Test website on different screen sizes"""
    
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # Screen sizes to test (width, height, name)
    screen_sizes = [
        (1920, 1080, "Desktop"),
        (1366, 768, "Laptop"),
        (768, 1024, "Tablet"),
        (375, 667, "Mobile"),
        (414, 736, "Large Mobile")
    ]
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        test_url = "http://localhost:8000"
        
        print("MOBILE RESPONSIVENESS TEST")
        print("=" * 50)
        
        for width, height, name in screen_sizes:
            print(f"\nTesting: {name} ({width}x{height})")
            print("-" * 30)
            
            # Set window size
            driver.set_window_size(width, height)
            driver.get(test_url)
            
            # Take screenshot
            screenshot_file = f"screenshot_{name.lower().replace(' ', '_')}.png"
            driver.save_screenshot(screenshot_file)
            print(f"Screenshot saved: {screenshot_file}")
            
            # Check viewport
            viewport = driver.execute_script("return document.querySelector('meta[name=\"viewport\"]')")
            if viewport:
                print("PASS: Viewport meta tag present")
            else:
                print("WARN: No viewport meta tag")
            
            # Check if horizontal scroll exists
            has_horizontal_scroll = driver.execute_script("return document.documentElement.scrollWidth > document.documentElement.clientWidth")
            if has_horizontal_scroll:
                print("WARN: Horizontal scrolling detected")
            else:
                print("PASS: No horizontal scrolling")
            
            time.sleep(1)
        
        print("\n" + "=" * 50)
        print("MOBILE TESTING COMPLETE")
        print("Check the screenshot files for visual verification")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    test_mobile_responsiveness()
"""Quick debug script: opens Menards, waits for CAPTCHA, navigates to a category page,
saves the rendered HTML so we can inspect the actual DOM structure."""
import time, os, sys
try:
    import undetected_chromedriver as uc
except ImportError:
    print("Run: pip install undetected-chromedriver")
    sys.exit(1)

opts = uc.ChromeOptions()
opts.add_argument("--window-size=1920,1080")
driver = uc.Chrome(options=opts, use_subprocess=True)

print("Opening Menards... pass the CAPTCHA in the browser window.")
driver.get("https://www.menards.com/main/home.htm")

# Wait for CAPTCHA
for i in range(120):
    src = driver.page_source.lower()
    if 'incapsula' not in src and len(src) > 5000:
        title = driver.title.lower()
        if 'menards' in title:
            print(f"CAPTCHA passed! (took {i}s)")
            break
    if i % 10 == 0 and i > 0:
        print(f"  Waiting... {i}s")
    time.sleep(1)
else:
    print("Timed out")
    driver.quit()
    sys.exit(1)

# Navigate to PEX fittings category
url = "https://www.menards.com/main/plumbing/pipe-fittings/pex-pipe-fittings/c-5897.htm"
print(f"\nNavigating to: {url}")
driver.get(url)
time.sleep(8)

# Scroll to trigger lazy loading
for pos in range(0, 5000, 400):
    driver.execute_script(f"window.scrollTo(0, {pos});")
    time.sleep(0.5)
driver.execute_script("window.scrollTo(0, 0);")
time.sleep(2)

# Save full page source
out_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'menards_debug')
os.makedirs(out_dir, exist_ok=True)
html_path = os.path.join(out_dir, 'pex_fittings_full.html')
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(driver.page_source)
print(f"Saved full HTML to: {html_path} ({len(driver.page_source)} chars)")

# Also extract and print some key selectors to see what exists
selectors_to_test = [
    "#search-items",
    ".search-item",
    "[data-product]",
    ".product-card",
    ".product-tile",
    ".in-store-item",
    "[class*='product']",
    "[class*='item']",
    "[class*='price']",
    "[class*='Price']",
    ".value-price",
    ".sale-price",
    ".was-price",
    ".price-wrap",
    ".details",
    ".item-description",
    ".product-title",
    "a[href*='/p-']",
]

print("\n--- CSS SELECTOR PROBE ---")
for sel in selectors_to_test:
    try:
        from selenium.webdriver.common.by import By
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        if els:
            sample = els[0].text[:100].replace('\n', ' | ') if els[0].text else "(empty)"
            print(f"  {sel}: {len(els)} found  ->  sample: {sample}")
    except Exception as e:
        print(f"  {sel}: ERROR {e}")

# Also dump outer HTML of first few product-like elements
print("\n--- FIRST 3 PRODUCT-LIKE ELEMENTS ---")
for sel in [".search-item", "[class*='product']", "a[href*='/p-']"]:
    try:
        from selenium.webdriver.common.by import By
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        if els:
            for i, el in enumerate(els[:3]):
                outer = el.get_attribute("outerHTML")
                if outer and len(outer) > 50:
                    print(f"\n  [{sel}][{i}] ({len(outer)} chars):")
                    print(f"  {outer[:500]}")
    except:
        pass

input("\nPress Enter to close browser...")
driver.quit()

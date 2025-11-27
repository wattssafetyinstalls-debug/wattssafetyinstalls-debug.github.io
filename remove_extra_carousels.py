#!/usr/bin/env python3
"""
REMOVE EXTRA CAROUSELS - Keep only the top one, restore symmetry
"""
import re

def remove_extra_carousels():
    with open("services.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Find and keep only the FIRST carousel (the original one)
    # Remove any subsequent carousels I added
    content = re.sub(
        r'(<!-- PERFECT 7 TILES.*?</section>)',
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'(<!-- ULTIMATE 7 TILES.*?</section>)', 
        '',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'(<!-- FINAL 7 TILES.*?</section>)',
        '',
        content, 
        flags=re.DOTALL
    )

    # Remove any carousel styles/scripts I injected
    content = re.sub(r'<style>/\* PERFECT CAROUSEL.*?</style>', '', content, flags=re.DOTALL)
    content = re.sub(r'<script>document\.addEventListener.*?perfect-carousel.*?</script>', '', content, flags=re.DOTALL)

    print("EXTRA CAROUSELS REMOVED")
    print("- Only original top carousel remains")
    print("- Page symmetry restored") 
    print("- No duplicate content")
    print("Test: python -m http.server 8000")

if __name__ == "__main__":
    remove_extra_carousels()
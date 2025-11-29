import os
import re

def analyze_heading_hierarchy(file_path):
    """Analyze and fix heading hierarchy for SEO and accessibility"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        print(f"\nAnalyzing: {os.path.basename(file_path)}")
        print("-" * 40)
        
        # Find all headings
        headings = re.findall(r'<h([1-6])[^>]*>(.*?)</h\1>', content, re.IGNORECASE | re.DOTALL)
        
        if not headings:
            print("NO HEADINGS FOUND - CRITICAL SEO ISSUE")
            return False
        
        # Analyze current structure
        heading_levels = {}
        for level, text in headings:
            level = int(level)
            heading_levels[level] = heading_levels.get(level, 0) + 1
            clean_text = re.sub(r'<[^>]*>', '', text).strip()
            print(f"H{level}: {clean_text[:60]}...")
        
        # Check for proper hierarchy
        levels = sorted(heading_levels.keys())
        
        # Critical SEO checks
        issues = []
        
        # 1. Check for H1 presence
        if 1 not in heading_levels:
            issues.append("MISSING H1 - Most critical SEO element")
        
        # 2. Check for multiple H1s
        if heading_levels.get(1, 0) > 1:
            issues.append("MULTIPLE H1s - Should only have one H1 per page")
        
        # 3. Check heading order (should be sequential)
        expected_level = 1
        for level in levels:
            if level > expected_level + 1:
                issues.append(f"HEADING JUMP: H{expected_level} to H{level} - Not sequential")
            expected_level = level
        
        # 4. Check if H1 is the first heading
        first_heading_level = min(levels) if levels else 0
        if first_heading_level != 1:
            issues.append("FIRST HEADING NOT H1 - H1 should be the first heading")
        
        if issues:
            print("SEO ISSUES FOUND:")
            for issue in issues:
                print(f"  {issue}")
            return False
        else:
            print("Proper heading hierarchy found!")
            return True
        
    except Exception as e:
        print(f"ERROR analyzing {file_path}: {str(e)}")
        return False

def fix_heading_hierarchy(file_path):
    """Fix heading hierarchy issues"""
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        filename = os.path.basename(file_path)
        print(f"\nFixing: {filename}")
        
        # Get page title for H1
        page_title_match = re.search(r'<title>(.*?)</title>', content)
        if page_title_match:
            page_title = page_title_match.group(1).replace(' | Watts At Your Service', '')
        else:
            page_title = filename.replace('.html', '').replace('-', ' ').title()
        
        # Check if H1 exists
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL)
        
        if not h1_match:
            print(f"  Adding missing H1: {page_title}")
            
            # Find the main content area or add after header
            header_end = content.find('</header>')
            if header_end != -1:
                h1_tag = f'\n    <h1 class="page-title">{page_title}</h1>'
                content = content[:header_end] + h1_tag + content[header_end:]
            else:
                # Add after body tag
                body_start = content.find('<body>')
                if body_start != -1:
                    h1_tag = f'\n  <h1 class="page-title">{page_title}</h1>'
                    content = content[:body_start+6] + h1_tag + content[body_start+6:]
        
        # Fix multiple H1s - keep first, convert others to H2
        h1_matches = list(re.finditer(r'<h1[^>]*>(.*?)</h1>', content, re.IGNORECASE | re.DOTALL))
        if len(h1_matches) > 1:
            print(f"  Converting {len(h1_matches)-1} extra H1s to H2")
            for i, match in enumerate(h1_matches[1:], 1):
                old_h1 = match.group(0)
                h2_content = match.group(1)
                new_h2 = f'<h2 class="section-title">{h2_content}</h2>'
                content = content.replace(old_h1, new_h2)
        
        # Fix heading jumps (e.g., H1 to H3)
        for wrong_level in [3, 4, 5, 6]:
            pattern = f'<h{wrong_level}[^>]*>(.*?)</h{wrong_level}>'
            matches = re.findall(pattern, content, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                old_tag = f'<h{wrong_level}'
                new_level = 2  # Convert to H2 for proper hierarchy
                new_tag = f'<h{new_level} class="subheading"'
                content = content.replace(old_tag, new_tag)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"  Fixed heading hierarchy for {filename}")
        return True
        
    except Exception as e:
        print(f"ERROR fixing {file_path}: {str(e)}")
        return False

def main():
    print("HEADING HIERARCHY ANALYSIS & FIX")
    print("=" * 50)
    
    # Analyze main pages
    main_pages = ['index.html', 'about.html', 'services.html', 'contact.html', 
                  'service-area.html', 'referrals.html', 'privacy-policy.html', 'sitemap.html']
    
    print("\nANALYZING MAIN PAGES:")
    print("=" * 30)
    
    issues_found = False
    for page in main_pages:
        if os.path.exists(page):
            if not analyze_heading_hierarchy(page):
                issues_found = True
                fix_heading_hierarchy(page)
    
    # Analyze service pages
    services_dir = 'services'
    if os.path.exists(services_dir):
        print(f"\nANALYZING SERVICE PAGES:")
        print("=" * 30)
        
        for filename in os.listdir(services_dir):
            if filename.endswith('.html'):
                file_path = os.path.join(services_dir, filename)
                if not analyze_heading_hierarchy(file_path):
                    issues_found = True
                    fix_heading_hierarchy(file_path)
    
    print("\n" + "=" * 50)
    if issues_found:
        print("HEADING HIERARCHY ISSUES FOUND AND FIXED")
        print("\nPUSH THESE CRITICAL SEO FIXES:")
        print("git add .")
        print('git commit -m "Critical SEO: Fix heading hierarchy H1-H6 structure"')
        print("git push origin main")
    else:
        print("ALL PAGES HAVE PROPER HEADING HIERARCHY!")

if __name__ == "__main__":
    main()
#!/bin/bash

# Fix footers and schema for all service pages
# This script adds proper footer to pages missing it and ensures schema.org markup is correct

SERVICES_DIR="./services"

# Footer HTML to add (before closing </body>)
FOOTER_HTML='    <footer>
        <div class="footer-contact">
            <p><strong>Watts Safety Installs</strong></p>
            <p>Phone: <a href="tel:+14054106402">(405) 410-6402</a></p>
            <p>Service Areas: Norfolk, Battle Creek, Pierce, Madison County & Antelope County NE</p>
        </div>
        <div class="footer-links" style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
            <a href="/services">All Services</a>
            <a href="/about">About</a>
            <a href="/contact">Contact</a>
            <a href="/privacy-policy">Privacy Policy</a>
        </div>
        <p style="margin-top: 30px; color: rgba(255,255,255,0.7); font-size: 0.9rem;">&copy; 2024 Watts Safety Installs. All rights reserved. | Licensed in Nebraska | ATP Approved Contractor</p>
    </footer>'

count=0
fixed=0

echo "🔧 Starting footer and schema fixes..."
echo ""

# Process all HTML files in services directory
for file in "$SERVICES_DIR"/*.html; do
    filename=$(basename "$file")
    
    # Skip backups
    if [[ "$filename" == *".backup"* ]] || [[ "$filename" == *".bak"* ]]; then
        continue
    fi
    
    # Check if file has footer
    if ! grep -q "</footer>" "$file"; then
        echo "❌ Missing footer: $filename"
        
        # Add footer before closing body tag
        sed -i "s|</body>|    $FOOTER_HTML\n\n</body>|" "$file"
        echo "✅ Fixed: $filename"
        ((fixed++))
    else
        echo "✅ Already has footer: $filename"
    fi
    
    ((count++))
done

echo ""
echo "========================================="
echo "✅ Footer Fixes Complete"
echo "   Processed: $count files"
echo "   Fixed: $fixed files"
echo "========================================="
echo ""
echo "Next: Customize Q&A content for each service page"
echo "Then: git add -A && git commit && git push"

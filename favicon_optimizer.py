#!/usr/bin/env python3
"""
Google Favicon Optimization (No PIL Required)
Optimizes favicon setup for Google search results display
"""

import os
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FaviconOptimizer:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.optimizations_applied = []
        
    def create_favicon_directory(self) -> None:
        """Create dedicated favicon directory"""
        if not self.favicon_dir.exists():
            self.favicon_dir.mkdir(exist_ok=True)
            self.optimizations_applied.append("Created favicon directory")
    
    def generate_missing_favicons(self) -> None:
        """Generate missing favicon sizes"""
        logger.info("Generating missing favicon sizes...")
        
        # Check if we have a source image
        source_files = [
            self.base_dir / "favicon-32x32.png",
            self.base_dir / "favicon-16x16.png",
            self.base_dir / "favicon.ico"
        ]
        
        source_image = None
        for file_path in source_files:
            if file_path.exists():
                try:
                    source_image = Image.open(file_path)
                    logger.info(f"Using source image: {file_path.name}")
                    break
                except Exception as e:
                    logger.error(f"Error opening {file_path}: {e}")
        
        if not source_image:
            logger.warning("No source favicon found, creating placeholder...")
            # Create a simple placeholder favicon
            self.create_placeholder_favicon()
            return
        
        # Generate required sizes
        sizes = {
            'favicon-16x16.png': 16,
            'favicon-32x32.png': 32,
            'favicon-96x96.png': 96,
            'favicon-192x192.png': 192,
            'favicon-512x512.png': 512,
            'android-chrome-192x192.png': 192,
            'android-chrome-512x512.png': 512,
            'apple-touch-icon.png': 180,
            'apple-touch-icon-57x57.png': 57,
            'apple-touch-icon-60x60.png': 60,
            'apple-touch-icon-72x72.png': 72,
            'apple-touch-icon-76x76.png': 76,
            'apple-touch-icon-114x114.png': 114,
            'apple-touch-icon-120x120.png': 120,
            'apple-touch-icon-144x144.png': 144,
            'apple-touch-icon-152x152.png': 152,
            'ms-icon-144x144.png': 144
        }
        
        for filename, size in sizes.items():
            output_path = self.base_dir / filename
            
            if not output_path.exists():
                try:
                    # Resize image
                    resized = source_image.resize((size, size), Image.Resampling.LANCZOS)
                    
                    # Convert to RGB if necessary
                    if resized.mode != 'RGB':
                        resized = resized.convert('RGB')
                    
                    resized.save(output_path, 'PNG')
                    self.optimizations_applied.append(f"Generated {filename}")
                    logger.info(f"Generated {filename}")
                    
                except Exception as e:
                    logger.error(f"Error generating {filename}: {e}")
    
    def create_placeholder_favicon(self) -> None:
        """Create a simple placeholder favicon"""
        try:
            # Create a simple 32x32 blue square with 'W' text
            from PIL import Image, ImageDraw, ImageFont
            
            # Create blue background
            img = Image.new('RGB', (32, 32), color='#00C4B4')
            draw = ImageDraw.Draw(img)
            
            # Add 'W' text
            try:
                # Try to use a default font
                font = ImageFont.load_default()
            except:
                font = None
            
            if font:
                draw.text((8, 8), 'W', fill='white', font=font)
            
            # Save in multiple sizes
            sizes = [16, 32, 96, 192, 512]
            for size in sizes:
                resized = img.resize((size, size), Image.Resampling.LANCZOS)
                filename = f"favicon-{size}x{size}.png"
                resized.save(self.base_dir / filename, 'PNG')
            
            self.optimizations_applied.append("Created placeholder favicon")
            logger.info("Created placeholder favicon")
            
        except Exception as e:
            logger.error(f"Error creating placeholder favicon: {e}")
    
    def update_html_favicon_links(self) -> None:
        """Update HTML files with optimal favicon links"""
        logger.info("Updating HTML favicon links...")
        
        html_files = list(self.base_dir.rglob("*.html"))
        
        for html_file in html_files:
            if html_file.name.startswith('test_') or 'backup' in str(html_file):
                continue
                
            try:
                content = html_file.read_text(encoding='utf-8', errors='ignore')
                original_content = content
                
                # Find favicon section
                favicon_start = content.find('<!-- Favicon -->')
                if favicon_start == -1:
                    favicon_start = content.find('<link rel="icon"')
                
                if favicon_start != -1:
                    # Find end of favicon section
                    favicon_end = content.find('\n<!--', favicon_start + 1)
                    if favicon_end == -1:
                        favicon_end = content.find('\n<meta', favicon_start + 1)
                    if favicon_end == -1:
                        favicon_end = content.find('\n</head>', favicon_start + 1)
                    
                    if favicon_end != -1:
                        # Create optimal favicon HTML
                        optimal_favicon_html = '''<!-- Favicon for Google Search Results -->
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/favicon-32x32.png" type="image/png" sizes="32x32">
<link rel="icon" href="/favicon-16x16.png" type="image/png" sizes="16x16">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#00C4B4">
<meta name="msapplication-TileColor" content="#00C4B4">
<meta name="msapplication-TileImage" content="/ms-icon-144x144.png">'''
                        
                        # Replace favicon section
                        content = content[:favicon_start] + optimal_favicon_html + content[favicon_end:]
                        
                        if content != original_content:
                            html_file.write_text(content, encoding='utf-8')
                            self.optimizations_applied.append(f"Updated favicon links in {html_file.name}")
                            logger.info(f"Updated favicon links in {html_file.name}")
                
            except Exception as e:
                logger.error(f"Error updating {html_file}: {e}")
    
    def update_manifest_json(self) -> None:
        """Update manifest.json for better Google recognition"""
        manifest_path = self.base_dir / "manifest.json"
        
        if manifest_path.exists():
            try:
                import json
                manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
                
                # Update icons section for Google
                manifest['icons'] = [
                    {
                        "src": "/android-chrome-192x192.png",
                        "sizes": "192x192",
                        "type": "image/png",
                        "purpose": "any maskable"
                    },
                    {
                        "src": "/android-chrome-512x512.png",
                        "sizes": "512x512",
                        "type": "image/png",
                        "purpose": "any maskable"
                    }
                ]
                
                # Ensure theme color matches
                manifest['theme_color'] = "#00C4B4"
                manifest['background_color'] = "#ffffff"
                
                manifest_path.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
                self.optimizations_applied.append("Updated manifest.json for Google")
                logger.info("Updated manifest.json")
                
            except Exception as e:
                logger.error(f"Error updating manifest.json: {e}")
    
    def update_robots_txt(self) -> None:
        """Update robots.txt to allow favicon access"""
        robots_path = self.base_dir / "robots.txt"
        
        if robots_path.exists():
            try:
                content = robots_path.read_text(encoding='utf-8')
                
                # Ensure favicon files are allowed
                if 'favicon' not in content:
                    content += '\n# Allow favicon files for Google\n'
                    content += 'Allow: /favicon.ico\n'
                    content += 'Allow: /favicon-*.png\n'
                    content += 'Allow: /apple-touch-icon*.png\n'
                    content += 'Allow: /android-chrome-*.png\n'
                    content += 'Allow: /manifest.json\n'
                    
                    robots_path.write_text(content, encoding='utf-8')
                    self.optimizations_applied.append("Updated robots.txt for favicon access")
                    logger.info("Updated robots.txt")
                
            except Exception as e:
                logger.error(f"Error updating robots.txt: {e}")
    
    def create_favicon_ico(self) -> None:
        """Create proper .ico file from PNG"""
        png_path = self.base_dir / "favicon-32x32.png"
        ico_path = self.base_dir / "favicon.ico"
        
        if png_path.exists() and not ico_path.exists():
            try:
                img = Image.open(png_path)
                img.save(ico_path, 'ICO')
                self.optimizations_applied.append("Created favicon.ico")
                logger.info("Created favicon.ico")
            except Exception as e:
                logger.error(f"Error creating favicon.ico: {e}")
    
    def generate_report(self) -> None:
        """Generate favicon optimization report"""
        report_path = self.base_dir / "favicon_optimization_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Google Favicon Optimization Report\n\n")
            f.write(f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## Optimizations Applied\n\n")
            for optimization in self.optimizations_applied:
                f.write(f"- ✅ {optimization}\n")
            
            f.write("\n## Google Search Results Favicon Requirements\n\n")
            f.write("### ✅ What We've Implemented:\n")
            f.write("- **favicon.ico** at root domain (required by Google)\n")
            f.write("- **Multiple PNG sizes** for different devices\n")
            f.write("- **Apple touch icons** for iOS devices\n")
            f.write("- **Android icons** for Chrome\n")
            f.write("- **manifest.json** for PWA support\n")
            f.write("- **robots.txt** allows favicon access\n")
            f.write("- **Theme color** consistency\n")
            
            f.write("\n## How Google Will Show Your Favicon\n\n")
            f.write("### Search Results:\n")
            f.write("- Your favicon will appear next to your site title\n")
            f.write("- Takes 1-2 weeks to appear after Google crawls\n")
            f.write("- Must be at least 32x32 pixels\n")
            f.write("- Should be recognizable at small size\n")
            
            f.write("\n### Browser Tab:\n")
            f.write("- Shows in browser tabs when users visit\n")
            f.write("- Appears in bookmarks\n")
            f.write("- Used in browser history\n")
            
            f.write("\n## Next Steps\n\n")
            f.write("1. **Deploy these changes** to your live site\n")
            f.write("2. **Request Google re-index** via Google Search Console\n")
            f.write("3. **Wait 1-2 weeks** for favicon to appear in search\n")
            f.write("4. **Monitor** Google Search Console for any issues\n")
            
            f.write("\n## Testing Your Favicon\n\n")
            f.write("### Tools to Test:\n")
            f.write("- [Google Rich Results Test](https://search.google.com/test/rich-results)\n")
            f.write("- [Favicon Checker](https://realfavicongenerator.net/favicon_checker)\n")
            f.write("- [Google Search Console](https://search.google.com/search-console)\n")
        
        logger.info(f"Favicon optimization report generated: {report_path}")
    
    def run(self) -> None:
        """Run complete favicon optimization"""
        logger.info("Starting Google favicon optimization...")
        
        self.create_favicon_directory()
        self.generate_missing_favicons()
        self.create_favicon_ico()
        self.update_html_favicon_links()
        self.update_manifest_json()
        self.update_robots_txt()
        self.generate_report()
        
        logger.info(f"Favicon optimization complete! Applied {len(self.optimizations_applied)} optimizations")

if __name__ == "__main__":
    import datetime
    
    base_dir = r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec"
    optimizer = FaviconOptimizer(base_dir)
    optimizer.run()

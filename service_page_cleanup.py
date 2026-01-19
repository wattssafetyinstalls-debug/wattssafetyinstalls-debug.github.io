#!/usr/bin/env python3
"""
Service Page Cleanup and Analysis
Properly analyzes and cleans up the service pages structure
"""

import os
import re
import shutil
from pathlib import Path
from typing import List, Dict, Set
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ServicePageCleanup:
    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.services_dir = self.base_dir / "services"
        self.duplicates_found = []
        self.pages_to_keep = []
        self.pages_to_remove = []
        
    def analyze_service_pages(self) -> Dict:
        """Analyze all service pages for duplicates and structure"""
        logger.info("Analyzing service pages structure...")
        
        service_pages = list(self.services_dir.rglob("*.html"))
        logger.info(f"Found {len(service_pages)} service pages")
        
        # Group by service name (remove path variations)
        service_groups = {}
        for page in service_pages:
            # Extract service name from filename/path
            service_name = self.extract_service_name(page)
            
            if service_name not in service_groups:
                service_groups[service_name] = []
            service_groups[service_name].append(page)
        
        # Identify duplicates
        duplicates = {}
        for service_name, pages in service_groups.items():
            if len(pages) > 1:
                duplicates[service_name] = pages
                self.duplicates_found.extend(pages)
        
        logger.info(f"Found {len(duplicates)} services with duplicates")
        
        return {
            'total_pages': len(service_pages),
            'unique_services': len(service_groups),
            'duplicate_groups': duplicates,
            'service_groups': service_groups
        }
    
    def extract_service_name(self, page_path: Path) -> str:
        """Extract normalized service name from file path"""
        # Remove index.html and normalize
        name = page_path.stem.lower()
        if name == "index":
            # Use parent directory name
            name = page_path.parent.name.lower()
        
        # Normalize common variations
        name = re.sub(r'[-_]', ' ', name)
        name = re.sub(r'\s+', ' ', name).strip()
        
        # Map similar services together
        service_mappings = {
            'tv mounting residential': 'tv mounting',
            'tv home theater installation': 'home theater installation',
            'home audio': 'audio visual',
            'sound system setup': 'audio visual',
            'soundbar setup': 'audio visual',
            'smart audio': 'audio visual',
            'projector install': 'audio visual',
            'handyman repair services': 'handyman services',
            'property maintenance services': 'property maintenance',
            'emergency snow': 'snow removal',
            'seasonal cleanup': 'seasonal prep',
            'ada compliant showers bathrooms': 'ada compliant showers',
            'bathroom accessibility': 'ada compliant showers',
            'senior safety': 'accessibility safety',
            'accessibility safety solutions': 'accessibility safety',
            'custom ramps': 'wheelchair ramp installation',
            'grab bars': 'grab bar installation',
            'non slip flooring solutions': 'non slip flooring',
            'onyx countertops': 'countertop repair',
            'custom cabinets': 'cabinet refacing',
            'home remodeling renovation': 'home remodeling',
            'painting drywall': 'painting services',
            'seasonal prep': 'seasonal cleanup',
        }
        
        return service_mappings.get(name, name)
    
    def identify_pages_to_remove(self, analysis: Dict) -> None:
        """Identify which pages should be removed"""
        for service_name, pages in analysis['duplicate_groups'].items():
            # Keep the one in the most logical location
            # Priority: services/servicename/index.html > other locations
            
            best_page = None
            for page in pages:
                # Check if it's in the standard location
                if page.parent.name.lower().replace('-', ' ').replace('_', ' ') == service_name.replace(' ', '-'):
                    best_page = page
                    break
            
            # If no standard location found, keep the shortest path
            if not best_page:
                best_page = min(pages, key=lambda p: len(str(p)))
            
            # Mark others for removal
            for page in pages:
                if page != best_page:
                    self.pages_to_remove.append(page)
                else:
                    self.pages_to_keep.append(page)
        
        logger.info(f"Keeping {len(self.pages_to_keep)} pages")
        logger.info(f"Removing {len(self.pages_to_remove)} duplicate pages")
    
    def remove_duplicates(self) -> None:
        """Remove duplicate service pages"""
        logger.info("Removing duplicate service pages...")
        
        for page in self.pages_to_remove:
            try:
                if page.exists():
                    page.unlink()
                    logger.info(f"Removed: {page}")
            except Exception as e:
                logger.error(f"Error removing {page}: {e}")
    
    def create_redirects(self) -> None:
        """Create redirects for removed pages"""
        redirects_file = self.base_dir / "service_redirects.txt"
        
        with open(redirects_file, 'w', encoding='utf-8') as f:
            f.write("# Service Page Redirects\n")
            f.write("# Add these to your netlify.toml or .htaccess\n\n")
            
            for removed_page in self.pages_to_remove:
                # Find the corresponding kept page
                service_name = self.extract_service_name(removed_page)
                kept_page = None
                
                for kept in self.pages_to_keep:
                    if self.extract_service_name(kept) == service_name:
                        kept_page = kept
                        break
                
                if kept_page:
                    # Create redirect from removed to kept
                    removed_url = '/' + str(removed_page.relative_to(self.base_dir))
                    kept_url = '/' + str(kept_page.relative_to(self.base_dir))
                    
                    f.write(f"# Redirect: {removed_url} → {kept_url}\n")
                    f.write(f"[[redirects]]\n")
                    f.write(f"  from = \"{removed_url}\"\n")
                    f.write(f"  to = \"{kept_url}\"\n")
                    f.write(f"  status = 301\n\n")
        
        logger.info(f"Created redirects file: {redirects_file}")
    
    def generate_report(self) -> None:
        """Generate cleanup report"""
        report_path = self.base_dir / "service_cleanup_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write("# Service Page Cleanup Report\n\n")
            f.write(f"Total service pages found: {len(self.pages_to_keep) + len(self.pages_to_remove)}\n")
            f.write(f"Unique services: {len(self.pages_to_keep)}\n")
            f.write(f"Duplicate pages removed: {len(self.pages_to_remove)}\n\n")
            
            f.write("## Pages Kept\n\n")
            for page in sorted(self.pages_to_keep):
                service_name = self.extract_service_name(page)
                f.write(f"- **{service_name.title()}**: `{page.relative_to(self.base_dir)}`\n")
            
            f.write("\n## Pages Removed\n\n")
            for page in sorted(self.pages_to_remove):
                service_name = self.extract_service_name(page)
                f.write(f"- **{service_name.title()}**: `{page.relative_to(self.base_dir)}`\n")
            
            f.write("\n## Impact\n\n")
            f.write("- ✅ Reduced duplicate content\n")
            f.write("- ✅ Cleaner URL structure\n")
            f.write("- ✅ Better SEO (no duplicate pages)\n")
            f.write("- ✅ Easier maintenance\n")
            f.write("- ✅ Redirects created for removed pages\n")
        
        logger.info(f"Cleanup report generated: {report_path}")
    
    def run(self) -> None:
        """Run the complete cleanup process"""
        logger.info("Starting service page cleanup...")
        
        # Analyze current structure
        analysis = self.analyze_service_pages()
        
        # Identify pages to remove
        self.identify_pages_to_remove(analysis)
        
        # Remove duplicates
        self.remove_duplicates()
        
        # Create redirects
        self.create_redirects()
        
        # Generate report
        self.generate_report()
        
        logger.info("Service page cleanup completed!")

if __name__ == "__main__":
    base_dir = r"C:\Users\User\.windsurf\worktrees\my-website\my-website-1f903bec"
    cleanup = ServicePageCleanup(base_dir)
    cleanup.run()

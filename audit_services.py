#!/usr/bin/env python3
"""
Audit existing service pages and identify what needs updating
"""

import os
import glob

def audit_service_pages():
    services_dir = './services'
    existing_files = glob.glob(os.path.join(services_dir, '*.html'))
    
    print(f"📊 AUDIT REPORT: Found {len(existing_files)} service pages")
    print("=" * 60)
    
    # Check file sizes and identify potentially
import os
import re

# SEO-optimized page data for each service
seo_data = {
    # Accessibility & Safety Services
    "grab-bars.html": {
        "title": "Grab Bars | Watts Safety Installs | Norfolk NE",
        "description": "Professional Grab Bars in Norfolk NE. Same-day service. Call (405) 410-6402."
    },
    "ada-compliant-showers.html": {
        "title": "ADA Compliant Showers | Watts Safety Installs | Norfolk NE",
        "description": "ADA Compliant Showers & Bathrooms in Norfolk NE. Senior safety modifications. Free assessment."
    },
    "non-slip-flooring.html": {
        "title": "Non-Slip Flooring | Watts Safety Installs | Norfolk NE",
        "description": "Non-slip flooring solutions in Norfolk NE. Prevent falls with professional safety flooring."
    },
    "custom-ramps.html": {
        "title": "Custom Ramps | Watts Safety Installs | Norfolk NE",
        "description": "Custom wheelchair ramps in Norfolk NE. ADA compliant ramp installation. Free quotes."
    },
    "senior-safety.html": {
        "title": "Senior Safety | Watts Safety Installs | Norfolk NE",
        "description": "Senior safety modifications in Norfolk NE. Fall prevention & accessibility solutions."
    },
    "bathroom-accessibility.html": {
        "title": "Bathroom Accessibility | Watts Safety Installs | Norfolk NE",
        "description": "Accessible bathroom modifications in Norfolk NE. ADA compliant designs for safety."
    },
    
    # Home Remodeling Services
    "kitchen-renovations.html": {
        "title": "Kitchen Renovations | Watts Safety Installs | Norfolk NE",
        "description": "Kitchen remodeling in Norfolk NE. Custom cabinets, countertops & full renovations."
    },
    "deck-construction.html": {
        "title": "Deck Construction | Watts Safety Installs | Norfolk NE",
        "description": "Custom deck construction in Norfolk NE. Professional deck building & repair services."
    },
    "siding-replacement.html": {
        "title": "Siding Replacement | Watts Safety Installs | Norfolk NE",
        "description": "Siding replacement in Norfolk NE. Professional siding installation & repair services."
    },
    "home-remodeling.html": {
        "title": "Home Remodeling | Watts Safety Installs | Norfolk NE",
        "description": "Home remodeling in Norfolk NE. Complete renovation services from design to completion."
    },
    "basement-finishing.html": {
        "title": "Basement Finishing | Watts Safety Installs | Norfolk NE",
        "description": "Basement finishing in Norfolk NE. Transform your basement into usable living space."
    },
    "window-doors.html": {
        "title": "Windows & Doors | Watts Safety Installs | Norfolk NE",
        "description": "Window & door installation in Norfolk NE. Energy efficient replacement services."
    },
    "fence-installation.html": {
        "title": "Fence Installation | Watts Safety Installs | Norfolk NE",
        "description": "Fence installation in Norfolk NE. Professional fencing services for residential & commercial."
    },
    "drywall-repair.html": {
        "title": "Drywall Repair | Watts Safety Installs | Norfolk NE",
        "description": "Drywall repair in Norfolk NE. Professional drywall installation & repair services."
    },
    "painting-services.html": {
        "title": "Painting Services | Watts Safety Installs | Norfolk NE",
        "description": "Professional painting services in Norfolk NE. Interior & exterior painting experts."
    },
    
    # Concrete & Flooring Services
    "concrete-pouring.html": {
        "title": "Concrete Pouring | Watts Safety Installs | Norfolk NE",
        "description": "Concrete pouring in Norfolk NE. Professional concrete installation for driveways & patios."
    },
    "driveway-installation.html": {
        "title": "Driveway Installation | Watts Safety Installs | Norfolk NE",
        "description": "Driveway installation in Norfolk NE. Concrete & asphalt driveway services."
    },
    "patio-construction.html": {
        "title": "Patio Construction | Watts Safety Installs | Norfolk NE",
        "description": "Patio construction in Norfolk NE. Custom patio design & installation services."
    },
    "floor-refinishing.html": {
        "title": "Floor Refinishing | Watts Safety Installs | Norfolk NE",
        "description": "Floor refinishing in Norfolk NE. Hardwood floor restoration & refinishing services."
    },
    "hardwood-flooring.html": {
        "title": "Hardwood Flooring | Watts Safety Installs | Norfolk NE",
        "description": "Hardwood flooring in Norfolk NE. Professional installation & refinishing services."
    },
    "concrete-repair.html": {
        "title": "Concrete Repair | Watts Safety Installs | Norfolk NE",
        "description": "Concrete repair in Norfolk NE. Professional concrete restoration & crack repair."
    },
    
    # Cabinets & Countertops
    "custom-cabinets.html": {
        "title": "Custom Cabinets | Watts Safety Installs | Norfolk NE",
        "description": "Custom cabinets in Norfolk NE. Professional cabinet design & installation services."
    },
    "cabinet-refacing.html": {
        "title": "Cabinet Refacing | Watts Safety Installs | Norfolk NE",
        "description": "Cabinet refacing in Norfolk NE. Update your kitchen without full replacement."
    },
    "onyx-countertops.html": {
        "title": "Onyx Countertops | Watts Safety Installs | Norfolk NE",
        "description": "Onyx countertops in Norfolk NE. Luxury countertop installation & fabrication."
    },
    "kitchen-cabinetry.html": {
        "title": "Kitchen Cabinetry | Watts Safety Installs | Norfolk NE",
        "description": "Kitchen cabinetry in Norfolk NE. Custom kitchen cabinet design & installation."
    },
    "custom-storage.html": {
        "title": "Custom Storage | Watts Safety Installs | Norfolk NE",
        "description": "Custom storage solutions in Norfolk NE. Built-in storage & organization systems."
    },
    "countertop-repair.html": {
        "title": "Countertop Repair | Watts Safety Installs | Norfolk NE",
        "description": "Countertop repair in Norfolk NE. Professional repair for all countertop types."
    },
    
    # Property Maintenance
    "property-maintenance-routine.html": {
        "title": "Property Maintenance | Watts Safety Installs | Norfolk NE",
        "description": "Property maintenance in Norfolk NE. Routine & emergency repair services."
    },
    "emergency-repairs.html": {
        "title": "Emergency Repairs | Watts Safety Installs | Norfolk NE",
        "description": "Emergency repairs in Norfolk NE. 24/7 emergency home repair services."
    },
    "snow-removal.html": {
        "title": "Snow Removal | Watts Safety Installs | Norfolk NE",
        "description": "Snow removal in Norfolk NE. Commercial & residential snow removal services."
    },
    "seasonal-prep.html": {
        "title": "Seasonal Preparation | Watts Safety Installs | Norfolk NE",
        "description": "Seasonal preparation in Norfolk NE. Get your property ready for changing seasons."
    },
    "tree-trimming.html": {
        "title": "Tree Trimming | Watts Safety Installs | Norfolk NE",
        "description": "Tree trimming in Norfolk NE. Professional tree care & maintenance services."
    },
    "emergency-snow.html": {
        "title": "Emergency Snow Removal | Watts Safety Installs | Norfolk NE",
        "description": "Emergency snow removal in Norfolk NE. 24/7 snow clearing services."
    },
    
    # Lawn & Landscape
    "lawn-maintenance.html": {
        "title": "Lawn Maintenance | Watts Safety Installs | Norfolk NE",
        "description": "Lawn maintenance in Norfolk NE. Professional mowing & lawn care services."
    },
    "fertilization.html": {
        "title": "Lawn Fertilization | Watts Safety Installs | Norfolk NE",
        "description": "Lawn fertilization in Norfolk NE. Professional lawn treatment & care services."
    },
    "landscape-design.html": {
        "title": "Landscape Design | Watts Safety Installs | Norfolk NE",
        "description": "Landscape design in Norfolk NE. Custom landscape design & installation."
    },
    "seasonal-cleanup.html": {
        "title": "Seasonal Cleanup | Watts Safety Installs | Norfolk NE",
        "description": "Seasonal cleanup in Norfolk NE. Spring & fall property cleanup services."
    },
    "garden-maintenance.html": {
        "title": "Garden Maintenance | Watts Safety Installs | Norfolk NE",
        "description": "Garden maintenance in Norfolk NE. Professional garden care & landscaping services."
    },
    
    # TV & Audio Visual Services
    "tv-mounting-residential.html": {
        "title": "TV Mounting | Watts Safety Installs | Norfolk NE",
        "description": "TV mounting in Norfolk NE. Professional TV installation & mounting services."
    },
    "home-theater.html": {
        "title": "Home Theater | Watts Safety Installs | Norfolk NE",
        "description": "Home theater installation in Norfolk NE. Professional audio video setup services."
    },
    "soundbar-setup.html": {
        "title": "Soundbar Setup | Watts Safety Installs | Norfolk NE",
        "description": "Soundbar setup in Norfolk NE. Professional audio system installation."
    },
    "cable-management.html": {
        "title": "Cable Management | Watts Safety Installs | Norfolk NE",
        "description": "Cable management in Norfolk NE. Professional wire organization & hiding services."
    },
    "smart-audio.html": {
        "title": "Smart Audio | Watts Safety Installs | Norfolk NE",
        "description": "Smart audio installation in Norfolk NE. Whole home audio system setup."
    },
    "projector-install.html": {
        "title": "Projector Installation | Watts Safety Installs | Norfolk NE",
        "description": "Projector installation in Norfolk NE. Professional home theater projector setup."
    },
    "home-audio.html": {
        "title": "Home Audio | Watts Safety Installs | Norfolk NE",
        "description": "Home audio systems in Norfolk NE. Professional audio installation services."
    },
    "audio-visual.html": {
        "title": "Audio Visual | Watts Safety Installs | Norfolk NE",
        "description": "Audio visual installation in Norfolk NE. Professional AV system setup services."
    },
    
    # Additional Services
    "bathroom-remodels.html": {
        "title": "Bathroom Remodels | Watts Safety Installs | Norfolk NE",
        "description": "Bathroom remodeling in Norfolk NE. Complete bathroom renovation services."
    },
    "fence-repair.html": {
        "title": "Fence Repair | Watts Safety Installs | Norfolk NE",
        "description": "Fence repair in Norfolk NE. Professional fence maintenance & repair services."
    },
    "gutter-cleaning.html": {
        "title": "Gutter Cleaning | Watts Safety Installs | Norfolk NE",
        "description": "Gutter cleaning in Norfolk NE. Professional gutter maintenance & cleaning."
    },
    "handyman-services.html": {
        "title": "Handyman Services | Watts Safety Installs | Norfolk NE",
        "description": "Handyman services in Norfolk NE. Professional home repair & maintenance."
    },
    "pressure-washing.html": {
        "title": "Pressure Washing | Watts Safety Installs | Norfolk NE",
        "description": "Pressure washing in Norfolk NE. Professional exterior cleaning services."
    },
    "room-additions.html": {
        "title": "Room Additions | Watts Safety Installs | Norfolk NE",
        "description": "Room additions in Norfolk NE. Professional home expansion services."
    },
    "stairlift-elevator-installation.html": {
        "title": "Stairlift Installation | Watts Safety Installs | Norfolk NE",
        "description": "Stairlift installation in Norfolk NE. Mobility & accessibility solutions."
    },
    "wheelchair-ramp-installation.html": {
        "title": "Wheelchair Ramps | Watts Safety Installs | Norfolk NE",
        "description": "Wheelchair ramp installation in Norfolk NE. ADA compliant ramp services."
    }
}

def update_seo_metadata(file_path, title, description):
    """Update the SEO metadata in an HTML file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Update title tag
        title_pattern = r'<title>.*?</title>'
        new_title = f'<title>{title}</title>'
        content = re.sub(title_pattern, new_title, content)
        
        # Update meta description
        desc_pattern = r'<meta name="description" content=".*?"'
        new_desc = f'<meta name="description" content="{description}"'
        content = re.sub(desc_pattern, new_desc, content)
        
        # Update og:title
        og_title_pattern = r'<meta property="og:title" content=".*?"'
        new_og_title = f'<meta property="og:title" content="{title}"'
        content = re.sub(og_title_pattern, new_og_title, content)
        
        # Update og:description
        og_desc_pattern = r'<meta property="og:description" content=".*?"'
        new_og_desc = f'<meta property="og:description" content="{description}"'
        content = re.sub(og_desc_pattern, new_og_desc, content)
        
        # Write updated content back to file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        return True
    
    except Exception as e:
        print(f"Error updating {file_path}: {str(e)}")
        return False

def validate_seo_lengths():
    """Validate that all titles and descriptions are optimal length"""
    print("Validating SEO lengths...")
    print("=" * 60)
    
    all_valid = True
    for filename, data in seo_data.items():
        title_len = len(data['title'])
        desc_len = len(data['description'])
        
        title_status = "OK" if 40 <= title_len <= 60 else "TOO LONG"
        desc_status = "OK" if 120 <= desc_len <= 160 else "TOO LONG"
        
        print(f"{filename:<40} | Title: {title_len:2d} chars ({title_status}) | Desc: {desc_len:3d} chars ({desc_status})")
        
        if not (40 <= title_len <= 60) or not (120 <= desc_len <= 160):
            all_valid = False
    
    print("=" * 60)
    if all_valid:
        print("SUCCESS: All SEO titles and descriptions are optimal length!")
    else:
        print("WARNING: Some items need length adjustment")
    
    return all_valid

def main():
    print("Watts Safety Installs - SEO Optimization Script")
    print("=" * 60)
    
    # First validate all SEO data
    if not validate_seo_lengths():
        print("\nWARNING: Please fix length issues before proceeding")
        return
    
    print("\nUpdating SEO metadata for all service pages...")
    print("-" * 60)
    
    services_dir = "services"
    updated_count = 0
    error_count = 0
    
    for filename, seo_info in seo_data.items():
        file_path = os.path.join(services_dir, filename)
        
        if os.path.exists(file_path):
            success = update_seo_metadata(file_path, seo_info['title'], seo_info['description'])
            if success:
                print(f"SUCCESS: Updated {filename}")
                updated_count += 1
            else:
                print(f"ERROR: Failed to update {filename}")
                error_count += 1
        else:
            print(f"WARNING: File not found - {filename}")
            error_count += 1
    
    print("-" * 60)
    print("RESULTS:")
    print(f"  Successfully updated: {updated_count} files")
    print(f"  Errors/Not found: {error_count} files")
    print(f"  Total processed: {len(seo_data)} files")
    
    if error_count == 0:
        print("\nSUCCESS: All service pages have been optimized for SEO!")
        print("   Titles: 40-60 characters (optimal for search results)")
        print("   Descriptions: 120-160 characters (optimal for search snippets)")
    else:
        print(f"\nWARNING: {error_count} files need attention")

if __name__ == "__main__":
    main()
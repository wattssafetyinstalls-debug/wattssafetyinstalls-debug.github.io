import os
import re

# SEO-optimized page data for each service - UPDATED WITH LONGER DESCRIPTIONS
seo_data = {
    # Accessibility & Safety Services
    "grab-bars.html": {
        "title": "Grab Bars | Watts Safety Installs | Norfolk NE",
        "description": "Professional grab bar installation in Norfolk NE. ADA compliant safety bars for bathrooms & showers. Fall prevention for seniors & mobility assistance. Same-day service available. Call (405) 410-6402 for free safety assessment."
    },
    "ada-compliant-showers.html": {
        "title": "ADA Compliant Showers | Watts Safety Installs | Norfolk NE",
        "description": "ADA compliant shower & bathroom modifications in Norfolk NE. Barrier-free showers, grab bars, and accessibility features. Senior safety solutions with professional installation. Free home assessment available."
    },
    "non-slip-flooring.html": {
        "title": "Non-Slip Flooring | Watts Safety Installs | Norfolk NE",
        "description": "Non-slip flooring solutions in Norfolk NE for bathrooms, kitchens & entryways. Slip-resistant surfaces for fall prevention. Professional installation for senior safety & ADA compliance. Free quotes available."
    },
    "custom-ramps.html": {
        "title": "Custom Ramps | Watts Safety Installs | Norfolk NE",
        "description": "Custom wheelchair ramp installation in Norfolk NE. ADA compliant ramps for homes & businesses. Permanent & portable ramp solutions. Professional installation with lifetime warranty. Free ramp assessment."
    },
    "senior-safety.html": {
        "title": "Senior Safety | Watts Safety Installs | Norfolk NE",
        "description": "Senior safety modifications in Norfolk NE. Fall prevention solutions including grab bars, ramps, and bathroom safety features. Aging in place modifications with professional installation. Free safety assessment."
    },
    "bathroom-accessibility.html": {
        "title": "Bathroom Accessibility | Watts Safety Installs | Norfolk NE",
        "description": "Accessible bathroom modifications in Norfolk NE. ADA compliant designs with walk-in showers, grab bars, and raised toilets. Senior safety solutions for independent living. Professional installation services."
    },
    
    # Home Remodeling Services
    "kitchen-renovations.html": {
        "title": "Kitchen Renovations | Watts Safety Installs | Norfolk NE",
        "description": "Kitchen remodeling & renovation services in Norfolk NE. Custom cabinets, countertops, flooring & full kitchen transformations. Professional design & installation with quality craftsmanship. Free estimates available."
    },
    "deck-construction.html": {
        "title": "Deck Construction | Watts Safety Installs | Norfolk NE",
        "description": "Custom deck construction & building services in Norfolk NE. Wood, composite & PVC deck installation. Professional deck design, repair & maintenance. Outdoor living space experts serving Norfolk area."
    },
    "siding-replacement.html": {
        "title": "Siding Replacement | Watts Safety Installs | Norfolk NE",
        "description": "Siding replacement & installation services in Norfolk NE. Vinyl, fiber cement & wood siding options. Professional siding repair, installation & maintenance. Improve curb appeal & energy efficiency."
    },
    "home-remodeling.html": {
        "title": "Home Remodeling | Watts Safety Installs | Norfolk NE",
        "description": "Complete home remodeling services in Norfolk NE. Room additions, kitchen & bathroom remodels, basement finishing. Professional contractors serving Norfolk & surrounding areas. Free project consultation."
    },
    "basement-finishing.html": {
        "title": "Basement Finishing | Watts Safety Installs | Norfolk NE",
        "description": "Basement finishing & remodeling services in Norfolk NE. Transform unused basement space into living areas, home theaters, or guest suites. Professional waterproofing, framing & finishing services."
    },
    "window-doors.html": {
        "title": "Windows & Doors | Watts Safety Installs | Norfolk NE",
        "description": "Window & door installation services in Norfolk NE. Energy efficient replacement windows, patio doors & entry doors. Professional installation with improved security & energy savings. Free estimates."
    },
    "fence-installation.html": {
        "title": "Fence Installation | Watts Safety Installs | Norfolk NE",
        "description": "Fence installation services in Norfolk NE. Wood, vinyl, aluminum & chain link fencing for residential & commercial properties. Professional fence repair, replacement & maintenance services."
    },
    "drywall-repair.html": {
        "title": "Drywall Repair | Watts Safety Installs | Norfolk NE",
        "description": "Drywall repair & installation services in Norfolk NE. Professional drywall hanging, finishing, texturing & repair. Hole patching, crack repair & water damage restoration. Quality workmanship guaranteed."
    },
    "painting-services.html": {
        "title": "Painting Services | Watts Safety Installs | Norfolk NE",
        "description": "Professional painting services in Norfolk NE. Interior & exterior painting for homes & businesses. Quality preparation, multiple coats & clean finishes. Residential & commercial painting experts."
    },
    
    # Concrete & Flooring Services
    "concrete-pouring.html": {
        "title": "Concrete Pouring | Watts Safety Installs | Norfolk NE",
        "description": "Concrete pouring & installation services in Norfolk NE. Driveways, patios, sidewalks & foundations. Professional concrete finishing, stamping & coloring. Quality concrete work for residential & commercial projects."
    },
    "driveway-installation.html": {
        "title": "Driveway Installation | Watts Safety Installs | Norfolk NE",
        "description": "Driveway installation services in Norfolk NE. Concrete, asphalt & paver driveways. Professional driveway repair, replacement & maintenance. Enhance curb appeal with durable driveway solutions."
    },
    "patio-construction.html": {
        "title": "Patio Construction | Watts Safety Installs | Norfolk NE",
        "description": "Patio construction & design services in Norfolk NE. Concrete, paver & stone patios for outdoor living spaces. Professional patio installation, repair & maintenance. Create your perfect backyard oasis."
    },
    "floor-refinishing.html": {
        "title": "Floor Refinishing | Watts Safety Installs | Norfolk NE",
        "description": "Floor refinishing services in Norfolk NE. Hardwood floor sanding, staining & refinishing. Restore old floors to like-new condition. Professional floor repair, buffing & sealing services available."
    },
    "hardwood-flooring.html": {
        "title": "Hardwood Flooring | Watts Safety Installs | Norfolk NE",
        "description": "Hardwood flooring installation & refinishing in Norfolk NE. Solid hardwood, engineered wood & laminate flooring options. Professional installation, repair & maintenance services. Free flooring estimates."
    },
    "concrete-repair.html": {
        "title": "Concrete Repair | Watts Safety Installs | Norfolk NE",
        "description": "Concrete repair services in Norfolk NE. Crack filling, leveling, resurfacing & restoration. Professional concrete repair for driveways, sidewalks & foundations. Extend the life of your concrete surfaces."
    },
    
    # Cabinets & Countertops
    "custom-cabinets.html": {
        "title": "Custom Cabinets | Watts Safety Installs | Norfolk NE",
        "description": "Custom cabinet design & installation in Norfolk NE. Kitchen cabinets, bathroom vanities & built-in storage solutions. Professional cabinet installation, repair & refacing services. Free design consultation."
    },
    "cabinet-refacing.html": {
        "title": "Cabinet Refacing | Watts Safety Installs | Norfolk NE",
        "description": "Cabinet refacing services in Norfolk NE. Update your kitchen cabinets without full replacement. New doors, drawer fronts & hardware installation. Affordable kitchen transformation with professional results."
    },
    "onyx-countertops.html": {
        "title": "Onyx Countertops | Watts Safety Installs | Norfolk NE",
        "description": "Onyx countertop installation in Norfolk NE. Luxury natural stone countertops for kitchens & bathrooms. Professional fabrication, installation & sealing services. Create stunning surfaces with durable onyx."
    },
    "kitchen-cabinetry.html": {
        "title": "Kitchen Cabinetry | Watts Safety Installs | Norfolk NE",
        "description": "Kitchen cabinetry services in Norfolk NE. Custom kitchen cabinet design, installation & organization solutions. Professional cabinet repair, refacing & hardware updates. Transform your kitchen space."
    },
    "custom-storage.html": {
        "title": "Custom Storage | Watts Safety Installs | Norfolk NE",
        "description": "Custom storage solutions in Norfolk NE. Built-in shelving, closet systems & organizational solutions. Maximize space with professional storage design & installation. Free storage assessment available."
    },
    "countertop-repair.html": {
        "title": "Countertop Repair | Watts Safety Installs | Norfolk NE",
        "description": "Countertop repair services in Norfolk NE. Fix chips, cracks & damage in granite, quartz & laminate countertops. Professional countertop restoration, sealing & maintenance. Extend countertop life."
    },
    
    # Property Maintenance
    "property-maintenance-routine.html": {
        "title": "Property Maintenance | Watts Safety Installs | Norfolk NE",
        "description": "Property maintenance services in Norfolk NE. Routine & preventive maintenance for residential & commercial properties. Seasonal upkeep, repairs & inspection services. Keep your property in top condition year-round."
    },
    "emergency-repairs.html": {
        "title": "Emergency Repairs | Watts Safety Installs | Norfolk NE",
        "description": "Emergency repair services in Norfolk NE. 24/7 emergency home repairs for plumbing, electrical & structural issues. Rapid response team available for urgent repair needs. Call (405) 410-6402 for emergency service."
    },
    "snow-removal.html": {
        "title": "Snow Removal | Watts Safety Installs | Norfolk NE",
        "description": "Snow removal services in Norfolk NE. Commercial & residential snow clearing for driveways, parking lots & walkways. 24/7 emergency snow removal with prompt service. Seasonal contracts available."
    },
    "seasonal-prep.html": {
        "title": "Seasonal Preparation | Watts Safety Installs | Norfolk NE",
        "description": "Seasonal preparation services in Norfolk NE. Get your property ready for winter, spring, summer & fall. Weatherproofing, system checks & maintenance services. Prevent seasonal damage with professional preparation."
    },
    "tree-trimming.html": {
        "title": "Tree Trimming | Watts Safety Installs | Norfolk NE",
        "description": "Tree trimming & care services in Norfolk NE. Professional tree pruning, removal & maintenance. Storm damage cleanup & hazardous branch removal. Keep your trees healthy & property safe."
    },
    "emergency-snow.html": {
        "title": "Emergency Snow Removal | Watts Safety Installs | Norfolk NE",
        "description": "Emergency snow removal services in Norfolk NE. 24/7 snow clearing for businesses & residences. Rapid response team for urgent snow removal needs. Call (405) 410-6402 for immediate snow clearing service."
    },
    
    # Lawn & Landscape
    "lawn-maintenance.html": {
        "title": "Lawn Maintenance | Watts Safety Installs | Norfolk NE",
        "description": "Lawn maintenance services in Norfolk NE. Professional mowing, trimming, edging & lawn care. Seasonal fertilization, aeration & weed control. Keep your lawn healthy & beautiful year-round."
    },
    "fertilization.html": {
        "title": "Lawn Fertilization | Watts Safety Installs | Norfolk NE",
        "description": "Lawn fertilization services in Norfolk NE. Professional lawn treatment with customized fertilizer programs. Weed control, pest management & soil health improvement. Achieve a lush, green lawn with expert care."
    },
    "landscape-design.html": {
        "title": "Landscape Design | Watts Safety Installs | Norfolk NE",
        "description": "Landscape design services in Norfolk NE. Custom landscape design, installation & renovation. Plant selection, hardscaping & outdoor living spaces. Transform your property with professional landscape design."
    },
    "seasonal-cleanup.html": {
        "title": "Seasonal Cleanup | Watts Safety Installs | Norfolk NE",
        "description": "Seasonal cleanup services in Norfolk NE. Spring & fall property cleanup including leaf removal, debris clearing & garden preparation. Yard waste removal & property revitalization services."
    },
    "garden-maintenance.html": {
        "title": "Garden Maintenance | Watts Safety Installs | Norfolk NE",
        "description": "Garden maintenance services in Norfolk NE. Professional garden care, planting, pruning & weeding. Seasonal garden preparation & ongoing maintenance. Keep your gardens beautiful & thriving."
    },
    
    # TV & Audio Visual Services
    "tv-mounting-residential.html": {
        "title": "TV Mounting | Watts Safety Installs | Norfolk NE",
        "description": "TV mounting services in Norfolk NE. Professional TV installation on walls, ceilings & above fireplaces. Cable management, sound system integration & smart home setup. Safe, secure TV mounting with clean installation."
    },
    "home-theater.html": {
        "title": "Home Theater | Watts Safety Installs | Norfolk NE",
        "description": "Home theater installation in Norfolk NE. Complete audio video setup with surround sound, projectors & screen installation. Professional home theater design, wiring & calibration. Create your perfect entertainment space."
    },
    "soundbar-setup.html": {
        "title": "Soundbar Setup | Watts Safety Installs | Norfolk NE",
        "description": "Soundbar setup & installation in Norfolk NE. Professional soundbar mounting, wiring & audio calibration. TV audio enhancement with clean cable management. Improve your TV sound with expert installation."
    },
    "cable-management.html": {
        "title": "Cable Management | Watts Safety Installs | Norfolk NE",
        "description": "Cable management services in Norfolk NE. Professional wire organization, hiding & labeling for TV setups & home offices. In-wall cable routing & cord concealment solutions. Eliminate cable clutter with clean organization."
    },
    "smart-audio.html": {
        "title": "Smart Audio | Watts Safety Installs | Norfolk NE",
        "description": "Smart audio installation in Norfolk NE. Whole home audio systems, multi-room speakers & smart sound solutions. Professional audio system setup, wiring & integration. Enjoy seamless music throughout your home."
    },
    "projector-install.html": {
        "title": "Projector Installation | Watts Safety Installs | Norfolk NE",
        "description": "Projector installation services in Norfolk NE. Home theater projector mounting, screen installation & calibration. Professional audio video integration for optimal viewing experience. Create cinema-quality viewing at home."
    },
    "home-audio.html": {
        "title": "Home Audio | Watts Safety Installs | Norfolk NE",
        "description": "Home audio system installation in Norfolk NE. Whole house audio, surround sound & speaker setup. Professional audio system design, wiring & calibration. Enhanced sound quality for music & entertainment."
    },
    "audio-visual.html": {
        "title": "Audio Visual | Watts Safety Installs | Norfolk NE",
        "description": "Audio visual installation services in Norfolk NE. Professional AV system setup for home theaters, conference rooms & entertainment spaces. Complete audio video integration with clean wiring & calibration."
    },
    
    # Additional Services
    "bathroom-remodels.html": {
        "title": "Bathroom Remodels | Watts Safety Installs | Norfolk NE",
        "description": "Bathroom remodeling services in Norfolk NE. Complete bathroom renovations with new fixtures, tile, vanities & lighting. Professional bathroom design, plumbing & electrical work. Transform your bathroom space."
    },
    "fence-repair.html": {
        "title": "Fence Repair | Watts Safety Installs | Norfolk NE",
        "description": "Fence repair services in Norfolk NE. Professional fence maintenance, post replacement & structural repairs. Wood, vinyl & chain link fence restoration. Extend the life of your fence with quality repairs."
    },
    "gutter-cleaning.html": {
        "title": "Gutter Cleaning | Watts Safety Installs | Norfolk NE",
        "description": "Gutter cleaning services in Norfolk NE. Professional gutter cleaning, debris removal & downspout clearing. Prevent water damage with regular gutter maintenance. Residential & commercial gutter services available."
    },
    "handyman-services.html": {
        "title": "Handyman Services | Watts Safety Installs | Norfolk NE",
        "description": "Handyman services in Norfolk NE. Professional home repairs, maintenance & small projects. Drywall repair, painting, carpentry & general home maintenance. Reliable handyman services for your to-do list."
    },
    "pressure-washing.html": {
        "title": "Pressure Washing | Watts Safety Installs | Norfolk NE",
        "description": "Pressure washing services in Norfolk NE. Professional exterior cleaning for siding, driveways, decks & patios. Remove dirt, mold & stains with high-pressure cleaning. Restore your property's appearance."
    },
    "room-additions.html": {
        "title": "Room Additions | Watts Safety Installs | Norfolk NE",
        "description": "Room addition services in Norfolk NE. Professional home expansions including sunrooms, bedrooms & office additions. Complete construction from foundation to finish work. Increase your living space with quality additions."
    },
    "stairlift-elevator-installation.html": {
        "title": "Stairlift Installation | Watts Safety Installs | Norfolk NE",
        "description": "Stairlift & elevator installation in Norfolk NE. Mobility solutions for multi-level homes. Professional stairlift installation, maintenance & repair. Improve accessibility with reliable mobility equipment."
    },
    "wheelchair-ramp-installation.html": {
        "title": "Wheelchair Ramps | Watts Safety Installs | Norfolk NE",
        "description": "Wheelchair ramp installation in Norfolk NE. ADA compliant ramp solutions for homes & businesses. Permanent & temporary ramp options. Professional installation with safety & accessibility in mind."
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
        desc_status = "OK" if 120 <= desc_len <= 300 else "TOO LONG"
        
        print(f"{filename:<40} | Title: {title_len:2d} chars ({title_status}) | Desc: {desc_len:3d} chars ({desc_status})")
        
        if not (40 <= title_len <= 60) or not (120 <= desc_len <= 300):
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
        print("   Descriptions: 120-300 characters (optimal for search snippets)")
    else:
        print(f"\nWARNING: {error_count} files need attention")

if __name__ == "__main__":
    main()
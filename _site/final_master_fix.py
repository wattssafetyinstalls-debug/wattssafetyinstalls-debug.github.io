import os
import re

def final_master_fix():
    print("RUNNING FINAL MASTER FIX - THIS WILL SOLVE EVERYTHING")
    print("=" * 60)
    
    services_dir = 'services'
    files = [f for f in os.listdir(services_dir) if f.endswith('.html')]
    
    # Professional descriptions (the ones you approved)
    professional_descriptions = {
    "accessibility-safety-solutions.html": "Expert accessibility and senior safety solutions in Norfolk, Nebraska. Licensed contractors providing grab bar installation, ADA-compliant modifications, non-slip flooring, and full home safety assessments throughout Northeast Nebraska.",
    "ada-compliant-showers-bathrooms.html": "ADA-compliant shower and bathroom remodeling in Norfolk, NE. Professional roll-in showers, zero-threshold entries, comfort-height toilets, and accessible vanities installed by licensed, insured contractors with ATP approval.",
    "ada-compliant-showers.html": "Professional ADA-compliant shower installation in Norfolk and Northeast Nebraska. Walk-in showers, roll-in access, safety grab bars, and anti-slip flooring with guaranteed code compliance and senior-friendly design.",
    "audio-visual.html": "Complete audio-visual and smart home technology services in Norfolk, NE. TV mounting, whole-home audio, surround sound systems, and smart lighting control installed by certified technicians.",
    "basement-finishing.html": "Professional basement finishing and remodeling in Norfolk, Nebraska. Transform your basement into a family room, home theater, guest suite, or gym with licensed, insured craftsmanship.",
    "bathroom-accessibility.html": "Bathroom accessibility upgrades in Norfolk, NE. Walk-in tubs, roll-in showers, raised toilets, grab bars, and senior-safe modifications installed with care and precision.",
    "bathroom-remodels.html": "Full bathroom remodeling services in Norfolk and Northeast Nebraska. Modern designs, luxury finishes, tile work, vanities, lighting, and plumbing upgrades by licensed professionals.",
    "cabinet-refacing.html": "Cabinet refacing and kitchen refresh services in Norfolk, NE. Update your kitchen or bathroom cabinets with new doors, hardware, and countertops — faster and more affordable than full replacement.",
    "cable-management.html": "Professional cable management and wire concealment services in Norfolk, Nebraska. Clean, hidden wiring for TV mounts, home theaters, security cameras, and smart home systems.",
    "concrete-pouring.html": "Concrete pouring and flatwork services in Norfolk, NE. Driveways, sidewalks, patios, garage slabs, and stamped concrete installed with precision and durability.",
    "concrete-repair.html": "Expert concrete repair and restoration in Norfolk and surrounding areas. Cracked driveway repair, sidewalk leveling, foundation sealing, and resurfacing by experienced contractors.",
    "countertop-repair.html": "Countertop repair and refinishing in Norfolk, NE. Chip repair, crack filling, seam fixes, and surface restoration for granite, quartz, laminate, and solid surface countertops.",
    "custom-cabinets.html": "Custom cabinet design and installation in Norfolk, Nebraska. Kitchen cabinets, bathroom vanities, built-ins, and storage solutions crafted to your exact specifications.",
    "custom-ramps.html": "Custom wheelchair ramp design and installation in Norfolk, NE. Aluminum, wood, and modular ramps built to ADA standards with safe, non-slip surfaces.",
    "custom-storage.html": "Custom storage and organization solutions in Norfolk, Nebraska. Garage shelving, closet systems, pantry organization, and built-in storage designed for maximum efficiency.",
    "deck-construction.html": "Professional deck building and patio construction in Norfolk, NE. Wood and composite decks, multi-level designs, railings, pergolas, and outdoor living spaces.",
    "driveway-installation.html": "New driveway installation and replacement in Norfolk, Nebraska. Concrete, asphalt, paver, and gravel driveways built to last with proper grading and drainage.",
    "drywall-repair.html": "Expert drywall repair and patching in Norfolk, NE. Water damage repair, hole patching, crack filling, and professional finishing with seamless results.",
    "emergency-repairs.html": "24/7 emergency handyman and repair services in Norfolk, Nebraska. Fast response for plumbing leaks, electrical issues, broken doors, storm damage, and urgent home repairs.",
    "emergency-snow.html": "Emergency snow removal and ice management in Norfolk, NE. Same-day service for driveways, sidewalks, parking lots, and rooftops during winter storms.",
    "fence-installation.html": "Professional fence installation in Norfolk and Northeast Nebraska. Wood privacy, vinyl, chain link, aluminum, and farm fencing installed with lifetime workmanship guarantee.",
    "fence-repair.html": "Fence repair and restoration services in Norfolk, NE. Post replacement, panel repair, gate fixing, and storm damage restoration for all fence types.",
    "fertilization.html": "Professional lawn fertilization and weed control in Norfolk, Nebraska. Customized treatment programs for thick, green, weed-free lawns all season long.",
    "floor-refinishing.html": "Hardwood floor refinishing and restoration in Norfolk, NE. Sanding, staining, and sealing to bring your floors back to life with a factory-fresh finish.",
    "flooring-installation.html": "Professional flooring installation in Norfolk, Nebraska. Hardwood, luxury vinyl plank, laminate, tile, and carpet installed with precision and care.",
    "garden-maintenance.html": "Complete garden and landscape maintenance in Norfolk, NE. Planting, pruning, mulching, weeding, and seasonal cleanup for beautiful, healthy gardens.",
    "grab-bar-installation.html": "Professional grab bar installation in Norfolk and Northeast Nebraska. Secure, ADA-compliant grab bars installed in bathrooms for senior safety and fall prevention.",
    "grab-bars.html": "Safety grab bar installation specialists in Norfolk, NE. Bathroom, shower, and toilet grab bars professionally mounted into studs for maximum strength and security.",
    "gutter-cleaning.html": "Professional gutter cleaning and maintenance in Norfolk, Nebraska. Clog removal, downspout clearing, and gutter guard recommendations to protect your home.",
    "handyman-repair-services.html": "Reliable handyman services in Norfolk, NE. Small repairs, assembly, mounting, painting, and odd jobs completed fast by experienced professionals.",
    "handyman-services.html": "Trusted local handyman in Norfolk, Nebraska. No job too small — TV mounting, furniture assembly, light plumbing, electrical, and general repairs.",
    "hardwood-flooring.html": "Premium hardwood flooring installation in Norfolk, NE. Solid and engineered hardwood in oak, maple, hickory, and exotic species with professional finishing.",
    "home-audio.html": "Whole-home audio and distributed sound systems in Norfolk, Nebraska. Indoor/outdoor speakers, multi-room music, and seamless integration with your smart home.",
    "home-remodeling-renovation.html": "Full-service home remodeling and renovation in Norfolk, NE. Kitchen, bathroom, basement, and whole-home transformations by licensed, insured contractors.",
    "home-remodeling.html": "Expert home remodeling services in Norfolk, Nebraska. Modern updates, open-concept layouts, energy-efficient upgrades, and beautiful finishes throughout.",
    "home-theater-installation.html": "Professional home theater design and installation in Norfolk, NE. Projectors, screens, surround sound, seating, lighting, and acoustic treatments for the ultimate experience.",
    "kitchen-cabinetry.html": "Custom kitchen cabinetry and design in Norfolk, Nebraska. New cabinets, refacing, organization solutions, and hardware upgrades for your dream kitchen.",
    "kitchen-renovations.html": "Complete kitchen renovation services in Norfolk, NE. Layout changes, new cabinets, countertops, flooring, lighting, and appliances installed with precision.",
    "landscape-design.html": "Professional landscape design and installation in Norfolk, Nebraska. Custom outdoor living spaces, planting plans, hardscaping, and water features.",
    "lawn-maintenance.html": "Weekly lawn mowing and maintenance in Norfolk, NE. Precision cutting, edging, trimming, and blowing for a perfectly manicured lawn all season.",
    "non-slip-flooring-solutions.html": "Non-slip flooring solutions for seniors and accessibility in Norfolk, NE. Textured tile, rubber flooring, and safety coatings that prevent slips and falls.",
    "non-slip-flooring.html": "Anti-slip and non-slip flooring installation in Norfolk, Nebraska. Safety flooring for bathrooms, kitchens, ramps, and commercial spaces.",
    "onyx-countertops.html": "Luxury onyx collection countertops and surfaces in Norfolk, NE. Translucent onyx slabs with backlighting for stunning kitchen and bathroom designs.",
    "painting-drywall.html": "Interior and exterior painting plus drywall services in Norfolk, NE. Color consultations, prep work, clean lines, and flawless finish every time.",
    "painting-services.html": "Professional house painting services in Norfolk, Nebraska. Interior, exterior, cabinets, decks, and fences painted with premium materials and expert technique.",
    "patio-construction.html": "Custom patio design and construction in Norfolk, NE. Pavers, stamped concrete, fire pits, seating walls, and outdoor kitchens for perfect backyard living.",
    "pressure-washing.html": "Professional pressure washing services in Norfolk, Nebraska. House washing, driveway cleaning, deck restoration, and fence cleaning with eco-friendly solutions.",
    "projector-install.html": "Professional projector installation and home cinema setup in Norfolk, NE. Ceiling mounts, screen installation, wiring concealment, and calibration.",
    "property-maintenance-services.html": "Complete property maintenance packages in Norfolk, NE. Lawn care, snow removal, repairs, cleaning, and seasonal services for homeowners and landlords.",
    "room-additions.html": "Home room additions and expansions in Norfolk, Nebraska. Bedrooms, sunrooms, in-law suites, and garage additions built seamlessly onto your existing home.",
    "seasonal-cleanup.html": "Spring and fall yard cleanup services in Norfolk, NE. Leaf removal, branch hauling, garden prep, gutter cleaning, and full property refresh.",
    "seasonal-prep.html": "Seasonal home preparation services in Norfolk, Nebraska. Winterization, storm prep, holiday lighting, and spring opening — everything your home needs year-round.",
    "senior-safety.html": "Senior home safety modifications in Norfolk, NE. Fall prevention, mobility aids, lighting upgrades, and emergency response systems installed with compassion.",
    "siding-replacement.html": "Professional siding replacement and repair in Norfolk, Nebraska. Vinyl, fiber cement, steel, and wood siding with expert installation and lifetime warranties.",
    "smart-audio.html": "Smart home audio and voice-controlled music systems in Norfolk, NE. Sonos, Control4, Josh.ai, and multi-room streaming with invisible speakers.",
    "snow-removal.html": "Reliable snow removal and plowing services in Norfolk, Nebraska. Residential driveways, sidewalks, and commercial lots cleared fast and thoroughly all winter.",
    "sound-system-setup.html": "Professional sound system design and installation in Norfolk, NE. Home theater audio, whole-house music, outdoor speakers, and acoustic calibration.",
    "soundbar-setup.html": "Expert soundbar installation and TV audio upgrades in Norfolk, Nebraska. Wall mounting, wireless subwoofers, cable hiding, and perfect sound calibration.",
    "stairlift-elevator-installation.html": "Stairlift and home elevator installation in Norfolk, NE. Straight, curved, and outdoor stairlifts plus residential elevators for full accessibility.",
    "tree-trimming.html": "Professional tree trimming and pruning in Norfolk, Nebraska. Safety pruning, crown reduction, deadwood removal, and storm damage cleanup by certified arborists.",
    "tv-home-theater-installation.html": "Complete TV and home theater installation in Norfolk, NE. Wall mounting, surround sound, projector systems, seating, and lighting control.",
    "tv-mounting-residential.html": "Professional residential TV mounting in Norfolk, Nebraska. Any size, any wall — brick, drywall, fireplace, or ceiling — with perfect placement and hidden cables.",
    "tv-mounting.html": "Expert TV wall mounting services in Norfolk, NE. Fixed, tilting, full-motion mounts installed securely with cable management and soundbar integration.",
    "wheelchair-ramp-installation.html": "Wheelchair ramp installation specialists in Norfolk, Nebraska. Permanent and portable ramps built to ADA standards with non-slip surfaces and handrails.",
    "window-doors.html": "Window and door replacement services in Norfolk, NE. Energy-efficient windows, patio doors, entry doors, and storm doors installed by certified professionals."
}
    
    fixed = 0
    for filename in files:
        path = os.path.join(services_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        original = content
        
        # 1. Fix the main service tile description
        key = filename
        if key in professional_descriptions:
            new_desc = professional_descriptions[key]
            # Replace whatever is in <p class="service-description">
            content = re.sub(
                r'<p class="service-description">.*?</p>',
                f'<p class="service-description">{new_desc}</p>',
                content,
                flags=re.DOTALL
            )
        
        # 2. Fix service-category hover text visibility (force dark background + white text)
        bad_css = re.search(r'\.service-category:hover\s*{[^}]*}', content)
        if bad_css:
            good_hover_css = '''
        /* FIXED: Service category hover - always readable */
        .service-category:hover,
        .service-category:active {
            background: linear-gradient(135deg, #00C4B4, #0A1D37) !important;
            color: white !important;
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 25px 60px rgba(10,29,55,0.4);
        }
        .service-category:hover .category-title,
        .service-category:hover .category-services,
        .service-category:active .category-title,
        .service-category:active .category-services {
            color: white !important;
        }
        .service-category:hover .category-icon,
        .service-category:active .category-icon {
            color: #FFD700 !important;
        }
        '''
            content = content.replace(bad_css.group(0), good_hover_css)
        
        # 3. Make mobile animation permanent (remove the timeout that deletes it)
        content = re.sub(
            r'// Remove animation after it finishes[\s\S]*?}, 3000\);',
            '', 
            content
        )
        # Ensure the add-animation part stays
        if 'mobile-animated' not in content:
            mobile_js = '''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            if (window.innerWidth <= 768) {
                setTimeout(function() {
                    document.getElementById('mainServiceTile')?.classList.add('mobile-animated');
                    document.querySelectorAll('.service-category').forEach(el => el.classList.add('mobile-animated'));
                }, 3000);
            }
        });
        </script>
        '''
            content = content.replace('</body>', mobile_js + '</body>')
        
        if content != original:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1
            print(f"Fixed: {filename}")
    
    print("=" * 60)
    print(f"DONE! Fixed {fixed} pages. Everything is now consistent and unbreakable.")
    print("\nNow run:")
    print("git add services/")
    print('git commit -m "FINAL FIX: Professional descriptions + readable hover text + permanent mobile animations"')
    print("git push origin main")

if __name__ == "__main__":
    final_master_fix()
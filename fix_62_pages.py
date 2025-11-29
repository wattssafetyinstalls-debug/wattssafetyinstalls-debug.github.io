import os, re
print("Fixing all 62 service pages - removing .html from links")
total = updated = 0
for p in ["ada-compliant-showers.html","grab-bars.html","non-slip-flooring.html","custom-ramps.html","senior-safety.html","bathroom-accessibility.html","kitchen-renovations.html","deck-construction.html","siding-replacement.html","home-remodeling.html","basement-finishing.html","window-doors.html","fence-installation.html","drywall-repair.html","painting-services.html","concrete-pouring.html","driveway-installation.html","patio-construction.html","floor-refinishing.html","hardwood-flooring.html","concrete-repair.html","custom-cabinets.html","cabinet-refacing.html","onyx-countertops.html","kitchen-cabinetry.html","custom-storage.html","countertop-repair.html","property-maintenance-routine.html","emergency-repairs.html","snow-removal.html","seasonal-prep.html","tree-trimming.html","emergency-snow.html","lawn-maintenance.html","fertilization.html","landscape-design.html","seasonal-cleanup.html","garden-maintenance.html","tv-mounting-residential.html","home-theater.html","soundbar-setup.html","cable-management.html","smart-audio.html","projector-install.html","home-audio.html","audio-visual.html","bathroom-remodels.html","fence-repair.html","gutter-cleaning.html","handyman-services.html","pressure-washing.html","room-additions.html","stairlift-elevator-installation.html","wheelchair-ramp-installation.html"]:
    if os.path.exists(p):
        with open(p,"r",encoding="utf-8") as f: c = f.read()
        new, n1 = re.subn(r'(\bhref="[^"]*/services/[^"/]+)\.html(")', r'\1\2', c)
        new, n2 = re.subn(r'(og:url" content="[^"]+/services/[^"/]+)\.html(")', r'\1\2', new)
        if n1+n2:
            with open(p,"w",encoding="utf-8") as f: f.write(new)
            print(f"{p} → {n1+n2} links fixed")
            total += n1+n2; updated += 1
print(f"\nDONE! {updated} files updated, {total} .html removed")

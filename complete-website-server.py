#!/usr/bin/env python3
"""
Complete local website server - ALL pages working with proper redirects
"""

import http.server
import socketserver
import os
import urllib.parse

class CompleteWebsiteHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle root path
        if self.path == '/':
            self.path = '/index.html'
        
        # Handle main navigation pages
        elif self.path == '/contact':
            self.path = '/contact.html'
        elif self.path == '/about':
            self.path = '/about.html'
        elif self.path == '/services':
            self.path = '/services.html'
        elif self.path == '/service-area':
            self.path = '/service-area.html'
        elif self.path == '/referrals':
            self.path = '/referrals.html'
        
        # Handle ALL service page redirects (pretty URLs)
        elif self.path == '/ada-compliant-showers':
            self.path = '/services/ada-compliant-showers.html'
        elif self.path == '/grab-bars':
            self.path = '/services/grab-bars.html'
        elif self.path == '/non-slip-flooring':
            self.path = '/services/non-slip-flooring.html'
        elif self.path == '/custom-ramps':
            self.path = '/services/custom-ramps.html'
        elif self.path == '/senior-safety':
            self.path = '/services/senior-safety.html'
        elif self.path == '/bathroom-accessibility':
            self.path = '/services/bathroom-accessibility.html'
        elif self.path == '/wheelchair-ramps':
            self.path = '/services/wheelchair-ramp-installation.html'
        elif self.path == '/stairlift-installation':
            self.path = '/services/stairlift-elevator-installation.html'
        elif self.path == '/kitchen-renovations':
            self.path = '/services/kitchen-renovations.html'
        elif self.path == '/bathroom-remodels':
            self.path = '/services/bathroom-remodels.html'
        elif self.path == '/deck-construction':
            self.path = '/services/deck-construction.html'
        elif self.path == '/siding-replacement':
            self.path = '/services/siding-replacement.html'
        elif self.path == '/home-remodeling':
            self.path = '/services/home-remodeling.html'
        elif self.path == '/basement-finishing':
            self.path = '/services/basement-finishing.html'
        elif self.path == '/room-additions':
            self.path = '/services/room-additions.html'
        elif self.path == '/fence-installation':
            self.path = '/services/fence-installation.html'
        elif self.path == '/window-doors':
            self.path = '/services/window-doors.html'
        elif self.path == '/painting-services':
            self.path = '/services/painting-services.html'
        elif self.path == '/tv-mounting':
            self.path = '/services/tv-mounting.html'
        elif self.path == '/home-theater':
            self.path = '/services/home-theater-installation.html'
        elif self.path == '/soundbar-setup':
            self.path = '/services/sound-system-setup.html'
        elif self.path == '/cable-management':
            self.path = '/services/cable-management.html'
        elif self.path == '/smart-audio':
            self.path = '/services/audio-visual.html'
        elif self.path == '/projector-install':
            self.path = '/services/tv-home-theater-installation.html'
        elif self.path == '/snow-removal':
            self.path = '/services/snow-removal.html'
        elif self.path == '/lawn-maintenance':
            self.path = '/services/lawn-maintenance.html'
        elif self.path == '/landscape-design':
            self.path = '/services/landscape-design.html'
        elif self.path == '/garden-maintenance':
            self.path = '/services/garden-maintenance.html'
        elif self.path == '/tree-trimming':
            self.path = '/services/tree-trimming.html'
        elif self.path == '/emergency-repairs':
            self.path = '/services/emergency-repairs.html'
        elif self.path == '/seasonal-cleanup':
            self.path = '/services/seasonal-cleanup.html'
        elif self.path == '/gutter-cleaning':
            self.path = '/services/gutter-cleaning.html'
        elif self.path == '/pressure-washing':
            self.path = '/services/pressure-washing.html'
        elif self.path == '/concrete-pouring':
            self.path = '/services/concrete-pouring.html'
        elif self.path == '/driveway-installation':
            self.path = '/services/driveway-installation.html'
        elif self.path == '/patio-construction':
            self.path = '/services/patio-construction.html'
        elif self.path == '/hardwood-flooring':
            self.path = '/services/hardwood-flooring.html'
        elif self.path == '/floor-refinishing':
            self.path = '/services/floor-refinishing.html'
        elif self.path == '/custom-cabinets':
            self.path = '/services/custom-cabinets.html'
        elif self.path == '/cabinet-refacing':
            self.path = '/services/cabinet-refacing.html'
        elif self.path == '/onyx-countertops':
            self.path = '/services/onyx-countertops.html'
        elif self.path == '/kitchen-cabinetry':
            self.path = '/services/kitchen-cabinetry.html'
        elif self.path == '/accessibility-safety':
            self.path = '/services/accessibility-safety-solutions.html'
        elif self.path == '/ada-showers-bathrooms':
            self.path = '/services/ada-compliant-showers-bathrooms.html'
        elif self.path == '/audio-visual':
            self.path = '/services/audio-visual.html'
        elif self.path == '/basement-finishing':
            self.path = '/services/basement-finishing.html'
        elif self.path == '/cabinet-refacing':
            self.path = '/services/cabinet-refacing.html'
        elif self.path == '/concrete-repair':
            self.path = '/services/concrete-repair.html'
        elif self.path == '/countertop-repair':
            self.path = '/services/countertop-repair.html'
        elif self.path == '/custom-storage':
            self.path = '/services/custom-storage.html'
        elif self.path == '/drywall-repair':
            self.path = '/services/drywall-repair.html'
        elif self.path == '/emergency-snow':
            self.path = '/services/emergency-snow.html'
        elif self.path == '/fence-repair':
            self.path = '/services/fence-repair.html'
        elif self.path == '/fertilization':
            self.path = '/services/fertilization.html'
        elif self.path == '/flooring-installation':
            self.path = '/services/flooring-installation.html'
        elif self.path == '/grab-bar-installation':
            self.path = '/services/grab-bar-installation.html'
        elif self.path == '/handyman-repair':
            self.path = '/services/handyman-repair-services.html'
        elif self.path == '/handyman-services':
            self.path = '/services/handyman-services.html'
        elif self.path == '/home-audio':
            self.path = '/services/home-audio.html'
        elif self.path == '/home-remodeling-renovation':
            self.path = '/services/home-remodeling-renovation.html'
        elif self.path == '/non-slip-flooring-solutions':
            self.path = '/services/non-slip-flooring-solutions.html'
        elif self.path == '/painting-drywall':
            self.path = '/services/painting-drywall.html'
        elif self.path == '/property-maintenance':
            self.path = '/services/property-maintenance-services.html'
        elif self.path == '/seasonal-prep':
            self.path = '/services/seasonal-prep.html'
        elif self.path == '/sound-system-setup':
            self.path = '/services/sound-system-setup.html'
        elif self.path == '/stairlift-elevator':
            self.path = '/services/stairlift-elevator-installation.html'
        elif self.path == '/tv-home-theater':
            self.path = '/services/tv-home-theater-installation.html'
        elif self.path == '/tv-mounting-residential':
            self.path = '/services/tv-mounting-residential.html'
        elif self.path == '/wheelchair-ramp-installation':
            self.path = '/services/wheelchair-ramp-installation.html'

        # Serve the file
        return super().do_GET()

def run_complete_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), CompleteWebsiteHandler) as httpd:
        print("COMPLETE WEBSITE SERVER RUNNING")
        print("=" * 50)
        print("Server: http://localhost:8000")
        print("Directory: " + os.getcwd())
        print()
        print("TEST ALL PAGES:")
        print("Homepage: http://localhost:8000/")
        print("Services: http://localhost:8000/services")
        print("Contact: http://localhost:8000/contact")
        print("About: http://localhost:8000/about")
        print("Service Area: http://localhost:8000/service-area")
        print("Referrals: http://localhost:8000/referrals")
        print()
        print("TEST PRETTY URLS:")
        print("TV Mounting: http://localhost:8000/tv-mounting")
        print("Snow Removal: http://localhost:8000/snow-removal")
        print("Kitchen Renovations: http://localhost:8000/kitchen-renovations")
        print("ADA Showers: http://localhost:8000/ada-compliant-showers")
        print("Wheelchair Ramps: http://localhost:8000/wheelchair-ramps")
        print()
        print("TEST DIRECT SERVICE PAGES:")
        print("http://localhost:8000/services/tv-mounting.html")
        print("http://localhost:8000/services/snow-removal.html")
        print("http://localhost:8000/services/ada-compliant-showers.html")
        print()
        print("CLICK EVERYTHING! All navigation should work.")
        print("Press Ctrl+C to stop server")
        print("=" * 50)
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")

if __name__ == "__main__":
    run_complete_server()
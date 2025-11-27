#!/usr/bin/env python3
"""
Local test server that handles pretty URL redirects - Windows compatible
"""

import http.server
import socketserver
import urllib.parse

# Your redirect mappings
REDIRECTS = {
    '/ada-compliant-showers': '/services/ada-compliant-showers.html',
    '/grab-bars': '/services/grab-bars.html',
    '/non-slip-flooring': '/services/non-slip-flooring.html',
    '/custom-ramps': '/services/custom-ramps.html',
    '/senior-safety': '/services/senior-safety.html',
    '/bathroom-accessibility': '/services/bathroom-accessibility.html',
    '/wheelchair-ramps': '/services/wheelchair-ramp-installation.html',
    '/stairlift-installation': '/services/stairlift-elevator-installation.html',
    '/kitchen-renovations': '/services/kitchen-renovations.html',
    '/bathroom-remodels': '/services/bathroom-remodels.html',
    '/deck-construction': '/services/deck-construction.html',
    '/siding-replacement': '/services/siding-replacement.html',
    '/home-remodeling': '/services/home-remodeling.html',
    '/basement-finishing': '/services/basement-finishing.html',
    '/room-additions': '/services/room-additions.html',
    '/fence-installation': '/services/fence-installation.html',
    '/window-doors': '/services/window-doors.html',
    '/painting-services': '/services/painting-services.html',
    '/tv-mounting': '/services/tv-mounting.html',
    '/home-theater': '/services/home-theater-installation.html',
    '/soundbar-setup': '/services/sound-system-setup.html',
    '/cable-management': '/services/cable-management.html',
    '/smart-audio': '/services/audio-visual.html',
    '/projector-install': '/services/tv-home-theater-installation.html',
    '/snow-removal': '/services/snow-removal.html',
    '/lawn-maintenance': '/services/lawn-maintenance.html',
    '/landscape-design': '/services/landscape-design.html',
    '/garden-maintenance': '/services/garden-maintenance.html',
    '/tree-trimming': '/services/tree-trimming.html',
    '/emergency-repairs': '/services/emergency-repairs.html',
    '/seasonal-cleanup': '/services/seasonal-cleanup.html',
    '/gutter-cleaning': '/services/gutter-cleaning.html',
    '/pressure-washing': '/services/pressure-washing.html',
    '/concrete-pouring': '/services/concrete-pouring.html',
    '/driveway-installation': '/services/driveway-installation.html',
    '/patio-construction': '/services/patio-construction.html',
    '/hardwood-flooring': '/services/hardwood-flooring.html',
    '/floor-refinishing': '/services/floor-refinishing.html',
    '/custom-cabinets': '/services/custom-cabinets.html',
    '/cabinet-refacing': '/services/cabinet-refacing.html',
    '/onyx-countertops': '/services/onyx-countertops.html',
    '/kitchen-cabinetry': '/services/kitchen-cabinetry.html'
}

class LocalRedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Handle pretty URL redirects
        if self.path in REDIRECTS:
            self.send_response(302)
            self.send_header('Location', REDIRECTS[self.path])
            self.end_headers()
            return
        
        # Serve files normally
        super().do_GET()

def run_local_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), LocalRedirectHandler) as httpd:
        print("Local test server running at: http://localhost:8000")
        print("Serving from: " + os.getcwd())
        print("Testing pretty URLs:")
        print("  http://localhost:8000/tv-mounting")
        print("  http://localhost:8000/snow-removal") 
        print("  http://localhost:8000/kitchen-renovations")
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()

if __name__ == "__main__":
    import os
    run_local_server()
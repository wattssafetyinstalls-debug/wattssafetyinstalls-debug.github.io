#!/usr/bin/env python3
"""
Local test server that serves content at pretty URLs without redirecting
"""

import http.server
import socketserver
import os

# Map pretty URLs to actual files
PRETTY_URLS = {
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

class PrettyURLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Check if this is a pretty URL
        if self.path in PRETTY_URLS:
            # Serve the file content directly without redirecting
            file_path = PRETTY_URLS[self.path]
            if os.path.exists('.' + file_path):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                with open('.' + file_path, 'rb') as f:
                    self.wfile.write(f.read())
                return
        
        # Serve files normally for everything else
        super().do_GET()

def run_pretty_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), PrettyURLHandler) as httpd:
        print("Pretty URL server running at: http://localhost:8000")
        print("Testing pretty URLs (will NOT show .html extension):")
        print("  http://localhost:8000/tv-mounting")
        print("  http://localhost:8000/snow-removal") 
        print("  http://localhost:8000/kitchen-renovations")
        print("Press Ctrl+C to stop the server")
        httpd.serve_forever()

if __name__ == "__main__":
    run_pretty_server()
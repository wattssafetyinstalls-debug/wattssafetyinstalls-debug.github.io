import http.server
import socketserver
import os

PORT = 8000

class PrettyURLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        if path.endswith('/'):
            path += 'index.html'
        
        # Handle pretty URLs for main pages and services
        if '.' not in os.path.basename(path) and not path.endswith('/'):
            html_path = path + '.html'
            if os.path.exists(html_path.lstrip('/')):
                self.path = html_path
        
        # Special case for /services -> services.html
        if path == '/services' or path == '/services/':
            self.path = '/services.html'
        
        # Handle service pages like /services/siding-replacement -> services/siding-replacement.html
        if path.startswith('/services/') and '.' not in os.path.basename(path):
            service_html = path.lstrip('/') + '.html'
            if os.path.exists(service_html):
                self.path = '/' + service_html
            else:
                self.send_error(404, "File not found")
                return
        
        return super().do_GET()
    
    def list_directory(self, path):
        self.send_error(403, "Directory listing denied")
        return None

with socketserver.TCPServer(("", PORT), PrettyURLHandler) as httpd:
    print(f"Server running at http://localhost:{PORT}")
    print("Supports pretty URLs (no .html), mobile animation testing, no directory listings.")
    print("Test URLs:")
    print("  Home: http://localhost:8000/")
    print("  About: http://localhost:8000/about")
    print("  Services: http://localhost:8000/services")
    print("  Service Page: http://localhost:8000/services/siding-replacement")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()
import http.server
import socketserver
import os
import urllib.parse

PORT = 8000

class ImprovedPrettyURLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse and normalize path (handle query params if any)
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        # Normalize trailing slash
        if path.endswith('/') and path != '/':
            path = path.rstrip('/')
        
        # Handle root
        if path == '/' or path == '':
            self.path = '/index.html'
            return super().do_GET()
        
        # Special case for /services (with or without slash)
        if path in ['/services', '/services/']:
            if os.path.exists('services.html'):
                self.path = '/services.html'
                return super().do_GET()
            else:
                self.send_error(404, "Services page not found")
                return
        
        # Handle main pages without extension
        if '.' not in os.path.basename(path):
            html_path = path + '.html'
            if os.path.exists(html_path.lstrip('/')):
                self.path = html_path
                return super().do_GET()
        
        # Handle service pages like /services/siding-replacement
        if path.startswith('/services/') and '.' not in os.path.basename(path):
            service_name = path.split('/')[-1]
            service_html = f'services/{service_name}.html'
            if os.path.exists(service_html):
                self.path = '/' + service_html
                return super().do_GET()
            else:
                self.send_error(404, "Service page not found")
                return
        
        # Fallback to default handling
        return super().do_GET()
    
    def list_directory(self, path):
        self.send_error(403, "Directory listing denied")
        return None

with socketserver.TCPServer(("", PORT), ImprovedPrettyURLHandler) as httpd:
    print(f"Improved Server running at http://localhost:{PORT}")
    print("Handles pretty URLs, fixes services link, no directory listings.")
    print("Test URLs:")
    print("  Home: http://localhost:8000/")
    print("  About: http://localhost:8000/about")
    print("  Services: http://localhost:8000/services")
    print("  Service Page: http://localhost:8000/services/siding-replacement")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()
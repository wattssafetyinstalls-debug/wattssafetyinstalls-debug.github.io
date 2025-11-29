import http.server
import socketserver
import os
import urllib.parse

PORT = 8000

class RedirectPrettyURLHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path.rstrip('/')  # Normalize by removing trailing slash
        
        # If path ends with .html, redirect (301) to extensionless version
        if path.endswith('.html'):
            redirect_path = path[:-5]  # Remove .html
            if redirect_path == '/services':  # Special case for services.html
                redirect_path = '/services'
            self.send_response(301)
            self.send_header('Location', redirect_path)
            self.end_headers()
            return
        
        # Handle /services specially (serve services.html)
        if path == '/services':
            file_path = 'services.html'
            if os.path.exists(file_path):
                self.path = '/services.html'
                return super().do_GET()
            else:
                self.send_error(404, "File not found")
                return
        
        # For main pages (e.g., /about), append .html if exists
        html_path = path + '.html'
        if os.path.exists(html_path.lstrip('/')):
            self.path = html_path
            return super().do_GET()
        
        # For service subpages (e.g., /services/siding-replacement)
        if path.startswith('/services/'):
            service_name = path.split('/')[-1]
            service_html = f'services/{service_name}.html'
            if os.path.exists(service_html):
                self.path = '/' + service_html
                return super().do_GET()
        
        # Fallback: if no match, 404 instead of listing
        self.send_error(404, "File not found")
    
    def list_directory(self, path):
        self.send_error(403, "Directory listing denied")
        return None

with socketserver.TCPServer(("", PORT), RedirectPrettyURLHandler) as httpd:
    print(f"Redirect Server running at http://localhost:{PORT}")
    print("Handles 301 redirects for .html to pretty URLs, fixes services link, no 404s for valid pages.")
    print("Test URLs:")
    print("  Home: http://localhost:8000/")
    print("  About: http://localhost:8000/about")
    print("  Services: http://localhost:8000/services")
    print("  Service Page: http://localhost:8000/services/siding-replacement")
    print("  Test Redirect: http://localhost:8000/about.html (should 301 to /about)")
    print("Press Ctrl+C to stop.")
    httpd.serve_forever()
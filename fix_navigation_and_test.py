import os
import http.server
import socketserver

# First, let's create proper redirects for the main pages
def create_redirect_html():
    """Create redirect pages for main navigation"""
    main_pages = ['about', 'service-area', 'referrals', 'contact', 'privacy-policy', 'sitemap']
    
    for page in main_pages:
        redirect_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="refresh" content="0; url=/{page}.html">
</head>
<body>
    <p>Redirecting to <a href="/{page}.html">{page}</a>...</p>
</body>
</html>"""
        
        with open(f'{page}', 'w') as f:
            f.write(redirect_html)
        print(f"Created redirect for: {page}")

# Custom handler to serve HTML files without extensions
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # If path doesn't have an extension and file exists with .html, serve it
        if '.' not in self.path.split('/')[-1]:
            html_path = self.path + '.html'
            if os.path.exists(html_path.lstrip('/')):
                self.path = html_path
        elif self.path.endswith('/'):
            # Handle directory listings properly
            self.path = self.path + 'index.html'
            
        return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def list_directory(self, path):
        # Disable directory listings
        self.send_error(404, "No permission to list directory")
        return None

def start_proper_server():
    PORT = 8000
    
    # Create redirect files first
    create_redirect_html()
    
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Proper Website Server running at http://localhost:{PORT}")
        print("Test these URLs:")
        print(f"  Home: http://localhost:{PORT}/")
        print(f"  Services: http://localhost:{PORT}/services.html") 
        print(f"  About: http://localhost:{PORT}/about")
        print(f"  Contact: http://localhost:{PORT}/contact")
        print(f"  Service Area: http://localhost:{PORT}/service-area")
        print(f"  Service Page: http://localhost:{8000}/services/siding-replacement.html")
        print("")
        print("IMPORTANT: Use these exact URLs for testing")
        print("Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")

if __name__ == "__main__":
    start_proper_server()
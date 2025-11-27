#!/usr/bin/env python3
import http.server
import socketserver
import os
import urllib.parse

class RedirectHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse the path
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        print(f"REQUEST: {path}")
        
        # Check if it's a service page without .html
        if path.startswith('/services/') and not path.endswith('.html'):
            service_name = path.split('/')[-1]
            html_path = f"/services/{service_name}.html"
            
            # Check if the HTML file exists
            if os.path.exists(html_path[1:]):  # Remove leading slash for file path
                print(f"REDIRECTING: {path} -> {html_path}")
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                # Serve the HTML file
                with open(html_path[1:], 'rb') as f:
                    self.wfile.write(f.read())
                return
            else:
                print(f"NOT FOUND: {html_path}")
        
        # Default behavior - serve files normally
        super().do_GET()

def run_server():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), RedirectHandler) as httpd:
        print(f" Server running at http://localhost:{PORT}")
        print(" Serving from:", os.getcwd())
        print("\n Test these service page redirects:")
        print("   http://localhost:8000/services/tv-mounting")
        print("   http://localhost:8000/services/ada-compliant-showers") 
        print("   http://localhost:8000/services/kitchen-renovations")
        print("   http://localhost:8000/services/snow-removal")
        print("\n Or access with .html extension:")
        print("   http://localhost:8000/services/tv-mounting.html")
        print("\nPress Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n⏹️ Server stopped")

if __name__ == "__main__":
    run_server()
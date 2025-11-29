import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

def start_test_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Mobile Testing Server running at http://localhost:{PORT}")
        print("Test these URLs:")
        print(f"   http://localhost:{PORT}/services/siding-replacement.html")
        print(f"   http://localhost:{PORT}/services/tv-mounting.html")
        print(f"   http://localhost:{PORT}/services/ada-compliant-showers.html")
        print("Use Chrome DevTools Mobile Emulation or visit on your phone")
        print("Press Ctrl+C to stop the server")
        
        # Open in browser
        webbrowser.open(f'http://localhost:{PORT}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")

if __name__ == "__main__":
    start_test_server()
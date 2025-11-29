import http.server
import socketserver
import webbrowser
import os

PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

def start_full_server():
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Full Website Server running at http://localhost:{PORT}")
        print("Test ALL pages and navigation:")
        print(f"  Home: http://localhost:{PORT}/")
        print(f"  Services: http://localhost:{PORT}/services")
        print(f"  About: http://localhost:{PORT}/about") 
        print(f"  Contact: http://localhost:{PORT}/contact")
        print(f"  Service Area: http://localhost:{PORT}/service-area")
        print(f"  Example Service: http://localhost:{PORT}/services/siding-replacement.html")
        print("Use Chrome Mobile Emulation (F12 -> Ctrl+Shift+M) to test mobile")
        print("Press Ctrl+C to stop the server")
        
        webbrowser.open(f'http://localhost:{PORT}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("Server stopped.")

if __name__ == "__main__":
    start_full_server()
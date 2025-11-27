import http.server
import socketserver
import webbrowser
import os
import sys

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        super().end_headers()
    
    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {self.address_string()} - {format % args}")

def start_test_server(port=8000):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
        print("=" * 60)
        print("LOCAL TEST SERVER RUNNING")
        print(f"Serving from: {os.getcwd()}")
        print(f"Local URL: http://localhost:{port}")
        print("=" * 60)
        print("Press Ctrl+C to stop the server")
        print("-" * 60)
        
        webbrowser.open(f'http://localhost:{port}')
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nSERVER STOPPED")

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    start_test_server(port)
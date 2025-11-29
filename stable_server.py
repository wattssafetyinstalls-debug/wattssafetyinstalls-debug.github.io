# stable_server.py
import http.server
import socketserver
import os
import urllib.parse
import time

class StableHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def log_message(self, format, *args):
        # Custom logging to avoid connection error spam
        try:
            print(f"{self.log_date_time_string()} - {format % args}")
        except:
            pass
    
    def do_GET(self):
        try:
            # Parse the path
            parsed_path = urllib.parse.urlparse(self.path)
            path = parsed_path.path
            
            # Handle pretty URLs
            if path == '/':
                path = '/index.html'
            elif not '.' in path.split('/')[-1] and path != '/':  # No file extension
                if os.path.exists('.' + path + '.html'):
                    path = path + '.html'
            
            # Set the path and serve the file
            self.path = path
            
            # Call the parent method with error handling
            super().do_GET()
            
        except (ConnectionAbortedError, BrokenPipeError) as e:
            # Silently handle connection errors - they're usually browser-side
            pass
        except Exception as e:
            print(f"Unexpected error: {e}")

# Use port 8080 for better stability
PORT = 8080

with socketserver.TCPServer(("", PORT), StableHTTPRequestHandler) as httpd:
    print(f"Stable server running at http://localhost:{PORT}")
    print("Handles connection errors gracefully")
    print("Press Ctrl+C to stop the server")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped gracefully")
#!/usr/bin/env python3
"""
Simple HTTP server to serve the GarageBand Voice Controller web interface
This allows persistent microphone permissions and better browser compatibility

Usage:
python http_server.py
Then open http://localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
import threading
import time

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add headers for better security and functionality
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_GET(self):
        # Serve app.html for the root path (the working interface)
        if self.path == '/':
            self.path = '/app.html'
        return super().do_GET()

def start_http_server(port=8000):
    """Start HTTP server to serve the web interface"""
    
    # Change to the directory containing the HTML file
    web_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(web_dir)
    
    handler = CustomHTTPRequestHandler
    
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print("🌐 GarageBand Voice Controller Web Server")
            print("=" * 50)
            print(f"Serving at: http://localhost:{port}")
            print("Web interface will open automatically...")
            print("Make sure the WebSocket server is also running!")
            print("=" * 50)
            
            # Open browser after a short delay
            def open_browser():
                time.sleep(1)
                webbrowser.open(f'http://localhost:{port}')
            
            browser_thread = threading.Thread(target=open_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Port {port} is already in use.")
            print(f"Try opening http://localhost:{port} in your browser,")
            print("or stop the existing server and try again.")
        else:
            print(f"❌ Error starting server: {e}")

if __name__ == "__main__":
    start_http_server() 
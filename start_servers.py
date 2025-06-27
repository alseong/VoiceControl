#!/usr/bin/env python3
"""
Start both servers for GarageBand Voice Controller
- WebSocket server (for GarageBand control)
- HTTP server (for web interface)

Usage:
python start_servers.py
"""

import subprocess
import sys
import time
import signal
import os

def start_servers():
    """Start both WebSocket and HTTP servers"""
    print("🎵 Starting GarageBand Voice Controller Servers")
    print("=" * 50)
    
    # Start WebSocket server
    print("Starting WebSocket server...")
    websocket_process = subprocess.Popen([
        sys.executable, "web_server.py"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Give WebSocket server time to start
    time.sleep(2)
    
    # Start HTTP server
    print("Starting HTTP server...")
    http_process = subprocess.Popen([
        sys.executable, "http_server.py"
    ])
    
    print("\n✅ Both servers started!")
    print("🎵 WebSocket server: localhost:8765")
    print("🌐 Web interface: http://localhost:8000")
    print("\nPress Ctrl+C to stop both servers")
    
    def signal_handler(sig, frame):
        print("\n🛑 Shutting down servers...")
        websocket_process.terminate()
        http_process.terminate()
        print("👋 Goodbye!")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        # Wait for both processes
        websocket_process.wait()
        http_process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    start_servers() 
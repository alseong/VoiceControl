#!/usr/bin/env python3
"""
GarageBand Voice Control - Standalone Version
Complete voice control for GarageBand with web interface

Download and run this single file:
1. Install dependencies: pip install speechrecognition pyaudio pynput
2. Run: python3 garageband_voice_control_standalone.py
3. Open browser to http://localhost:8080
4. Click microphone and start voice controlling GarageBand!

Requirements:
- macOS with GarageBand
- Python 3.6+
- Microphone access permission
- Accessibility permission for keyboard control
"""

import speech_recognition as sr
import time
from pynput import keyboard
from pynput.keyboard import Key
import threading
import sys
import http.server
import socketserver
import webbrowser
import json
import os
from urllib.parse import urlparse, parse_qs

class GarageBandController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.controller = keyboard.Controller()
        self.last_command = ""
        self.command_history = []
        
        # GarageBand commands
        self.commands = {
            # Playback & Recording
            "play": [Key.space], "stop": [Key.space], "pause": [Key.space],
            "record": ['r'], "start recording": ['r'], "stop recording": ['r'],
            
            # Navigation
            "go to beginning": [Key.enter], "beginning": [Key.enter],
            "rewind": [Key.home], "fast forward": [Key.end],
            "next bar": ['.'], "previous bar": [','],
            
            # Zoom
            "zoom in": [Key.cmd, Key.right], "zoom out": [Key.cmd, Key.left],
            
            # Tracks
            "new track": [Key.cmd, Key.alt, 'n'], "delete track": [Key.cmd, Key.delete],
            "duplicate track": [Key.cmd, 'd'], "mute track": ['m'], "solo track": ['s'],
            "next track": [Key.down], "previous track": [Key.up],
            
            # Editing
            "undo": [Key.cmd, 'z'], "redo": [Key.cmd, Key.shift, 'z'],
            "cut": [Key.cmd, 'x'], "copy": [Key.cmd, 'c'], "paste": [Key.cmd, 'v'],
            "split": [Key.cmd, 't'], "join": [Key.cmd, 'j'], "delete": [Key.delete],
            
            # Tools
            "toggle loop": ['l'], "toggle cycle": ['c'], "toggle metronome": ['k'],
            "save": [Key.cmd, 's'], "new project": [Key.cmd, 'n'],
            
            # Display
            "show library": ['y'], "show editor": ['e'], "show piano roll": ['p'],
            "show smart controls": ['b'], "show automation": ['a'],
        }
        
        # Setup microphone
        print("🎵 Setting up GarageBand Voice Control...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("✅ Ready!")

    def send_keyboard_shortcut(self, keys):
        """Send keyboard shortcut to GarageBand"""
        try:
            if len(keys) == 1:
                self.controller.press(keys[0])
                self.controller.release(keys[0])
            else:
                # Press modifiers first
                for key in keys[:-1]:
                    self.controller.press(key)
                self.controller.press(keys[-1])
                self.controller.release(keys[-1])
                for key in reversed(keys[:-1]):
                    self.controller.release(key)
            
            # Format shortcut display
            key_names = []
            for key in keys:
                if hasattr(key, 'name'):
                    key_names.append(key.name.upper())
                elif isinstance(key, str):
                    key_names.append(key.upper())
                else:
                    key_names.append(str(key))
            
            shortcut = " + ".join(key_names)
            print(f"🎹 Executed: {shortcut}")
            return shortcut
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def process_command(self, command_text):
        """Process voice command"""
        command_text = command_text.lower().strip()
        self.last_command = command_text
        
        # Check for exact match
        if command_text in self.commands:
            shortcut = self.send_keyboard_shortcut(self.commands[command_text])
            result = {
                "success": True,
                "command": command_text,
                "shortcut": shortcut,
                "timestamp": time.strftime("%H:%M:%S")
            }
            self.command_history.append(result)
            return result
        
        # Try partial matching
        for cmd in self.commands:
            if cmd in command_text or command_text in cmd:
                shortcut = self.send_keyboard_shortcut(self.commands[cmd])
                result = {
                    "success": True,
                    "command": f"{command_text} → {cmd}",
                    "shortcut": shortcut,
                    "timestamp": time.strftime("%H:%M:%S")
                }
                self.command_history.append(result)
                return result
        
        # Command not found
        result = {
            "success": False,
            "command": command_text,
            "error": "Command not recognized",
            "timestamp": time.strftime("%H:%M:%S")
        }
        self.command_history.append(result)
        return result

    def start_listening(self):
        """Start continuous voice recognition"""
        if self.is_listening:
            return
            
        self.is_listening = True
        print("🎧 Starting voice recognition...")
        
        def listen_loop():
            while self.is_listening:
                try:
                    with self.microphone as source:
                        audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    
                    command = self.recognizer.recognize_google(audio, language='en-US')
                    print(f"🎤 Heard: '{command}'")
                    self.process_command(command)
                    
                except sr.UnknownValueError:
                    pass  # No speech detected
                except sr.RequestError as e:
                    print(f"❌ Speech recognition error: {e}")
                except sr.WaitTimeoutError:
                    pass  # Timeout, continue listening
                except Exception as e:
                    print(f"❌ Error: {e}")
                    time.sleep(1)
        
        self.listen_thread = threading.Thread(target=listen_loop)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def stop_listening(self):
        """Stop voice recognition"""
        self.is_listening = False
        print("⏹️ Stopped listening")

    def get_status(self):
        """Get current status"""
        return {
            "listening": self.is_listening,
            "last_command": self.last_command,
            "history": self.command_history[-10:],  # Last 10 commands
            "total_commands": len(self.commands)
        }

# Web Interface HTML
WEB_INTERFACE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GarageBand Voice Control</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh; color: white; padding: 20px;
        }
        .container { max-width: 800px; margin: 0 auto; }
        .header { text-align: center; margin-bottom: 40px; }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .controls { text-align: center; margin-bottom: 40px; }
        .mic-button {
            width: 120px; height: 120px; border-radius: 50%; border: none;
            font-size: 3rem; cursor: pointer; margin: 0 10px;
            transition: all 0.3s ease; color: white;
        }
        .mic-button.start { background: linear-gradient(135deg, #4CAF50, #45a049); }
        .mic-button.stop { background: linear-gradient(135deg, #f44336, #d32f2f); }
        .mic-button:hover { transform: scale(1.1); }
        .status { 
            background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px;
            margin-bottom: 30px; backdrop-filter: blur(10px);
        }
        .history { background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; }
        .command-item { 
            padding: 10px; margin: 5px 0; border-radius: 5px;
            background: rgba(255,255,255,0.1);
        }
        .success { border-left: 4px solid #4CAF50; }
        .error { border-left: 4px solid #f44336; }
        .commands-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px; margin-top: 20px;
        }
        .command-category { background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; }
        .command-category h4 { margin-bottom: 10px; color: #ffd93d; }
        .command-list { list-style: none; }
        .command-list li { padding: 3px 0; font-size: 0.9rem; opacity: 0.9; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎵 GarageBand Voice Control</h1>
            <p>Control GarageBand with your voice - Make sure GarageBand is open!</p>
        </div>
        
        <div class="controls">
            <button id="startBtn" class="mic-button start" onclick="startListening()">🎤</button>
            <button id="stopBtn" class="mic-button stop" onclick="stopListening()">⏹️</button>
        </div>
        
        <div class="status">
            <h3>Status: <span id="status">Ready</span></h3>
            <p>Last Command: <span id="lastCommand">None</span></p>
            <p>Total Commands Available: <span id="totalCommands">0</span></p>
        </div>
        
        <div class="history">
            <h3>Recent Commands</h3>
            <div id="commandHistory"></div>
        </div>
        
        <div class="commands-grid">
            <div class="command-category">
                <h4>🎤 Playback</h4>
                <ul class="command-list">
                    <li>play / stop / pause</li>
                    <li>record</li>
                    <li>beginning</li>
                </ul>
            </div>
            <div class="command-category">
                <h4>🎵 Tracks</h4>
                <ul class="command-list">
                    <li>new track</li>
                    <li>delete track</li>
                    <li>mute track / solo track</li>
                    <li>next track / previous track</li>
                </ul>
            </div>
            <div class="command-category">
                <h4>✂️ Editing</h4>
                <ul class="command-list">
                    <li>undo / redo</li>
                    <li>cut / copy / paste</li>
                    <li>split / join</li>
                </ul>
            </div>
            <div class="command-category">
                <h4>🔧 Tools</h4>
                <ul class="command-list">
                    <li>zoom in / zoom out</li>
                    <li>toggle loop</li>
                    <li>toggle metronome</li>
                    <li>save</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        function startListening() {
            fetch('/api/start').then(r => r.json()).then(updateStatus);
        }
        
        function stopListening() {
            fetch('/api/stop').then(r => r.json()).then(updateStatus);
        }
        
        function updateStatus(data) {
            document.getElementById('status').textContent = data.listening ? 'Listening...' : 'Ready';
            document.getElementById('lastCommand').textContent = data.last_command || 'None';
            document.getElementById('totalCommands').textContent = data.total_commands;
            
            const historyDiv = document.getElementById('commandHistory');
            historyDiv.innerHTML = '';
            
            data.history.forEach(cmd => {
                const div = document.createElement('div');
                div.className = `command-item ${cmd.success ? 'success' : 'error'}`;
                div.innerHTML = `
                    <strong>${cmd.command}</strong>
                    ${cmd.success ? `→ ${cmd.shortcut}` : `(${cmd.error})`}
                    <small style="float: right;">${cmd.timestamp}</small>
                `;
                historyDiv.appendChild(div);
            });
        }
        
        // Update status every 2 seconds
        setInterval(() => {
            fetch('/api/status').then(r => r.json()).then(updateStatus);
        }, 2000);
        
        // Initial status load
        updateStatus({listening: false, last_command: '', history: [], total_commands: 0});
    </script>
</body>
</html>"""

class WebHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, controller=None, **kwargs):
        self.controller = controller
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(WEB_INTERFACE.encode())
        elif self.path == '/api/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = self.controller.get_status()
            self.wfile.write(json.dumps(status).encode())
        elif self.path == '/api/start':
            self.controller.start_listening()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = self.controller.get_status()
            self.wfile.write(json.dumps(status).encode())
        elif self.path == '/api/stop':
            self.controller.stop_listening()
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            status = self.controller.get_status()
            self.wfile.write(json.dumps(status).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress server logs

def main():
    print("🎵 GarageBand Voice Control - Standalone Version")
    print("=" * 50)
    
    # Create controller
    controller = GarageBandController()
    
    # Create web server
    handler = lambda *args, **kwargs: WebHandler(*args, controller=controller, **kwargs)
    
    port = 8080
    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print(f"🌐 Web interface: http://localhost:{port}")
            print("🎤 Voice control ready!")
            print("=" * 50)
            print("1. Open the web interface in your browser")
            print("2. Make sure GarageBand is open and focused")
            print("3. Click the microphone button to start voice control")
            print("4. Say commands like 'play', 'stop', 'new track', etc.")
            print("=" * 50)
            print("Press Ctrl+C to stop")
            
            # Open browser
            webbrowser.open(f'http://localhost:{port}')
            
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        controller.stop_listening()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 
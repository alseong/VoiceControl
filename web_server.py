#!/usr/bin/env python3
"""
GarageBand Web Control Server
WebSocket server that receives commands from web browser and controls GarageBand

Requirements:
pip install websockets pynput

Usage:
python web_server.py
Then open http://localhost:8000 in your browser
"""

import asyncio
import websockets
import json
import time
from pynput import keyboard
from pynput.keyboard import Key
import threading
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GarageBandWebController:
    def __init__(self):
        self.controller = keyboard.Controller()
        self.connected_clients = set()
        
        # GarageBand voice commands mapped to keyboard shortcuts
        self.commands = {
            # === PLAYBACK & RECORDING ===
            "play": [Key.space],
            "stop": [Key.space],
            "pause": [Key.space],
            "record": ['r'],
            "start recording": ['r'],
            "stop recording": ['r'],
            
            # === NAVIGATION ===
            "go to beginning": [Key.enter],
            "go to start": [Key.enter],
            "beginning": [Key.enter],
            "rewind": [Key.home],
            "fast forward": [Key.end],
            "next bar": ['.'],
            "previous bar": [','],
            "move forward": ['.'],
            "move back": [','],
            
            # === ZOOM ===
            "zoom in": [Key.cmd, Key.right],
            "zoom out": [Key.cmd, Key.left],
            
            # === TRACK OPERATIONS ===
            "new track": [Key.cmd, Key.alt, 'n'],
            "create track": [Key.cmd, Key.alt, 'n'],
            "add track": [Key.cmd, Key.alt, 'n'],
            "new audio track": [Key.cmd, Key.alt, 'a'],
            "delete track": [Key.cmd, Key.delete],
            "duplicate track": [Key.cmd, 'd'],
            "mute track": ['m'],
            "solo track": ['s'],
            "unmute track": ['m'],
            "unsolo track": ['s'],
            
            # === EDITING ===
            "undo": [Key.cmd, 'z'],
            "redo": [Key.cmd, Key.shift, 'z'],
            "cut": [Key.cmd, 'x'],
            "copy": [Key.cmd, 'c'],
            "paste": [Key.cmd, 'v'],
            "split": [Key.cmd, 't'],
            "split region": [Key.cmd, 't'],
            "join": [Key.cmd, 'j'],
            "join regions": [Key.cmd, 'j'],
            "delete": [Key.delete],
            
            # === LOOP & CYCLE ===
            "toggle loop": ['l'],
            "loop region": ['l'],
            "cycle on": ['c'],
            "cycle off": ['c'],
            "toggle cycle": ['c'],
            
            # === METRONOME ===
            "metronome on": ['k'],
            "metronome off": ['k'],
            "toggle metronome": ['k'],
            "click track": ['k'],
            
            # === DISPLAY TOGGLES ===
            "show library": ['y'],
            "hide library": ['y'],
            "show browser": ['o'],
            "hide browser": ['o'],
            "show editor": ['e'],
            "hide editor": ['e'],
            "show piano roll": ['p'],
            "hide piano roll": ['p'],
            "show smart controls": ['b'],
            "hide smart controls": ['b'],
            
            # === PROJECT MANAGEMENT ===
            "save": [Key.cmd, 's'],
            "save project": [Key.cmd, 's'],
            "new project": [Key.cmd, 'n'],
            "open project": [Key.cmd, 'o'],
            
            # === AUTOMATION ===
            "show automation": ['a'],
            "hide automation": ['a'],
            "automation on": ['a'],
            "automation off": ['a'],
            
            # === USEFUL COMBINATIONS ===
            "count in": [Key.shift, 'k'],
            "snap to grid": [Key.cmd, 'g'],
            "full screen": [Key.cmd, Key.ctrl, 'f'],
            
            # === TRACK SELECTION ===
            "next track": [Key.down],
            "previous track": [Key.up],
            "track up": [Key.up],
            "track down": [Key.down],
        }
        
        # Alternative phrases for common commands
        self.command_aliases = {
            # Playback alternatives
            "start": "play",
            "go": "play",
            "hit play": "play",
            "start playback": "play",
            "stop playback": "stop",
            
            # Recording alternatives  
            "start rec": "record",
            "begin recording": "record",
            "stop rec": "record",
            
            # Navigation alternatives
            "start": "beginning",
            "top": "beginning", 
            "home": "beginning",
            "back": "move back",
            "forward": "move forward",
            
            # Track alternatives
            "add new track": "new track",
            "create new track": "new track",
            "remove track": "delete track",
            "copy track": "duplicate track",
            
            # Edit alternatives
            "cut region": "cut",
            "copy region": "copy",
            "paste region": "paste",
            "delete region": "delete",
            
            # Loop alternatives
            "repeat": "toggle loop",
            "loop on": "toggle loop",
            "loop off": "toggle loop",
            
            # Metronome alternatives
            "click": "toggle metronome",
            "click on": "metronome on",
            "click off": "metronome off",
        }

    def send_keyboard_shortcut(self, keys):
        """Send keyboard shortcut to GarageBand"""
        try:
            if len(keys) == 1:
                # Single key
                self.controller.press(keys[0])
                self.controller.release(keys[0])
            else:
                # Key combination - press modifiers first
                for key in keys[:-1]:
                    self.controller.press(key)
                
                # Press main key
                self.controller.press(keys[-1])
                self.controller.release(keys[-1])
                
                # Release modifiers in reverse order
                for key in reversed(keys[:-1]):
                    self.controller.release(key)
            
            # Show what was executed
            key_names = []
            for key in keys:
                if hasattr(key, 'name'):
                    key_names.append(key.name)
                elif isinstance(key, str):
                    key_names.append(key.upper())
                else:
                    key_names.append(str(key))
            
            shortcut_display = " + ".join(key_names)
            logger.info(f"Executed: {shortcut_display}")
            return shortcut_display
            
        except Exception as e:
            logger.error(f"Error sending shortcut: {e}")
            return f"Error: {e}"

    def process_voice_command(self, command_text):
        """Process recognized voice command"""
        command_text = command_text.lower().strip()
        
        # Check for exact matches first
        if command_text in self.commands:
            logger.info(f"Command: '{command_text}'")
            shortcut = self.send_keyboard_shortcut(self.commands[command_text])
            return {"success": True, "command": command_text, "shortcut": shortcut}
        
        # Check aliases
        if command_text in self.command_aliases:
            actual_command = self.command_aliases[command_text]
            logger.info(f"Command: '{command_text}' -> '{actual_command}'")
            shortcut = self.send_keyboard_shortcut(self.commands[actual_command])
            return {"success": True, "command": f"{command_text} -> {actual_command}", "shortcut": shortcut}
        
        # Try partial matching for flexibility
        for cmd in self.commands:
            if cmd in command_text or command_text in cmd:
                logger.info(f"Partial match: '{command_text}' -> '{cmd}'")
                shortcut = self.send_keyboard_shortcut(self.commands[cmd])
                return {"success": True, "command": f"{command_text} -> {cmd}", "shortcut": shortcut}
        
        logger.warning(f"Command not recognized: '{command_text}'")
        return {"success": False, "command": command_text, "error": "Command not recognized"}

    async def handle_client(self, websocket):
        """Handle WebSocket client connection"""
        self.connected_clients.add(websocket)
        client_ip = websocket.remote_address[0]
        logger.info(f"Client connected from {client_ip}")
        
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    
                    if data.get("type") == "command":
                        command = data.get("command", "").strip()
                        if command:
                            result = self.process_voice_command(command)
                            await websocket.send(json.dumps({
                                "type": "result",
                                "data": result
                            }))
                    
                    elif data.get("type") == "get_commands":
                        # Send available commands
                        commands_list = list(self.commands.keys()) + list(self.command_aliases.keys())
                        await websocket.send(json.dumps({
                            "type": "commands_list",
                            "data": sorted(commands_list)
                        }))
                
                except json.JSONDecodeError:
                    logger.error("Invalid JSON received")
                    await websocket.send(json.dumps({
                        "type": "error",
                        "data": {"error": "Invalid JSON"}
                    }))
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_ip} disconnected")
        finally:
            self.connected_clients.discard(websocket)

    async def start_server(self, host="localhost", port=8765):
        """Start the WebSocket server"""
        logger.info(f"Starting WebSocket server on {host}:{port}")
        return await websockets.serve(self.handle_client, host, port)

def main():
    """Main function"""
    print("🎵 GarageBand Web Controller Server")
    print("=" * 50)
    print("Make sure GarageBand is open and focused!")
    print("WebSocket server will start on localhost:8765")
    print("Open the web interface to control GarageBand")
    print("=" * 50)
    
    controller = GarageBandWebController()
    
    # Start WebSocket server
    start_server = controller.start_server()
    
    # Run the server
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start_server)
    logger.info("WebSocket server started!")
    
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
    finally:
        loop.close()

if __name__ == "__main__":
    main() 
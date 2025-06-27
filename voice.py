#!/usr/bin/env python3
"""
GarageBand Voice Control Program for Mac
Simple voice commands to control GarageBand using keyboard shortcuts

Requirements:
pip install speechrecognition pyaudio pynput

Usage:
python garageband_voice_control.py
"""

import speech_recognition as sr
import time
from pynput import keyboard
from pynput.keyboard import Key
import threading
import sys

class GarageBandVoiceController:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.is_listening = False
        self.controller = keyboard.Controller()
        
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
        
        # Adjust microphone for ambient noise
        print("🎵 GarageBand Voice Controller Starting...")
        print("Adjusting for ambient noise... Please wait.")
        
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
        
        print("✅ Ready for voice commands!")
        self.show_help()

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
            print(f"🎹 Executed: {shortcut_display}")
            
        except Exception as e:
            print(f"❌ Error sending shortcut: {e}")

    def process_voice_command(self, command_text):
        """Process recognized voice command"""
        command_text = command_text.lower().strip()
        
        # Check for exact matches first
        if command_text in self.commands:
            print(f"🎤 Command: '{command_text}'")
            self.send_keyboard_shortcut(self.commands[command_text])
            return True
        
        # Check aliases
        if command_text in self.command_aliases:
            actual_command = self.command_aliases[command_text]
            print(f"🎤 Command: '{command_text}' -> '{actual_command}'")
            self.send_keyboard_shortcut(self.commands[actual_command])
            return True
        
        # Try partial matching for flexibility
        for cmd in self.commands:
            if cmd in command_text or command_text in cmd:
                print(f"🎤 Partial match: '{command_text}' -> '{cmd}'")
                self.send_keyboard_shortcut(self.commands[cmd])
                return True
        
        print(f"❓ Command not recognized: '{command_text}'")
        return False

    def listen_for_commands(self):
        """Main listening loop"""
        print("\n🎧 Listening for voice commands...")
        print("💡 Say 'stop listening' or 'quit' to exit")
        print("💡 Say 'help' for command list")
        
        while self.is_listening:
            try:
                with self.microphone as source:
                    # Listen for audio
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=4)
                
                try:
                    # Recognize speech
                    command = self.recognizer.recognize_google(audio, language='en-US')
                    command_lower = command.lower()
                    
                    # Check for control commands
                    if any(phrase in command_lower for phrase in ["stop listening", "quit", "exit"]):
                        print("👋 Stopping voice control...")
                        self.is_listening = False
                        break
                    elif "help" in command_lower:
                        self.show_help()
                        continue
                    elif "list commands" in command_lower:
                        self.list_commands()
                        continue
                    
                    # Process GarageBand command
                    self.process_voice_command(command)
                    
                except sr.UnknownValueError:
                    # Speech not understood - normal, continue listening
                    pass
                except sr.RequestError as e:
                    print(f"❌ Speech recognition error: {e}")
                    time.sleep(1)
                    
            except sr.WaitTimeoutError:
                # No speech detected - normal, continue
                pass
            except KeyboardInterrupt:
                print("\n⏹️ Keyboard interrupt detected.")
                self.is_listening = False
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
                time.sleep(1)

    def show_help(self):
        """Show basic help information"""
        print("\n" + "="*50)
        print("🎵 GARAGEBAND VOICE CONTROL HELP")
        print("="*50)
        print("🎤 PLAYBACK:")
        print("   'play', 'stop', 'record', 'beginning'")
        print("\n🎵 TRACKS:")
        print("   'new track', 'delete track', 'mute track', 'solo track'")
        print("\n✂️ EDITING:")
        print("   'undo', 'redo', 'cut', 'copy', 'paste', 'split'")
        print("\n🔄 TOOLS:")
        print("   'toggle loop', 'toggle metronome', 'zoom in', 'zoom out'")
        print("\n💾 PROJECT:")
        print("   'save', 'new project'")
        print("\n🎛️ DISPLAY:")
        print("   'show library', 'show editor', 'show piano roll'")
        print("\n💡 CONTROL:")
        print("   'help', 'list commands', 'stop listening'")
        print("="*50)

    def list_commands(self):
        """List all available commands"""
        print("\n📋 ALL AVAILABLE COMMANDS:")
        print("-" * 40)
        
        categories = {
            "Playback": ["play", "stop", "record", "beginning"],
            "Navigation": ["next bar", "previous bar", "zoom in", "zoom out"],
            "Tracks": ["new track", "delete track", "mute track", "solo track", "duplicate track"],
            "Editing": ["undo", "redo", "cut", "copy", "paste", "split", "join"],
            "Loop/Cycle": ["toggle loop", "toggle cycle"],
            "Metronome": ["toggle metronome"],
            "Display": ["show library", "show editor", "show piano roll", "show smart controls"],
            "Project": ["save", "new project"],
        }
        
        for category, commands in categories.items():
            print(f"\n{category.upper()}:")
            for cmd in commands:
                if cmd in self.commands:
                    keys = self.commands[cmd]
                    key_str = " + ".join([str(k) if isinstance(k, str) else k.name for k in keys])
                    print(f"   '{cmd}' -> {key_str}")

    def start(self):
        """Start the voice control system"""
        self.is_listening = True
        
        # Start listening in a separate thread
        listen_thread = threading.Thread(target=self.listen_for_commands)
        listen_thread.daemon = True
        listen_thread.start()
        
        # Keep main thread alive
        try:
            while self.is_listening:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n🛑 Shutting down...")
            self.is_listening = False

def main():
    """Main function"""
    print("🎵 GarageBand Voice Controller")
    print("=" * 50)
    print("Make sure GarageBand is open and focused!")
    print("Grant microphone and accessibility permissions if prompted.")
    print("=" * 50)
    
    try:
        controller = GarageBandVoiceController()
        controller.start()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error starting controller: {e}")
    
    print("🎵 Voice control stopped.")

if __name__ == "__main__":
    main()
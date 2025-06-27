# 🎵 GarageBand Voice Controller

Next-generation voice control for music production. Control GarageBand with your voice from a beautiful web interface.

![GarageBand Voice Controller](https://img.shields.io/badge/version-2.0%20Beta-blue) ![macOS](https://img.shields.io/badge/platform-macOS-lightgrey) ![Python](https://img.shields.io/badge/python-3.9+-green)

## ✨ Features

- 🎤 **Voice Control** - Speak commands to control GarageBand
- 🌐 **Web Interface** - Modern, startup-style UI accessible from any browser
- 🔄 **Continuous Listening** - No need to click buttons repeatedly
- 📱 **Real-time Activity Feed** - See command history in a beautiful feed
- 🎹 **80+ Commands** - Complete control over playback, tracks, editing, and more
- ⚡ **Instant Response** - Fast WebSocket communication

## 🎬 Demo

*(Add screenshots or GIF here)*

## 🚀 Quick Start

### Prerequisites

- **macOS** (required for GarageBand)
- **Python 3.9+**
- **GarageBand** installed
- **Modern browser** (Chrome, Safari, Firefox)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/garageband-voice-controller.git
   cd garageband-voice-controller
   ```

2. **Install dependencies**
   ```bash
   # Install system dependencies
   brew install portaudio
   
   # Install Python packages
   pip3 install speechrecognition pyaudio pynput websockets
   ```

3. **Start the application**
   ```bash
   python3 start_servers.py
   ```

4. **Open your browser**
   - Automatically opens at `http://localhost:8000`
   - Grant microphone permissions when prompted

## 🎵 Usage

1. **Open GarageBand** and keep it focused
2. **Click the microphone button** in the web interface
3. **Speak commands** like:
   - "play" / "stop" / "record"
   - "new track" / "delete track"
   - "undo" / "redo" / "save"
   - "zoom in" / "toggle loop"
   - And 70+ more commands!

## 📋 Available Commands

### 🎤 Playback & Recording
- play, stop, pause, record
- beginning, go to start
- start recording, stop recording

### 🎵 Track Operations
- new track, delete track
- mute track, solo track
- next track, previous track
- duplicate track

### ✂️ Editing Commands
- undo, redo, cut, copy, paste
- split, join, delete
- split region, join regions

### 🔄 Navigation & Tools
- zoom in, zoom out
- toggle loop, toggle metronome
- rewind, fast forward
- next bar, previous bar

### 👁️ Display Controls
- show/hide library, editor, piano roll
- show/hide smart controls, automation
- show/hide browser

### 💾 Project Management
- save, save project
- new project, open project

## 🛠️ Technical Details

### Architecture
```
Browser (Web UI) ←→ WebSocket ←→ Python Server ←→ GarageBand (Keyboard Shortcuts)
```

- **Frontend**: HTML/CSS/JavaScript with Web Speech API
- **Backend**: Python WebSocket server with pynput for keyboard control
- **Communication**: Real-time WebSocket connection
- **Voice Recognition**: Browser's native speech recognition

### Files Structure
```
VoiceControl/
├── start_servers.py    # Main launcher
├── web_server.py       # WebSocket server
├── http_server.py      # Web interface server
├── index.html          # Frontend interface
├── voice.py           # Original CLI version
└── README.md          # This file
```

## 🔧 Troubleshooting

### "Microphone permission required"
- Grant microphone access in your browser settings
- Try refreshing the page after granting permission

### "Connection failed" 
- Make sure both servers are running (`python3 start_servers.py`)
- Check that no firewall is blocking localhost:8765 or localhost:8000

### "Commands not working"
- Ensure GarageBand is the focused application
- Grant accessibility permissions to Terminal/Python in System Preferences > Security & Privacy

### Voice recognition issues
- Speak clearly and at normal volume
- Check your microphone is working in other apps
- Try Chrome for best Web Speech API support

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - feel free to use this project however you'd like!

## 🙏 Acknowledgments

- Built with modern web technologies
- Uses Web Speech API for voice recognition
- Inspired by the need for hands-free music production

---

**Note**: This application requires macOS and GarageBand to function properly, as it sends keyboard shortcuts to control the application. 
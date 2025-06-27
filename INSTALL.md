# 🎵 GarageBand Voice Control - Installation Guide

## Quick Start (3 steps)

### 1. Download the App
```bash
curl -O https://raw.githubusercontent.com/alseong/VoiceControl/main/garageband_voice_control_standalone.py
```

### 2. Install Dependencies
```bash
pip install speechrecognition pyaudio pynput
```

### 3. Run the App
```bash
python3 garageband_voice_control_standalone.py
```

That's it! Your browser will open automatically with the voice control interface.

## What You Get

✅ **Complete Voice Control** - Actually controls GarageBand with keyboard shortcuts  
✅ **Web Interface** - Beautiful browser-based control panel  
✅ **80+ Commands** - Full range of GarageBand voice commands  
✅ **Real-time Feedback** - See commands executed instantly  
✅ **No Servers Needed** - Everything runs locally in one file  

## System Requirements

- **macOS** (required for GarageBand)
- **Python 3.6+**
- **Microphone** (built-in or external)
- **GarageBand** installed and running

## Permissions Needed

When you first run the app, macOS will ask for:

1. **Microphone Access** - For voice recognition
2. **Accessibility Access** - For sending keyboard shortcuts to GarageBand

Both are required for the app to work.

## Usage

1. **Open GarageBand** first
2. **Run the Python script** - Browser opens automatically
3. **Click the microphone button** in the web interface
4. **Start talking!** - Say commands like "play", "stop", "new track"

## Voice Commands

Try saying any of these:

**Playback:** "play", "stop", "record", "beginning"  
**Tracks:** "new track", "delete track", "mute track", "solo track"  
**Editing:** "undo", "redo", "cut", "copy", "paste", "split"  
**Tools:** "zoom in", "zoom out", "toggle loop", "toggle metronome"  
**Project:** "save", "new project"  

## Troubleshooting

**"No module named 'pyaudio'"**
```bash
# Install PortAudio first
brew install portaudio
pip install pyaudio
```

**"Permission denied" errors**
- Go to System Preferences → Security & Privacy → Accessibility
- Add Terminal or your Python app to the allowed apps

**Voice not recognized**
- Check microphone permissions
- Speak clearly and wait for the interface to show "Listening..."
- Try different phrasings ("play" vs "start playback")

## Demo vs Full Version

🌐 **[Try the Demo](https://voice-control-blush.vercel.app)** - Voice recognition only, runs in browser  
⬇️ **Download Full Version** - Actually controls GarageBand, runs locally  

The demo shows voice recognition working perfectly, but only the downloaded version can actually control GarageBand due to browser security limitations.

---

**Questions?** [Open an issue on GitHub](https://github.com/alseong/VoiceControl/issues) 
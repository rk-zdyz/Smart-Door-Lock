# Smart Door Lock - Updated README

## Project Structure

```
smart_door_lock/
├── esp32_firmware/           # Arduino ESP32-CAM code
│   ├── smart_door_lock.ino   # Main program
│   ├── config.h              # ⚙️ Your settings (WiFi, pins)
│   ├── camera_pins.h         # Camera pin definitions
│   ├── camera_module.h       # Camera init & capture
│   ├── wifi_module.h         # WiFi connection
│   ├── api_client.h          # Server communication
│   └── lock_control.h        # Lock, LED, buzzer
│
├── server/                   # Python server
│   ├── server.py             # Main entry point
│   ├── config.py             # ⚙️ Server settings
│   ├── routes.py             # API endpoints
│   ├── face_service.py       # Face recognition
│   ├── database.py           # Data storage
│   ├── templates.py          # Web UI HTML
│   └── requirements.txt      # Dependencies
│
└── README.md
```

## Quick Start

### 1. Start Python Server
```bash
cd server
pip install -r requirements.txt
python server.py
```

### 2. Register Faces
Open http://localhost:5000/register-ui

### 3. Configure ESP32
Edit `esp32_firmware/config.h`:
- Set WiFi SSID/password
- Set server IP address

### 4. Upload to ESP32-CAM
1. Open Arduino IDE
2. Select "AI Thinker ESP32-CAM" board
3. Upload all files

## File Guide

| File | What to Edit |
|------|-------------|
| `config.h` | WiFi credentials, server IP, timing |
| `config.py` | Recognition threshold, server port |
| `camera_pins.h` | Only if using different ESP32 board |

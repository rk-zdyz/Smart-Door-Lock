# Smart Door Lock - Face Recognition Server

A face recognition door lock system using Flask and OpenCV.

## Features
- Face registration via webcam or image upload
- Real-time face verification
- Access logging
- Web-based management interface

## Quick Start

```bash
pip install -r requirements.txt
python server.py
```

## Deployment

This app is configured for deployment on:
- **Render.com** - Use the `render.yaml` blueprint
- **Railway.app** - Automatic detection via `Procfile`
- **Heroku** - Deploy via `Procfile`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new face |
| POST | `/verify` | Verify a face |
| GET | `/faces` | List registered faces |
| GET | `/logs` | View access history |

## Environment Variables

- `PORT` - Server port (default: 5000)

# Database Service
# Handles storage of faces and access logs

import json
import os
import numpy as np
from datetime import datetime
from config import FACES_FILE, LOGS_FILE, MAX_LOGS

# In-memory storage
known_faces = {}  # {id: {"name": str, "encoding": list}}
access_logs = []


def load_faces():
    """Load registered faces from JSON file"""
    global known_faces
    if os.path.exists(FACES_FILE):
        with open(FACES_FILE, 'r') as f:
            known_faces = json.load(f)
        print(f"Loaded {len(known_faces)} registered faces")
    else:
        known_faces = {}
        print("No existing faces found, starting fresh")


def save_faces():
    """Save registered faces to JSON file"""
    with open(FACES_FILE, 'w') as f:
        json.dump(known_faces, f, indent=2)


def add_face(name, encoding):
    """
    Add a new face to the database
    
    Args:
        name: Person's name
        encoding: Face encoding (numpy array or list)
        
    Returns:
        Face ID
    """
    # Generate unique ID
    face_id = str(len(known_faces) + 1)
    while face_id in known_faces:
        face_id = str(int(face_id) + 1)
    
    # Convert numpy array to list if needed
    if isinstance(encoding, np.ndarray):
        encoding = encoding.tolist()
    
    known_faces[face_id] = {
        "name": name,
        "encoding": encoding,
        "registered_at": datetime.now().isoformat()
    }
    save_faces()
    
    print(f"Added face: {name} (ID: {face_id})")
    return face_id


def delete_face(face_id):
    """Delete a face from the database"""
    if face_id in known_faces:
        name = known_faces[face_id]["name"]
        del known_faces[face_id]
        save_faces()
        return True, name
    return False, None


def get_all_faces():
    """Get list of all registered faces (without encodings)"""
    return [
        {
            "id": face_id,
            "name": data["name"],
            "registered_at": data.get("registered_at", "Unknown")
        }
        for face_id, data in known_faces.items()
    ]


def get_known_encodings():
    """Get all face encodings and names for matching"""
    encodings = [np.array(f["encoding"]) for f in known_faces.values()]
    names = [f["name"] for f in known_faces.values()]
    return encodings, names


def load_logs():
    """Load access logs from JSON file"""
    global access_logs
    if os.path.exists(LOGS_FILE):
        with open(LOGS_FILE, 'r') as f:
            access_logs = json.load(f)


def save_logs():
    """Save access logs to JSON file"""
    with open(LOGS_FILE, 'w') as f:
        json.dump(access_logs[-MAX_LOGS:], f, indent=2)


def log_access(authorized, name, confidence=0):
    """Log an access attempt"""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "authorized": authorized,
        "name": name,
        "confidence": round(confidence, 3)
    }
    access_logs.append(entry)
    save_logs()
    
    status = "GRANTED" if authorized else "DENIED"
    print(f"[LOG] {entry['timestamp']} - {name}: {status}")


def get_logs(limit=50):
    """Get recent access logs"""
    return access_logs[-limit:][::-1]  # Newest first

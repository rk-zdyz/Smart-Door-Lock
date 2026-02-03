# API Routes
# All HTTP endpoints for the server

from flask import Blueprint, request, jsonify, render_template_string
from config import RECOGNITION_THRESHOLD
from face_service import decode_image, detect_faces, encode_face, compare_faces
from database import (
    add_face, delete_face, get_all_faces, 
    get_known_encodings, log_access, get_logs
)
from templates import HOME_PAGE, REGISTER_PAGE, APP_PAGE
import database

# Create blueprint for routes
api = Blueprint('api', __name__)


@api.route('/')
def home():
    """Dashboard home page"""
    return render_template_string(
        HOME_PAGE,
        face_count=len(database.known_faces),
        log_count=len(database.access_logs)
    )


@api.route('/register-ui')
def register_ui():
    """Face registration web interface"""
    return render_template_string(REGISTER_PAGE)


@api.route('/app')
def app_ui():
    """Main integrated face recognition application"""
    return render_template_string(APP_PAGE)


@api.route('/register', methods=['POST'])
def register_face():
    """
    Register a new face
    
    Request JSON:
        {"name": "Person Name", "image": "base64_encoded_image"}
        
    Returns:
        {"success": bool, "id": str, "name": str, "message": str}
    """
    try:
        data = request.json
        
        # Validate input
        if not data or 'name' not in data or 'image' not in data:
            return jsonify({"success": False, "error": "Missing name or image"})
        
        name = data['name'].strip()
        if not name:
            return jsonify({"success": False, "error": "Name cannot be empty"})
        
        # Decode image
        image_array = decode_image(data['image'])
        if image_array is None:
            return jsonify({"success": False, "error": "Invalid image format"})
        
        # Detect faces
        face_locations = detect_faces(image_array)
        
        if len(face_locations) == 0:
            return jsonify({"success": False, "error": "No face detected in image"})
        
        if len(face_locations) > 1:
            return jsonify({"success": False, "error": "Multiple faces detected. Use single face image"})
        
        # Encode face
        encoding = encode_face(image_array, face_locations[0])
        if encoding is None:
            return jsonify({"success": False, "error": "Could not encode face"})
        
        # Store face
        face_id = add_face(name, encoding)
        
        return jsonify({
            "success": True,
            "id": face_id,
            "name": name,
            "message": f"Successfully registered {name}"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@api.route('/verify', methods=['POST'])
def verify_face():
    """
    Verify a face against registered users
    Used by ESP32-CAM
    
    Request JSON:
        {"image": "base64_encoded_image"}
        
    Returns:
        {"authorized": bool, "name": str, "confidence": float}
    """
    try:
        data = request.json
        
        if not data or 'image' not in data:
            log_access(False, "No image")
            return jsonify({"authorized": False, "name": "No image", "confidence": 0})
        
        # Decode image
        image_array = decode_image(data['image'])
        if image_array is None:
            log_access(False, "Invalid image")
            return jsonify({"authorized": False, "name": "Invalid image", "confidence": 0})
        
        # Detect face
        face_locations = detect_faces(image_array)
        
        if len(face_locations) == 0:
            log_access(False, "No face detected")
            return jsonify({"authorized": False, "name": "No face detected", "confidence": 0})
        
        # Encode first face
        face_encoding = encode_face(image_array, face_locations[0])
        if face_encoding is None:
            log_access(False, "Encoding failed")
            return jsonify({"authorized": False, "name": "Encoding failed", "confidence": 0})
        
        # Get known faces
        known_encodings, known_names = get_known_encodings()
        
        if not known_encodings:
            log_access(False, "No registered faces")
            return jsonify({"authorized": False, "name": "No registered faces", "confidence": 0})
        
        # Compare faces
        best_idx, distance, is_match = compare_faces(
            known_encodings, 
            face_encoding, 
            RECOGNITION_THRESHOLD
        )
        
        confidence = 1 - distance
        
        if is_match:
            name = known_names[best_idx]
            log_access(True, name, confidence)
            return jsonify({
                "authorized": True,
                "name": name,
                "confidence": round(confidence, 3)
            })
        else:
            log_access(False, "Unknown face", confidence)
            return jsonify({
                "authorized": False,
                "name": "Unknown",
                "confidence": round(confidence, 3)
            })
            
    except Exception as e:
        log_access(False, f"Error: {str(e)}")
        return jsonify({"authorized": False, "name": "Error", "confidence": 0, "error": str(e)})


@api.route('/faces', methods=['GET'])
def list_faces():
    """List all registered faces"""
    return jsonify(get_all_faces())


@api.route('/faces/<face_id>', methods=['DELETE'])
def remove_face(face_id):
    """Delete a registered face"""
    success, name = delete_face(face_id)
    if success:
        return jsonify({"success": True, "message": f"Deleted {name}"})
    return jsonify({"success": False, "error": "Face not found"})


@api.route('/logs', methods=['GET'])
def access_logs():
    """Get access logs"""
    return jsonify(get_logs())

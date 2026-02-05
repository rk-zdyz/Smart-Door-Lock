# Face Recognition Service
# Handles face detection, encoding, and matching
# Uses OpenCV for face detection when face_recognition is not available

import numpy as np
import base64
import io
import os
from PIL import Image

# Configuration
USE_MOCK_MODE = False  # Set to True to force mock mode
FACE_RECOGNITION_AVAILABLE = False

# Try to import face_recognition
if not USE_MOCK_MODE:
    try:
        # Suppress stdout during import to catch the "Please install" message
        import sys
        from io import StringIO
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        
        try:
            import face_recognition
            FACE_RECOGNITION_AVAILABLE = True
        except:
            pass
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
        if FACE_RECOGNITION_AVAILABLE:
            print("[OK] Face recognition library loaded successfully")
    except Exception as e:
        print(f"[WARN] Face recognition setup failed: {e}")

# Try OpenCV for face detection if face_recognition not available
OPENCV_AVAILABLE = False
CASCADE_PATH = None

if not FACE_RECOGNITION_AVAILABLE:
    try:
        import cv2
        OPENCV_AVAILABLE = True
        # Try to find the cascade file
        cascade_paths = [
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml',
            'haarcascade_frontalface_default.xml',
        ]
        for path in cascade_paths:
            if os.path.exists(path):
                CASCADE_PATH = path
                break
        
        if CASCADE_PATH:
            print(f"[OK] OpenCV face detection loaded (cascade: {os.path.basename(CASCADE_PATH)})")
        else:
            print("[WARN] OpenCV loaded but no cascade file found - using mock detection")
    except Exception as e:
        print(f"[WARN] OpenCV not available: {e}")

if not FACE_RECOGNITION_AVAILABLE and not OPENCV_AVAILABLE:
    print("  Running in DEMO mode - using mock face recognition")


def decode_image(base64_string):
    """
    Decode a base64 image string to numpy array
    
    Args:
        base64_string: Base64 encoded image
        
    Returns:
        numpy array of image, or None if failed
    """
    try:
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        image_array = np.array(image)
        
        # Convert to RGB if needed
        if len(image_array.shape) == 2:
            # Grayscale to RGB
            image_array = np.stack([image_array] * 3, axis=-1)
        elif len(image_array.shape) == 3 and image_array.shape[2] == 4:
            # RGBA to RGB
            image_array = image_array[:, :, :3]
            
        return image_array
    except Exception as e:
        print(f"Error decoding image: {e}")
        return None


def detect_faces(image_array):
    """
    Detect faces in an image
    
    Args:
        image_array: numpy array of image
        
    Returns:
        List of face locations as (top, right, bottom, left)
    """
    if FACE_RECOGNITION_AVAILABLE:
        return face_recognition.face_locations(image_array)
    
    if OPENCV_AVAILABLE and CASCADE_PATH:
        import cv2
        # Convert to grayscale
        gray = cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        face_cascade = cv2.CascadeClassifier(CASCADE_PATH)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4, minSize=(30, 30))
        
        # Convert from (x, y, w, h) to (top, right, bottom, left)
        locations = []
        for (x, y, w, h) in faces:
            locations.append((y, x + w, y + h, x))
        return locations
    
    # Mock mode: always detect a face in the center
    h, w = image_array.shape[:2]
    return [(h//4, 3*w//4, 3*h//4, w//4)]


def encode_face(image_array, face_location=None):
    """
    Get face encoding from image
    
    Args:
        image_array: numpy array of image
        face_location: optional specific face location
        
    Returns:
        Face encoding (128-dimensional vector), or None if no face found
    """
    if FACE_RECOGNITION_AVAILABLE:
        if face_location:
            encodings = face_recognition.face_encodings(image_array, [face_location])
        else:
            encodings = face_recognition.face_encodings(image_array)
        return encodings[0] if encodings else None
    else:
        # Create a simplified encoding based on face region
        if face_location:
            top, right, bottom, left = face_location
            face_region = image_array[top:bottom, left:right]
        else:
            # Use center region
            h, w = image_array.shape[:2]
            face_region = image_array[h//4:3*h//4, w//4:3*w//4]
        
        # Create a simple encoding from the face region
        # Resize to standard size and flatten
        from PIL import Image as PILImage
        face_img = PILImage.fromarray(face_region)
        face_img = face_img.resize((16, 16))
        small = np.array(face_img).flatten().astype(float)
        
        # Normalize and pad/truncate to 128 dimensions
        if len(small) < 128:
            encoding = np.pad(small, (0, 128 - len(small)))
        else:
            encoding = small[:128]
        
        # Normalize
        norm = np.linalg.norm(encoding)
        if norm > 0:
            encoding = encoding / norm
        
        return encoding


def compare_faces(known_encodings, face_to_check, threshold=0.6):
    """
    Compare a face against known faces
    
    Args:
        known_encodings: List of known face encodings
        face_to_check: Face encoding to verify
        threshold: Maximum distance for match (lower = stricter)
        
    Returns:
        Tuple of (best_match_index, distance, is_match)
    """
    if not known_encodings:
        return -1, 1.0, False
    
    if FACE_RECOGNITION_AVAILABLE:
        distances = face_recognition.face_distance(known_encodings, face_to_check)
    else:
        # Calculate cosine similarity converted to distance
        face_to_check = np.array(face_to_check)
        distances = []
        for known in known_encodings:
            known = np.array(known)
            # Cosine similarity
            dot = np.dot(known, face_to_check)
            norm1 = np.linalg.norm(known)
            norm2 = np.linalg.norm(face_to_check)
            if norm1 > 0 and norm2 > 0:
                similarity = dot / (norm1 * norm2)
                # Convert to distance (0 = identical, 1 = different)
                distance = 1 - (similarity + 1) / 2
            else:
                distance = 1.0
            distances.append(distance)
    
    distances = np.array(distances)
    best_match_idx = np.argmin(distances)
    best_distance = distances[best_match_idx]
    
    return int(best_match_idx), float(best_distance), best_distance < threshold

# Webcam Face Capture Script
# Captures images from webcam and saves them for training/registration

import cv2
import os
from datetime import datetime

# Configuration
SAVE_FOLDER = "captured_faces"
WINDOW_NAME = "Face Capture - Press SPACE to capture, Q to quit"

def ensure_folder():
    """Create the save folder if it doesn't exist"""
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)
        print(f"Created folder: {SAVE_FOLDER}")

def capture_faces():
    """Main capture loop"""
    ensure_folder()
    
    # Open webcam (0 = default camera)
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print("=" * 50)
    print("WEBCAM FACE CAPTURE")
    print("=" * 50)
    print("Controls:")
    print("  SPACE  - Capture and save image")
    print("  Q      - Quit")
    print("=" * 50)
    
    capture_count = 0
    
    while True:
        # Read frame from webcam
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Could not read frame")
            break
        
        # Mirror the frame for natural view
        frame = cv2.flip(frame, 1)
        
        # Add instructions overlay
        cv2.putText(
            frame, 
            "SPACE: Capture | Q: Quit", 
            (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, 
            (0, 255, 0), 
            2
        )
        
        # Show capture count
        cv2.putText(
            frame, 
            f"Captured: {capture_count}", 
            (10, 60), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            0.7, 
            (0, 255, 255), 
            2
        )
        
        # Display the frame
        cv2.imshow(WINDOW_NAME, frame)
        
        # Wait for key press
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q') or key == ord('Q'):
            print("\nExiting...")
            break
            
        elif key == ord(' '):  # Space key
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"face_{timestamp}_{capture_count + 1}.jpg"
            filepath = os.path.join(SAVE_FOLDER, filename)
            
            # Save the image
            cv2.imwrite(filepath, frame)
            capture_count += 1
            
            print(f"[{capture_count}] Saved: {filepath}")
            
            # Flash effect - show green border briefly
            flash_frame = frame.copy()
            cv2.rectangle(flash_frame, (0, 0), (frame.shape[1], frame.shape[0]), (0, 255, 0), 10)
            cv2.putText(flash_frame, "CAPTURED!", (frame.shape[1]//2 - 80, frame.shape[0]//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
            cv2.imshow(WINDOW_NAME, flash_frame)
            cv2.waitKey(200)  # Show for 200ms
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\nTotal images captured: {capture_count}")
    print(f"Saved to folder: {os.path.abspath(SAVE_FOLDER)}")


def capture_with_name():
    """Capture images for a specific person"""
    name = input("Enter person's name: ").strip()
    if not name:
        print("Name cannot be empty!")
        return
    
    # Create person-specific folder
    person_folder = os.path.join(SAVE_FOLDER, name.lower().replace(" ", "_"))
    if not os.path.exists(person_folder):
        os.makedirs(person_folder)
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    print(f"\nCapturing faces for: {name}")
    print("Press SPACE to capture, Q to quit")
    print("-" * 40)
    
    count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        frame = cv2.flip(frame, 1)
        
        # Overlay
        cv2.putText(frame, f"Person: {name}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, f"Images: {count}", (10, 60), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, "SPACE: Capture | Q: Quit", (10, 90), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        cv2.imshow(f"Capturing: {name}", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord(' '):
            timestamp = datetime.now().strftime("%H%M%S")
            filename = f"{name.lower().replace(' ', '_')}_{count + 1}_{timestamp}.jpg"
            filepath = os.path.join(person_folder, filename)
            cv2.imwrite(filepath, frame)
            count += 1
            print(f"  Captured {count}: {filename}")
    
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\nCaptured {count} images for {name}")
    print(f"Folder: {os.path.abspath(person_folder)}")


if __name__ == "__main__":
    print("\n=== Face Capture Tool ===")
    print("1. Quick capture (numbered files)")
    print("2. Capture for specific person")
    print("Q. Quit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        capture_faces()
    elif choice == "2":
        capture_with_name()
    else:
        print("Goodbye!")

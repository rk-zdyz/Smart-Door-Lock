# Test Face Recognition
# Opens webcam and verifies faces against registered users in real-time

import cv2
import base64
import requests
import numpy as np

SERVER_URL = "http://localhost:5000"

def test_recognition():
    """Real-time face recognition test"""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return
    
    print("=" * 50)
    print("FACE RECOGNITION TEST")
    print("=" * 50)
    print("Controls:")
    print("  SPACE  - Scan and verify face")
    print("  Q      - Quit")
    print("=" * 50)
    
    last_result = None
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        display = frame.copy()
        
        # Show instructions
        cv2.putText(display, "Press SPACE to scan face", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Show last result if exists
        if last_result:
            color = (0, 255, 0) if last_result["authorized"] else (0, 0, 255)
            status = "AUTHORIZED" if last_result["authorized"] else "DENIED"
            name = last_result.get("name", "Unknown")
            confidence = last_result.get("confidence", 0)
            
            cv2.putText(display, f"{status}: {name}", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(display, f"Confidence: {confidence:.1%}", (10, 100),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Draw border
            cv2.rectangle(display, (0, 0), (display.shape[1]-1, display.shape[0]-1), color, 5)
        
        cv2.imshow("Face Recognition Test", display)
        
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord(' '):
            print("\nScanning face...")
            
            # Encode frame to base64
            _, buffer = cv2.imencode('.jpg', frame)
            image_b64 = base64.b64encode(buffer).decode('utf-8')
            
            try:
                # Send to server
                response = requests.post(
                    f"{SERVER_URL}/verify",
                    json={"image": image_b64},
                    timeout=10
                )
                last_result = response.json()
                
                # Print result
                if last_result["authorized"]:
                    print(f"✓ AUTHORIZED: {last_result['name']} ({last_result['confidence']:.1%})")
                else:
                    print(f"✗ DENIED: {last_result.get('name', 'Unknown')} ({last_result.get('confidence', 0):.1%})")
                    
            except requests.exceptions.ConnectionError:
                print("ERROR: Cannot connect to server. Is it running?")
                last_result = {"authorized": False, "name": "Server offline", "confidence": 0}
            except Exception as e:
                print(f"ERROR: {e}")
                last_result = {"authorized": False, "name": f"Error: {e}", "confidence": 0}
    
    cap.release()
    cv2.destroyAllWindows()


def continuous_scan():
    """Continuously scan faces (like ESP32 would)"""
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return
    
    print("=" * 50)
    print("CONTINUOUS FACE SCANNING")
    print("Scanning every 2 seconds... Press Q to quit")
    print("=" * 50)
    
    scan_interval = 60  # frames between scans (~2 sec at 30fps)
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        display = frame.copy()
        
        # Auto-scan every interval
        if frame_count % scan_interval == 0:
            _, buffer = cv2.imencode('.jpg', frame)
            image_b64 = base64.b64encode(buffer).decode('utf-8')
            
            try:
                response = requests.post(
                    f"{SERVER_URL}/verify",
                    json={"image": image_b64},
                    timeout=5
                )
                result = response.json()
                
                color = (0, 255, 0) if result["authorized"] else (0, 0, 255)
                status = "GRANTED" if result["authorized"] else "DENIED"
                
                cv2.putText(display, f"{status}: {result.get('name', 'Unknown')}", 
                           (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
                cv2.rectangle(display, (0, 0), (display.shape[1]-1, display.shape[0]-1), color, 8)
                
                print(f"[Scan] {status}: {result.get('name', 'Unknown')} ({result.get('confidence', 0):.1%})")
                
            except Exception as e:
                cv2.putText(display, "Scan failed", (10, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        cv2.putText(display, "Continuous scan mode | Q to quit", (10, 25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        cv2.imshow("Continuous Face Scan", display)
        frame_count += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print("\n=== Face Recognition Test ===")
    print("1. Manual scan (press SPACE to verify)")
    print("2. Continuous scan (auto every 2 sec)")
    print("Q. Quit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        test_recognition()
    elif choice == "2":
        continuous_scan()
    else:
        print("Goodbye!")

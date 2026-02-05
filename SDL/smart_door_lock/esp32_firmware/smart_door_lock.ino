// ============================================
//        SMART DOOR LOCK - MAIN PROGRAM
// ============================================
// Face recognition door lock using ESP32-CAM
// 
// Files:
//   config.h        - User configuration (WiFi, pins, etc.)
//   camera_pins.h   - Camera pin definitions
//   camera_module.h - Camera initialization and capture
//   wifi_module.h   - WiFi connection handling
//   api_client.h    - Server communication
//   lock_control.h  - Lock, LED, buzzer control

#include "config.h"
#include "camera_module.h"
#include "wifi_module.h"
#include "api_client.h"
#include "lock_control.h"

// ============================================
//                   SETUP
// ============================================
void setup() {
  // Start serial for debugging
  Serial.begin(115200);
  delay(1000);
  
  Serial.println("\n");
  Serial.println("========================================");
  Serial.println("    SMART DOOR LOCK - Starting Up");
  Serial.println("========================================");
  
  // Step 1: Initialize lock control (pins)
  initLockControl();
  
  // Step 2: Initialize camera
  if (!initCamera()) {
    Serial.println("FATAL: Camera initialization failed!");
    showError();
    return;
  }
  
  // Step 3: Connect to WiFi
  if (!connectWiFi()) {
    Serial.println("WARNING: WiFi not connected. Will retry...");
    showError();
  }
  
  // Ready!
  showStartupComplete();
  Serial.println("\n========================================");
  Serial.println("    System Ready - Watching for faces");
  Serial.println("========================================\n");
}

// ============================================
//                 MAIN LOOP
// ============================================
void loop() {
  // Capture image from camera
  camera_fb_t* fb = captureImage();
  
  if (fb == NULL) {
    Serial.println("Capture failed, retrying...");
    delay(1000);
    return;
  }
  
  // Send to server for verification
  VerifyResult result = verifyFace(fb->buf, fb->len);
  
  // Release camera buffer
  releaseImage(fb);
  
  // Act on result
  if (result.success) {
    if (result.authorized) {
      grantAccess(result.name);
    } else {
      denyAccess(result.name);
    }
  } else {
    Serial.println("Verification failed: " + result.name);
  }
  
  // Wait before next check
  delay(CHECK_INTERVAL);
}

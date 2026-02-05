// ============================================
//         SMART DOOR LOCK - CONFIGURATION
// ============================================
// Edit these values for your setup

#ifndef CONFIG_H
#define CONFIG_H

// --- WiFi Settings ---
#define WIFI_SSID     "YOUR_WIFI_SSID"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

// --- Server Settings ---
// Replace with your PC's IP address (run 'ipconfig' to find it)
#define SERVER_IP     "192.168.1.100"
#define SERVER_PORT   5000
#define API_VERIFY    "/verify"

// --- Pin Definitions ---
#define PIN_LOCK      12    // Relay control pin
#define PIN_LED_GREEN 13    // Access granted LED
#define PIN_LED_RED   14    // Access denied LED
#define PIN_BUZZER    15    // Buzzer for audio feedback
#define PIN_FLASH_LED 4     // Onboard flash LED

// --- Timing Settings (milliseconds) ---
#define UNLOCK_DURATION   5000   // How long door stays unlocked
#define CHECK_INTERVAL    3000   // Time between face checks
#define WIFI_TIMEOUT      15000  // WiFi connection timeout
#define API_TIMEOUT       10000  // API request timeout

// --- Recognition Settings ---
#define JPEG_QUALITY      12     // 0-63, lower = better quality
#define FRAME_SIZE        FRAMESIZE_VGA  // 640x480

#endif

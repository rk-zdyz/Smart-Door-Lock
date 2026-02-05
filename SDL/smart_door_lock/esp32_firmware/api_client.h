// ============================================
//           API CLIENT MODULE
// ============================================
// Handles communication with Python server

#ifndef API_CLIENT_H
#define API_CLIENT_H

#include <HTTPClient.h>
#include <ArduinoJson.h>
#include "base64.h"
#include "config.h"
#include "wifi_module.h"

// Structure to hold verification result
struct VerifyResult {
  bool authorized;
  String name;
  float confidence;
  bool success;  // true if API call succeeded
};

// Build the full API URL
String getApiUrl(const char* endpoint) {
  return String("http://") + SERVER_IP + ":" + SERVER_PORT + endpoint;
}

// Send image to server and verify face
// Parameters:
//   imageData - pointer to JPEG image data
//   imageLen  - size of image in bytes
// Returns: VerifyResult struct with authorization status
VerifyResult verifyFace(uint8_t* imageData, size_t imageLen) {
  VerifyResult result = {false, "Error", 0.0, false};
  
  // Check WiFi connection
  if (!ensureWiFiConnection()) {
    result.name = "No WiFi";
    Serial.println("Cannot verify: WiFi not connected");
    return result;
  }
  
  HTTPClient http;
  String url = getApiUrl(API_VERIFY);
  
  Serial.printf("Sending to: %s\n", url.c_str());
  
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  http.setTimeout(API_TIMEOUT);
  
  // Encode image to base64
  String base64Image = base64::encode(imageData, imageLen);
  
  // Build JSON payload
  String payload = "{\"image\":\"" + base64Image + "\"}";
  
  Serial.println("Sending request...");
  int httpCode = http.POST(payload);
  
  if (httpCode == 200) {
    String response = http.getString();
    Serial.println("Response: " + response);
    
    // Parse JSON response
    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, response);
    
    if (!error) {
      result.success = true;
      result.authorized = doc["authorized"] | false;
      result.name = doc["name"] | "Unknown";
      result.confidence = doc["confidence"] | 0.0;
      
      Serial.printf("Result: %s - %s (%.1f%%)\n", 
                    result.authorized ? "AUTHORIZED" : "DENIED",
                    result.name.c_str(),
                    result.confidence * 100);
    } else {
      Serial.println("JSON parse error");
      result.name = "Parse error";
    }
  } else if (httpCode < 0) {
    Serial.printf("Connection failed: %s\n", http.errorToString(httpCode).c_str());
    result.name = "Connection failed";
  } else {
    Serial.printf("HTTP error: %d\n", httpCode);
    result.name = "HTTP " + String(httpCode);
  }
  
  http.end();
  return result;
}

#endif

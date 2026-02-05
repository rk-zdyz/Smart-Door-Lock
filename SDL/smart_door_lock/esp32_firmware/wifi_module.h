// ============================================
//           WIFI MODULE
// ============================================
// Handles WiFi connection and status

#ifndef WIFI_MODULE_H
#define WIFI_MODULE_H

#include <WiFi.h>
#include "config.h"

// Connect to WiFi network
// Returns: true if connected, false if timeout
bool connectWiFi() {
  Serial.printf("Connecting to WiFi: %s", WIFI_SSID);
  
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  
  unsigned long startTime = millis();
  
  while (WiFi.status() != WL_CONNECTED) {
    if (millis() - startTime > WIFI_TIMEOUT) {
      Serial.println("\nWiFi connection timeout!");
      return false;
    }
    delay(500);
    Serial.print(".");
  }
  
  Serial.println("\n----------------------------------------");
  Serial.println("WiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
  Serial.print("Signal Strength: ");
  Serial.print(WiFi.RSSI());
  Serial.println(" dBm");
  Serial.println("----------------------------------------");
  
  return true;
}

// Check if WiFi is still connected
bool isWiFiConnected() {
  return WiFi.status() == WL_CONNECTED;
}

// Reconnect if disconnected
bool ensureWiFiConnection() {
  if (!isWiFiConnected()) {
    Serial.println("WiFi disconnected, reconnecting...");
    return connectWiFi();
  }
  return true;
}

// Get WiFi signal strength
int getSignalStrength() {
  return WiFi.RSSI();
}

#endif

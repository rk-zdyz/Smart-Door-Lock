// ============================================
//         LOCK CONTROL MODULE
// ============================================
// Handles door lock, LEDs, and buzzer feedback

#ifndef LOCK_CONTROL_H
#define LOCK_CONTROL_H

#include "config.h"

// Initialize all control pins
void initLockControl() {
  pinMode(PIN_LOCK, OUTPUT);
  pinMode(PIN_LED_GREEN, OUTPUT);
  pinMode(PIN_LED_RED, OUTPUT);
  pinMode(PIN_BUZZER, OUTPUT);
  pinMode(PIN_FLASH_LED, OUTPUT);
  
  // Start with everything off, lock engaged
  digitalWrite(PIN_LOCK, LOW);
  digitalWrite(PIN_LED_GREEN, LOW);
  digitalWrite(PIN_LED_RED, LOW);
  digitalWrite(PIN_BUZZER, LOW);
  digitalWrite(PIN_FLASH_LED, LOW);
  
  Serial.println("Lock control initialized");
}

// Quick beep
void beep(int frequency, int duration) {
  tone(PIN_BUZZER, frequency, duration);
  delay(duration);
}

// Blink an LED
void blinkLED(int pin, int times, int delayMs = 100) {
  for (int i = 0; i < times; i++) {
    digitalWrite(pin, HIGH);
    delay(delayMs);
    digitalWrite(pin, LOW);
    delay(delayMs);
  }
}

// Grant access - unlock door with positive feedback
void grantAccess(String name) {
  Serial.println("========================================");
  Serial.println(">>> ACCESS GRANTED <<<");
  Serial.printf(">>> Welcome, %s!\n", name.c_str());
  Serial.println("========================================");
  
  // Visual feedback - green LED on
  digitalWrite(PIN_LED_GREEN, HIGH);
  
  // Audio feedback - happy beep
  beep(1000, 200);
  
  // Unlock the door
  Serial.println("Unlocking door...");
  digitalWrite(PIN_LOCK, HIGH);
  
  // Keep unlocked
  delay(UNLOCK_DURATION);
  
  // Re-lock
  digitalWrite(PIN_LOCK, LOW);
  Serial.println("Door locked");
  
  // Turn off LED
  digitalWrite(PIN_LED_GREEN, LOW);
}

// Deny access - show rejection feedback
void denyAccess(String reason) {
  Serial.println("========================================");
  Serial.println(">>> ACCESS DENIED <<<");
  Serial.printf(">>> Reason: %s\n", reason.c_str());
  Serial.println("========================================");
  
  // Visual feedback - red LED on
  digitalWrite(PIN_LED_RED, HIGH);
  
  // Audio feedback - three short beeps
  for (int i = 0; i < 3; i++) {
    beep(500, 100);
    delay(100);
  }
  
  delay(500);
  digitalWrite(PIN_LED_RED, LOW);
}

// Startup indicator
void showStartupComplete() {
  // Three quick green blinks
  blinkLED(PIN_LED_GREEN, 3, 100);
  beep(1500, 100);
}

// Error indicator
void showError() {
  // Five quick red blinks
  blinkLED(PIN_LED_RED, 5, 100);
}

#endif

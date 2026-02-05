// ============================================
//           CAMERA MODULE
// ============================================
// Handles camera initialization and image capture

#ifndef CAMERA_MODULE_H
#define CAMERA_MODULE_H

#include "esp_camera.h"
#include "camera_pins.h"
#include "config.h"

// Initialize the camera
// Returns: true if successful, false otherwise
bool initCamera() {
  camera_config_t config;
  
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  
  // Data pins
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  
  // Control pins
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  
  // Image settings
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAME_SIZE;
  config.jpeg_quality = JPEG_QUALITY;
  config.fb_count = 1;
  
  esp_err_t err = esp_camera_init(&config);
  
  if (err != ESP_OK) {
    Serial.printf("Camera init failed with error 0x%x\n", err);
    return false;
  }
  
  Serial.println("Camera initialized successfully");
  return true;
}

// Capture an image from the camera
// Returns: frame buffer pointer (must call esp_camera_fb_return after use)
camera_fb_t* captureImage() {
  // Flash LED on briefly for capture
  digitalWrite(PIN_FLASH_LED, HIGH);
  delay(50);
  
  camera_fb_t* fb = esp_camera_fb_get();
  
  digitalWrite(PIN_FLASH_LED, LOW);
  
  if (!fb) {
    Serial.println("Image capture failed");
    return NULL;
  }
  
  Serial.printf("Captured: %d bytes\n", fb->len);
  return fb;
}

// Release the frame buffer
void releaseImage(camera_fb_t* fb) {
  if (fb) {
    esp_camera_fb_return(fb);
  }
}

#endif

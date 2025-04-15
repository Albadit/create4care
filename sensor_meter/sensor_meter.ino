#include <ArduinoBLE.h>
#include <ArduinoJson.h>
#include "Ultrasonic.h"

Ultrasonic ultrasonic(7);  // Ultrasonic sensor on pin 7

// Define a BLE service and characteristic
BLEService distanceService("180C"); // Custom service
BLECharacteristic distanceCharacteristic("2A56", BLERead | BLENotify, 50); // Increase buffer for JSON data

void setup() {
  Serial.begin(9600);
  
  if (!BLE.begin()) {
    Serial.println("Failed to initialize BLE!");
    while (1);
  }

  setupBluetooth(); // Set up BLE
}

void loop() {
  handleBluetooth(); // Continuously handle BLE communication
}

// Function to measure distance using the ultrasonic sensor
long getUltrasonicDistance() {
  return ultrasonic.MeasureInMillimeters();
}

// Function to generate JSON data and return a buffer
size_t generateJsonData(char *jsonBuffer, size_t bufferSize) {
  StaticJsonDocument<50> jsonDoc;
  jsonDoc["distance"] = getUltrasonicDistance();
  jsonDoc["unit"] = "mm";

  return serializeJson(jsonDoc, jsonBuffer, bufferSize);
}

// Function to set up Bluetooth (BLE) service and characteristic
void setupBluetooth() {
  BLE.setLocalName("Arduino_R4_WiFi");
  BLE.setAdvertisedService(distanceService);
  distanceService.addCharacteristic(distanceCharacteristic);
  BLE.addService(distanceService);
  
  BLE.advertise(); // Make the device discoverable
  Serial.println("BLE Device Ready! Connect to receive JSON data.");
}

// Function to handle Bluetooth communication and send JSON data
void handleBluetooth() {
  BLEDevice central = BLE.central(); // Wait for a BLE device to connect

  if (central) {
    Serial.print("Connected to: ");
    Serial.println(central.address());

    while (central.connected()) {
      char jsonBuffer[50]; // Buffer to store JSON
      size_t jsonLength = generateJsonData(jsonBuffer, sizeof(jsonBuffer));

      // Send JSON data as binary over BLE
      bool sent = distanceCharacteristic.writeValue((uint8_t*)jsonBuffer, jsonLength);

      delay(1000);  // Send data every second
    }
    Serial.println("Disconnected.");
  }
}

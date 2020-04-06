// Including the ESP8266 WiFi library
#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// Replace with your network details
// const char* ssid = "mnbv";
// const char* password = "lkjh9876";

const char* ssid[] = {"518_hozzegysort","Olympos","Olympos2"};
const char* password[] = {"miertnemhoztalsortt","Diofa90Asszonyi","Diofa90Asszonyi"};

// Data wire is plugged into GPIO2
#define ONE_WIRE_BUS 2

// Setup a oneWire instance to communicate with any OneWire devices (not just Maxim/Dallas temperature ICs)
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature DS18B20(&oneWire);
char temperatureCString[6];
char temperatureFString[6];

// Web Server on port 1111
WiFiServer server(1111);

// only runs once on boot
void setup() {
  // Initializing serial port for debugging purposes
  Serial.begin(115200);
   
  delay(50);
   
  // Connect to WiFi network
  bool connecteD = false;
  int x = 0;
  while(!connecteD)
  {
      Serial.print("Connecting to ");
      Serial.println(ssid[x]);
      WiFi.begin(ssid[x], password[x]);
      for (int y = 0;y<15;y++)
      {
        if (WiFi.status() == WL_CONNECTED)
        {
          connecteD = true;
          break;
        }
        delay(500);
        Serial.print(".");
      }
      x++;
      if (WiFi.status() != WL_CONNECTED)
      {
        WiFi.disconnect();
      }
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  // Starting the web server
  server.begin();
  Serial.println("Web server running. Waiting for the ESP IP...");
  delay(2000);
  
  // Printing the ESP IP address
  Serial.println(WiFi.localIP());

  DS18B20.begin(); // IC Default 9 bit. If you have troubles consider upping it 12. Ups the delay giving the IC more time to process the temperature measurement
}

void getTemperature() {
  float tempC;
  float tempF;
  do {
    DS18B20.requestTemperatures(); 
    tempC = DS18B20.getTempCByIndex(0);
    dtostrf(tempC, 2, 2, temperatureCString);
    tempF = DS18B20.getTempFByIndex(0);
    dtostrf(tempF, 3, 2, temperatureFString);
    delay(100);
  } while (tempC == 85.0 || tempC == (-127.0));
}

// runs over and over again
void loop() {
  // Listenning for new clients
  WiFiClient client = server.available();
  
  if (client) {
    Serial.println("New client");
    while (client.connected()) {
     getTemperature();
     Serial.println("[{\"deviceid\":\"h1\",\"data\":" + String(temperatureCString) + ",\"unit\":\"C\"}]");
     client.println("[{\"deviceid\":\"h1\",\"data\":" + String(temperatureCString) + ",\"unit\":\"C\"}]");
     delay(1000);
    }  
    // closing the client connection
    delay(1);
    client.stop();
    Serial.println("Client disconnected.");
  }
}   

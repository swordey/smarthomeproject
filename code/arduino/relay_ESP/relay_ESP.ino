/*
 *  This sketch demonstrates how to set up a simple HTTP-like server.
 *  The server will set a GPIO pin depending on the request
 *    http://server_ip/gpio/0 will set the GPIO2 low,
 *    http://server_ip/gpio/1 will set the GPIO2 high
 *  server_ip is the IP address of the ESP8266 module, will be 
 *  printed to Serial when the module is connected.
 */

#include <ESP8266WiFi.h>
#include <ArduinoJson.h>

const char* ssid[] = {"wifi_name"};
const char* password[] = {"wifi_password"};



// Create an instance of the server
// specify the port to listen on as an argument
WiFiServer server(2222); // It will be reachable on this port (sensors will be on 1111 port, actuators will be on 2222 port)
WiFiClient client;
bool relayStatus;

void setup() {
  pinMode(2, OUTPUT);
  digitalWrite(2, HIGH);
  relayStatus = 0;
  Serial.begin(115200);
  delay(10000);
   
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
      if (x == 3)
      { x = 0;}
      
      if (WiFi.status() != WL_CONNECTED)
      {
        WiFi.disconnect();
      }
  }
  Serial.println("");
  Serial.println("WiFi connected");
  
  // Start the server
  server.begin();
  Serial.println("Server started");

  // Print the IP address
  Serial.println(WiFi.localIP());
}

void loop() {
  client = server.available();
  if (client) {
    Serial.println("Client connected");
    while(client.connected())
    {    
      String data = client.readString();
      Serial.println(data);
      char cdata[150];
      data.toCharArray(cdata,150);
      if(data.length() > 0)
      {
        StaticJsonBuffer<200> jsonBuffer;
        JsonObject& root = jsonBuffer.parseObject(cdata);

        if (!root.success())
        {
          Serial.println("parseObject() failed");
          client.print("[{\"deviceid\":\"actuator1\",\"status\":\"parseerror\"}]");
          continue;
        }
        // Serial.println(data);
        if (root.containsKey("get"))
        {
          if (root["get"]=="commands")
          {            
            Serial.println("getcommands");
            client.print("[{\"deviceid\":\"actuator1\",\"set\":\"on|off\"}]");
          }
          else if(root["get"]=="status")
          {
            if(relayStatus == 1)
            {              
              Serial.println("getstatus_on");
              client.print("[{\"deviceid\":\"actuator1\",\"status\":\"on\"}]");
            }
            else
            {
              Serial.println("getstatus_off");
              client.print("[{\"deviceid\":\"actuator1\",\"status\":\"off\"}]");
            }
          }
          else
          {
            Serial.println("unknown command");
            client.print("[{\"deviceid\":\"actuator1\",\"status\":\"unknowncommand\"}]");
          }
        }
        else if (root.containsKey("set"))
        {
          if (root["set"]=="on")
          {
            relayStatus = 1;
            digitalWrite(2, LOW);
            Serial.println("turn_on");
            String response = "[{\"deviceid\":\"actuator1\",\"status\":\"on\"}]";
            client.print(response);
          }
          else if(root["set"]=="off")
          {
            relayStatus = 0;
            digitalWrite(2, HIGH);
            Serial.println("turn_off");
            String response = "[{\"deviceid\":\"actuator1\",\"status\":\"off\"}]";
            client.print(response);    
          }
          else
          {            
            Serial.println("unknown command");
            client.print("[{\"deviceid\":\"actuator1\",\"status\":\"unknowncommand\"}]");
          }
        }
        else
        {
          Serial.println("unknown command");
          client.print("[{\"deviceid\":\"actuator1\",\"status\":\"unknowncommand\"}]");
        }
      }  
      delay(100);
    }
  }
  
  // The client will actually be disconnected 
  // when the function returns and 'client' object is detroyed
}

#include "ESP8266WiFi.h"
#include <ESP8266HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>

#define SS_PIN1 D8
#define RST_PIN1 D3

#define WIFI_SSID "CAMILA"
#define WIFI_PASS "fabian3104"
#define SERVER_LINK "https://myserver1-in01.onrender.com/string"  // Cambia esto a la IP de tu servidor


MFRC522 rfid1(SS_PIN1, RST_PIN1); // Crea una nueva instancia MFRC522
void SendData(String data);

WiFiClient wifiClient;
HTTPClient http;

void setup() {
  Serial.begin(9600);
  
  Serial.println("Conectando a la red wifi indicada, espere por favor");

  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
  }

  Serial.println("Nos hemos conectado, la IP asignada por el router es ");
  Serial.println(WiFi.localIP());
  Serial.print("\nDirección MAC: ");
  Serial.println(WiFi.macAddress());
  SPI.begin(); // Inicia el bus SPI
  rfid1.PCD_Init(); // Inicia sensor 1
}
String data = "";
void loop() {

  if(rfid1.PICC_IsNewCardPresent() && rfid1.PICC_ReadCardSerial()){
    
    data = "SENSOR 1";
    Serial.println("El sensor es" + data);
    SendData(data);
  }
  delay(120);
}

void SendData(String data)
{
    WiFiClientSecure wifiClient;
    wifiClient.setInsecure(); // Ignora la verificación del certificado SSL. No es seguro para producción.

    http.begin(wifiClient, SERVER_LINK);
    http.addHeader("Content-Type", "text/plain");
    int httpResponseCode = http.POST(data);

    if (httpResponseCode > 0) {
      String response = http.getString();
      Serial.println(httpResponseCode);
      Serial.println(response);
    } else {
      Serial.print("Error en la solicitud: ");
      Serial.println(httpResponseCode);
    }
    http.end();
}

// ParkingPlaceSCREEN

#include <GxEPD.h>
#define LILYGO_T5_V213
#include <boards.h>
#include <WiFi.h>
#include <HTTPClient.h>

int place1;
int place2;
int place3;
int place4;

// WiFi
WiFiClient wifiClient;
const char* ssid{"iPhone"};
const char* password{"bloempot"};
const char* serverName = "http://vincentsomers.sinners.be/post-esp-data.php";
const char *host = "https://vincentsomers.sinners.be";
String apiKeyValue = "tPmAT5Ab3j7F9";

// select the display class to use, only one, copy from GxEPD_Example
#include <GxDEPG0213BN/GxDEPG0213BN.h>    // 2.13" b/w  form DKE GROUP

#include <GxIO/GxIO_SPI/GxIO_SPI.h>
#include <GxIO/GxIO.h>

// constructor for AVR Arduino, copy from GxEPD_Example else
GxIO_Class io(SPI,  EPD_CS, EPD_DC,  EPD_RSET);
GxEPD_Class display(io, EPD_RSET, EPD_BUSY);

void setupWiFi();

void setup()
{
  Serial.begin(9600);
  display.init();
  display.eraseDisplay();
  setupWiFi();
  // comment out next line to have no or minimal Adafruit_GFX code
  //display.drawPaged(drawParking);
}

void setupWiFi()
{
  display.setTextColor(GxEPD_BLACK);
  Serial.println("setupWiFi");
  vTaskDelay(10 / portTICK_PERIOD_MS);
  // We start by connecting to a WiFi network
  Serial.println("Connecting to ");
  Serial.print(ssid);
  Serial.println();
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    vTaskDelay(200 / portTICK_PERIOD_MS);
    Serial.print(".");
  }
  randomSeed(micros());
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.print(WiFi.localIP());
  Serial.println();
}

void drawParking()
{
  display.setTextColor(GxEPD_BLACK);
  // PLACE 1
  if (place1 == 1){
   display.fillRect(0, 0, 125, 62, GxEPD_BLACK);
  }
  display.drawLine(0, 62, 125, 62, GxEPD_BLACK);
  // PLACE 2
  if (place2 == 1){
    display.fillRect(0, 62, 125, 62, GxEPD_BLACK);
  }
  display.drawLine(0, 125, 125, 125, GxEPD_BLACK);
  // PLACE 3
  if (place3 == 1){
    display.fillRect(0, 125, 125, 125, GxEPD_BLACK);
  }
  display.drawLine(0, 187, 125, 187, GxEPD_BLACK);
  // PLACE 4
  if (place4 == 1){
    display.fillRect(0, 187, 125, 187, GxEPD_BLACK);
  }

  if (place1 == 1 && place2 == 1 && place3 == 1 && place4 == 1){

  display.setTextColor(GxEPD_WHITE);
  display.setCursor(25, 125);
  display.print("PARKING FULL");
  }
}

void loop() {
  display.init();
  display.eraseDisplay();
  place1 = 0;
  place2 = 0;
  place3 = 0;
  place4 = 0;
  // comment out next line to have no or minimal Adafruit_GFX code

  // put your main code here, to run repeatedly:
  HTTPClient http; //--> Declare object of class HTTPClient

  //----------------------------------------Getting Data from MySQL Database
  String GetAddress, LinkGet, getData;
  int id = 1; //--> ID in Database
  GetAddress = "/esp-data.php"; 
  LinkGet = host + GetAddress; //--> Make a Specify request destination
  getData = "id=" + String(id);
  Serial.println("----------------Connect to Server-----------------");
  Serial.println("Get Parking Status from Server or Database");
  Serial.print("Request Link : ");
  Serial.println(LinkGet);
  http.begin(LinkGet); //--> Specify request destination
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");    //Specify content-type header
  int httpCodeGet = http.POST(getData); //--> Send the request
  String payloadGet = http.getString(); //--> Get the response payload from server
  Serial.print("Response Code : "); //--> If Response Code = 200 means Successful connection, if -1 means connection failed. For more information see here : https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
  Serial.println(httpCodeGet); //--> Print HTTP return code
  Serial.print("Returned data from Server : ");
  Serial.println(payloadGet); //--> Print request response payload

  if(payloadGet.indexOf("1") >= 0){
    place1 = 1;
  }

   if(payloadGet.indexOf("2") >= 0){
    place2 = 1;
  }

   if(payloadGet.indexOf("3") >= 0){
    place3 = 1;
  }

   if(payloadGet.indexOf("4") >= 0){
    place4 = 1;
  }
  
  Serial.println("----------------Closing Connection----------------");
  http.end(); //--> Close connection
  Serial.println();
  Serial.println("Please wait 10 seconds for the next connection.");
  Serial.println();
  display.drawPaged(drawParking);
  delay(10000);
  };

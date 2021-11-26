// ParkingPlaceSCREEN

#include <GxEPD.h>
#define LILYGO_T5_V213
#include <boards.h>
int place1 = 0;
int place2 = 0;
int place3 = 0;
int place4 = 0;

// select the display class to use, only one, copy from GxEPD_Example
#include <GxDEPG0213BN/GxDEPG0213BN.h>    // 2.13" b/w  form DKE GROUP

#include <GxIO/GxIO_SPI/GxIO_SPI.h>
#include <GxIO/GxIO.h>

// constructor for AVR Arduino, copy from GxEPD_Example else
GxIO_Class io(SPI,  EPD_CS, EPD_DC,  EPD_RSET);
GxEPD_Class display(io, EPD_RSET, EPD_BUSY);

void setup()
{
  display.init();
  display.eraseDisplay();
  // comment out next line to have no or minimal Adafruit_GFX code
  display.drawPaged(drawParking);
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
}

void loop() {};

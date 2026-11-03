#include <Adafruit_GFX.h>
#include <MCUFRIEND_kbv.h>
#include <stdio.h>        //input output library
#include <stdint.h>       //integer type library
#include <string.h>       //string library
#include <Wire.h>
MCUFRIEND_kbv tft;

#define LOWFLASH (defined(__AVR_ATmega328P__) && defined(MCUFRIEND_KBV_H_))
#include "bitmap_RGB.h"
//#include "image.h"
#define BLACK   0x0000
#define BLUE    0x001F
#define RED     0xF800
#define GREEN   0x07E0
#define CYAN    0x07FF
#define MAGENTA 0xF81F
#define YELLOW  0xFFE0
#define WHITE   0xFFFF
#define GREY    0x8410
#define ORANGE  0xE880
float InletFlow;
float InletTot;
float OutletFlow;
float OutletTot;
float i=0;
float j=0;
int width = 320;
int height = 480;


void logo(int x, int y, int w, int h) {
    tft.drawRGBBitmap(x, y, gowatr_64x64, w, h);
    //tft.drawRGBBitmap(x+200, y, somerset_64x64, w, h);
}

void setup() {
  Serial.begin(9600); // Set the baud rate to match the Raspberry Pi
  uint16_t ID = tft.readID();
    Serial.print("TFT ID = 0x");
    Serial.println(ID, HEX);
    if (ID == 0xD3D3) ID = 0x9486; // write-only shield
    tft.begin(ID);
    tft.setRotation(1);            //PORTRAIT
    tft.fillScreen(BLACK);
    tft.setTextColor(YELLOW, BLACK);
    tft.setTextSize(2);
    // testing();
    tft.setTextSize(2);
    tft.setCursor(135, 25);
    tft.setTextColor(WHITE,BLACK);
    tft.print("Somerset STP Flowmeters");
    tft.setTextSize(2);
    tft.setCursor(135, 47);
    tft.print("(in LPH)");
    printUI();   
}

void loop() {
  if (Serial.available() > 0) {
    String sensorData = Serial.readStringUntil('\n');
    // Parse received data
    int separatorIndex = sensorData.indexOf(':');
    if (separatorIndex != -1) {
      String sensorName = sensorData.substring(0, separatorIndex);
      if(sensorName.equals("Flow"))
      {
      float InletFlow = sensorData.substring(separatorIndex + 1).toFloat();
      Serial.print("Received Sensor: ");
      Serial.print(sensorName);
      Serial.print(", Value: ");
      Serial.println(InletFlow);
      tft.fillRect(8,179,220,27,BLACK);
      tft.setCursor(10, 180);
      tft.setTextSize(3);
      tft.print(InletFlow);
      }
      if(sensorName.equals("Tot"))
      {
      float InletTot = sensorData.substring(separatorIndex + 1).toFloat();
      Serial.print("Received Sensor: ");
      Serial.print(sensorName);
      Serial.print(", Value: ");
      Serial.println(InletTot);
      tft.fillRect(8,258,220,27,BLACK); 
      tft.setCursor(10, 260);
      tft.setTextSize(3);
      tft.print(InletTot);
      }
//////////////////////////////////////////////////////////////////
      if(sensorName.equals("Flow2"))
      {
      float OutletFlow = sensorData.substring(separatorIndex + 1).toFloat();
      Serial.print("Received Sensor: ");
      Serial.print(sensorName);
      Serial.print(", Value: ");
      Serial.println(OutletFlow);
      tft.fillRect(248,179,220,27,BLACK);
      tft.setCursor(249, 180);
      tft.setTextSize(3);
      tft.print(OutletFlow);
      }
      if(sensorName.equals("Tot2"))
      {
      float OutletTot = sensorData.substring(separatorIndex + 1).toFloat();
      Serial.print("Received Sensor: ");
      Serial.print(sensorName);
      Serial.print(", Value: ");
      Serial.println(OutletTot);
      tft.fillRect(248,258,220,27,BLACK);
      tft.setCursor(249, 260);
      tft.setTextSize(3);
      tft.print(OutletTot);
      delay(1000);
      }
    }
  }
}

void printUI()
{
tft.drawRoundRect(5,5,470,71,5,TFT_WHITE);
tft.drawRoundRect(6,6,470,71,5,TFT_WHITE);

tft.drawRoundRect(5,90,235,225,5,TFT_WHITE);
tft.drawRoundRect(6,91,235,225,5,TFT_WHITE);

tft.drawRoundRect(240,90,235,225,5,TFT_WHITE);
tft.drawRoundRect(241,91,235,225,5,TFT_WHITE);

logo(40, 10, 64, 64);

tft.fillRect(26,90,180,40,TFT_GREEN);
tft.fillRect(270,90,180,40,TFT_CYAN);

tft.setCursor(62,100);
tft.setTextColor(TFT_BLACK);
tft.setTextSize(3);
tft.print("INLET");

tft.setCursor(10,140);
tft.setTextColor(TFT_GREEN);
tft.setTextSize(4);
tft.print("F~");

tft.setCursor(10,215);
tft.setTextColor(TFT_GREEN);
tft.setTextSize(4);
tft.print("T+");
//////////////////////////////////////////////////////////////////////

tft.setCursor(312,100);
tft.setTextColor(TFT_BLACK);
tft.setTextSize(3);
tft.print("OUTLET");

tft.setCursor(250,140);
tft.setTextColor(TFT_CYAN);
tft.setTextSize(4);
tft.print("F~");

tft.setCursor(250,215);
tft.setTextColor(TFT_CYAN);
tft.setTextSize(4);
tft.print("T+");

/*tft.setCursor(210,245);
tft.setTextColor(TFT_GREEN);
tft.setTextSize(2);
tft.print("+");*/

/*tft.setCursor(455,245);
tft.setTextColor(TFT_CYAN);
tft.setTextSize(2);
tft.print("+");*/
}


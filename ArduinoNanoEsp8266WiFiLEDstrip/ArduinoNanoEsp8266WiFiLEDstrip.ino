/**
 *  SSID: LED
 *  http://192.168.4.1
 *
 */

#include <SoftwareSerial.h>

// Taken from https://learn.adafruit.com/adafruit-neopixel-uberguide/arduino-library
#include <Adafruit_NeoPixel.h>

#define NUM_LEDS      8
#define PIN_LED_STRIP 9

SoftwareSerial esp8266(11, 12);

/* Alternative Progmem: Converted with http://www.percederberg.net/tools/text_converter.html to C-String Text and saved as char */
const char site[] PROGMEM = {
"<HTML><HEAD>\n<link rel=\"icon\" href=\"data:;base64,iVBORw0KGgo=\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=2.0, user-scalable=yes\">\n<title>\nRGB LED\n</title>\n</HEAD>\n\n<BODY bgcolor=\"#FFFF99\" text=\"#000000\">\n<FONT size=\"6\" FACE=\"Verdana\">\nSelect Color\n</FONT>\n\n<HR>\n<BR>\n<FONT size=\"3\" FACE=\"Verdana\">\nChange the Color<BR>\nof the RGB-LED\n<BR>\n<BR>\n<form method=\"GET\">\n\t<input type=\"color\" name=\"rgb\" onchange=\"this.form.submit()\"><BR>\n</form>\n<form method=\"get\">\n    <input type=\"submit\" value=\"FF0000\" name=\"rgb\" id=\"button_red\"></input>\n\t<input type=\"submit\" value=\"00FF00\" name=\"rgb\" id=\"button_gre\"></input><br/>\n\t<input type=\"submit\" value=\"0000FF\" name=\"rgb\" id=\"button_blu\"></input>\n\t<input type=\"submit\" value=\"FFFF00\" name=\"rgb\" id=\"button_yel\"></input><br/>\n\t<input type=\"submit\" value=\"FF00FF\" name=\"rgb\" id=\"button_xxx\"></input>\n\t<input type=\"submit\" value=\"00FFFF\" name=\"rgb\" id=\"button_yyy\"></input><br/>\t\n\t<input type=\"submit\" value=\"FFFFFF\" name=\"rgb\" id=\"button_zzz\"></input>\t\n</form>\n<BR>\n<HR>\n\n</font>\n</HTML>\n\n\0"
};
String webpage;

Adafruit_NeoPixel strip = Adafruit_NeoPixel(
  NUM_LEDS, 
  PIN_LED_STRIP, 
    NEO_GRB 
  + NEO_KHZ800
  );

const struct {
   unsigned char r;
   unsigned char g;
   unsigned char b;
} c[NUM_LEDS] = {
  {   0,   0,   0},
  { 255,   0,   0},
  {   0, 255,   0},
  {   0,   0, 255},
  { 255, 255,   0},
  { 255,   0, 255},
  {   0, 255, 255},
  { 255, 255, 255},
};

void setup() {
  esp8266.begin(19200);
  esp8266.setTimeout(5000);
  esp8266.println("AT+RST");                        esp8266.readString();
  esp8266.setTimeout(1000);
  esp8266.println("AT+CWMODE=2");                   esp8266.readString();
  esp8266.println("AT+CWSAP=\"LED\",\"\",5,0"); esp8266.readString();
  esp8266.println("AT+CIPMUX=1");                   esp8266.readString();
  esp8266.println("AT+CIPSERVER=1,80");             esp8266.readString();

  webpage = createWebsite();
  
  strip.begin();
  strip.setBrightness(8);
  for(int i = 0; i < strip.numPixels(); ++i){
    strip.setPixelColor(i, c[i].r, c[i].g, c[i].b);  
  }
  strip.show();
}

void loop() {
  if (esp8266.available()){
     if (esp8266.find("+IPD,")){
        int connectionId = esp8266.parseInt();
        if (esp8266.findUntil("?rgb=", "\n")){
           /* Do actuation here */
           String hexstring = esp8266.readStringUntil(' ');
           long number = (long) strtol( &hexstring[3], NULL, 16); /**< Convert String to Hex http://stackoverflow.com/questions/23576827/arduino-convert-a-sting-hex-ffffff-into-3-int */

           /* Split them up into r, g, b values */
           int r = number >> 16;
           int g = number >> 8 & 0xFF;           
           int b = number & 0xFF;

           strip.setBrightness(128);
           for(int i = 0; i < strip.numPixels(); ++i){
              strip.setPixelColor(i, r, g, b);  
           }
           strip.show();
        }
        /* sendWebsite here */
        esp8266.println("AT+CIPSEND=" + String(connectionId) + "," + String(webpage.length()));
        esp8266.readString();
        esp8266.print(webpage);
        esp8266.readString();
        esp8266.println("AT+CIPCLOSE=" + String(connectionId));
        esp8266.readString();
     }
  }
}

String createWebsite()
{
  String xBuffer;

  for (int i = 0; i <= sizeof(site); i++)
  {
    char myChar = pgm_read_byte_near(site + i);
    xBuffer += myChar;
  }

  return xBuffer;
}


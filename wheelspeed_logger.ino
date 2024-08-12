#include <SPI.h>
#include <SD.h>
#include <RTClib.h>

#define SD_CS_PIN 6


RTC_DS3231 rtc;

File dataFile;

DateTime now;


int count = 0;
int RLvalue1, RLvalue2;
unsigned long int time1, time2;
float RLspeed = 0;

int count2 = 0;
int RRvalue1, RRvalue2;
unsigned long int time1r, time2r;
float RRspeed = 0;

unsigned long int logt, loglast;

void setup() {
  Serial.begin(115200);

  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");

  } else{
      Serial.println("RTC connected");
  }

  if (!SD.begin(6)) {
      Serial.println("SD initialization failed!");
      return;
  }
  else{
      Serial.println("SD initialization done");

  }

    dataFile = SD.open("data.csv", FILE_WRITE);
  if (dataFile) {
      dataFile.println("Date,TimeStamp,Millis,RLwheel-speed,RRwheel-speed");
      dataFile.close();
  } else {
      Serial.println("Error creating data.csv");
      return;
  }

  delay(1000);

pinMode(A0,INPUT);
pinMode(A1,INPUT);

RRvalue1=analogRead(A0);
RRvalue2=RRvalue1;

RLvalue1=analogRead(A1);
RLvalue2=RLvalue1;
}

void loop() {

  now = rtc.now();


  logt = millis();

  RLvalue1 = analogRead(A1);
  if (abs(RLvalue1 - RLvalue2) > 200) {
    count = count + 1;
    Serial.println(count);
  }

  RLvalue2 = RLvalue1;


  RRvalue1 = analogRead(A0);
  if (abs(RRvalue1 - RRvalue2) > 200) {
    count2 = count2 + 1;
    // Serial.println(count);
  }

  RRvalue2 = RRvalue1;


  if (count == 1) {
    time1 = millis();
  } else if (count / 32 == 1) {
    time2 = millis();
    RLspeed = ((1.0 / (time2 - time1)) * 1000 * 60 );
    Serial.print("RLspeed ");

    Serial.print(RLspeed);
    Serial.print(" rpm       ");
    count = 0;
  }

  if (count2 == 1) {
    time1r = millis();
  } else if (count2 / 32 == 1) {
    time2r = millis();
    RRspeed = ((1.0 / (time2r - time1r)) * 1000 * 60 );
    Serial.print("RRspeed  ");

    Serial.print(RRspeed);
    Serial.println(" rpm");
    count2 = 0;
  }

  if ((logt - loglast) > 999) {
    speed_logger();
    loglast = millis();
    Serial.println("logging");
  }
}



void speed_logger() {


  dataFile = SD.open("data.csv", FILE_WRITE);
  if (dataFile) {

    dataFile.print(now.year(), DEC);
    dataFile.print('/');
    dataFile.print(now.month(), DEC);
    dataFile.print('/');
    dataFile.print(now.day(), DEC);
    dataFile.print(",");
    dataFile.print(now.hour(), DEC);
    dataFile.print(':');
    dataFile.print(now.minute(), DEC);
    dataFile.print(':');
    dataFile.print(now.second(), DEC);
    dataFile.print(",");

    dataFile.print(millis());
    dataFile.print(",");


    dataFile.print(RLspeed);
    dataFile.print(",");
    dataFile.println(RRspeed);
    dataFile.close();
  } else {

    Serial.println("Error writing to data.csv");
  }
}
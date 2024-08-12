#include <mcp_can.h>
#include <SPI.h>
#include <SD.h>
#include <RTClib.h>

RTC_DS3231 rtc;

File dataFile;

DateTime now;

float lv_ladderout;
float lv_in;

float MotorTemp;
float MotorRPM;
float MotorI;
float MotorVdc;
float MotorAirT;
float temp;

float packV;
float packI;
float packSOC;
float packHTemp;


float MotorTemp_raw;
float MotorRPM_raw;
float MotorI_raw;
float MotorVdc_raw;
float MotorAirT_raw;

float packV_raw;
float packI_raw;
float packSOC_raw;
float packHTemp_raw;

unsigned long int t1 = 0, t2 = 0;

#define lv_pin A2
#define iqthresold 169.9
#define tempthresold 100.0
#define rpmthresold 6000.0
#define vdcthresold 1028.0

uint16_t sa, sb, sc, sd, se, sf, sg, sh,si;
long unsigned int rxId;
unsigned char len = 0;
unsigned char rxBuf[8];


long unsigned int BMSrxId = 0x005;

#define CAN0_INT 2
#define MCP_CS_PIN 5
#define SD_CS_PIN 6


MCP_CAN CAN0(MCP_CS_PIN);

void setup() {
  Serial.begin(115200);

  pinMode(lv_pin, INPUT);
  pinMode(CAN0_INT, INPUT);
  pinMode(MCP_CS_PIN,OUTPUT);
  pinMode(SD_CS_PIN,OUTPUT);

  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    // while (1)
      // ;
  }




  if (!SD.begin(SD_CS_PIN)) {
    Serial.println("SD initialization failed!");
    return;
  }


  dataFile = SD.open("data.csv", FILE_WRITE);
  if (dataFile) {
    dataFile.println("Date,TimeStamp,MotorRPM,PackSOC,PackI,MotorI,PackHTEMP,PackV");
    Serial.println("creating data.csv");
    dataFile.close();
  } else {
    Serial.println("Error creating data.csv");
    return;
  }
    CAN0.begin(MCP_ANY, CAN_500KBPS, MCP_8MHZ);

  CAN0.setMode(MCP_NORMAL);




  delay(2000);


  Request_motor_rpm_Bamocar();
  Request_motor_temp_Bamocar();


}

void loop() {
  // put your main code here, to run repeatedly:
  
  now = rtc.now();

  // Serial.print(now.year(), DEC);
  // Serial.print('/');
  // Serial.print(now.month(), DEC);
  // Serial.print('/');
  // Serial.print(now.day(), DEC);
  // Serial.print("  ");
  // Serial.print(now.hour(), DEC);
  // Serial.print(':');
  // Serial.print(now.minute(), DEC);
  // Serial.print(':');
  // Serial.print(now.second(), DEC);.
  
  // Serial.print("  ");

  MotorRPM = Capture_motor_rpm_Bamocar();
  MotorTemp = Capture_motor_temp_Bamocar();
  packV = Extract_BMS_PackV();
  packI = Extract_BMS_PackI();
  packSOC = Extract_BMS_PackSOC();
  packHTemp = Extract_BMS_PackHTEMP();
  MotorI = Capture_Iq_Bamocar();

  lv_ladderout = ((float(analogRead(lv_pin)) / 1024.00) * 5.00);
  lv_in = lv_ladderout * ((4550.00 + 1156.00) / 1156.00);
 
  Serial.print(int(MotorRPM));
  Serial.print(",");

  Serial.print(int(packV));
  Serial.print(",");

  Serial.print(packHTemp,1);
  Serial.print(",");


  Serial.print(MotorTemp,1);
  Serial.print(",");

  Serial.println((lv_in),1);
  logDataOnSD();

  delay(50);
}


void logDataOnSD() {

  dataFile = SD.open("data.csv", FILE_WRITE);
  // Serial.println(dataFile);

  if (dataFile) {
    // Print date and time
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
    
    // Print sensor data
    dataFile.print(int(MotorRPM));
    dataFile.print(",");
    dataFile.print(packSOC);
    dataFile.print(",");
    dataFile.print(packI);
    dataFile.print(",");
    dataFile.print(MotorI);
    dataFile.print(",");
    dataFile.print(packHTemp);
    dataFile.print(",");
    dataFile.print(packV);
    dataFile.println(); // Move to the next line

    dataFile.close(); // Close the file
    // Serial.println("Data logged successfully");
  } else {
    // Serial.println("Error opening data.csv");
  }
  

}



void Request_Vdc_Bamocar() {
  //Requesting Data From the bamocar_______________________________________________________
  byte data[8] = { 0x3D, 0xEB, 0x0004, 0x00, 0x00, 0x00, 0x00, 0x00 };
  // send data:  ID = 0x100, Standard CAN Frame, Data length = 8 bytes, 'data' = array of data bytes to send
  // Serial.println();
  byte sndStat = CAN0.sendMsgBuf(0x201, 0, 8, data);  //Tx ID x201 by Bamocar
  // if(sndStat == CAN_OK){
  //   Serial.println("Message Sent Successfully Bamo VDC_Bus!");
  // } else {
  //   Serial.println("Error Sending Message...");
  // }

  delay(2);
}

float Capture_Vdc_Bamocar() {
  //Fetching the Received data_____________________________________________________________
  CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Read data: len = data length, buf = data byte(s)
  if (rxId == 0x181 && rxBuf[0] == 235) {
    // Serial.print(rxBuf[0]);
    uint16_t sa = (uint16_t)rxBuf[1] | (uint16_t)(rxBuf[2] << 8);  //Extracting MSB and LSB
                                                                   // for(int i=0; i <=8;i++){
                                                                   //   Serial.println(rxBuf[i]);
                                                                   // }



    //Throwing out Live BUS Voltage data in float
    float V = (float)sa;
    float Value = V * (vdcthresold / 32767.0);  //16-Bit Value Conversion into Voltage Bus
    // Serial.println(floatValue, 4);
    return Value;
  }
}

void Request_motor_rpm_Bamocar() {
  //Requesting Data From the bamocar_______________________________________________________
  byte data[8] = { 0x3D, 0xA8, 0x0004, 0x00, 0x00, 0x00, 0x00, 0x00 };
  // send data:  ID = 0x100, Standard CAN Frame, Data length = 8 bytes, 'data' = array of data bytes to send
  // Serial.println();
  byte sndStat = CAN0.sendMsgBuf(0x201, 0, 8, data);  //Tx ID x201 by Bamocar
  // if(sndStat == CAN_OK){
  //   Serial.println("Message Sent Successfully Bamo VDC_Bus!");
  // } else {
  //   Serial.println("Error Sending Message...");
  // }
  delay(2);
}

float Capture_motor_rpm_Bamocar() {
  //Fetching the Received data_____________________________________________________________
  CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Read data: len = data length, buf = data byte(s)
  if (rxId == 0x181 && rxBuf[0] == 168) {
    uint16_t sb = (uint16_t)rxBuf[1] | (uint16_t)(rxBuf[2] << 8);  //Extracting MSB and LSB
                                                                   // Serial.print(sb);

    //Throwing out Live BUS Voltage data in float
    float rpm = (float)sb;
    if (rpm == 0) {  //eliminate garbage value at 0 i.e 12000
      return 0;
    } else {
      float Value = (65534-rpm)*(rpmthresold/32767.0);         // Serial.println(floatValue, 4);
          if (Value > 10000) {  //eliminate garbage value at 0 i.e 12000
      return 0;
    }
      return Value;
    }
  }
}


void Request_motor_temp_Bamocar() {
  //Requesting Data From the bamocar_______________________________________________________
  byte data[8] = { 0x3D, 0x49, 0x0004, 0x00, 0x00, 0x00, 0x00, 0x00 };
  // send data:  ID = 0x100, Standard CAN Frame, Data length = 8 bytes, 'data' = array of data bytes to send
  // Serial.println();
  byte sndStat = CAN0.sendMsgBuf(0x201, 0, 8, data);  //Tx ID x201 by Bamocar
  // if(sndStat == CAN_OK){
  //   Serial.println("Message Sent Successfully Bamo VDC_Bus!");
  // } else {
  //   Serial.println("Error Sending Message...");
  // }
  // delay(10);   // send data per 100ms
  delay(2);
}

float Capture_motor_temp_Bamocar() {
  //Fetching the Received data_____________________________________________________________
  CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Read data: len = data length, buf = data byte(s)
  if (rxId == 0x181 && rxBuf[0] == 73) {
    uint16_t sc = (uint16_t)rxBuf[1] | (uint16_t)(rxBuf[2] << 8);  //Extracting MSB and LSB
                                                                   // Serial.print(sc);
                                                                   //  for(int i=0; i <=8;i++){
                                                                   //   Serial.println(rxBuf[i]);
                                                                   // }

    //Throwing out Live BUS Voltage data in float
    float t = (float)sc;
    float Value = t * (tempthresold / 32767.0);  //16-Bit Value Conversion into Voltage Bus
    // Serial.println(floatValue, 4);
    return Value;
  }
}


void Request_Icmd_Bamocar() {
  //Requesting Data From the bamocar_______________________________________________________
  byte data[8] = { 0x3D, 0x26, 0x0004, 0x00, 0x00, 0x00, 0x00, 0x00 };
  // send data:  ID = 0x100, Standard CAN Frame, Data length = 8 bytes, 'data' = array of data bytes to send
  // Serial.println();
  byte sndStat = CAN0.sendMsgBuf(0x201, 0, 8, data);  //Tx ID x201 by Bamocar
  // if(sndStat == CAN_OK){
  //   Serial.println("Message Sent Successfully Bamo VDC_Bus!");
  // } else {
  //   Serial.println("Error Sending Message...");
  // }
  // delay(10);   // send data per 100ms
  delay(2);
}
float Capture_Icmd_Bamocar() {
  //Fetching the Received data_____________________________________________________________
  CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Read data: len = data length, buf = data byte(s)
  if (rxId == 0x181 && rxBuf[0] == 38) {
    uint16_t sd = (uint16_t)rxBuf[1] | (uint16_t)(rxBuf[2] << 8);  //Extracting MSB and LSB
                                                                   // Serial.print(sd);

    //Throwing out Live BUS Voltage data in float
    float icmd = (float)sd;
    float Value = icmd * (iqthresold / 1023.0);  //16-Bit Value Conversion into Voltage Bus
    // Serial.println(floatValue, 4);
    return Value;
  }
}

void Request_Iq_Bamocar() {
  //Requesting Data From the bamocar_______________________________________________________
  byte data[8] = { 0x3D, 0x5F, 0x0004, 0x00, 0x00, 0x00, 0x00, 0x00 };
  // send data:  ID = 0x100, Standard CAN Frame, Data length = 8 bytes, 'data' = array of data bytes to send
  // Serial.println();
  byte sndStat = CAN0.sendMsgBuf(0x201, 0, 8, data);  //Tx ID x201 by Bamocar
  // if(sndStat == CAN_OK){
  //   Serial.println("Message Sent Successfully Bamo VDC_Bus!");
  // } else {
  //   Serial.println("Error Sending Message...");
  // }
  // delay(10);   // send data per 100ms
  delay(2);
}

float Capture_Iq_Bamocar() {
  //Fetching the Received data_____________________________________________________________
  CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Read data: len = data length, buf = data byte(s)
  if (rxId == 0x181 && rxBuf[0] == 95) {
    uint16_t se = (uint16_t)rxBuf[1] | (uint16_t)(rxBuf[2] << 8);  //Extracting MSB and LSB
                                                                   // Serial.print(se);

    //Throwing out Live BUS Voltage data in float
    float iq = (float)se;
    float Value = (iq) * (iqthresold / 1023.0);  //16-Bit Value Conversion into Voltage Bus
    // Serial.println(floatValue, 4);
    return Value;
  }
}

float Extract_BMS_PackV() {
  //Fetching the Received data_____________________________________________________________

  //CAN Packet to be made for ORION BMS 2
  //txID = 0x008;
  //byte 0 = Most significant bit
  //byte 1 = Least Significant bit


  CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Read data: len = data length, buf = data byte(s)
  if (rxId == BMSrxId) {
    uint16_t sb = (uint16_t)rxBuf[0] | (uint16_t)(rxBuf[1] << 8);  //Extracting MSB and LSB
    // Serial.println(sb);
    temp = (float)sb / 10;
    return temp;
  }
}


float Extract_BMS_PackI() {
  //Fetching the Received data_____________________________________________________________

  //CAN Packet to be made for ORION BMS 2
  //txID = 0x008;
  //byte 0 = Most significant bit
  //byte 1 = Least Significant bit


  CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Read data: len = data length, buf = data byte(s)
  if (rxId == BMSrxId) {
    uint16_t sb = (uint16_t)rxBuf[2] | (uint16_t)(rxBuf[3] << 8);  //Extracting MSB and LSB
    // Serial.println(sb);
    temp = (float)sb;

    return temp;
  }
}


float Extract_BMS_PackSOC() {
  //Fetching the Received data_____________________________________________________________

  //CAN Packet to be made for ORION BMS 2
  //txID = 0x008;
  //byte 0 = Most significant bit
  //byte 1 = Least Significant bit


  CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Read data: len = data length, buf = data byte(s)
  if (rxId == BMSrxId) {
    uint16_t sb = (uint16_t)rxBuf[6] | (uint16_t)(rxBuf[7] << 8);  //Extracting MSB and LSB
    // Serial.println(sb);
    temp = (float)sb / 2;
    return temp;
  }
}


float Extract_BMS_PackHTEMP() {
  //Fetching the Received data_____________________________________________________________

  //CAN Packet to be made for ORION BMS 2
  //txID = 0x008;
  //byte 0 = Most significant bit
  //byte 1 = Least Significant bit


  CAN0.readMsgBuf(&rxId, &len, rxBuf);  // Read data: len = data length, buf = data byte(s)
  if (rxId == BMSrxId) {
    uint16_t sb = (uint16_t)rxBuf[4] | (uint16_t)(rxBuf[5] << 8);  //Extracting MSB and LSB
    // Serial.println(sb);
    temp = (float)sb;
    return temp;
  }
}
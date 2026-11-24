//Temp_7Seg.ino
//
// Simple script that uses a DHT11 to measure temperature and then displays it to a 7 segment display
//
// INFO ON SENSOR
// ------------------------------------
// Temperature Sensor
// Sensor Type: DHT11
// Driver Ver:  1
// Unique ID:   -1
// Max Value:   50.00°C
// Min Value:   0.00°C
// Resolution:  2.00°C
// ------------------------------------
// Humidity Sensor
// Sensor Type: DHT11
// Driver Ver:  1
// Unique ID:   -1
// Max Value:   80.00%
// Min Value:   20.00%
// Resolution:  5.00%
// ------------------------------------
//

#define LED_BUILTIN 2

#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

// DHT11 defines
#define DHTPIN 18      // Digital pin connected to the DHT sensor
#define DHTTYPE DHT11  // DHT 11
DHT_Unified dht(DHTPIN, DHTTYPE);

// Event for measurement
sensors_event_t event;

// Fault check
unsigned long lastCheck = 0;
const unsigned long CHECK_INTERVAL = 10000;  // every 30 seconds

// Sensor Check
unsigned long lastAutoRead = 0;
const unsigned long AUTO_READ_INTERVAL = 1000;  // 1 minutes, in milliseconds (60 * 1000)

float tempC = 0;
float humid = 0;
float tempF = 0;


// Seven Seg Disp defines
const int segmentPins[] = {22, 19, 14, 33, 32, 23, 25, 4};

const int digitPins[] = {13, 27, 26, 21};

const int numDisp = 4;

const int numeral[10]= { 

B11111100, // 0
B01100000, // 1
B11011010, // 2
B11110010, // 3
B01100110, // 4
B10110110, // 5
B10111110, // 6 
B11100000, // 7 
B11111110, // 8 
B11110110, // 9

};

unsigned long digitHex[4] = { 0x0E, 0x0D, 0x0B, 0x07}; 

typedef struct{
    int ones;
    int tens;
    int hundreds;
    int thousands;
} strippedNum;



// Sensor Functions
void checkSensorHealth() {
  bool health = false;
  //check
  dht.humidity().getEvent(&event);
  dht.temperature().getEvent(&event);

  while (health == false) {
    if (isnan(event.temperature)) {
// error temp
  digitalWrite(LED_BUILTIN, HIGH);  
  delay(500);                      
  digitalWrite(LED_BUILTIN, LOW);   
  delay(500);      
    } else if (isnan(event.relative_humidity)) {
  digitalWrite(LED_BUILTIN, HIGH);  
  delay(500);                      
  digitalWrite(LED_BUILTIN, LOW);   
  delay(500);   
      } else {

      health = true;
    }
  }
}

void readSensor() {

  int idx = 0;
  float lasttempF = 0;
  float lasthumid = 0;
  for (int i = 0; i < 6; ++i) {

    // Get measurements
    dht.temperature().getEvent(&event);
    tempC = event.temperature;
    dht.humidity().getEvent(&event);
    humid = event.relative_humidity;
    tempF = tempC * (9.0 / 5.0) + 32;
    lasttempF += tempF;
    lasthumid += humid;

    ++idx;
  }

}

// Seven Seg functions

strippedNum extractNum(float inNum){
  strippedNum fin;
    int num1 = round(inNum*100);
    
    fin.ones = num1 % 10;
    fin.tens = num1/10 % 10;    
    fin.hundreds = num1/100 % 10;
    fin.thousands = num1/1000 % 10;

    return fin;
} 


void clearDigit(){
    for(int segment = 0; segment<8; segment++ ){
    digitalWrite(segmentPins[segment],LOW);
  }
}


void showDigit(int digit, int number, bool dp){
  
  int pattern = numeral[number];
  if (dp) pattern |= 1;
  clearDigit();

  for (int i = 0; i<numDisp ; i++){
  digitalWrite(digitPins[i],((digitHex[digit]>> i )& 1));
  }

  for(int segment = 0; segment<8; segment++ ){
    bool segOn = bitRead(pattern,segment);
    digitalWrite(segmentPins[segment],segOn);
  }
  delay(1);
}



uint32_t delayMS;

void setup() {
// Sensor setup
  dht.begin();
  delay(100);
  // Print temperature sensor details.
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  // Print humidity sensor details.
  dht.humidity().getSensor(&sensor);
  delay(100);

  // Set delay between sensor readings based on sensor details.
  // delayMS = sensor.min_delay;
  // 1000000 = delayMS

  //Seven seg setup

 for(int i = 0; i<8; i++ ){
  pinMode(segmentPins[i], OUTPUT);
 }

 for (int i = 0; i < numDisp; i++){

  pinMode(digitPins[i], OUTPUT);
 }

  pinMode(LED_BUILTIN, OUTPUT);

}

void loop() {


  unsigned long now = millis();
  bool timeToAutoRead = (now - lastAutoRead >= AUTO_READ_INTERVAL);

  if (now - lastCheck >= CHECK_INTERVAL) {
    lastCheck = now;
    checkSensorHealth();
  }

  if (timeToAutoRead) {
      lastAutoRead = now;  // only reset the timer on an auto-triggered read
    
    readSensor();
  }

  strippedNum output = extractNum(tempF);
  int digits[4] = {output.thousands, output.hundreds, output.tens, output.ones};

  for(int i = 0; i<4; i++){
  showDigit(i,digits[i], i==1 );
  }

}

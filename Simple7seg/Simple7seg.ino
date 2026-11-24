
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



void setup() {
 

 for(int i = 0; i<8; i++ ){
  pinMode(segmentPins[i], OUTPUT);
 }

 for (int i = 0; i < numDisp; i++){

  pinMode(digitPins[i], OUTPUT);
 }
}

float num = 55.67;

void loop() {

  strippedNum output = extractNum(num);
  int digits[4] = {output.thousands, output.hundreds, output.tens, output.ones};

  for(int i = 0; i<4; i++){
  showDigit(i,digits[i], i==1 );
  }

}





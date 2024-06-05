#include <Servo.h>


// left motor
const int leftEn = 24;
const int leftDir = 22;
const int leftStep = 23;
// right motor
const int rightEn = 28;
const int rightDir = 26;
const int rightStep = 27;
// front motor
const int frontEn = 32;
const int frontDir = 30;
const int frontStep = 31;
// back motor
const int backEn = 36;
const int backDir = 34;
const int backStep = 35;
// up motor
const int upEn = 40;
const int upDir = 38;
const int upStep = 39;
// down motor
const int downEn = 44;
const int downDir = 42;
const int downStep = 43;

// servo motors
const int leftServoPin = 48;
const int rightServoPin = 49;
const int frontServoPin = 50;
const int backServoPin = 51;
const int upServoPin = 52;
Servo leftServo;
Servo rightServo;
Servo frontServo;
Servo backServo;
Servo upServo;

// speed
const int speed = 200;
// serial read
bool isReadable = true;
char char1;
char char2;
char char3;
// servo position
int pos = 0;


// ============================== SETUP =============================
void setup() {
  Serial.begin(9600);

  // left
  pinMode(leftEn, OUTPUT);
  pinMode(leftDir, OUTPUT);
  pinMode(leftStep, OUTPUT);
  // right
  pinMode(rightEn, OUTPUT);
  pinMode(rightDir, OUTPUT);
  pinMode(rightStep, OUTPUT);
  // front
  pinMode(frontEn, OUTPUT);
  pinMode(frontDir, OUTPUT);
  pinMode(frontStep, OUTPUT);
  // back
  pinMode(backEn, OUTPUT);
  pinMode(backDir, OUTPUT);
  pinMode(backStep, OUTPUT);
  // up
  pinMode(upEn, OUTPUT);
  pinMode(upDir, OUTPUT);
  pinMode(upStep, OUTPUT);
  // down
  pinMode(downEn, OUTPUT);
  pinMode(downDir, OUTPUT);
  pinMode(downStep, OUTPUT);

  disableMotors();

  leftServo.attach(leftServoPin);
  rightServo.attach(rightServoPin);
  frontServo.attach(frontServoPin);
  backServo.attach(backServoPin);
  upServo.attach(upServoPin);

  leftServo.write(0);
  rightServo.write(0);
  frontServo.write(0);
  backServo.write(0);
  upServo.write(0);
}


// ============================== LOOP ==============================
void loop() {
  if(Serial.available()) {
    String movements = Serial.readStringUntil('\n');

    for(int i=0; i<movements.length(); i++) {
      char1 = movements.charAt(i);

      if(char1=='1') {
        enableMotors();
      }
      else if(char1=='2') {
        disableMotors();
      }
      else if(char1=='3') {
        hookCube();
      }
      else if(char1=='4') {
        unHookCube();
      }
      else if(i+1<movements.length()) {
        char2 = movements.charAt(i+1);
        if(char2=='2') {
          move(char1, true);
          move(char1, true);
          i++;
        }
        else if(char2=='\'') {
          move(char1, false);
          i++;
        }
        else {
          move(char1, true);
        }
        delay(50);
      }
      else {
        move(char1, true);
        delay(50);
      }
    }
  }
}


// ========================== ENABLE MOTORS =========================
void enableMotors() {
  digitalWrite(leftEn, LOW);
  digitalWrite(rightEn, LOW);
  digitalWrite(frontEn, LOW);
  digitalWrite(backEn, LOW);
  digitalWrite(upEn, LOW);
  digitalWrite(downEn, LOW);
  Serial.println("Motors Enabled");
}


// ========================= DISABLE MOTORS =========================
void disableMotors() {
  digitalWrite(leftEn, HIGH);
  digitalWrite(rightEn, HIGH);
  digitalWrite(frontEn, HIGH);
  digitalWrite(backEn, HIGH);
  digitalWrite(upEn, HIGH);
  digitalWrite(downEn, HIGH);
  Serial.println("Motors Disabled");
}


// =========================== HOOK CUBE ============================
void hookCube() {
  if(pos != 80) {
    for (pos = pos; pos <= 80; pos += 1) {
      // in steps of 1 degree
      leftServo.write(pos);
      rightServo.write(pos);
      frontServo.write(pos);
      backServo.write(pos);
      upServo.write(pos);
      delay(15);
    }
  }
}


// ========================== UNHOOK CUBE ===========================
void unHookCube() {
  if(pos!=0) {
    for (pos = pos; pos >= 0; pos -= 1) {
    // in steps of 1 degree
    leftServo.write(pos);
    rightServo.write(pos);
    frontServo.write(pos);
    backServo.write(pos);
    upServo.write(pos);
    delay(15);
    }
  }
}


// =========================== MOVE MOTOR ===========================
void move(char motor, bool dir) {
  int dirPin, stepPin;

  switch(motor) {
    case 'L':
    dirPin = leftDir;
    stepPin = leftStep;
    break;

    case 'R':
    dirPin = rightDir;
    stepPin = rightStep;
    break;

    case 'F':
    dirPin = frontDir;
    stepPin = frontStep;
    break;

    case 'B':
    dirPin = backDir;
    stepPin = backStep;
    break;

    case 'U':
    dirPin = upDir;
    stepPin = upStep;
    break;

    case 'D':
    dirPin = downDir;
    stepPin = downStep;
    break;
  }

  if(dir) {
    digitalWrite(dirPin, HIGH);
  }
  else {
    digitalWrite(dirPin, LOW);
  }

  for (int i = 0; i < 400; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(speed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(speed);
  }
}

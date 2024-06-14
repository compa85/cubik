#include <Servo.h>


// up motor
const int upEn = 24;
const int upDir = 22;
const int upStep = 23;
// left motor
const int leftEn = 28;
const int leftDir = 26;
const int leftStep = 27;
// front motor
const int frontEn = 32;
const int frontDir = 30;
const int frontStep = 31;
// right motor
const int rightEn = 36;
const int rightDir = 34;
const int rightStep = 35;
// back motor
const int backEn = 40;
const int backDir = 38;
const int backStep = 39;
// down motor
const int downEn = 44;
const int downDir = 42;
const int downStep = 43;

// servo motors
const int upServoPin = 48;
const int leftServoPin = 49;
const int frontServoPin = 50;
const int rightServoPin = 51;
const int backServoPin = 52;

Servo upServo;
Servo leftServo;
Servo frontServo;
Servo rightServo;
Servo backServo;

bool hooked = false;

// servo max positions
const int posServoUp = 45;
const int posServoLeft = 60;
const int posServoFront = 48;
const int posServoRight = 80;
const int posServoBack = 52;

// speed
const int motorSpeed = 200; // delay in microseconds
const int servoSpeed = 15;  // delay in milliseconds

// serial read
bool isReadable = true;
char char1;
char char2;
char char3;


// ============================== SETUP =============================
void setup() {
  Serial.begin(9600);

  // up motor
  pinMode(upEn, OUTPUT);
  pinMode(upDir, OUTPUT);
  pinMode(upStep, OUTPUT);
  // left motor
  pinMode(leftEn, OUTPUT);
  pinMode(leftDir, OUTPUT);
  pinMode(leftStep, OUTPUT);
  // front motor
  pinMode(frontEn, OUTPUT);
  pinMode(frontDir, OUTPUT);
  pinMode(frontStep, OUTPUT);
  // right motor
  pinMode(rightEn, OUTPUT);
  pinMode(rightDir, OUTPUT);
  pinMode(rightStep, OUTPUT);
  // back motor
  pinMode(backEn, OUTPUT);
  pinMode(backDir, OUTPUT);
  pinMode(backStep, OUTPUT);
  // down motor
  pinMode(downEn, OUTPUT);
  pinMode(downDir, OUTPUT);
  pinMode(downStep, OUTPUT);

  // servo motors
  upServo.attach(upServoPin);
  leftServo.attach(leftServoPin);
  frontServo.attach(frontServoPin);
  rightServo.attach(rightServoPin);
  backServo.attach(backServoPin);

  // disable all motors
  disableMotors();
  upServo.write(0);
  leftServo.write(0);
  frontServo.write(0);
  rightServo.write(0);
  backServo.write(0);
}


// ============================== LOOP ==============================
void loop() {
  if (Serial.available()) {
    String movements = Serial.readStringUntil('\n');

    for (int i = 0; i < movements.length(); i++) {
      char1 = movements.charAt(i);

      if (char1 == '1') {
        enableMotors();
      }
      else if (char1 == '2') {
        disableMotors();
      }
      else if (char1 == '3') {
        hookCube();
      }
      else if (char1 == '4') {
        unHookCube();
      }
      else if (i + 1 < movements.length()) {
        char2 = movements.charAt(i + 1);
        if (char2 == '2') {
          move(char1, true);
          move(char1, true);
          i++;
        }
        else if (char2 == '\'') {
          move(char1, false);
          i++;
        }
        else {
          move(char1, true);
        }
        delay(60);
      }
      else {
        move(char1, true);
        delay(60);
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


// =========================== MOVE MOTOR ===========================
void move(char motor, bool dir) {
  int dirPin, stepPin;

  switch (motor) {
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

  if (dir) {
    digitalWrite(dirPin, HIGH);
  }
  else {
    digitalWrite(dirPin, LOW);
  }

  for (int i = 0; i < 400; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(motorSpeed);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(motorSpeed);
  }
}


// =========================== MOVE SERVO ===========================
void moveServo(Servo servo, int pos, int posMax) {
  if (pos > 0 && pos < posMax) {
    servo.write(pos);
  }
}


// =========================== HOOK CUBE ============================
void hookCube() {
  if (!hooked) {
    for (int pos = 0; pos <= 80; pos += 1) {
      moveServo(upServo, pos, posServoUp);
      delay(servoSpeed);
    }

    delay(500);

    for (int pos = 0; pos <= 80; pos += 1) {
      moveServo(leftServo, pos, posServoLeft);
      moveServo(frontServo, pos, posServoFront);
      moveServo(rightServo, pos, posServoRight);
      moveServo(backServo, pos, posServoBack);
      delay(servoSpeed);
    }
  }

  hooked = true;
  Serial.println("Hook");
}


// ========================== UNHOOK CUBE ===========================
void unHookCube() {
  if (hooked) {
    for (int pos = 80; pos >= 0; pos -= 1) {
      moveServo(upServo, pos, posServoUp);
      moveServo(leftServo, pos, posServoLeft);
      moveServo(frontServo, pos, posServoFront);
      moveServo(rightServo, pos, posServoRight);
      moveServo(backServo, pos, posServoBack);
      delay(servoSpeed);
    }
  }

  hooked = false;
  Serial.println("Unhook");
}

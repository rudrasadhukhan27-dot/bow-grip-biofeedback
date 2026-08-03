/*
 * Bench test: verifies all sensor channels and the motor before collection.
 * Prints averaged readings, pulses the motor, and flags common fault
 * signatures on the FSR channels.  Serial Monitor at 115200.
 *
 * Licence: MIT
 */
#include <Wire.h>
#include <MPU6050_tockn.h>

const int FSR1_PIN = 35, FSR2_PIN = 34, EMG_PIN = 32;
const int SDA_PIN = 21, SCL_PIN = 22, MOTOR_PIN = 25;
const int MOTOR_FREQ = 20000, MOTOR_RES = 8;

MPU6050 mpu(Wire);
bool imuOK = false;

void analyze(int pin, int &lo, int &hi, int &avg) {
  const int N = 200;
  long sum = 0; lo = 4095; hi = 0;
  for (int i = 0; i < N; i++) {
    int v = analogRead(pin);
    sum += v;
    if (v < lo) lo = v;
    if (v > hi) hi = v;
    delayMicroseconds(200);
  }
  avg = sum / N;
}

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetPinAttenuation(FSR1_PIN, ADC_11db);
  analogSetPinAttenuation(FSR2_PIN, ADC_11db);
  analogSetPinAttenuation(EMG_PIN,  ADC_11db);
  ledcAttach(MOTOR_PIN, MOTOR_FREQ, MOTOR_RES);
  ledcWrite(MOTOR_PIN, 0);

  Wire.begin(SDA_PIN, SCL_PIN);
  Serial.println("Scanning I2C...");
  for (byte a = 1; a < 127; a++) {
    Wire.beginTransmission(a);
    if (Wire.endTransmission() == 0) {
      Serial.print("  device at 0x"); Serial.println(a, HEX);
      if (a == 0x68) imuOK = true;
    }
  }
  if (imuOK) { mpu.begin(); mpu.calcGyroOffsets(true); Serial.println("MPU6050 OK"); }
  else Serial.println("MPU6050 NOT FOUND - check D21/D22, power, ground");
}

void loop() {
  int l1, h1, a1, l2, h2, a2, le, he, ae;
  analyze(FSR1_PIN, l1, h1, a1);
  analyze(FSR2_PIN, l2, h2, a2);
  analyze(EMG_PIN,  le, he, ae);

  Serial.print("FSR1 avg="); Serial.print(a1);
  Serial.print(" spread="); Serial.print(h1 - l1);
  Serial.print(" | FSR2 avg="); Serial.print(a2);
  Serial.print(" spread="); Serial.print(h2 - l2);
  Serial.print(" | EMG avg="); Serial.print(ae);

  // fault signatures on the primary grip channel
  if (l1 == 0 && h1 >= 4090)  Serial.print("   <-- FSR1 jumping 0<->4095 (loose connection)");
  else if (a1 >= 4090)        Serial.print("   <-- FSR1 railed (floating: check divider)");
  else if (h1 - l1 > 300)     Serial.print("   <-- FSR1 noisy");

  if (imuOK) {
    mpu.update();
    Serial.print(" | accel ");
    Serial.print(mpu.getAccX(), 2); Serial.print("/");
    Serial.print(mpu.getAccY(), 2); Serial.print("/");
    Serial.print(mpu.getAccZ(), 2);
  }
  Serial.println();

  Serial.println(">>> motor ON 1s");
  ledcWrite(MOTOR_PIN, 180);
  delay(1000);
  ledcWrite(MOTOR_PIN, 0);
  delay(2000);
}

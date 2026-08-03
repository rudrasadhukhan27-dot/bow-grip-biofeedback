/*
 * Bow-Grip Biofeedback Wearable - logging + feedback firmware
 *
 * Samples thumb force (FSR), forearm EMG, and hand IMU on a fixed schedule
 * and streams CSV over USB serial at 115200 baud:
 *
 *     t_ms,fsr1,fsr2,emg,ax,ay,az,gx,gy,gz,mode
 *
 * Modes, switched by sending a single character over serial:
 *     'R'  record   - motor disabled (baseline / withdrawal / transfer)
 *     'F'  feedback - motor driven by grip above threshold (intervention)
 *
 * IMPORTANT: GRIP_THRESH and ZONE2_START below must be derived from the
 * individual wearer's own baseline data. The values here are the 85th and
 * 95th percentiles of one participant's baseline grip distribution and are
 * meaningless for anyone else.
 *
 * Requires ESP32 Arduino core 3.x (uses ledcAttach / pin-addressed ledcWrite)
 * and the MPU6050_tockn library (many cheap MPU-6050 modules are clones that
 * fail to initialise with other drivers; note it reports accel in g, not m/s^2).
 *
 * Keep the board still at power-up: the gyroscope calibrates on boot.
 *
 * Licence: MIT
 */

#include <Wire.h>
#include <MPU6050_tockn.h>

// ---- Pin map (all analog inputs on ADC1, safe with radio active) ----
const int FSR1_PIN  = 35;   // thumb force sensor - primary grip signal
const int FSR2_PIN  = 34;   // second FSR channel (unused in this build)
const int EMG_PIN   = 32;   // BioAmp EXG Pill output
const int SDA_PIN   = 21;   // IMU I2C
const int SCL_PIN   = 22;
const int MOTOR_PIN = 25;   // MOSFET gate

const int MOTOR_FREQ = 20000;   // above audible range
const int MOTOR_RES  = 8;       // 8-bit duty (0-255)

MPU6050 mpu(Wire);
bool imuOK = false;
char mode = 'R';                // default to record: motor off

// ---- Feedback curve - PERSONALISE THESE ----
const int GRIP_THRESH = 1301;   // 85th percentile of wearer's baseline grip
const int ZONE2_START = 1584;   // 95th percentile - steeper ramp above this
const int MIN_MOTOR   = 60;     // lowest perceptible duty
const int ZONE1_MAX   = 110;
const int MAX_MOTOR   = 220;

// Two-zone proportional ramp: gentle nudge just above threshold,
// stronger response for pronounced overgrip.
int gripToMotor(int g) {
  if (g <= GRIP_THRESH) return 0;
  if (g <= ZONE2_START) {
    float t = (float)(g - GRIP_THRESH) / (ZONE2_START - GRIP_THRESH);
    return (int)(MIN_MOTOR + t * (ZONE1_MAX - MIN_MOTOR));
  }
  float t = (float)(g - ZONE2_START) / (4095 - ZONE2_START);
  int d = (int)(ZONE1_MAX + t * (MAX_MOTOR - ZONE1_MAX));
  return d > MAX_MOTOR ? MAX_MOTOR : d;
}

unsigned long lastSample = 0;
const unsigned long SAMPLE_US = 10000;   // 100 Hz target

void setup() {
  Serial.begin(115200);   // 230400 produced intermittent row corruption

  analogReadResolution(12);
  analogSetPinAttenuation(FSR1_PIN, ADC_11db);
  analogSetPinAttenuation(FSR2_PIN, ADC_11db);
  analogSetPinAttenuation(EMG_PIN,  ADC_11db);

  ledcAttach(MOTOR_PIN, MOTOR_FREQ, MOTOR_RES);
  ledcWrite(MOTOR_PIN, 0);

  Wire.begin(SDA_PIN, SCL_PIN);
  bool seen = false;
  for (byte a = 1; a < 127; a++) {
    Wire.beginTransmission(a);
    if (Wire.endTransmission() == 0 && a == 0x68) seen = true;
  }
  if (seen) {
    mpu.begin();
    mpu.calcGyroOffsets(false);
    imuOK = true;
  }

  Serial.println("# t_ms,fsr1,fsr2,emg,ax,ay,az,gx,gy,gz,mode");
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == 'R' || c == 'r') { mode = 'R'; ledcWrite(MOTOR_PIN, 0); }
    if (c == 'F' || c == 'f') { mode = 'F'; }
  }

  unsigned long now = micros();
  if (now - lastSample >= SAMPLE_US) {
    lastSample += SAMPLE_US;

    int f1 = analogRead(FSR1_PIN);
    int f2 = analogRead(FSR2_PIN);
    int e  = analogRead(EMG_PIN);

    float ax = 0, ay = 0, az = 0, gx = 0, gy = 0, gz = 0;
    if (imuOK) {
      mpu.update();
      ax = mpu.getAccX();  ay = mpu.getAccY();  az = mpu.getAccZ();
      gx = mpu.getGyroX(); gy = mpu.getGyroY(); gz = mpu.getGyroZ();
    }

    int grip = (f1 > f2) ? f1 : f2;
    ledcWrite(MOTOR_PIN, (mode == 'F') ? gripToMotor(grip) : 0);

    Serial.print(millis()); Serial.print(',');
    Serial.print(f1); Serial.print(','); Serial.print(f2); Serial.print(','); Serial.print(e); Serial.print(',');
    Serial.print(ax, 3); Serial.print(','); Serial.print(ay, 3); Serial.print(','); Serial.print(az, 3); Serial.print(',');
    Serial.print(gx, 2); Serial.print(','); Serial.print(gy, 2); Serial.print(','); Serial.print(gz, 2); Serial.print(',');
    Serial.println(mode);
  }
}

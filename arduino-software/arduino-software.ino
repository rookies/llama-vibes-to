#include <Servo.h>
#include "CommandReader.hh"

const byte pinServo = 9;

void parseCommand(char *);

Servo servo;
CommandReader<50> commandReader(parseCommand);

int targetValue = 0;
int initialValue = 0;
unsigned long initialTime = millis();
unsigned long duration = 1000;

void setup() {
  Serial.begin(9600);
  servo.attach(pinServo);
}

void loop() {
  commandReader.run();

  if (millis() >= initialTime + duration) {
    servo.write(targetValue);
  } else {
    float timeFractionElapsed = float(millis() - initialTime) / duration;
    int newValue = initialValue + ((targetValue - initialValue) * timeFractionElapsed);
    servo.write(newValue);
  }
}

void parseCommand(char *cmd) {
  char *comma = strchr(cmd, ',');
  if (comma) {
    *comma = '\0';
    int cmdValue = atoi(cmd);
    int cmdDuration = atoi(comma + 1);

    if (cmdValue >= 0 && cmdValue <= 180 && cmdDuration > 0 && cmdDuration < 10000) {
      Serial.print("Setting to ");
      Serial.print(cmdValue);
      Serial.print(" after ");
      Serial.print(cmdDuration);
      Serial.println("ms");

      targetValue = cmdValue;
      duration = cmdDuration;
      initialValue = servo.read();
      initialTime = millis();
    } else {
      Serial.println("error");
    }
  } else {
    Serial.println("error");
  }

}

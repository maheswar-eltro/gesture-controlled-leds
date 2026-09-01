int leds[] = {3, 4, 5, 6, 7, 8, 9, 10, 11, 12};

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < 10; i++) {
    pinMode(leds[i], OUTPUT);
  }
}

void loop() {

  if (Serial.available() > 0) {

    int number = Serial.parseInt();

    // Keep number between 0 and 10
    number = constrain(number, 0, 10);

    // Turn ON first 'number' LEDs
    for (int i = 0; i < 10; i++) {

      if (i < number) {
        digitalWrite(leds[i], HIGH);
      } 
      else {
        digitalWrite(leds[i], LOW);
      }
    }
  }
}

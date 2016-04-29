const int ledPin= 13;
const int inputPin= 4;

void setup(){
 pinMode(ledPin, OUTPUT);
 pinMode(inputPin, INPUT);
}

void loop(){
 int value= digitalRead(inputPin);

 if (value == HIGH)
 {
  digitalWrite(ledPin, HIGH);
  delay(60000);
  digitalWrite(ledPin, LOW);
 }
 else
 {
  digitalWrite(ledPin, LOW);
 }
}

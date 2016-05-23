const int ledPin= 13;
const int espPin= 12;
const int inputPin= 4;

void setup(){
 pinMode(ledPin, OUTPUT);
 pinMode(espPin, OUTPUT);
 pinMode(inputPin, INPUT);
}

void loop(){
 int value= digitalRead(inputPin);

 if (value == HIGH)
 {
  digitalWrite(ledPin, HIGH);
  digitalWrite(espPin, HIGH);
  delay(600);
  digitalWrite(ledPin, LOW);
  digitalWrite(espPin, LOW);
 }
 else
 {
  digitalWrite(ledPin, LOW);
  digitalWrite(espPin, LOW);
 }
}

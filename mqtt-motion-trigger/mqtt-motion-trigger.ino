
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

const char* ssid = "openhardware";
const char* password = "iotecuador";
const char* mqtt_server = "test.mosquitto.org";
const int movimiento = 0;
const int triggerPin = 4;

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
int lastValue = 0;

void setup() {
  pinMode(BUILTIN_LED, OUTPUT);
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {

  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);
  } else {
    digitalWrite(BUILTIN_LED, HIGH);
  }

}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      //client.publish("iotTW", "IoT Welcome");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void loop() {
  int valor = digitalRead(triggerPin);
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  char* message;
  if (valor != lastValue) {
    Serial.println("");
    if(valor == movimiento){
      Serial.println("Hay movimiento");
      message = "{\"presence\": true}";
    }else {
      Serial.println("NO hay movimiento");
      message = "{\"presence\": false}";
    }
    Serial.println(message);
    client.publish("iotTW", message);
    lastValue = valor;
  }
  delay(1000);
}

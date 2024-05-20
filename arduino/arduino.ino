#include <DHT.h>
#include <Servo.h>

#define DHTPIN 2     // Pin connected to the DHT22 sensor
#define DHTTYPE DHT22   // DHT 22 (AM2302) sensor type
#define SOIL_MOIST_SENSOR A0
#define LDR_SENSOR A1
#define SERVO_MOTOR A2
#define LED_PIN 8
#define BUZZER_PIN 7

DHT dht(DHTPIN, DHTTYPE);
Servo servoBase;
int actuator_status;

int activate_servo(int second){
  servoBase.write(22);
  delay(second*1000);
  servoBase.write(0); 
}

void setup() {
  Serial.begin(9600); 
  pinMode(SOIL_MOIST_SENSOR, INPUT);
  servoBase.attach(SERVO_MOTOR);
  servoBase.write(0);
  dht.begin();
}

void mouse_detected(int status){
  if(status == 1){
    for(int i=0; i<2;i++){
      digitalWrite(LED_PIN, HIGH);
      tone(BUZZER_PIN, 400 , 200);
      delay(150);
      noTone(BUZZER_PIN);
      delay(400);
      digitalWrite(LED_PIN, LOW);
    }
  } else {
    digitalWrite(LED_PIN, LOW);
  }
 
}

void water_trigger(int second){
  if(second <= 99){
    actuator_status = 1;
    activate_servo(second);
  } 
}

void loop() {
  delay(500);  

  // Membaca nilai sensor
  int moist_value = analogRead(SOIL_MOIST_SENSOR); 
  int light_intensity = analogRead(LDR_SENSOR);
  float moisture_percentage = (moist_value/1023.00) * 100 ;
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  // Membaca data dari papan pengembang lainnya
  // Jikalau disediakan dua byte data, maka data tersebut merupakan lama penyiraman dalam detik
  // Jikalau data berukuran satu byte, maka data tersebut merupakan status apakah terdeteksi tikus
  if (Serial.available() >= 2) {
    int second = Serial.read() << 8 | Serial.read();
    water_trigger(second);
  } else {
    int status = Serial.read();
    mouse_detected(status);
  }
  
  // Kondisi untuk penyiraman (menggerakan microservo)
  if(moisture_percentage < 85 && light_intensity > 20 && temperature > 24 && humidity < 55){
    water_trigger(1);
  } else {
    actuator_status= 0;
    digitalWrite(LED_PIN, LOW);
  }
  // Mencetak hasil pengukuran sehingga dapat dibaca dari papan pengembang lainnya
  String result = String(humidity) + ',' + String(temperature) + ',' + String(moisture_percentage) + ',' + String(light_intensity) + ',' + String(actuator_status);
  Serial.println(result);

}

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
Servo servoBase;//Asigno un nombre específico
int actuator_status;

int activate_servo(int second){
   for(int i=0; i<second;i++){
    servoBase.write(0);
    delay(600);
    servoBase.write(180);
    delay(400);
  }
}

void setup() {
  Serial.begin(9600); 
  pinMode(SOIL_MOIST_SENSOR, INPUT);
  servoBase.attach(SERVO_MOTOR);//Pin a utilizar para servo
  servoBase.write(50);
  dht.begin();
}

void activate_buzzer(int status){
  if(status == 1){
    for(int i=0; i<2;i++){
      tone(BUZZER_PIN, 400 , 200);
      delay(150);
      noTone(BUZZER_PIN);
      delay(400);
    }
  }
 
}

void triggered(int second){
  if(second < 99){
    actuator_status = 1;
    digitalWrite(LED_PIN, HIGH);
    activate_servo(second);
  } 
  // else {
  //   activate_buzzer(); 
  // }
}

void loop() {
  delay(100);  // Delay between sensor readings
  int moist_value = analogRead(SOIL_MOIST_SENSOR); 
  int light_intensity = analogRead(LDR_SENSOR);
  float moisture_percentage = (moist_value/1023.00) * 100 ;
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  if (Serial.available() >= 2) {
    int second = Serial.read() << 8 | Serial.read();
    triggered(second);
  } else {
    int status = Serial.read();
    activate_buzzer(status);
  }
  
  if(moisture_percentage < 75 && light_intensity > 30){
    triggered(1);
  } else {
    actuator_status= 0;
    digitalWrite(LED_PIN, LOW);
  }
  String result = String(humidity) + ',' + String(temperature) + ',' + String(moisture_percentage) + ',' + String(light_intensity) + ',' + String(actuator_status);
  Serial.println(result);

}

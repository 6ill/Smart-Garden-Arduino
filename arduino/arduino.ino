#include <DHT.h>
#include <Servo.h>

#define DHTPIN 2     // Pin connected to the DHT22 sensor
#define DHTTYPE DHT22   // DHT 22 (AM2302) sensor type
#define SOIL_MOIST_SENSOR A0
#define LDR_SENSOR A1
#define SERVO_MOTOR A2

DHT dht(DHTPIN, DHTTYPE);
Servo servoBase;//Asigno un nombre específico

int activate_servo(){
  servoBase.write(0);
  delay(500);
  servoBase.write(180);
}

void setup() {
  Serial.begin(9600);
  pinMode(SOIL_MOIST_SENSOR, INPUT);
  servoBase.attach(SERVO_MOTOR);//Pin a utilizar para servo
  servoBase.write(50);
  dht.begin();
}

void loop() {
  delay(1000);  // Delay between sensor readings
  int moist_value = analogRead(SOIL_MOIST_SENSOR); 
  int light_intensity = analogRead(LDR_SENSOR);
  float moisture_percentage = (moist_value/1023.00) * 100 ;
  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
  int servo_status = 0;
  if(moisture_percentage < 75 && light_intensity > 30){
    activate_servo();
    servo_status = 1;
  }
  String result = String(humidity) + ',' + String(temperature) + ',' + String(moisture_percentage) + ',' + String(light_intensity) + ',' + String(servo_status);
  Serial.println(result);

}

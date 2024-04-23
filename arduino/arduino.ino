#include <DHT.h>

#define DHTPIN 2     // Pin connected to the DHT22 sensor
#define DHTTYPE DHT22   // DHT 22 (AM2302) sensor type

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(2000);  // Delay between sensor readings

  float humidity = dht.readHumidity();
  float temperature = dht.readTemperature();

  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }

  Serial.print(humidity);
  Serial.print(",");
  Serial.println(temperature);
}

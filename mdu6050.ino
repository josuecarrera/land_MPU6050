// Incluir la librería Adafruit MPU6050
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

// Crear un objeto sensor
Adafruit_MPU6050 mpu;

// Definir los umbrales de movimiento para cada tipo de suelo
// Estos valores se pueden ajustar según la necesidad
#define UMBRAL_FIRME 181 // Aceleración máxima en m/s^2 para suelo firme
#define UMBRAL_BLANDO 905 // Aceleración máxima en m/s^2 para suelo blando
#define UMBRAL_LIQUIDO 1810 // Aceleración máxima en m/s^2 para suelo líquido


// Definir una variable para almacenar el tipo de suelo
String tipo_suelo = "";

void setup(void) {
  Serial.begin(115200);
  // Esperar a que el puerto serie esté disponible
  while (!Serial)
    delay(10);

  Serial.println("Iniciando el sensor MPU6050");

  // Inicializar el sensor con los valores por defecto
  if (!mpu.begin()) {
    Serial.println("No se pudo encontrar el sensor MPU6050, comprueba las conexiones!");
    while (1)
      delay(10);
  }

  // Establecer el rango del acelerómetro a +/- 4G
  mpu.setAccelerometerRange(MPU6050_RANGE_4_G);

  // Establecer el rango del giroscopio a +/- 250 grados/segundo
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);

  // Establecer el filtro pasa-bajos a 5 Hz
  mpu.setFilterBandwidth(MPU6050_BAND_5_HZ);

  // Imprimir los valores actuales del sensor
  Serial.println("Valores del sensor:");
  Serial.print("Rango del acelerómetro = ");
  Serial.print(mpu.getAccelerometerRange());
  Serial.println("G");
  Serial.print("Rango del giroscopio = ");
  Serial.print(mpu.getGyroRange());
  Serial.println("grados/segundo");
  Serial.print("Filtro pasa-bajos = ");
  Serial.print(mpu.getFilterBandwidth());
  Serial.println("Hz");
}

void loop() {
  
  // Leer los datos del sensor
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp);

  // Calcular la magnitud de la aceleración en m/s^2
  float magnitud = sqrt(a.acceleration.x * a.acceleration.x + 
                        a.acceleration.y * a.acceleration.y + 
                        a.acceleration.z * a.acceleration.z);

  // Clasificar el tipo de suelo según la magnitud de la aceleración
  if (magnitud < UMBRAL_FIRME) {
    tipo_suelo = "Firme";
  }
  else if (magnitud < UMBRAL_BLANDO) {
    tipo_suelo = "Blando";
  }
  else if (magnitud < UMBRAL_LIQUIDO) {
    tipo_suelo = "Líquido";
  }
  
  // Imprimir los datos del sensor y el tipo de suelo en el monitor serie
  Serial.print("Aceleración: X=");
  Serial.print(a.acceleration.x);
  Serial.print(", Y=");
  Serial.print(a.acceleration.y);
  Serial.print(", Z=");
  Serial.print(a.acceleration.z);
  
   Serial.print(", Magnitud=");
   Serial.print(magnitud);
   Serial.print(", Tipo de suelo=");
   Serial.println(tipo_suelo);

   // Esperar un segundo entre lecturas
   delay(1000);
}
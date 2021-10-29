/* Modern Device Wind Sensor Sketch for Rev C Wind Sensor
  This sketch is only valid if the wind sensor if powered from
  a regulated 5 volt supply.

  Hardware Setup:
  Wind Sensor Signals    Arduino
  GND                    GND
  +V                     5V
  RV                     A1    // modify the definitions below to use other pins
  TMP                    A0    // modify the definitions below to use other pins
*/

#include <SPI.h>
#include <SD.h>

#define LED_PIN 2
#define LED_COUNT 4
#define analogPinForRV    1
#define analogPinForTMP   0
#define potentiometer_analog 3 // sets up a pin for the analog value of the potentiometer to go into
#define calibrate_button 12
#define calibrate_indicator 9

const float zeroWindAdjustment =  0.2; // negative numbers yield smaller wind speeds and vice versa.

float TMP_Therm_ADunits;  //temp termistor value from wind sensor
float RV_Wind_ADunits;    //RV output from wind sensor
float RV_Wind_Volts;
unsigned long lastMillis;
float TempCtimes100;
float TempC;
float zeroWind_ADunits;
float zeroWind_volts;
float WindSpeed_MPH;

float avg_WindSpeed_MPH = 0;
float temps_total = 0;
float speed_total = 0;
float count = 0;
float nowtime = 0;
float starttime;
float avg_temp = 15.0;
float avg_speed = 10.0;
int flag = 0;
float max_speed_total = 0;
float nowtime_max;
float count_max = 0;
float avg_max;
float max_speed_total_in = 0;
float nowtime_max_in;
float count_max_in = 0;
float avg_max_in;
float overall_out = 0;
float overall_in = 0;
float avg_overall_max = 25.0;
float avg_overall_max_in = 25.0;

float num_levels = 5.0;
float range_in = 1.0;
float range_out = 1.0;
int value;


void setup() {
  //  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);

  while (!Serial) {
    ; // wait for serial port to connect. Needed for native USB port only
  }
  pinMode(calibrate_button, INPUT);
  pinMode(calibrate_indicator, OUTPUT);
}

void loop() {
  WindSpeed_MPH, TempC = measure();

  if (digitalRead(calibrate_button)) {
    avg_temp, avg_speed, avg_overall_max, avg_overall_max_in = calibrate();
    //    Serial.println("calibrate");
  }

  //  Serial.println(WindSpeed_MPH);
  //  Serial.println(TempC);

  value = levels(WindSpeed_MPH, avg_temp, avg_speed, avg_overall_max, avg_overall_max_in, num_levels);
  Serial.println(value);

  delay(500);

  //    Serial.println(1);
  //    delay(500);
}


float measure() {
  //      if (isnan(WindSpeed_MPH)) {
  //      WindSpeed_MPH = 0;
  //    }

  TMP_Therm_ADunits = analogRead(analogPinForTMP);
  RV_Wind_ADunits = analogRead(analogPinForRV);
  RV_Wind_Volts = (RV_Wind_ADunits *  0.0048828125); //Converts to voltage ((5.0/1023.0) * float(RV_Wind_ADunits);)

  TempCtimes100 = (0.005 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits)) - (16.862 * (float)TMP_Therm_ADunits) + 9075.4;
  TempC = TempCtimes100 / 100.0;
  zeroWind_ADunits = -0.0006 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits) + 1.0727 * (float)TMP_Therm_ADunits + 47.172; //  13.0C  553  482.39
  zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment;
  WindSpeed_MPH =  pow(((RV_Wind_Volts - zeroWind_volts) / .2300) , 2.7265);
  return WindSpeed_MPH, TempC;
}

float calibrate() {
  flag = 1;
  starttime = millis();
  Serial.println(400);
  //  Serial.println(starttime);
  while (flag == 1) {
    digitalWrite(calibrate_indicator, HIGH);
    WindSpeed_MPH, TempC = measure();
    //    Serial.println(WindSpeed_MPH);
    //    Serial.println(TempC);
    temps_total += TempC;
    speed_total += WindSpeed_MPH;
    count += 1.0;
    nowtime = millis();
    if ((nowtime - starttime) >= (5000)) {
      avg_temp = temps_total / count;
      avg_speed = speed_total / count;
      count = 0;
      temps_total = 0;
      flag = 0;
      for (int i = 0; i < 3; i++) { //Bad because repeatedly uses same wind_speed paramater throughout entire for loop
        Serial.println(500);
        delay(3000);
        WindSpeed_MPH, TempC = measure();
        //        Serial.println(WindSpeed_MPH);
        max_speed_total += WindSpeed_MPH;
        count_max += 1.0;
        //        Serial.println(max_speed_total);
        //        Serial.println(count_max);

        Serial.println(600);
        delay(3000);
        WindSpeed_MPH, TempC = measure();
        //        Serial.println(WindSpeed_MPH);
        max_speed_total_in += WindSpeed_MPH;
        count_max_in += 1.0;
        //        Serial.println(max_speed_total);
        //        Serial.println(count_max_in);

      }
      avg_overall_max = max_speed_total / count_max;
      avg_overall_max_in = max_speed_total_in / count_max_in;
      //      overall_out += avg_max;
      //      overall_in += avg_max_in;
    }
  }
  //  avg_overall_max = overall_out / 3.0;
  //  avg_overall_max_in = overall_in / 3.0;
  //  Serial.println(avg_overall_max);
  //  Serial.println(avg_overall_max_in);
  Serial.println(700);
  digitalWrite(calibrate_indicator, LOW);
  return avg_temp, avg_speed, avg_overall_max, avg_overall_max_in;
}

int levels(float WindSpeed_MPH, float avg_temp, float avg_speed, float avg_overall_max, float avg_overall_max_in, float num_levels) {
  //  Serial.println(WindSpeed_MPH);


  WindSpeed_MPH, TempC = measure();
  //
  //  Serial.println(WindSpeed_MPH);
  //  Serial.println(TempC);

  if (WindSpeed_MPH > avg_speed && TempC <= avg_temp) { //breathing in
    range_in = (avg_overall_max_in - avg_speed) / num_levels;
    value = WindSpeed_MPH / range_in;
  }
  else if (WindSpeed_MPH > avg_speed && TempC >= avg_temp) { //breathing out
    //    WindSpeed_MPH = (-1 * WindSpeed_MPH);
    range_out = (avg_overall_max - avg_speed) / num_levels;
    value = -WindSpeed_MPH / range_out;
  }
  else if (WindSpeed_MPH < avg_speed) {
    value = 0;
  }
  //  Serial.println(value);
  return value;
}

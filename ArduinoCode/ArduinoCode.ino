/* Modern Device Wind Sensor Sketch for Rev C Wind Sensor
  This sketch is only valid if the wind sensor if powered from
  a regulated 5 volt supply.

  Hardware Setup:
  Arduino                Nano Every
  Wind Sensor Signals    Modern Device Wind Sensor Rev C
  GND                    GND
  +V                     5V
  RV                     A1
  TMP                    A0
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
#define zeroWindAdjustment 0.2 // negative numbers yield smaller wind speeds and vice versa.
#define voltage 5.0
#define bit_depth 1023.0
#define ambient_delay 5000 //[milliseconds]
#define max_delay 3000 //[milliseconds]
#define num_levels 5
#define wait_code 400
#define exhale_code 500
#define inhale_code 600
#define calibration_over_code 700

float WindSpeed_MPH;
float TempC;
float avg_temp = 15.0;
float avg_speed = 10.0;
float avg_overall_max_out = 25.0;
float avg_overall_max_in = 25.0;
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
  /* Measure windspeed and temperature, listen for activation of calibration button, and Serial print value

    This function calls the measure(), calibrate(), and levels() functions in order to run the full code.
    After running this, it Serial prints the "level" (-5 to 5) every 0.5 seconds.
  */
  WindSpeed_MPH, TempC = measure();

  if (digitalRead(calibrate_button)) {
    avg_temp, avg_speed, avg_overall_max_out, avg_overall_max_in = calibrate();
  }

  value = levels(avg_temp, avg_speed, avg_overall_max_out, avg_overall_max_in);
  Serial.println(value);

  delay(500);
}


float measure() {
  /* Read and convert windspeed and temperature from analog inputs of sensor

     This function analog reads the current windspeed and temperature and uses a series of empirically
     derived relationships to convert both windspeed to units of miles per hour and temperature to
     degrees Celsius.

     :returns: float containing windspeed in miles per hour
     :returns: float containing temperature in Celsius
  */
  float TMP_Therm_ADunits;  //temp termistor value from wind sensor
  float RV_Wind_ADunits;    //RV output from wind sensor
  float RV_Wind_Volts;
  float TempCtimes100;
  float TempC;
  float zeroWind_ADunits;
  float zeroWind_volts;

  TMP_Therm_ADunits = analogRead(analogPinForTMP);
  RV_Wind_ADunits = analogRead(analogPinForRV);
  RV_Wind_Volts = (RV_Wind_ADunits *  (voltage / bit_depth)); //Converts to voltage

  TempCtimes100 = (0.005 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits)) - (16.862 * (float)TMP_Therm_ADunits) + 9075.4;
  TempC = TempCtimes100 / 100.0;
  zeroWind_ADunits = -0.0006 * ((float)TMP_Therm_ADunits * (float)TMP_Therm_ADunits) + 1.0727 * (float)TMP_Therm_ADunits + 47.172; //  13.0C  553  482.39
  zeroWind_volts = (zeroWind_ADunits * 0.0048828125) - zeroWindAdjustment;
  WindSpeed_MPH =  pow(((RV_Wind_Volts - zeroWind_volts) / .2300) , 2.7265);
  return WindSpeed_MPH, TempC;
}

float calibrate() {
  /*
     Measure the ambient temperature and windspeed and the patient's maximum inhale and exhale windspeeds.

     This function is called when the calibration button is pressed on the device. Once the function begins,
     it outputs the wait_code to the Serial monitor, which is interpretted by the computer interface and
     tells the user to "wait." During this waiting period, it measures the ambient temperature and windspeed
     for the delay time specific by ambient_delay. Then, it sends alternating codes for exhale and inhale to
     the Serial monitor, which the user interface interprets, telling the user to breathe out and in as hard
     as possible for the delay time specifed by max_delay. During each of these delays, it measures windspeed,
     doing this 3 times in total and then averaging the values. It the outputs the average ambient temperature
     and windspeed and the maximum inhale and exhale windspeeds.

     :returns: float containing average ambient windspeed
     :returns: float containing average ambient temperature
     :returns: float containing average maximum exhale windspeed
     :returns: float containing average maximum inhale windspeed
  */
  float temps_total = 0;
  float speed_total = 0;
  int count = 0;
  float nowtime;
  float starttime;
  int flag = 0;
  float max_speed_total = 0.0;
  int count_max = 0;
  float avg_max;
  float max_speed_total_in = 0;
  int count_max_in = 0;

  flag = 1;
  starttime = millis();
  Serial.println(wait_code);
  while (flag == 1) { //ambient temp/speed calibration
    digitalWrite(calibrate_indicator, HIGH);
    WindSpeed_MPH, TempC = measure();
    temps_total += TempC;
    speed_total += WindSpeed_MPH;
    count += 1;
    nowtime = millis();
    if ((nowtime - starttime) >= (ambient_delay)) {
      avg_temp = temps_total / float(count);
      avg_speed = speed_total / float(count);
      count = 0;
      temps_total = 0;
      flag = 0;
      for (int i = 0; i < 3; i++) {
        Serial.println(exhale_code); //max exhale speed calibration
        delay(max_delay);
        WindSpeed_MPH, TempC = measure();
        max_speed_total += WindSpeed_MPH;
        count_max += 1;

        Serial.println(inhale_code); //max inhale speed calibration
        delay(max_delay);
        WindSpeed_MPH, TempC = measure();
        max_speed_total_in += WindSpeed_MPH;
        count_max_in += 1;

      }
      avg_overall_max_out = max_speed_total / float(count_max);
      avg_overall_max_in = max_speed_total_in / float(count_max_in);
    }
  }
  Serial.println(calibration_over_code);
  digitalWrite(calibrate_indicator, LOW);
  return avg_temp, avg_speed, avg_overall_max_out, avg_overall_max_in;
}

int levels(float avg_temp, float avg_speed, float avg_overall_max_out, float avg_overall_max_in) {
  /*
    Calculate the level of the patient's breath based on windspeed as compared to average and maximum
    windspeeds

    This function measures the patient's current windspeed and temperature, and then sorts the breaths
    into inhales or exhales. Inhales occur when the temperature of the breath is below the ambient
    temperature, and exhales occur when the temperature of the breath is above the ambient temperature.
    Once the breaths are sorted, the range of each of the five levels is determined by calculating
    the difference between maximum windspeed and ambient windspeed and dividing by the number of levels,
    5. Then, the specific level for the current breath is calculated by dividing the current speed by the
    range previously calculated. If it is an inhale, the level is positive. If it is an exhale, the level
    is negative. If there is no breath (the current windspeed is lower than the ambient speed), the level
    is zero.

    :param avg_temp: float containing the ambient temperature in Celsius
    :param avg_speed: float containing the ambient windspeed in miles per hour
    :param avg_overal_max_out: float containing average maximum exhale windspeed
    :param avg_overal_max_in: float containing average maximum inhale windspeed
    :param num_levels: int containing the total number of levels (usually 5)
  */

  float range_in = 1.0;
  float range_out = 1.0;

  WindSpeed_MPH, TempC = measure();

  if (WindSpeed_MPH > avg_speed && TempC <= avg_temp) { //breathing in
    range_in = (avg_overall_max_in - avg_speed) / float(num_levels);
    value = WindSpeed_MPH / range_in;
  }
  else if (WindSpeed_MPH > avg_speed && TempC >= avg_temp) { //breathing out
    range_out = (avg_overall_max_out - avg_speed) / float(num_levels);
    value = -WindSpeed_MPH / range_out;
  }
  else if (WindSpeed_MPH < avg_speed) {
    value = 0;
  }
  return value;
}

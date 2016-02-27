/******************************************************************************/
/*macro definitions of Rotary angle sensor and LED pin*/
#define ROTARY_ANGLE_SENSOR A0
#define ADC_REF 5
#define GROVE_VCC 5//VCC of the grove interface is normally 5v
#define FULL_ANGLE 300//full value of the rotary angle is 300 degrees
void setup()
{
  Serial.begin(19200);
  pinsInit();
}

void loop()
{
  int degrees;
  degrees = getDegree();
  Serial.println(degrees);
  delay(10);
}
void pinsInit()
{
  pinMode(ROTARY_ANGLE_SENSOR, INPUT);
}

/************************************************************************/
/*Function: Get the angle between the mark and the starting position  */
/*Parameter:-void                           */
/*Return: -int,the range of degrees is 0~300              */
int getDegree()
{
  int sensor_value = analogRead(ROTARY_ANGLE_SENSOR);
  float voltage;
  voltage = (float)sensor_value*ADC_REF/1023;
  float degrees = (voltage*FULL_ANGLE)/GROVE_VCC;
  return degrees;
}

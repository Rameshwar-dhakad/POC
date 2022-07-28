#include <Servo.h> // include servo library to use its related functions
#define Servo_PWM 5 // A descriptive name for D6 pin of Arduino to provide PWM signal
#define pi 3.142
Servo MG995_Servo;  // Define an instance of of Servo with the name of "MG995_Servo"
  

void setup() {
  Serial.begin(9600); // Initialize UART with 9600 Baud rate
  MG995_Servo.attach(Servo_PWM);  // Connect D6 of Arduino with PWM signal pin of servo motor
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() 
{
  if (Serial.available()>0)
  {
    char action=Serial.read();
    if (action=='s')
    {
       byte data[6];
       Serial.readBytes(data, 6); //reading the buffer on serial monitor
       int input=data[0];
       float offset=data[1];
       float amplitude=data[2];
       float TP=(data[3])*1000;
       int duty_cycle=data[4];
       int Total_cycles=data[5];
       
      if (input==1)
      {
        sine( offset,amplitude,TP,Total_cycles); 
      }
      else if(input==2)
      {
        saw_tooth(offset,amplitude,TP,Total_cycles); 
      }
      else if(input==3)
      {
        linear(offset,amplitude,TP,Total_cycles); 
      }
      else if (input==4) //rectangular function
      {
        
       rectangular(offset,amplitude,TP,duty_cycle,Total_cycles );
        
      }
      exit(0);
    }
    else if (action=='p')
    {
      pause();
      
    }
    else if (action=='e')
    {
      exit(0);
    }
  }
     
 
}

// Rectangular waveform
void rectangular(float offset,float amplitude,float TP,int duty_cycle,int Total_cycles)
{    
     while (Total_cycles>0)
     {   
         if (Serial.available()>0)  // checking for pause and exit interrupt
         {
          char x= Serial.read();
          if (x=='p')
          {
            pause();
          }
          else if (x=='e')
          {
            exit(0);
          }
         }
         MG995_Servo.write(amplitude);
         float t1=duty_cycle*TP/100;
         delay(t1);
         MG995_Servo.write(offset);
         float t2=((100-duty_cycle)*TP/100);
         delay(t2);
         Total_cycles-=1;
     }
     
}

// Triangular waveform
void saw_tooth(float offset,float amplitude,float TP,int Total_cycles)
{
  while (Total_cycles>0)
  {
    
    int delta=10;
    for (int t=0; t<(TP/2);t+=delta)
    {
      if (Serial.available()>0)  // checking for pause and exit interrupt
         {
          char x= Serial.read();
          if (x=='p')
          {
            pause();
          }
          else if (x=='e')
          {
            exit(0);
          }
         }
      MG995_Servo.write(offset+(2*t*amplitude/TP));
      delay(delta);
    }
    for (int t=0; t<(TP/2);t+=delta)
    {
      if (Serial.available()>0)  // checking for pause and exit interrupt
         {
          char x= Serial.read();
          if (x=='p')
          {
            pause();
          }
          else if (x=='e')
          {
            exit(0);
          }
         }
      MG995_Servo.write(amplitude-offset-(2*t*amplitude/TP));
      delay(delta);
    }
    Total_cycles-=1;
  }
  
}


// Linear waveform
void linear(float offset,float amplitude,float TP,int Total_cycles)
{  
  
    while(Total_cycles>0)
    {
      
      int delta=100;
      for (int t=0; t<TP;t+=delta)
      {
        if (Serial.available()>0)  // checking for pause and exit interrupt
         {
          char x= Serial.read();
          if (x=='p')
          {
            pause();
          }
          else if (x=='e')
          {
            exit(0);
          }
         }
        float angle=offset+(t*amplitude/TP);
        MG995_Servo.write(angle);
        delay(delta);
      }
      MG995_Servo.write(offset);
      Total_cycles-=1;
    }
}


// Sinusodial waveform 
void sine(float offset,float amplitude,float TP,int Total_cycles)
{
  while (Total_cycles>0)
  {
    
    int delta=10;
    for (int t=0; t<TP; t+=delta)
      {
      if (Serial.available()>0)  // checking for pause and exit interrupt
         {
          char x= Serial.read();
          if (x=='p')
          {
            pause();
          }
          else if (x=='e')
          {
            exit(0);
          }
         } 
      MG995_Servo.write(offset+amplitude*(sin(t*pi/TP)));
      delay(delta);
      }
    Total_cycles-=1;
  }
}
// pause function for interrupt
void pause()
{
  while(1)
  {
    if (Serial.available()>0)
         {
          char x= Serial.read();
          if (x=='s')
          {
            break;
          }
          else if (x=='e')
          {
            exit(0);
          }
         }
  }
}

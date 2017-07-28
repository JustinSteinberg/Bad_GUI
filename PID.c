/*
  Blank Simple Project.c
  http://learn.parallax.com/propeller-c-tutorials 
*/

#include "simpletools.h"    
#include "time.h"                                         

void adder(void *par);

static int stack[256];

volatile int TicSumLeft;                     //Total sum of ticks for motors 
volatile int TicSumRight;
volatile float diff; 
                                             //Time code runs 
volatile float ticsPerSecR;
volatile float ticsPerSecL; 

int flag = 0;                      

int main()                                   // Main function
{
  pwm_start(1000);
  
  cogstart(adder, NULL, stack, sizeof(stack));  
  
 float errorTotalL;
 float errorTotalR;
 float lastErrorL;
 float lastErrorR;
 float proportionL;
 float proportionR;
 float integralL;
 float integralR;
 float derivativeL;
 float derivativeR;
 float x;
 float integralActiveZone = 10.0; 
 float kd = 0.65;
 float kp = 17.0;
 float ki = 1.25;
 int maxValue = 900;
 float currentL;
 float currentR;
 int powerL = 0;
 int powerR = 0;
 
 print("Enter desired speed (m/s): ");
 scan("%f\n",&x);
 
  while(1)
  {  
   if (flag == 1)
   {
    float Meters_Per_SecL=(500*((ticsPerSecL/36))/1000);
    float Meters_Per_SecR=(500*((ticsPerSecR/36))/1000);  
    float errorL = x - Meters_Per_SecL; 
    float errorR = x - Meters_Per_SecR;
    
    if (errorL < integralActiveZone && errorL != 0)
    {
     errorTotalL += errorL;
    }  
    else
    {
      errorTotalL = 0;
    }
   
    if (errorR < integralActiveZone && errorR != 0)
    {
      errorTotalR += errorR;
    }
    else
    {
      errorTotalR = 0;
    }
   
    if(errorTotalL > 10/ki) //Cap off error at 10
    {
      errorTotalL = 10/ki;
    }
    
    if(errorTotalR > 10/ki)
    {
      errorTotalR = 10/ki;  
    }
  
    proportionL = errorL * kp;
    proportionR = errorR * kp;
    integralL = errorTotalL *ki;
    integralR = errorTotalR *ki;
    derivativeL = (errorL - lastErrorL) * kd;  //(rate of change of error)
    derivativeR = (errorR - lastErrorR) * kd;
    lastErrorL = errorL;
    lastErrorR = errorR;
    
    currentL = proportionL + integralL + derivativeL; //(power sent to motors)
    currentR = proportionR + integralR + derivativeR;
    
    powerL += (int)currentL;
    powerR += (int)currentR;

    if(powerL > maxValue) 
    {
     powerL = maxValue;
    }  
    
    if(powerR > maxValue)
    {
      powerR = maxValue;
    }  
    
    if(powerL < 0)
    {
      powerL = 0;
    }  
    
    if(powerR < 0)
    {
      powerR = 0;
    }  
    
  
    pwm_set(0,1,powerR);
    pwm_set(1,0,powerL);
    
    pause(100);
    
    putChar(HOME);
        
    print("\nPower L: %d Power R: %d\n",powerL,powerR);
    
    print("Left Tic_Sum  = %d Right Tic_Sum  = %d\n",TicSumLeft,TicSumRight);
    
    print("Error_L = %f Error_R = %f\n", errorL,errorR);
    
    print("Speed_L: %f Speed_R: %f\n",Meters_Per_SecL,Meters_Per_SecR);
    
    print("Time: %f\n",diff);
   
    print("Left Tics/Sec: %f Right Tics/Sec: %f\n",ticsPerSecL,ticsPerSecR);


    }    
  
      flag = 0;
  }  
}  
  
/////////////////////////////////////////////////////////////////////////////////////
  
  void adder(void *par) 
 {   
  clock_t launch = clock();                      //Wheel Circumfrence 500mm
  
  int prev_output1 = 0;
  int prev_output3 = 0; 
  
  int i = 0;
  
   while (1)
   {
    
      int output1 = input(14);
      int output2 = input(15);
      int output3 = input(16);
      int output4 = input(17);
      
      
      if (prev_output1 == 0 && output1 == 1)  
      {
        TicSumRight++;
      }
      
      prev_output1 = output1;

      
      if(prev_output3 == 0 && output3 == 1)
      {
        TicSumLeft++;
      }     
      
      prev_output3 = output3;
            
      pause(1);   //Loop every one millisec


     if(i==50) 
     {
      flag = 1;
      clock_t done = clock();
      diff = (float)(done - launch) / CLOCKS_PER_SEC;  
      ticsPerSecR = ((float)TicSumRight)/diff;
      ticsPerSecL = ((float)TicSumLeft)/diff;
      i=0;
      launch = clock();
      TicSumRight = 0;
      TicSumLeft = 0;
     }   
   
   i++;
  } 
     
 }


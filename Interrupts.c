/*
  Blank Simple Project.c
  http://learn.parallax.com/propeller-c-tutorials 
*/
#include "simpletools.h"
#include "stdbool.h"                     
void high();
void low();
volatile unsigned long pwm_value = 0; 
volatile unsigned long prev_time = 0;
int pin1 = 1; 

int main()                                    // Main function
{
  if(input(pin1) == 1)
  {
    waitpeq(1,1);                //wait pin0 to high 
    cog_run(high, 128);
  }     
} 

void high()
{
  while(1)
  {
    waitpne(1,1);             //wait pin0 to low
    cog_run(low, 128)
    
  }  
}

void low()
{
  while(1)
  {
    waitpeq(1,1);   
    cog_run(high, 128)
    
  }  
}

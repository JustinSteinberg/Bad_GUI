/*
  Blank Simple Project.c
  http://learn.parallax.com/propeller-c-tutorials 
*/
#include "simpletools.h"                      // Include simple tools
#include "arlodrive.h"

void adder(void *par);

unsigned int safetyOverrideStack[128];

volatile int safeToProceed = 0;
volatile int check = 0;
int pin = 2; 
long x = 0;

int main()                                    // Main function
{
  
  set_io_timeout(CLKFREQ/1);
  set_io_dt(CLKFREQ/1000000);
  set_direction(pin, 1);
  
  cogstart(adder, NULL, safetyOverrideStack, sizeof(safetyOverrideStack));

  while(1)
  {
    x = pulse_in(pin, 1); 
    print("%d\n",x);
    
    if(x == 23)
    {
     safeToProceed = 1;
    }  
    else if(x <= 100)
    {
      safeToProceed = 0;
    }          
    else
    { 
    safeToProceed = 1; 
    }
    
    if(check == 1){
      print("Motors Off\n");    
    }
    
    if(check == 2){
      print("Motors on\n");
    }      
        
  } 
  
}

void adder(void *par)
{
  while(1)
  {
    
    if(safeToProceed == 0){
      
      low(26);
       
      check = 1;
      
    } 
      
    if(safeToProceed == 1){
     // drive_speed(100, 100);
      high(26);
      check = 2;

    }     
  }     
}

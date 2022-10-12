#include <ros.h>
#include <std_msgs/String.h>
#include <stdio.h>

//Pins on Arduino connected to the Joystick
int VRx = A0;
int VRy = A1;
int SW = 9;

//ROS node initilize
ros::NodeHandle  nh;
std_msgs::String joy_msg;
ros::Publisher joy_axes("joy_axes", &joy_msg);

int xPosition = 0;
int yPosition = 0;
int SW_state = 0;
int mapX = 0;
int mapY = 0;
int xdz = 0;
int ydz = 0; 

void setup() {
  //ros start node
  nh.initNode();
  nh.advertise(joy_axes);
  
  //set pinmodes
  pinMode(VRx, INPUT);
  pinMode(VRy, INPUT);
  pinMode(SW, INPUT_PULLUP); 

  //set deadzone
  xPosition = analogRead(VRx);
  yPosition = analogRead(VRy);
  mapX = map(xPosition, 0, 1023, -512, 512);
  mapY = map(yPosition, 0, 1023, -512, 512);
  xdz = mapX;
  ydz  = mapY;
}

void loop() {
  //read joystick values
  xPosition = analogRead(VRx);
  yPosition = analogRead(VRy);
  mapX = map(xPosition, 0, 1023, -512, 512);
  mapY = map(yPosition, 0, 1023, -512, 512);
  if(abs(mapX) <= abs(xdz)+30){
    mapX = 0;
  }
  if(abs(mapY) <= abs(ydz)+30){
    mapY = 0;
  }
  SW_state = digitalRead(SW);

  //generate joystick message and publish
  char dst[24] = "X:";
  itoa(mapX, dst+2, 10);
  strcat(dst, ";");
  char dst2[12] = "Y:";
  itoa(mapY, dst2+2, 10);
  strcat(dst2, ";");
  strcat(dst,dst2);
  joy_msg.data = dst;
  joy_axes.publish( &joy_msg );
  nh.spinOnce();
  
  delay(1);  
}

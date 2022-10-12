# joy_arduino_ros 

Package requires ROSserial to be installed and library to be available in Arduino IDE
follow http://wiki.ros.org/rosserial_arduino/Tutorials/Arduino%20IDE%20Setup

To use :
1. clone repo
2. Upload joy_arduino_ros/arduino_code/raw_joy_axes_arduino/raw_joy_axes_arduino.ino to your Arduino board (check pin connections)
3. | cd ~/joy_arduino_ros
4. | catkin_make
5. Check Serial port name - ACM0 / ACM1 /... 
6. | roscore
7. open a new terminal
8. | rosrun rosserial_python serial_node.py /dev/ttyACM0
9. | rosrun joy_arduino joyToTwist_node.py 
10.Thats it ! you can check if the joystick axes values are being sent to the topic by | rostopic echo /joy_axes

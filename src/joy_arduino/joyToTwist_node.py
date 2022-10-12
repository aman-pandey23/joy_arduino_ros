#!/usr/bin/env python
from tkinter import Y
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import math

#Code in triple quotes is to live plot the joystick output 

"""
import matplotlib.pyplot as plt
plt.ion()  # Note this correction
fig = plt.figure()
plt.axis([-1000, 1000, -1000, 1000])
i = 0
yd = list()
xd = list()
"""

#max analog value (coming from arduino) of the joystick on any side
maxAxes = 512

#Control mode 0 : yaw and x velocity on the two axes
#Control mode 1 : x and y velocities on the two axes
ctrl_mode = 0

#Max velocity outputs of the twist msg
maxXvel = 2
maxAngularRate = math.pi
maxYvel = maxXvel


pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

def mapTo(x, a, b, c, d):
   y = (x-a)/(b-a)*(d-c)+c
   return y

#Maps the square output of the joystick to a Circle
def circleMap(x, y):
    xa = abs(x)
    ya = abs(y)
    if (xa != 0):
        theta = math.atan(ya/xa)
    else:
        theta = math.pi/2

    if (theta < math.pi/4):
        M = math.sqrt(ya**2 + maxAxes**2)
    elif (theta <= math.pi/2):
        M = math.sqrt(xa**2 + maxAxes**2)

    a = (x/M)*maxAxes
    b = (y/M)*maxAxes

    return (a, b)


def callback(data):

    a = data.data.split(";")
    x = int(a[0].split(":")[1])
    y = int(a[1].split(":")[1])

    X, Y = circleMap(x, y)

    """
    global yd
    global xd
    xd.append(X)
    yd.append(Y)
    """
    
    vel = Twist()
    vel.linear.z = 0
    vel.angular.x = 0
    vel.angular.y = 0

    if(ctrl_mode == 0):
        xm = -mapTo(X, -maxAxes, maxAxes, -maxXvel, maxXvel)
        z = mapTo(Y, -maxAxes, maxAxes, -maxAngularRate, maxAngularRate)
        vel.linear.x = xm
        vel.linear.y = 0
        vel.angular.z = z

    if (ctrl_mode == 1):
        xm = -mapTo(X, -maxAxes, maxAxes, -maxXvel, maxXvel)
        ym = -mapTo(Y, -maxAxes, maxAxes, -maxYvel, maxYvel)
        vel.linear.x = xm
        vel.linear.y = ym
        vel.angular.z = 0

    pub.publish(vel)



def listener():

    rospy.init_node('joyToTwist', anonymous=True)

    rospy.Subscriber("/joy_axes", String, callback)

    """
    global i
    while i < 100000:
        plt.plot(xd, yd, color='r')
        i += 1
        plt.show()
        plt.pause(0.0001)  # Note this correction
    """

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()

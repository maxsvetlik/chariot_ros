#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

from chariot.control.odrive_manager import OdriveMotorManager

"""
This is an experimental TEST SCRIPT that has been developed for small scale, targeted testing only. This does not try to account for any unexpected behavior, which you should expect from a robot.

This driver should not be used in anything other than a controlled test setting. The executor of this script is responsible for ensuring safe execution.

"""
LINEAR_SPEED_MULT = 1
ANGULAR_SPEED_MULT = 5

class Driver:
    def __init__(self):
        # Optionally create a ROS message type as a wrapper for the motor manager's MotorInfo data. This message can be published easily.
        #self._pub = rospy.Publisher("/chariot/status", ChariotStatus, queue_size=1)
        
        rospy.Subscriber("/cmd_vel", Twist, self.vel_callback)
        self._mgr = OdriveMotorManager()
        # Prepare the motors
        self._mgr.set_motors_idle()
        self._mgr.set_motors_active()
        self._cmd_vel = Twist()
        rospy.init_node('chariot_driver', anonymous=False)
        
    def vel_callback(self, data):
        self._cmd_vel = data

    def publish_status(self):
        # Publish MotorInfo status messages
        pass

    def process_vel_cmd(self):
        lin = self._cmd_vel.linear.x
        radius = self._cmd_vel.angular.z
        self._mgr.set_motors_arc_velocity(lin * LINEAR_SPEED_MULT, radius * ANGULAR_SPEED_MULT)

    def run(self):
        while not rospy.is_shutdown():
            self.process_vel_cmd()
            rospy.sleep(0.05)
        self._mgr.set_motors_arc_velocity(0,0)

if __name__ == '__main__':
    d = Driver()
    d.run()

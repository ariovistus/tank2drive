#!/usr/bin/env python3

import wpilib
import xbox
import math
from datetime import datetime
from polartank import (
    normrad,
    joystick_as_polar,
    throttle_angle_to_thrust_right,
    throttle_angle_to_thrust_left,
)
from networktables import NetworkTable


class MyRobot(wpilib.IterativeRobot):
    '''Main robot class'''

    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        self.lstick = wpilib.Joystick(0)
        self.xbox = xbox.XboxController(self.lstick)
        self.rstick =  wpilib.Joystick(1)
        self.lmotor = wpilib.Jaguar(0)
        self.rmotor = wpilib.Jaguar(1)
        self.gyro = wpilib.AnalogGyro(1)
        self.sd = NetworkTable.getTable('SmartDashboard')

    def autonomousInit(self):
        '''Called only at the beginning of autonomous mode'''
        self.starttime = datetime.now()
        self.phase = 1
        self.heading = self.gyro.getAngle()
        self.last = datetime.now()

    def autonomousPeriodic(self):
        '''Called every 20ms in autonomous mode'''
        current = datetime.now()
        print (current-self.last)
        self.last = current
        if self.phase == 1:
            now = datetime.now()
            if (now - self.starttime).seconds > 2:
                self.phase = 2
                self.starttime = now
                print ('phase 2')
                self.heading = self.heading + 80

            theta = math.radians(self.heading - self.gyro.getAngle())
            r = 0.8
        elif self.phase == 2:
            now = datetime.now()
            if (self.heading - self.gyro.getAngle()) < 5:
                self.phase = 3
                self.starttime = now
                print ('phase 3')

            # theta = math.radians(self.heading - self.gyro.getAngle())
            theta = math.copysign(math.pi/2,
                                  self.heading - self.gyro.getAngle())
            r = 0.5
        else:
            theta = 0
            r = 0

        th_l = throttle_angle_to_thrust_left(r, theta)
        th_r = throttle_angle_to_thrust_right(r, theta)
        self.lmotor.set(th_l)
        self.rmotor.set(th_r)

    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        pass

    def disabledPeriodic(self):
        '''Called every 20ms in disabled mode'''
        pass

    def teleopInit(self):
        '''Called only at the beginning of teleoperated mode'''
        pass
        self.initial_heading = self.gyro.getAngle()
        print ('initial heading: ', math.degrees(self.initial_heading))

    def teleopPeriodic(self):
        '''Called every 20ms in teleoperated mode'''
        self.sd.putNumber('theta', self.gyro.getAngle())
        self.drive2()

    def drive1(self):
        x = self.xbox.analog_drive_x()
        y = self.xbox.analog_drive_y()
        r, th = joystick_as_polar(x, y)
        th_l = throttle_angle_to_thrust_left(r, th)
        th_r = throttle_angle_to_thrust_right(r, th)
        self.lmotor.set(th_l)
        self.rmotor.set(th_r)

    def drive2(self):
        x = self.xbox.analog_drive_x()
        y = self.xbox.analog_drive_y()
        r = -self.rstick.getRawAxis(1)
        print (x, y)
        r, th = joystick_as_polar(x, y)
        desired_abs_heading = th - math.pi/2
        desired_relative_heading = (desired_abs_heading -
                                    (math.radians(self.gyro.getAngle())))
        # if r2 < 0.2:
        #   desired_relative_heading = 0
        desired_relative_heading = normrad(desired_relative_heading)
        if abs(desired_relative_heading) > math.radians(10):
            desired_relative_heading = math.copysign(
                math.pi/2, desired_relative_heading)
            #r = 0.8
        th_l = throttle_angle_to_thrust_left(r, desired_relative_heading)
        th_r = throttle_angle_to_thrust_right(r, desired_relative_heading)
        self.lmotor.set(th_l)
        self.rmotor.set(th_r)


if __name__ == '__main__':
    wpilib.run(MyRobot)

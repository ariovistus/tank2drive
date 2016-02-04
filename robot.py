#!/usr/bin/env python3

import wpilib
import xbox
import math


def normalize_joystick_axes(x, y):
    """
    A joystick axis returns a value in the range [-1.0 .. 1.0]
    Then two joystick axes (x direction, y direction) give us a
    "unit square". We want a unit circle - i.e. the angle is preserved,
    but the magnitude is the same for any angle.
    Return (x, y) the scaled x, y components
    """
    magnitude = math.hypot(x, y)
    side = max(abs(x), abs(y))
    if magnitude == 0.0:
        return 0.0, 0.0
    return x * side / magnitude, y * side / magnitude


def joystick_as_polar(x, y):
    x, y = normalize_joystick_axes(x, y)
    h = math.hypot(x, y)
    if h == 0:
        return 0, 0
    th = math.asin(y/h) + math.pi/2
    return h, math.copysign(th, x)


def throttle_angle_to_thrust_right(r, theta):
    if (-math.pi/4) <= theta <= (3*math.pi/4):
        v_a = r * (math.pi/4 - theta) / (math.pi/2)
    elif theta < -math.pi/4:
        v_a = r * (theta + 3*math.pi/4) / (math.pi/2)
    elif theta > 3*math.pi/4:
        v_a = r * (theta - 5*math.pi/4) / (math.pi/2)
    return v_a


def throttle_angle_to_thrust_left(r, theta):
    v_a = 0
    if (math.pi/4) >= theta >= -(3*math.pi/4):
        v_a = r * (math.pi/4 + theta) / (math.pi/2)
    elif theta > math.pi/4:
        v_a = r * (-theta + 3*math.pi/4) / (math.pi/2)
    elif theta < -3*math.pi/4:
        v_a = r * (-theta - 5*math.pi/4) / (math.pi/2)
    return v_a


def signmod(a, b):
    return math.copysign(a % b, a)


class MyRobot(wpilib.IterativeRobot):
    '''Main robot class'''

    def robotInit(self):
        '''Robot-wide initialization code should go here'''

        self.lstick = wpilib.Joystick(0)
        self.xbox = xbox.XboxController(self.lstick)
        self.lmotor = wpilib.Jaguar(0)
        self.rmotor = wpilib.Jaguar(1)

    def autonomousInit(self):
        '''Called only at the beginning of autonomous mode'''
        pass

    def autonomousPeriodic(self):
        '''Called every 20ms in autonomous mode'''
        pass

    def disabledInit(self):
        '''Called only at the beginning of disabled mode'''
        pass

    def disabledPeriodic(self):
        '''Called every 20ms in disabled mode'''
        pass

    def teleopInit(self):
        '''Called only at the beginning of teleoperated mode'''
        pass

    def teleopPeriodic(self):
        '''Called every 20ms in teleoperated mode'''
        x = self.xbox.analog_drive_x()
        y = self.xbox.analog_drive_y()
        r, th = joystick_as_polar(y, x)
        th_l = throttle_angle_to_thrust_left(r, th)
        th_r = throttle_angle_to_thrust_right(r, th)
        self.lmotor.set(th_l)
        self.rmotor.set(th_r)


if __name__ == '__main__':
    wpilib.run(MyRobot)

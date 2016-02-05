from unittest import TestCase
import math
from polartank import (
    normdeg,
    normalize_joystick_axes,
    joystick_as_polar,
    throttle_angle_to_thrust_right,
    throttle_angle_to_thrust_left,
)


joystick_magnitude_data = [(1.0, 1.0, 1.0, 3*math.pi/4),
                           (0.0, 1.0, 1.0, math.pi),
                           (1.0, 0.0, 1.0, math.pi/2),
                           (1.0, 0.24, 1.0, 1.80634130),
                           (0.5, 0.0, 0.5, math.pi/2),
                           (0.0, 0.5, 0.5, math.pi),
                           (0.5, 0.5, 0.5, 3*math.pi/4),
                           (-0.5, -1.0, 1.0, -0.463647609),
                           (-1.0, -1.0, 1.0, -math.pi/4),
                           (0.0, 0.0, 0.0, 0)]


class PolarTankTests(TestCase):
    def test_normdeg(self):
        self.assertAlmostEqual(normdeg(0.), 0.)
        self.assertAlmostEqual(normdeg(45.5), 45.5)
        self.assertAlmostEqual(normdeg(90.5), 90.5)
        self.assertAlmostEqual(normdeg(135.5), 135.5)
        self.assertAlmostEqual(normdeg(180.), -180.)
        self.assertAlmostEqual(normdeg(-180.), -180.)
        self.assertAlmostEqual(normdeg(225.), -135.)
        self.assertAlmostEqual(normdeg(275.), -85.)
        self.assertAlmostEqual(normdeg(359.5), -.5)
        self.assertAlmostEqual(normdeg(379.5), 19.5)
        self.assertAlmostEqual(normdeg(-359.5), .5)
        self.assertAlmostEqual(normdeg(-.5), -.5)
        self.assertAlmostEqual(normdeg(-90.5), -90.5)
        self.assertAlmostEqual(normdeg(-135.5), -135.5)

    def test_joystick_axes_magnitudes(self):
        for (input_x, input_y,
             expected_magnitude,
             expected_theta) in joystick_magnitude_data:
            (x, y) = normalize_joystick_axes(input_x, input_y)
            self.assertAlmostEqual(expected_magnitude, math.hypot(x, y))

    def test_joystick_as_polar(self):
        for (input_x, input_y,
             expected_magnitude,
             expected_theta) in joystick_magnitude_data:
            (r, theta) = joystick_as_polar(input_x, input_y)
            self.assertAlmostEqual(expected_magnitude, r)
            self.assertAlmostEqual(expected_theta, theta)

    def test_right_throttle(self):
        def da_test(r, theta_deg, expected_thrust):
            self.assertAlmostEqual(throttle_angle_to_thrust_right(
                r, math.radians(theta_deg)), expected_thrust)
        da_test(0., 0., 0.)

        da_test(1., -180., -0.5)
        da_test(1., -135., 0.)
        da_test(1., -125., 0.111111111)
        da_test(1., -45., 1.)
        da_test(1., -35., 0.888888888)
        da_test(1., 0., 0.5)
        da_test(1., 35., 0.111111111)
        da_test(1., 45., 0.)
        da_test(1., 125., -0.888888888)
        da_test(1., 135., -1.)
        da_test(1., 145., -0.888888888)
        da_test(1., 180., -0.5)

    def test_left_throttle(self):
        def da_test(r, theta_deg, expected_thrust):
            self.assertAlmostEqual(throttle_angle_to_thrust_left(
                r, math.radians(theta_deg)), expected_thrust)
        da_test(0., 0., 0.)

        da_test(1., -180., 0.5)
        da_test(1., -135., 1.)
        da_test(1., -125., 0.888888888)
        da_test(1., -45., 0.0)
        da_test(1., -35., -0.111111111)
        da_test(1., 0., -0.5)
        da_test(1., 35., -0.888888888)
        da_test(1., 45., -1.)
        da_test(1., 125., -0.111111111)
        da_test(1., 135., 0.)
        da_test(1., 145., 0.111111111)
        da_test(1., 180., 0.5)

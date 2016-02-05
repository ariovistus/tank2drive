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


def normrad(r):
    return ((math.pi + r) % (2 * math.pi)) - math.pi


def normdeg(d):
    return math.degrees(normrad(math.radians(d)))


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
    return -v_a

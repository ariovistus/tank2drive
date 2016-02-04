#
# See the notes for the other physics sample
#


from pyfrc.physics import drivetrains


class PhysicsEngine(object):
    '''
       Simulates a 4-wheel robot using Tank Drive joystick control
    '''

    def __init__(self, physics_controller):
        '''
            :param physics_controller: `pyfrc.physics.core.Physics` object
                                       to communicate simulation effects to
        '''

        self.physics_controller = physics_controller
        self.physics_controller.add_analog_gyro_channel(1)

    def update_sim(self, hal_data, now, tm_diff):
        '''
            Called when the simulation parameters for the program need to be
            updated.

            :param now: The current time as a float
            :param tm_diff: The amount of time that has passed since the last
                            time that this function was called
        '''

        # Simulate the drivetrain
        l_motor = hal_data['pwm'][0]['value']
        r_motor = hal_data['pwm'][1]['value']

        speed, rotation = drivetrains.four_motor_drivetrain(
            l_motor, r_motor, l_motor, r_motor)
        self.physics_controller.drive(speed, rotation, tm_diff)

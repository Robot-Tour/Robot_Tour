# This example make the robot turn 90 degrees using the gyroscope.
#
# In the "Choose edition" menu, use the A and C buttons to select what type of
# 3pi+ robot you have and then press B to confirm.  Then press button A or C
# to make the robot turn.
#
# If you need the turn to be more accurate, you might consider calibrating the
# gyro (see rotation_resist.py), but that doesn't make much difference for
# short turns.

from pololu_3pi_2040_robot import robot
from pololu_3pi_2040_robot.extras import editions
import time

angle_to_turn = 90

motors = robot.Motors()
encoders = robot.Encoders()
button_a = robot.ButtonA()
button_c = robot.ButtonC()

imu = robot.IMU()
imu.reset()
imu.enable_default()

max_speed = 3000
kp = 140
kd = 4


drive_motors = False
last_time_gyro_reading = None
turn_rate = 0.0     # degrees per second
robot_angle = 0.0   # degrees
target_angle = 0.0
last_time_far_from_target = None

#important
def handle_turn_or_stop(button, angle):
    global target_angle, drive_motors
    global last_time_far_from_target, last_time_gyro_reading
    target_angle = robot_angle + angle
    drive_motors = not drive_motors
    if drive_motors:
        #while button.check() != False: pass  # wait for release
        time.sleep_ms(500)
        last_time_far_from_target = time.ticks_ms()
    last_time_gyro_reading = time.ticks_us()
    

def move():
    # 956, 1000
    motors.set_speeds(956,1000)
    for i in range (1987):
        
        time.sleep_ms(1)
        # imu.gyro.read()



    motors.set_speeds(0, 0)
    
def move():
    # 956, 1000
    motors.set_speeds(956,1000)
    for i in range (1987):
        
        time.sleep_ms(1)
        # imu.gyro.read()



    motors.set_speeds(0, 0)
    
def move():
    # 956, 1000
    motors.set_speeds(956,1000)
    for i in range (1987):
        
        time.sleep_ms(1)
        # imu.gyro.read()



    motors.set_speeds(0, 0)

'''
while True:
    if imu.gyro.data_ready():
       imu.gyro.read()
       turn_rate = imu.gyro.last_reading_dps[2]  # degrees per second
       now = time.ticks_us()
       if last_time_gyro_reading:
           dt = time.ticks_diff(now, last_time_gyro_reading)
           robot_angle += turn_rate * dt / 1000000
       last_time_gyro_reading = now
    
    handle_turn_or_stop(button_c, -angle_to_turn)
    time.sleep_ms(500)
    
    # Decide whether to stop the motors.
    if drive_motors:
        far_from_target = abs(robot_angle - target_angle) > 3
        if far_from_target:
            last_time_far_from_target = time.ticks_ms()
        elif time.ticks_diff(time.ticks_ms(), last_time_far_from_target) > 250:
            drive_motors = False

    # Drive motors.
    if drive_motors:
        turn_speed = (target_angle - robot_angle) * kp - turn_rate * kd
        if turn_speed > max_speed: turn_speed = max_speed
        if turn_speed < -max_speed: turn_speed = -max_speed
        motors.set_speeds(-turn_speed, turn_speed)
    else:
        motors.off()
        
'''

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
display = robot.Display()

imu = robot.IMU()
imu.reset()
imu.enable_default()

max_speed = 3000
kp = 140
kd = 4

drive_motors = False
last_time_gyro_reading = None
last_time_acc_reading = None
turn_rate = 0.0  # degrees per second
robot_angle = 0.0  # degrees
target_angle = 0.0
last_time_far_from_target = None


time.sleep_ms(500)
calibration_start = time.ticks_ms()
stationary_gz = 0.0
reading_count = 0
while time.ticks_diff(time.ticks_ms(), calibration_start) < 1000:
    if imu.gyro.data_ready():
        imu.gyro.read()
        stationary_gz += imu.gyro.last_reading_dps[2]
        reading_count += 1
stationary_gz /= reading_count



def moveg(dist):
    global drive_motors
    global last_time_far_from_target, last_time_gyro_reading, last_time_acc_reading, robot_angle, speed
    motors.off()
    target_angle = robot_angle
    sl = 1011*speed
    sr = 1000*speed
    travel = 0
    encoders.get_counts(reset = True)

    while abs(travel) < abs(dist):
        if imu.gyro.data_ready():
            imu.gyro.read()
            turn_rate = imu.gyro.last_reading_dps[2] - stationary_gz # degrees per second
            now = time.ticks_us()
            if last_time_gyro_reading:
                dt = time.ticks_diff(now, last_time_gyro_reading)
                robot_angle += turn_rate * dt / 1000000
            last_time_gyro_reading = now
            
        
        c = encoders.get_counts()
        travel = c[0]*10.5
        travel /= 360
        
        #adjustedl = max(((min(travel, dist-travel)/(dist/2))*sl), 500)
        #adjustedr = max(((min(travel, dist-travel)/(dist/2))*sr), 500)
        
        adjustedl = sl
        adjustedr = sr
        
        if abs(dist-travel) < 10:
            adjustedl = max((((dist-travel)/dist)*sl), 500)
            adjustedr = max((((dist-travel)/dist)*sr), 500)
        
        if dist < 0: 
            adjustedl *= -1
            adjustedr *= -1
        
        motors.set_speeds(adjustedl + 15*(robot_angle - target_angle), adjustedr + 15*(target_angle - robot_angle))
    '''
    if abs(target_angle - robot_angle) > 1:
        turn(target_angle - robot_angle)
    '''

    motors.off()


def turn(angle):
    global drive_motors, robot_angle
    global last_time_far_from_target, last_time_gyro_reading, robot_angle
    motors.off()
    drive_motors = not drive_motors
    max_speed1 = 500
    #og kp = 140 kd = 4
    kp = 140
    kd = 4
    turn_rate = 0
    target_angle = angle
    while drive_motors:
        if imu.gyro.data_ready():
            imu.gyro.read()
            turn_rate = imu.gyro.last_reading_dps[2] - stationary_gz # degrees per second
            now = time.ticks_us()
            if last_time_gyro_reading:
                dt = time.ticks_diff(now, last_time_gyro_reading)
                # initial value over dt 1000000
                robot_angle += turn_rate * dt / 1000000
            last_time_gyro_reading = now

        if drive_motors:
            far_from_target = abs(robot_angle - target_angle) > 2
            if far_from_target:
                last_time_far_from_target = time.ticks_ms()
            if time.ticks_diff(time.ticks_ms(), last_time_far_from_target) > 250:
                drive_motors = False
                motors.off()

        if drive_motors:
            turn_speed = (target_angle - robot_angle) * kp - turn_rate * kd
            if turn_speed > max_speed1: turn_speed = max_speed1
            if turn_speed < -max_speed1: turn_speed = -max_speed1

            motors.set_speeds(-turn_speed, turn_speed)
        else:
            motors.off()
            
    time.sleep_ms(150)


n = "t0"
w = "t90"
s= "t180"
e = "t-90"
f = "m50"


#enter moves here
    #l, r, f, are default move/turn values
    #manually type t[degree] to turn custom degree
    #manually type m[distance] to move custom distance

#moves = ["m30.5", l, f, r, f, r, f, l, "m100", l, f, l, f, r, f, l, "m100", r, f, r, r, f, l, "m100", l, f, l, f, l, l, "m100", r, r, f, l, "m100", l, f, l, "m42.5"]
#moves = [l, l, l, l, l, l, l, l, l, l, l, l]
#moves = [r, r, r, r, r, r, r, r, r, r, r, r]
#moves = ["m30.5", l, f, r, f, l, f, r, f, r, f, l, f, l, "m42.5"]
#moves = ["m80.5", l, f, l, f, r, "m100", r, f, r, f, l, "m100", "t180", f, r, f, r, f, "t-180", f, l, "m150", l, f, "t180", f, r, f, r, "m42.5"]
#moves = [x for x in range(3) for x in [f, r, f, r, f, r, f, r]]
moves = ["m81.5", w, "m26", "m-26", n, "m76", "m-26", w, "m100", s, f, w, f, s, "m26", "m-26", n, "m76","m-76", e, f, n, "m100", e, "m51.5"]
#moves = ["m80.5", l, f, "t-180", f, l, "m100", "t180", f, r, "m100", l, f, r, f, l, f, "t180", "m150", "t180", "m100", l, f, l, "m100", r, "m44"]


#base stats at speed 1
#t90 and m50
#turn time
tt = .65
#move time
mt = 4.5

#CHANGE DURING EVENT TIME
target_time = 60
#decimals for partial movess
#don't worry about this, it is calculated
nturns = 21
nmoves = 23.6

distance = 0
turns = 0
for x in moves:
    if x[0] == "t":
        turns += 1
    elif x[0] == "m":
        distance += float(x[1:])

nmoves = distance / 50
nturns = turns
#target_time += nturns / 3

speed = (target_time - (tt * nturns)) / (mt * nmoves)
#speed = 1.5
speed = 1.5 / speed


for x in moves:
    if x[0] == "t":
        degree = float(x[1:])
        turn(degree)
    elif x[0] == "m":
        distance = float(x[1:])
        moveg(distance)
        

display.text(f"Turns: {nturns}", 0, 0)
display.text(f"Moves: {nmoves}", 0, 10)
display.text(f"Angle: {robot_angle%360}", 0, 20)
display.show()

motors.off()

import time
from djitellopy import tello

# Initialize and connect to the drone
sparten = tello.Tello()
sparten.connect()
print(f"Drone Battery: {sparten.get_battery()} %")

# Automated takeoff
sparten.takeoff()

print("Flying upward")
# Fly upward
upward_speed = 50
upward_time = 20
sparten.send_rc_control(0, 0, upward_speed, 0)
time.sleep(upward_time)

# Fly forward
forward_speed = 50
fly_time = 45

print("Flying forward")
sparten.send_rc_control(0, forward_speed, 0, 0)
time.sleep(fly_time)

# Hover in place
sparten.send_rc_control(0, 0, 0, 0)
time.sleep(1)

# Perform a 360 degree rotation
print("Rotating 360 degrees")
sparten.rotate_clockwise(360)
time.sleep(1)

# Fly backward
print("Returning to initial position")
sparten.send_rc_control(0, -forward_speed, 0, 0)
time.sleep(fly_time)

# Hover in place
sparten.send_rc_control(0, 0, 0, 0)
time.sleep(1)

# Perform flips before landing
flips = ['l', 'r']  # List of directions to flip: left and right
for flip_direction in flips:
    print(f"Performing {flip_direction} flip")
    sparten.flip(flip_direction)
    time.sleep(3)  # Wait for a short period after each flip to stabilize

# Landing
print("Landing")
sparten.land()

print("Mission completed")

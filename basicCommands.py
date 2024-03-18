from djitellopy import tello
from time import sleep

# Create a Tello Object
sparten = tello.Tello()

# Connect to Tello
sparten.connect()

# Get battery percentage
print(f"The Sparten Tello Drone battery parcentage is: {sparten.get_battery()} %")

# Takeoff
sparten.takeoff()

# Move Right
sparten.send_rc_control(0, 30, 0, 0)

#  Wait for 2 seconds
sleep(2)

# Slow down before Landing
sparten.send_rc_control(-30, 0, 0, 0)

sleep(3)

sparten.send_rc_control(20, 0, 0, 0)

sleep(4)

# Slow down
sparten.send_rc_control(0 ,0, 0, 0)
# Land
sparten.land()




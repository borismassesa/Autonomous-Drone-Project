# Main Script
import keyPressModule as kp
from time import sleep
from djitellopy import tello
import cv2

kp.init()
sparten = tello.Tello()
sparten.connect()
print(f"Drone Battery: {sparten.get_battery()} %")

# Flag to track if the drone has taken off
has_taken_off = False

def getKeyboardInput():
    global has_taken_off
    lr, fb, ud, yv = 0, 0, 0, 0  # Initialize all control values to 0
    speed = 50

    # Check for the 'e' key to take off
    if not has_taken_off and kp.getKey("e"):
        sparten.takeoff()
        has_taken_off = True

    # After takeoff, check for other control keys
    if has_taken_off:
        if kp.getKey("LEFT"): lr = -speed
        elif kp.getKey("RIGHT"): lr = speed
        if kp.getKey("UP"): fb = speed
        elif kp.getKey("DOWN"): fb = -speed
        if kp.getKey("w"): ud = speed
        elif kp.getKey("s"): ud = -speed
        if kp.getKey("a"): yv = -speed
        elif kp.getKey("d"): yv = speed
        if kp.getKey("q"):  # Landing the drone
            sparten.land()
            has_taken_off = False

    return [lr, fb, ud, yv]

while True:
    vals = getKeyboardInput()
    if has_taken_off:
        # If no keys are pressed, vals will be [0, 0, 0, 0], keeping the drone hovering in place.
        sparten.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)

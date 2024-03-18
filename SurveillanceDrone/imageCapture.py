# Main Script
import os
import keyPressModule as kp
import time
from djitellopy import tello
import cv2
import numpy as np


kp.init()
sparten = tello.Tello()
sparten.connect()
print(f"Drone Battery: {sparten.get_battery()} %")

sparten.streamon()  # Turn on the video stream

# Flag to track if the drone has taken off
has_taken_off = False

# Create a directory to save images if it doesn't exist
img_dir = "captured_images"
os.makedirs(img_dir, exist_ok=True)

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

    # Take a picture on 'z' key press
    if kp.getKey("z"):
        cv2.imwrite(f"{img_dir}/{int(time.time())}.jpg", img)
        print("Image Captured")
        time.sleep(0.3)  # Delay to prevent multiple captures on a single press

    return [lr, fb, ud, yv]

while True:
    vals = getKeyboardInput()
    if has_taken_off:
        # If no keys are pressed, vals will be [0, 0, 0, 0], keeping the drone hovering in place.
        sparten.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    
    # Get the frame from the Tello drone
    img = sparten.get_frame_read().frame
    img = cv2.resize(img, (720, 480))

    # Improve coloring using histogram equalization
    img_y_cr_cb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(img_y_cr_cb)

    # Apply histogram equalization on the Y channel
    y_eq = cv2.equalizeHist(y)

    img_y_cr_cb_eq = cv2.merge((y_eq, cr, cb))
    img_eq = cv2.cvtColor(img_y_cr_cb_eq, cv2.COLOR_YCrCb2BGR)

    # Display the improved live stream
    cv2.imshow("Improved Live Stream", img_eq)

    # Break the loop with 'ESC' key
    if cv2.waitKey(1) & 0xFF == 27:  
        break

# When everything is done, release the capture and close windows
sparten.streamoff()
cv2.destroyAllWindows()

import keyPressModule as kp
from time import sleep
from djitellopy import tello
import numpy as np
import cv2

## Parameters ##
forward_speed = 117/10 # Forward speed in cm/s
angular_speed = 360/10 # Angular speed in degrees/s
interval = 0.25 # Time interval for which the drone moves in a particular direction

distance_interval = forward_speed * interval # Distance covered by the drone in a particular direction
angular_speed_interval = angular_speed * interval # Angle covered by the drone in a particular direction

x_val, y_val, z_val = 500, 500, 0 # Initial position of the drone
angle = 0 # Initial angle of the drone
yaw = 0 # Initial yaw of the drone
distance_value = 0 # Initial distance covered by the drone

points = [(0,0), (0,0)] # List to store the points

kp.init()
sparten = tello.Tello()
sparten.connect()
print(f"Drone Battery: {sparten.get_battery()} %")

# Flag to track if the drone has taken off
has_taken_off = False

def getKeyboardInput():
    global has_taken_off
    lr, fb, ud, yv = 0, 0, 0, 0  # Initialize all control values to 0 lr: left/right, fb: forward/backward, ud: up/down, yv: yaw value
    speed = 15  # Speed of the drone
    angular_speed = 50  # Angular speed of the drone
    global angle, yaw, distance_value, x_val, y_val, z_val # Global variables to store the angle, yaw, and distance covered by the drone

    # Check for the 'e' key to take off
    if not has_taken_off and kp.getKey("e"):
        sparten.takeoff()
        has_taken_off = True

    # After takeoff, check for other control keys
    if has_taken_off:
        if kp.getKey("LEFT"): 
            lr = -speed
            distance_value = distance_interval
            angle = -180
        elif kp.getKey("RIGHT"): 
            lr = speed
            distance_value = -distance_interval 
            angle = 180
        if kp.getKey("UP"): 
            fb = speed
            distance_value = -distance_interval
            angle = 270
        elif kp.getKey("DOWN"): 
            fb = -speed
            distance_value = distance_interval
            angle = -90
        if kp.getKey("w"): 
            ud = speed
        elif kp.getKey("s"): 
            ud = -speed
        if kp.getKey("a"): 
            yv = -angular_speed
            yaw -= angular_speed_interval
        elif kp.getKey("d"): 
            yv = angular_speed
            yaw += angular_speed_interval
        if kp.getKey("q"):  # Landing the drone
            sparten.land()
            has_taken_off = False

    sleep(interval) # Sleep for the interval time
    # Update the x, y, z values based on the distance covered by the drone
    angle += yaw
    x_val += int(distance_value * np.cos(np.radians(angle))) # Update the x value
    y_val += int(distance_value * np.sin(np.radians(angle))) # Update the y value


    return [lr, fb, ud, yv, x_val, y_val] # Return the control values


def drawPoints(img, points): # Function to draw the drone on the image
    for point in points:
        cv2.circle(img, point, 10, (0, 0, 255), cv2.FILLED) # Draw a red circle representing the drone movement.
    cv2.circle(img, points[-1], 15, (0, 255, 0), cv2.FILLED) # Draw a green circle representing the current position of the drone
    cv2.putText(img, f'({(points[-1][0] - 500)/100}, {(points[-1][1] - 500)/100})m', (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1) # Display the x, y values of the drone on the image

while True:
    vals = getKeyboardInput() # Get the control values from the keyboard
    if has_taken_off:
        # If no keys are pressed, vals will be [0, 0, 0, 0], keeping the drone hovering in place.
        sparten.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)

    img = np.zeros((1000, 1000, 3), np.uint8) # Create a black image
    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]): # Check if the drone has moved
        points.append((vals[4], vals[5])) # Get the x, y values of the drone
    drawPoints(img, points) # Draw the drone on the image
    cv2.imshow("Output", img) # Display the image
    cv2.waitKey(1) # Wait for a key press
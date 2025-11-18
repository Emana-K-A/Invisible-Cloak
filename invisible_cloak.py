import cv2
import numpy as np
import time

# Start the webcam
cap = cv2.VideoCapture(0)
time.sleep(3)  # Allow the camera to adjust

# Capture the background
background = None
for i in range(50):
    ret, background = cap.read()

# Flip the background for consistency
background = cv2.flip(background, 1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # HSV range for blue color
    lower_blue = np.array([94, 80, 2])
    upper_blue = np.array([126, 255, 255])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, np.ones((3, 3), np.uint8))

    mask_inv = cv2.bitwise_not(mask)
    res1 = cv2.bitwise_and(background, background, mask=mask)
    res2 = cv2.bitwise_and(frame, frame, mask=mask_inv)
    final_output = cv2.addWeighted(res1, 1, res2, 1, 0)

    window_name = "Invisible Cloak"
    cv2.imshow(window_name, final_output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import mss
import numpy as np
import pyautogui

# ==============================
# LOAD IMAGE
# ==============================
with mss.mss() as sct:
    monitor = sct.monitors[0]
    image = np.array(sct.grab(monitor))
    height, width, channels = image.shape

    top_quarter = height // 4
    image[0:top_quarter, 0:width] = 0

    if image is None:
        print("Error: Image not found.")
        exit()

    # ==============================
    # CONVERT TO HSV
    # ==============================
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # ==============================
    # DEFINE BLUE COLOR RANGE
    # ==============================
    lower_ring = np.array([75, 50, 150])
    upper_ring = np.array([105, 255, 255])

    # ==============================
    # CREATE MASK
    # ==============================
    mask = cv2.inRange(hsv, lower_ring, upper_ring)

    # ==============================
    # REMOVE NOISE (Optional but recommended)
    # ==============================
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # ==============================
    # FIND CONTOURS
    # ==============================
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # ==============================
    # DRAW CONTOURS
    # ==============================
    output = image.copy()
    cv2.drawContours(output, contours, -1, (0, 255, 0), 2)

    print("Number of blue objects detected:", len(contours))

    # ==============================
    # DISPLAY WINDOWS (PRESS Q TO CLOSE)
    # ==============================

    largest_contour = None
    max_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > max_area:
            max_area = area
            largest_contour = cnt

    if largest_contour is not None:

        x, y, w, h = cv2.boundingRect(largest_contour)

        bottom_center_x = x + w // 2
        bottom_center_y = y + h

        pyautogui.click(bottom_center_x, bottom_center_y)

    while True:
        # cv2.imshow("Original Image", image)
        cv2.imshow("Blue Mask", mask)
        cv2.imshow("Detected Blue Objects", output)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):  # press 'q' to quit
            break

    cv2.destroyAllWindows()

import mss
import cv2
import numpy as np
import time
import ctypes
import pydirectinput
import win32api
import win32con

# Esto es vital para que las coordenadas de Python coincidan con los píxeles reales de Windows
ctypes.windll.shcore.SetProcessDpiAwareness(1)
pydirectinput.FAILSAFE = False


def mover_mouse_absoluto(x, y):
    """Mueve el mouse a coordenadas absolutas de la pantalla (Teletransporte)."""
    ancho_pantalla = win32api.GetSystemMetrics(0)
    alto_pantalla = win32api.GetSystemMetrics(1)

    x_win = int((x / ancho_pantalla) * 65535)
    y_win = int((y / alto_pantalla) * 65535)

    ctypes.windll.user32.mouse_event(
        win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE,
        x_win, y_win, 0, 0)
    time.sleep(0.05)


def despertar_motor_juego():
    """Forza un movimiento relativo de hardware (1 píxel) para que Roblox actualice su cámara 3D."""
    # Mueve el ratón 1 píxel hacia la derecha y abajo
    ctypes.windll.user32.mouse_event(win32con.MOUSEEVENTF_MOVE, 1, 1, 0, 0)
    time.sleep(0.02)
    # Lo regresa a su posición original
    ctypes.windll.user32.mouse_event(win32con.MOUSEEVENTF_MOVE, -1, -1, 0, 0)
    time.sleep(0.05)


def clic_mouse(x, y):
    """Hace un clic rápido asegurando que el juego registre la posición correcta."""
    mover_mouse_absoluto(x, y)
    despertar_motor_juego()  # TRUCO PARA EVITAR COORDENADAS FANTASMAS

    ctypes.windll.user32.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.05)


def darcClickTP(x, y):
    pydirectinput.leftClick()
    mover_mouse_absoluto(x, y)
    despertar_motor_juego()
    pydirectinput.mouseDown(button='left')
    time.sleep(1.01)
    pydirectinput.mouseUp(button='left')


def detectarBanderaRoja(monitor):
    image = obtenerCurrFrame(monitor)
    height, width, _ = image.shape

    # Ignorar el cielo o la UI superior
    image[0:height // 3, 0:width] = 0

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    # Create masks
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    # ==============================
    # Combine MASK
    # ==============================

    mask = mask1 + mask2

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    largest_contour = None
    max_area = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 100:
            x, y, w, h = cv2.boundingRect(cnt)
            aspect_ratio = float(w) / h
            if aspect_ratio > 1.5:
                if area > max_area:
                    max_area = area
                    largest_contour = cnt
    if largest_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_contour)
        bottom_center_x = x + w // 2
        bottom_center_y = y + h

        target_x = int(monitor["left"] + bottom_center_x)
        target_y = int(monitor["top"] + bottom_center_y)

        darcClickTP(target_x, target_y-5)
    else:
        print("No se encontró la bandera roja en este escaneo.")


def obtenerCurrFrame(monitor):
    img = np.array(sct.grab(monitor))
    frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return frame


def ejecutar_accion(monitor):

    frame = obtenerCurrFrame(monitor)
    imgaenHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango para el marco inicial
    azul_bajo = np.array([100, 150, 50])
    azul_alto = np.array([140, 255, 255])
    mascara = cv2.inRange(imgaenHSV, azul_bajo, azul_alto)

    contornos, _ = cv2.findContours(
        mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contornos:
        c = max(contornos, key=cv2.contourArea)
        M = cv2.moments(c)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            target_cX = int(monitor["left"] + cX)
            target_cY = int(monitor["top"] + cY)

            clic_mouse(target_cX, target_cY)
            time.sleep(0.1)
            clic_mouse(target_cX, target_cY)

            time.sleep(2)

            detectarBanderaRoja(monitor)

    else:
        print("No se encontró ningún marco azul inicial en la pantalla.")


time.sleep(5)

while True:
    with mss.mss() as sct:
        monitor = sct.monitors[0]
        ejecutar_accion(monitor)
        x = 0
        time.sleep(1)
        while x < 2:
            if x == 0:
                pydirectinput.keyDown("down")
                time.sleep(2.4)
                pydirectinput.keyUp("down")
                pydirectinput.keyDown("up")
                time.sleep(2.8)
                pydirectinput.keyUp("up")
                pydirectinput.keyDown("down")
                time.sleep(2.6)
                pydirectinput.keyUp("down")
                detectarBanderaRoja(monitor)
            else:
                pydirectinput.keyDown("down")
                time.sleep(3)
                pydirectinput.keyUp("down")
            '''pydirectinput.keyDown("up")
            time.sleep(2.5)
            pydirectinput.keyUp("up")'''
            x = x+1
        time.sleep(27.5)

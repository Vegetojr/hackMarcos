import mss
import cv2
import numpy as np
import pyautogui
import time
import pydirectinput


def ejecutar_accion():
    # mss es lo que toma la cpatura de pantalla
    with mss.mss() as sct:
        time.sleep(5)
        # Esto camiba que mointor es importnate saber el del marcos
        monitor = sct.monitors[1]
        # esto convertimos la captura en un arrelgo de numPy
        img = np.array(sct.grab(monitor))

        # y le damos el formato de color que mejor maneja opencv
        frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        imgaenHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # aqui defino el rango de azules que quiero
        azul_bajo = np.array([100, 150, 50])
        azul_alto = np.array([140, 255, 255])

        # esto es lo que hcimos en el profe de python
        mascara = cv2.inRange(imgaenHSV, azul_bajo, azul_alto)
        contornos, _ = cv2.findContours(
            mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contornos:
            # Encontrar el contorno más grande (el marco)
            c = max(contornos, key=cv2.contourArea)
            # Obtener las coordenadas del centro

            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                pydirectinput.moveTo(cX, cY, duration=0.2)

                pydirectinput.leftClick()
                pydirectinput.leftClick()
                time.sleep(2)
                pydirectinput.moveTo(cX+5, cY+5, duration=0.2)
                pydirectinput.leftClick()
                time.sleep(10)
                pydirectinput.keyDown('up')
                time.sleep(2)  # El tiempo que desees mantener la tecla
                pydirectinput.keyUp('up')
                pydirectinput.keyDown('down')
                time.sleep(2)  # El tiempo que desees mantener la tecla
                pydirectinput.keyUp('down')
                pydirectinput.keyDown('left')
                time.sleep(2)  # El tiempo que desees mantener la tecla
                pydirectinput.keyUp('left')
                pydirectinput.keyDown('right')
                time.sleep(2)  # El tiempo que desees mantener la tecla
                pydirectinput.keyUp('right')
        else:
            print("No se encontró ningún marco azul en la pantalla.")


ejecutar_accion()

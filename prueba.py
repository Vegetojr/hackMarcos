import mss
import cv2
import numpy as np
import pyautogui
import time


def ejecutar_accion():
    # mss es lo que toma la cpatura de pantalla
    with mss.mss() as sct:
        time.sleep(10)
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
            pyautogui.sleep(10)
            M = cv2.moments(c)
            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                pyautogui.moveTo(cX, cY, duration=0.2)

                pyautogui.leftClick()
                pyautogui.leftClick()
                pyautogui.sleep(10)
                pyautogui.keyDown('up')
                time.sleep(2)  # El tiempo que desees mantener la tecla
                pyautogui.keyUp('up')
                pyautogui.keyDown('down')
                time.sleep(2)  # El tiempo que desees mantener la tecla
                pyautogui.keyUp('down')
                pyautogui.keyDown('left')
                time.sleep(2)  # El tiempo que desees mantener la tecla
                pyautogui.keyUp('left')
                pyautogui.keyDown('right')
                time.sleep(2)  # El tiempo que desees mantener la tecla
                pyautogui.keyUp('right')
        else:
            print("No se encontró ningún marco azul en la pantalla.")


ejecutar_accion()

from time import sleep

import cv2
import mss
import numpy as np
import pydirectinput


def detectar_azul_visible(sct, monitor, area_minima=5000):
    def es_rectangular(contorno, aspect_ratio_min=1.5, aspect_ratio_max=3.5):
        # Obtener el rectángulo delimitador del contorno
        x, y, w, h = cv2.boundingRect(contorno)

        # Calcular la relación de aspecto (ancho/alto)
        aspect_ratio = w / h if h != 0 else 0

        # Verificar si la relación de aspecto está dentro del rango esperado para una bandera
        return aspect_ratio_min <= aspect_ratio <= aspect_ratio_max
    img = np.array(sct.grab(monitor))

    # Filtro solo la parte inferior (ROI) de la pantalla
    roi_x1, roi_y1 = 0, monitor["height"] // 2
    roi_x2, roi_y2 = monitor["width"], monitor["height"]
    cropped_img = img[roi_y1:roi_y2, roi_x1:roi_x2]

    # Convertimos la imagen a HSV
    frame = cv2.cvtColor(cropped_img, cv2.COLOR_BGRA2BGR)
    imagenHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango ajustado de azul
    azul_bajo = np.array([90, 150, 120])  # Ajustamos la saturación y brillo
    azul_alto = np.array([130, 255, 255])

    # Detectamos la máscara azul
    mascara = cv2.inRange(imagenHSV, azul_bajo, azul_alto)
    contornos, _ = cv2.findContours(
        mascara, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contornos:
        for c in contornos:
            if es_rectangular(c):  # Solo consideramos formas rectangulares
                x, y, w, h = cv2.boundingRect(c)
                area = cv2.contourArea(c)

                if area > area_minima:
                    print(
                        f"Detected flag with bounding box: x={x}, y={y}, w={w}, h={h}")
                    # Calcular el centro inferior de la bandera
                    bottom_middle_x = x + w // 2
                    bottom_middle_y = y + h  # Fondo de la caja delimitadora

                    # Ajustar para un pequeño desplazamiento si es necesario
                    click_offset = 10  # Ajustar según sea necesario
                    bottom_middle_y -= click_offset

                    print(
                        f"Bottom middle: ({bottom_middle_x}, {bottom_middle_y})")

                    # Mover el mouse y hacer click
                    pydirectinput.moveTo(
                        bottom_middle_x, bottom_middle_y, duration=0.2)
                    pydirectinput.leftClick()
                    return True  # Aquí terminamos después de hacer el primer click

    return False  # Si no se detecta la bandera, devuelve False


sleep(5)

print("Started")
pydirectinput.keyDown("right")
sleep(.65)
pydirectinput.keyUp("right")
print("ended")


with mss.mss() as sct:
    monitor = sct.monitors[0]
    intentos = 0
    max_intentos = 15
    while intentos < max_intentos:
        if detectar_azul_visible(sct, monitor):
            print("Bandera completamente visible ✅")
            break
        else:
            print("Bandera tapada, girando...")
            pydirectinput.keyDown("right")
            sleep(0.15)
            pydirectinput.keyUp("right")
            sleep(0.4)

        intentos += 1

import cv2
import mediapipe as mp
import pyautogui
import time
import numpy as np
from directkeys import PressKey

from CerrarPrograma import cerrar_programas
from procesos import nombres_procesos
count_gesture_close = 0

pyautogui.FAILSAFE = False

time.sleep(1.0)

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

# Definición de dimensiones de la cámara y otras variables
anchocam, altocam = 640, 480
cuadro = 100 #Rango donde podemos interactura
screen_width, screen_height = pyautogui.size()
sua = 5
pubix, pubiy = 0,0
cubix, cubiy = 0,0

# Variables para el estado de clic derecho e izquierdo
hacer_clic_derecho = False
hacer_clic_izquierdo = False

# Inicialización de la cámara
video = cv2.VideoCapture(0)

# Configuración del modelo de manos de Mediapipe
with mp_hand.Hands(min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        frame_height, frame_width, _ = image.shape

        lmList = []
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            myHands = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHands.landmark):
                cx, cy = int(lm.x * frame_width), int(lm.y * frame_height)
                lmList.append([id, cx, cy])
            mp_draw.draw_landmarks(image, myHands, mp_hand.HAND_CONNECTIONS)

        # Procesar acciones basadas en los landmarks de las manos
        if len(lmList) != 0:
            hand_x, hand_y = lmList[5][1], lmList[5][2]  # Con el centro de la mano

            cv2.circle(image, (hand_x, hand_y), 10, (0, 0, 255), -1)
            cv2.rectangle(image, (cuadro, cuadro), (anchocam - cuadro, altocam - cuadro), (0, 0, 0), 2)  # Generamos cuadro

            # Lógica para cerrar el juego y abrir el menú principal ------------------------
            pinky_tip_y = lmList[20][2]  # cy del dedo meñique

            # Obtén las coordenadas y de las puntas de los demás dedos
            thumb_tip_y = lmList[4][2]   # cy del pulgar
            index_tip_y = lmList[8][2]   # cy del índice
            middle_tip_y = lmList[12][2]  # cy del medio
            ring_tip_y = lmList[16][2]    # cy del anular

            threshold = 20

            pinky_raised = (
                pinky_tip_y < thumb_tip_y - threshold and
                pinky_tip_y < index_tip_y - threshold and
                pinky_tip_y < middle_tip_y - threshold and
                pinky_tip_y < ring_tip_y - threshold
            )

            if pinky_raised:
                count_gesture_close += 1
                print(count_gesture_close)
                if count_gesture_close == 25:
                    # Cerrar el juego y abrir el menú principal
                    cerrar_programas(nombres_procesos)
                    cv2.destroyAllWindows()  # Cerrar la ventana de la cámara antes de abrir una nueva
                    video.release()  
                    from main import iniciarVentana
                    iniciarVentana()
                    PressKey(0x10)
            else:
                count_gesture_close = 0
            # ----------------------------

            # Convertir las coordenadas de la mano a las dimensiones de la pantalla
            # x3 = np.interp(hand_x, (cuadro, anchocam - cuadro), (0, screen_width)) # Con camara de lap?
            x3 = np.interp(hand_x, (cuadro, anchocam - cuadro), (screen_width, 0)) # Con fono
            y3 = np.interp(hand_y, (cuadro, altocam - cuadro), (0, screen_height))

            # Suavizar las coordenadas
            cubix = pubix + (x3 - pubix) / sua #Ubicacion actual = ubi anterior + x3 - Pa dividida el valor suavizado
            cubiy = pubiy + (y3 - pubiy) / sua

            # Mover el puntero en la pantalla a la posición de la mano
            pyautogui.moveTo(screen_width - cubix, cubiy, duration=0, tween=pyautogui.easeInOutQuad, _pause=False)
            pubix, pubiy = cubix, cubiy

            index_tip_x = lmList[8][1]  # Coordenada x del extremo del dedo índice
            index_tip_y = lmList[8][2]  # Coordenada y del extremo del dedo índice
            index_base_y = lmList[5][2]  # Coordenada y de la base del dedo índice
            thumb_tip_y = lmList[4][2]  # Coordenada y del extremo del dedo pulgar

            thumb_tip_x = lmList[4][1]
            thumb_tip_y = lmList[4][2]
            index_base_x = lmList[5][1]

            cv2.circle(image, (index_tip_x, index_tip_y), 10, (0, 0, 255), -1)
            cv2.circle(image, (thumb_tip_x, thumb_tip_y), 10, (0, 0, 255), -1)

            if thumb_tip_x > index_base_x - 20:
                if not hacer_clic_derecho:
                    print("Right click")
                    pyautogui.rightClick()
                    hacer_clic_derecho = True
            else:
                hacer_clic_derecho = False

            if index_tip_y > index_base_y - 30:
                if not hacer_clic_izquierdo:
                    print("Left click")
                    pyautogui.click()
                    hacer_clic_izquierdo = True
            else:
                hacer_clic_izquierdo = False

        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

video.release()
cv2.destroyAllWindows()

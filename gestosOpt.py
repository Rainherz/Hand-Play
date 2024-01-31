import cv2
import mediapipe as mp
import time
from directkeys import right_pressed, left_pressed, up_pressed, down_pressed
from directkeys import PressKey, ReleaseKey
import math
from CerrarPrograma import cerrar_programas
from procesos import nombres_procesos

count_gesture_close = 0

# Define una estructura para el estado del gesto
class GestureState:
    def __init__(self):
        self.last_direction = ""
        self.last_key = 0

# Inicializa el estado del gesto
gesture_state = GestureState()

# Función para calcular la distancia entre dos puntos
def calculate_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Función para obtener el ángulo y la distancia entre dos puntos
def get_angle_and_distance(center, target):
    angle = math.atan2(target[1] - center[1], target[0] - center[0])
    angle_deg = math.degrees(angle)
    distance = calculate_distance(center, target)
    return angle_deg, distance

# Función para procesar el gesto de la mano
def process_hand_gesture(image, lmList, current_key_pressed, gesture_threshold):
    global count_gesture_close
    keyPressed = False
    key_count = 0
    key_pressed = 0

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
    #------------------------
    # Lógica para la dirección del gesto
    index_finger_x, index_finger_y = lmList[8][1], lmList[8][2]
    middle_finger_pip_y, middle_finger_tip_y = lmList[10][2], lmList[12][2]
    reference_x, reference_y = lmList[0][1], lmList[0][2]
    distance = calculate_distance((index_finger_x, index_finger_y), (reference_x, reference_y))
    angle_deg, distance = get_angle_and_distance((reference_x, reference_y), (index_finger_x, index_finger_y))

    if distance > gesture_threshold:
        if middle_finger_tip_y < middle_finger_pip_y - 30:
            new_direction, new_key = "ABAJO", down_pressed
        elif -60 < angle_deg < 45:
            new_direction, new_key = "DERECHA", right_pressed
        elif -120 < angle_deg <= -60:
            new_direction, new_key = "ARRIBA", up_pressed
        elif -225 < angle_deg <= -120:
            new_direction, new_key = "IZQUIERDA", left_pressed
        elif middle_finger_tip_y < middle_finger_pip_y - 30:
            new_direction, new_key = "ABAJO", down_pressed
        else:
            new_direction, new_key = "", 0

        # Verificar si hay una transición de gesto
        if new_direction != gesture_state.last_direction:
            print(f"Cambio de {gesture_state.last_direction} a {new_direction}")

        # Actualizar el estado del gesto
        gesture_state.last_direction = new_direction
        gesture_state.last_key = new_key

        # Realizar acciones basadas en el historial de gestos
        if gesture_state.last_direction == "IZQUIERDA" and new_direction == "ABAJO":
            print("Realizar acción específica de transición de IZQUIERDA a ABAJO")

        cv2.putText(image, new_direction, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        PressKey(new_key)
        current_key_pressed.add(new_key)
        key_pressed = new_key
        keyPressed = True
        key_count += 1
    else:
        # Si la distancia es menor que el umbral, liberar todas las teclas
        cv2.putText(image, "", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        for key in current_key_pressed:
            ReleaseKey(key)

    for key in current_key_pressed:
        ReleaseKey(key)

    return keyPressed, key_count, key_pressed

# Configuración inicial
time.sleep(2.0)
current_key_pressed = set()
gesture_threshold = 30
mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands
video = cv2.VideoCapture(0)

# Bucle principal
with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = video.read()
        frame_height, frame_width, _ = image.shape
        # image = cv2.flip(image, 1)

        # Para la lógica de la dirección
        keyPressed = False
        key_count = 0
        key_pressed = 0

        lmList = []
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            myHands = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHands.landmark):
                cx, cy = int(lm.x * frame_width), int(lm.y * frame_height)
                lmList.append([id, cx, cy])
            mp_draw.draw_landmarks(image, myHands, mp_hand.HAND_CONNECTIONS)

        # POR GESTOS (pero las teclas a veces no se liberan)
        if len(lmList) != 0:
            keyPressed, key_count, key_pressed = process_hand_gesture(image, lmList, current_key_pressed, gesture_threshold)

        # Liberar las teclas si no se presionó ninguna
        if not keyPressed and current_key_pressed:
            for key in current_key_pressed:
                ReleaseKey(key)
            current_key_pressed.clear()

        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

# Liberar recursos después de salir del bucle
video.release()
cv2.destroyAllWindows()

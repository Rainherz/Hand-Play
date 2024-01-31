# sector.py
import cv2
import mediapipe as mp
from directkeys import right_pressed, left_pressed, up_pressed, down_pressed, b_pressed
from directkeys import PressKey, ReleaseKey
import time
from CerrarPrograma import cerrar_programas
from procesos import nombres_procesos

count_gesture_close = 0

# Función para dibujar elementos estáticos en la pantalla
def draw_static_elements(image, frame_width, frame_height):
    color = (0, 0, 0)
    thickness = 2

    # Dibujar líneas horizontales
    cv2.line(image, (0, 2 * frame_height // 3), (frame_width, 2 * frame_height // 3), color, thickness)
    cv2.line(image, (0, frame_height // 3), (frame_width, frame_height // 3), color, thickness)

    # Dibujar líneas verticales
    cv2.line(image, (2 * frame_width // 5, frame_height // 3), (2 * frame_width // 5, 2 * frame_height // 3), color, thickness)
    cv2.line(image, (3 * frame_width // 5, frame_height // 3), (3 * frame_width // 5, 2 * frame_height // 3), color, thickness)

    # Agregar textos estáticos
    directions = ["UP", "DOWN", "LEFT", "RIGHT"]
    positions = [(frame_width // 2, frame_height // 6), (frame_width // 2, 5 * frame_height // 6),
                 (frame_width // 6, frame_height // 2), (5 * frame_width // 6, frame_height // 2)]

    for direction, position in zip(directions, positions):
        cv2.putText(image, direction, position, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3, cv2.LINE_AA)

# Función para resaltar una zona rectangular en la imagen
def draw_highlighted_zone(image, x1, y1, x2, y2, color, alpha):
    overlay = image.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)  # -1 indica que el rectángulo debe estar relleno
    cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)     

# Función para procesar las manos detectadas en la imagen
def process_hands(image, frame_width, frame_height, last_key_press_times, key_delay):
    global current_key_pressed, count_gesture_close

    lmList = []
    key_pressed = 0
    keyPressed = False
    key_count = 0

    # (Código para procesar las posiciones de las manos y determinar las acciones a realizar)
    with mp_hand.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
        results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if results.multi_hand_landmarks:
            myHands = results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHands.landmark):
                cx, cy = int(lm.x * frame_width), int(lm.y * frame_height)
                lmList.append([id, cx, cy])
            mp_draw.draw_landmarks(image, myHands, mp_hand.HAND_CONNECTIONS)

    # Procesar acciones basadas en los landmarks de las manos
    if len(lmList) != 0:
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

        hand_x, hand_y = lmList[9][1], lmList[9][2]

        cv2.circle(image, (hand_x, hand_y), 15, (0, 255, 0), -1)

        vertical_threshold = frame_height // 3
        horizontal_threshold = frame_width // 5

        # Coordenadas del rectángulo que se va a resaltar
        color = (0, 255, 0)
        x1, y1, x2, y2 = 0, 0, 0, 0

        if hand_x < 2 * horizontal_threshold:
            key_pressed = left_pressed
            x1, y1, x2, y2 = 0, vertical_threshold, 2 * horizontal_threshold, 2 * vertical_threshold
        elif hand_x > 3 * horizontal_threshold:
            key_pressed = right_pressed
            x1, y1, x2, y2 = 3 * horizontal_threshold, vertical_threshold, frame_width, 2 * vertical_threshold

        # Determinar la dirección vertical
        if hand_y < vertical_threshold:
            key_pressed = up_pressed
            x1, y1, x2, y2 = 0, 0, frame_width, vertical_threshold
        elif hand_y > 2 * vertical_threshold:
            key_pressed = down_pressed
            x1, y1, x2, y2 = 0, 2 * vertical_threshold, frame_width, frame_height

        # Determinar si el puño está cerrado
        finger_states = [lmList[i][2] > lmList[i - 2][2] for i in tipIds[1:]]
        fist = all(finger_states)

        if fist:
            key_pressed = b_pressed
            color = (0, 0, 255)
            x1, y1, x2, y2 = 0, 0, frame_width, frame_height

        if key_pressed != 0:
            current_time = time.time()
            last_key_press_time = last_key_press_times.get(key_pressed, 0)

            if current_time - last_key_press_time >= key_delay:
                PressKey(key_pressed)
                current_key_pressed.add(key_pressed)
                keyPressed = True
                key_count += 1
                draw_highlighted_zone(image, x1, y1, x2, y2, color, 0.5)
                last_key_press_times[key_pressed] = current_time

    return keyPressed, key_count, key_pressed

# Función para liberar las teclas presionadas
def release_keys():
    global current_key_pressed

    for key in current_key_pressed:
        ReleaseKey(key)

    current_key_pressed = set()

# Bloque principal ejecutado solo si este script es ejecutado directamente
if __name__ == "__main__":
    time.sleep(1.0)
    current_key_pressed = set()

    mp_draw = mp.solutions.drawing_utils
    mp_hand = mp.solutions.hands

    tipIds = [4, 8, 12, 16, 20]

    video = cv2.VideoCapture(0)

    key_delay = 0.075  # Segundos de retraso entre pulsaciones
    last_key_press_times = {}  # Almacena el tiempo de la última pulsación para cada tecla

    while True:
        ret, image = video.read()
        frame_height, frame_width, _ = image.shape
        # image = cv2.flip(image, 1)

        draw_static_elements(image, frame_width, frame_height)

        keyPressed, key_count, key_pressed = process_hands(image, frame_width, frame_height, last_key_press_times, key_delay)

        # Lógica para liberar teclas si no se detectan acciones o si se detectan acciones específicas
        if not keyPressed and len(current_key_pressed) != 0:
            release_keys()
        elif key_count == 1 and len(current_key_pressed) == 2:
            for key in current_key_pressed:
                if key_pressed != key:
                    ReleaseKey(key)
            release_keys()

        # Mostrar la imagen en una ventana de visualización
        cv2.imshow("Frame", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break
    
    # Liberar recursos al finalizar el programa
    video.release()
    cv2.destroyAllWindows()
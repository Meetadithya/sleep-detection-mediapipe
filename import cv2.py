import cv2
import mediapipe as mp
import numpy as np
import threading
import pygame

# EAR threshold and frame count
EAR_THRESHOLD = 0.18
SLEEP_CONSEC_FRAMES = 20

# Alarm path (update if needed)
ALARM_PATH = r"C:\Users\Admin\Downloads\alarm_clock.wav"

# Initialize flags and counters
alarm_on = False
sleep_frame_counter = 0

# Initialize MediaPipe and webcam
mp_face_mesh = mp.solutions.face_mesh
vid = cv2.VideoCapture(0)
if not vid.isOpened():
    print("Unable to open camera")
    exit()

# Alarm thread
def play_alarm():
    global alarm_on
    pygame.mixer.init()
    pygame.mixer.music.load(ALARM_PATH)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    alarm_on = False

# Start Face Mesh detection
with mp_face_mesh.FaceMesh() as face_mesh:
    while True:
        ret, frame = vid.read()
        if not ret:
            print("Failed to capture frame.")
            break

        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb_frame)

        if result.multi_face_landmarks:
            landmarks = result.multi_face_landmarks[0].landmark

            def compute_ear(eye_points):
                p1 = np.array([eye_points[0].x * frame_width, eye_points[0].y * frame_height])
                p2 = np.array([eye_points[1].x * frame_width, eye_points[1].y * frame_height])
                p3 = np.array([eye_points[2].x * frame_width, eye_points[2].y * frame_height])
                p4 = np.array([eye_points[3].x * frame_width, eye_points[3].y * frame_height])
                p5 = np.array([eye_points[4].x * frame_width, eye_points[4].y * frame_height])
                p6 = np.array([eye_points[5].x * frame_width, eye_points[5].y * frame_height])
                vert1 = np.linalg.norm(p2 - p6)
                vert2 = np.linalg.norm(p3 - p5)
                hor = np.linalg.norm(p1 - p4)
                return (vert1 + vert2) / (2.0 * hor)

            left_eye_points = [landmarks[i] for i in [33, 160, 158, 133, 153, 144]]
            right_eye_points = [landmarks[i] for i in [362, 385, 387, 263, 373, 380]]
            left_ear = compute_ear(left_eye_points)
            right_ear = compute_ear(right_eye_points)
            avg_ear = (left_ear + right_ear) / 2.0

            if avg_ear < EAR_THRESHOLD:
                sleep_frame_counter += 1
                if sleep_frame_counter >= SLEEP_CONSEC_FRAMES:
                    cv2.putText(frame, "SLEEPING", (150, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
                    if not alarm_on:
                        alarm_on = True
                        threading.Thread(target=play_alarm).start()
            else:
                sleep_frame_counter = 0
                alarm_on = False

            # EAR display
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

            # Draw face mesh
            mp.solutions.drawing_utils.draw_landmarks(frame, result.multi_face_landmarks[0], mp_face_mesh.FACEMESH_TESSELATION)
            mp.solutions.drawing_utils.draw_landmarks(frame, result.multi_face_landmarks[0], mp_face_mesh.FACEMESH_LEFT_EYE)
            mp.solutions.drawing_utils.draw_landmarks(frame, result.multi_face_landmarks[0], mp_face_mesh.FACEMESH_RIGHT_EYE)
        else:
            print("No face detected.")

        # Add watermark
        watermark_text = "Made by Adithya"
        text_size = cv2.getTextSize(watermark_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_x = frame.shape[1] - text_size[0] - 10
        text_y = frame.shape[0] - 10
        cv2.putText(frame, watermark_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow("Sleep Detector", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

vid.release()
cv2.destroyAllWindows()
print("Program terminated.")

# Set environment variable to use python implementation for protobuf
import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

# Import libraries
import sys
import time
import cv2
import streamlit as st

try:
    import pyautogui
    import mediapipe as mp
    import screen_brightness_control as sbc
except ImportError as e:
    st.error(f"Error importing required libraries: {str(e)}")
    st.info("Please make sure all dependencies are correctly installed. You may need to restart the application.")
    st.stop()

def increase_volume():
    st.write("Increasing volume")

def decrease_volume():
    st.write("Decreasing volume")

def increase_brightness():
    st.write("Increasing brightness")

def decrease_brightness():
    st.write("Decreasing brightness")

# Initialize MediaPipe Hands
try:
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2,
                           min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_drawing = mp.solutions.drawing_utils
    st.success("MediaPipe initialized successfully")
except Exception as e:
    st.error(f"Error initializing MediaPipe: {str(e)}")
    st.info("This could be due to protobuf compatibility issues. Please try reinstalling the dependencies.")
    st.info("Try running: pip install protobuf==3.20.0 mediapipe==0.10.0")
    st.stop()

# Streamlit Title
st.title("Hand Gesture Controlled Volume and Brightness")

# Streamlit button to start/stop the camera
run = st.checkbox('Run')
FRAME_WINDOW = st.image([])

def calculate_distance(landmark1, landmark2):
    return ((landmark1.x - landmark2.x) ** 2 + (landmark1.y - landmark2.y) ** 2) ** 0.5

cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            if handedness.classification[0].label == 'Left':
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                index_thumb_distance = calculate_distance(index_finger_tip, thumb_tip)
                middle_thumb_distance = calculate_distance(middle_finger_tip, thumb_tip)

                threshold = 0.05

                if index_thumb_distance < threshold:
                    pyautogui.press('volumeup')
                    increase_volume()
                elif middle_thumb_distance < threshold:
                    pyautogui.press('volumedown')
                    decrease_volume()
            if handedness.classification[0].label == 'Right':
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                middle_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

                index_thumb_distance = calculate_distance(index_finger_tip, thumb_tip)
                middle_thumb_distance = calculate_distance(middle_finger_tip, thumb_tip)

                threshold = 0.05  

                if index_thumb_distance < threshold:
                    k = sbc.get_brightness()
                    sbc.set_brightness(k[0] + 1, display=0)
                    increase_brightness()
                elif middle_thumb_distance < threshold:
                    k = sbc.get_brightness()
                    sbc.set_brightness(k[0] - 1, display=0)
                    decrease_brightness()

        FRAME_WINDOW.image(frame, channels='BGR')

cap.release()
cv2.destroyAllWindows()

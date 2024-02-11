from flask import Flask, render_template, request, redirect
from datetime import datetime
import os
import threading
import time
import pyautogui
import cv2
import numpy as np
import atexit

app = Flask(__name__, template_folder='templates')

# Global variables
mouse_coordinates = []
eye_coordinates = []
tracking_active = False

# Function to track mouse coordinates
def track_mouse():
    global mouse_coordinates, tracking_active
    while tracking_active:
        # Get mouse coordinates using pyautogui
        x, y = pyautogui.position()
        
        # Append the coordinates with timestamp to the list
        timestamp = time.time()
        mouse_coordinates.append((timestamp, x, y))
        
        # Sleep for 5 seconds
        time.sleep(5)

# Function to track eye coordinates using OpenCV
def track_eye():
    global eye_coordinates, tracking_active
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    cap = cv2.VideoCapture(0)  # Change the index if using a different camera

    while tracking_active:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in eyes:
            eye_x = x + w // 2
            eye_y = y + h // 2
            timestamp = time.time()
            eye_coordinates.append((timestamp, eye_x, eye_y))

        time.sleep(5)

    cap.release()

# Start tracking mouse coordinates in a separate thread
def start_mouse_tracking():
    global tracking_active
    tracking_active = True
    mouse_tracking_thread = threading.Thread(target=track_mouse)
    mouse_tracking_thread.start()

# Start tracking eye coordinates in a separate thread
def start_eye_tracking():
    global tracking_active
    tracking_active = True
    eye_tracking_thread = threading.Thread(target=track_eye)
    eye_tracking_thread.start()

# Stop tracking mouse coordinates
def stop_mouse_tracking():
    global tracking_active
    tracking_active = False

# Stop tracking eye coordinates
def stop_eye_tracking():
    global tracking_active
    tracking_active = False

# Save mouse coordinates to a text file
def save_mouse_coordinates():
    file_path = 'data/mousetracking/mouse_data.txt'  # Replace with your desired file path
    with open(file_path, 'w') as f:
        for timestamp, x, y in mouse_coordinates:
            f.write(f'{timestamp},{x},{y}\n')

# Save eye coordinates to a text file
def save_eye_coordinates():
    file_path = 'data/eyetracking/eye_data.txt'  # Replace with your desired file path
    with open(file_path, 'w') as f:
        for timestamp, x, y in eye_coordinates:
            f.write(f'{timestamp},{x},{y}\n')

@app.route('/')
def list_viewer():
    return render_template('list_view.html')

@app.route('/my_pdf')
def my_pdf():
    start_eye_tracking()
    start_mouse_tracking()
    return render_template('/my_pdf/my_pdf_viewer.html')

@app.route('/start_tracking', methods=['POST'])
def start_tracking():
    #start_mouse_tracking()
    #start_eye_tracking()
    return {'status': 'success'}, 200

@app.route('/time_spent', methods=['POST'])
def time_spent():
    duration = request.form.get('duration')
    open_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('data/timespent/time_data.txt', 'a') as f:
        f.write(f'Window was opened at: {open_time}, Duration: {duration}\n')

    stop_mouse_tracking()
    stop_eye_tracking()

    return {'status': 'success'}, 200

# Register functions to save coordinates when the app exits
atexit.register(save_mouse_coordinates)
atexit.register(save_eye_coordinates)

if __name__ == '__main__':
    app.run(debug=True)
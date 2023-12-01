from flask import Flask, render_template, request
from datetime import datetime
import os
import threading
import time
import pyautogui
import atexit

app = Flask(__name__, template_folder='templates')

# Global variables
mouse_coordinates = []
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

# Start tracking mouse coordinates in a separate thread
def start_mouse_tracking():
    global tracking_active
    tracking_active = True
    mouse_tracking_thread = threading.Thread(target=track_mouse)
    mouse_tracking_thread.start()

# Stop tracking mouse coordinates
def stop_mouse_tracking():
    global tracking_active
    tracking_active = False


# Save mouse coordinates to a text file
def save_mouse_coordinates():
    file_path = 'data/mousetracking/mouse_data.txt'  # Replace with your desired file path
    with open(file_path, 'w') as f:
        for timestamp, x, y in mouse_coordinates:
            f.write(f'{timestamp},{x},{y}\n')


@app.route('/')
def list_viewer():
    return render_template('list_view.html')

@app.route('/my_pdf')
def my_pdf():
    start_mouse_tracking()
    return render_template('/my_pdf/my_pdf_viewer.html')




@app.route('/start_tracking', methods=['POST'])
def start_tracking():
    global tracking
    tracking = True
    # Start the mouse tracking in a separate thread
    threading.Thread(target=track_mouse, args=(tracking,)).start()
    return {'status': 'success'}, 200

@app.route('/time_spent', methods=['POST'])
def time_spent():
    duration = request.form.get('duration')
    open_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('data/timespent/time_data.txt', 'a') as f:
        f.write(f'Window was opened at: {open_time}, Duration: {duration}\n')

    return {'status': 'success'}, 200

# Route to stop mouse tracking
@app.route('/stop_tracking', methods=['POST'])
def stop_tracking():
    # Stop tracking mouse coordinates
    stop_mouse_tracking()
    return redirect('/')

# Register function to save coordinates when the app exits
atexit.register(save_mouse_coordinates)





if __name__ == '__main__':
    app.run(debug=True)

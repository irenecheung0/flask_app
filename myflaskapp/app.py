from flask import Flask, render_template, request
from datetime import datetime
import os
import threading
from eye_tracker import track_eyes  # Import the track_eyes function

app = Flask(__name__, template_folder='templates')

# Variable to control the eye tracking loop
tracking = False

@app.route('/')
def pdf_viewer():
    return render_template('pdf_viewer.html')

@app.route('/start_tracking', methods=['POST'])
def start_tracking():
    global tracking
    tracking = True
    # Start the eye tracking in a separate thread
    threading.Thread(target=track_eyes, args=(tracking,)).start()
    return {'status': 'success'}, 200

@app.route('/stop_tracking', methods=['POST'])
def stop_tracking():
    global tracking
    tracking = False
    return {'status': 'success'}, 200

@app.route('/time_spent', methods=['POST'])
def time_spent():
    duration = request.form.get('duration')
    open_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('data/timespent/time_data.txt', 'a') as f:
        f.write(f'Window was opened at: {open_time}, Duration: {duration}\n')

    return {'status': 'success'}, 200

if __name__ == '__main__':
    app.run(debug=True)

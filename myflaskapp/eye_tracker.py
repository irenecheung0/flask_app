# import cv2
# from datetime import datetime

# # Load the pre-trained haarcascade eye detector from OpenCV
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# def track_eyes(tracking):
#     # Start video capture
#     cap = cv2.VideoCapture(0)

#     while tracking:
#         # Read frame from video capture
#         ret, frame = cap.read()

#         if ret:
#             # Convert color image to grayscale
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#             # Detect eyes in the image
#             eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

#             # For each detected eye
#             for (ex, ey, ew, eh) in eyes:
#                 # Draw a rectangle around the eye
#                 cv2.rectangle(frame, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

#                 # Write the time and coordinates to a text file
#                 with open('data/timespent/eye_data.txt', 'a') as f:
#                     f.write(f'Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}, Coordinates: {(ex, ey, ew, eh)}\n')

#             # Display the resulting frame
#             cv2.imshow('Eye Tracker', frame)

#         # Break the loop on 'q' key press
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break

#     # Release the video capture and close windows
#     cap.release()
#     cv2.destroyAllWindows()

import cv2
from time import time
import numpy as np
from ultralytics.solutions.solutions import BaseSolution
from ultralytics.utils.plotting import Annotator, colors
from datetime import datetime
import requests
from paddleocr import PaddleOCR


class SpeedEstimator(BaseSolution):
    def __init__(self, api_url, **kwargs):
        super().__init__(**kwargs)
        self.initialize_region()  # Initialize speed region
        self.spd = {}  # Dictionary to store speed data
        self.trkd_ids = []  # List for already tracked and speed-estimated IDs
        self.trk_pt = {}  # Dictionary for previous timestamps
        self.trk_pp = {}  # Dictionary for previous positions
        self.logged_ids = set()  # Set to keep track of already logged IDs

        # Initialize the OCR system
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

        # API URL
        self.api_url = api_url

    def perform_ocr(self, image_array):
        """Performs OCR on the given image and returns the extracted text."""
        if image_array is None:
            raise ValueError("Image is None")
        if isinstance(image_array, np.ndarray):
            results = self.ocr.ocr(image_array, rec=True)
        else:
            raise TypeError("Input image is not a valid numpy array")
        return ' '.join([result[1][0] for result in results[0]] if results[0] else "")

    def send_to_django_api(self, date, time, track_id, class_name, speed, numberplate):
        """Send data to the Django API endpoint."""
        data = {
            "date": date,
            "time": time,
            "track_id": track_id,
            "class_name": class_name,
            "speed": speed,
            "numberplate": numberplate
        }
        try:
            response = requests.post(self.api_url, json=data)
            if response.status_code == 201:
                print(f"Data sent successfully: {response.json()}")
            else:
                print(f"Failed to send data: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"Error sending data to API: {e}")

    def estimate_speed(self, im0):
        """Estimate speed of objects and track them."""
        self.annotator = Annotator(im0, line_width=self.line_width)  # Initialize annotator
        self.extract_tracks(im0)  # Extract tracks

        # Get current date and time
        current_time = datetime.now()

        for box, track_id, cls in zip(self.boxes, self.track_ids, self.clss):
            self.store_tracking_history(track_id, box)  # Store track history

            if track_id not in self.trk_pt:
                self.trk_pt[track_id] = 0
            if track_id not in self.trk_pp:
                self.trk_pp[track_id] = self.track_line[-1]

            speed_label = f"{int(self.spd[track_id])} km/h" if track_id in self.spd else self.names[int(cls)]

            # Draw the bounding box and track ID on it
            label = f"ID: {track_id} {speed_label}"  # Show track ID along with speed
            self.annotator.box_label(box, label=label, color=colors(track_id, True))  # Draw bounding box

            # Speed and direction calculation
            if self.LineString([self.trk_pp[track_id], self.track_line[-1]]).intersects(self.r_s):
                direction = "known"
            else:
                direction = "unknown"

            # Calculate speed if the direction is known and the object is new
            if direction == "known" and track_id not in self.trkd_ids:
                self.trkd_ids.append(track_id)
                time_difference = time() - self.trk_pt[track_id]
                if time_difference > 0:
                    speed = np.abs(self.track_line[-1][1].item() - self.trk_pp[track_id][1].item()) / time_difference
                    self.spd[track_id] = round(speed)

            # Update the previous tracking time and position
            self.trk_pt[track_id] = time()
            self.trk_pp[track_id] = self.track_line[-1]
            x1, y1, x2, y2 = map(int, box)  # Convert box coordinates to integers
            cropped_image = np.array(im0)[y1:y2, x1:x2]
            ocr_text = self.perform_ocr(cropped_image)

            # Get the class name and speed
            class_name = self.names[int(cls)]
            speed = self.spd.get(track_id)

            # Ensure OCR text is not empty and send data to the Django API if not already logged
            if track_id not in self.logged_ids and ocr_text.strip() and speed is not None:
                self.send_to_django_api(
                    current_time.strftime("%Y-%m-%d"),
                    current_time.strftime("%H:%M:%S"),
                    track_id,
                    class_name,
                    speed if speed is not None else 0.0,
                    ocr_text
                )
                self.logged_ids.add(track_id)

        self.display_output(im0)  # Display output with base class function
        return im0


# Open the video file
cap = cv2.VideoCapture('video.mp4')

# Define region points for counting
region_points = [(0, 145), (1018, 145)]

# Initialize the object counter with the API URL
api_url = "http://127.0.0.1:8000/speed-records/"  # Replace with your Django API endpoint
speed_obj = SpeedEstimator(
    api_url=api_url,
    region=region_points,
    model="car.pt",  # Replace with your YOLO model file
    line_width=2
)

count = 0

while True:
    # Read a frame from the video
    ret, frame = cap.read()
    if not ret:
        break

    count += 1
    if count % 3 != 0:  # Skip odd frames
        continue

    frame = cv2.resize(frame, (720, 500))

    # Process the frame with the object counter
    result = speed_obj.estimate_speed(frame)

    # Show the frame
    cv2.imshow("RGB", result)
    if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

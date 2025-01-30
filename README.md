🚗 Vehicle Speed Detection & Tracking with Django Dashboard

This project is an advanced Vehicle Speed Detection and Tracking System using YOLO, OpenCV, and PaddleOCR, integrated with a Django-powered dashboard for real-time monitoring. It detects vehicles from a video stream, estimates their speed, extracts number plates using OCR, and sends the data to a Django API. The data is then displayed on an interactive dashboard with analytics.
✨ Features

✅ Real-time Vehicle Detection & Speed Estimation using YOLO and OpenCV
✅ OCR-based Number Plate Recognition with PaddleOCR
✅ Django API Integration to store speed records
✅ Attractive Dashboard for data visualization (total vehicles, top speeders, violations, etc.)
✅ Custom Speed Limit Monitoring to detect overspeeding vehicles
📌 Installation Guide
1️⃣ Clone the Repository

git clone  https://github.com/asifkhan-hub/Real-Time-Vehicle-Speed-Detection-Tracking-with-Yolov11-Django

2️⃣ Install Dependencies

pip install -r requirements.txt  

3️⃣ Run Vehicle Detection

To start the vehicle detection system, run:

python run.py  

4️⃣ Start Django Server

Open a new terminal, navigate to the Django project folder, and run:

cd pro  # Change directory to Django backend  
python manage.py runserver  

5️⃣ View the Dashboard

Now, open your browser and go to:

http://127.0.0.1:8000/

Here, you can see real-time speed tracking, total vehicle counts, violations, and more!
🖥️ Dashboard Features

📊 Total Vehicles Tracked
⚡ Average Speed of Vehicles
🏎️ Top 5 Fastest Vehicles
🚨 Speed Violations (Above Threshold)
🕒 Vehicle Counts by Time of Day (Morning, Afternoon, Evening)
📈 Speed Distribution Analysis
📷 Screenshots
![image](https://github.com/user-attachments/assets/a9a60240-d70b-4429-b309-df5205c9753a)

🚀 Future Enhancements

🔹 Live Streaming Support for Real-Time Road Monitoring
🔹 More Advanced Data Analytics & AI-based Traffic Insights

This project is perfect for traffic surveillance, law enforcement, and smart city applications 🚦🚓.

📩 Contributions & Feedback are Welcome! 😃

# ANPR-alert-system
This project aims to develop an Automatic Number Plate Recognition (ANPR) and Alert System that enhances security and streamlines vehicle entry/exit verification at checkpoints. The system captures vehicle images, detects and reads number plates using computer vision and OCR techniques, verifies the registration numbers against a database, and sends SMS alerts to vehicle owners. The application is built using Python and integrates several powerful libraries and APIs for efficient and accurate performance.

# Key Features
Real-time Number Plate Detection: Utilizes OpenCV's Haar Cascade Classifier to detect number plates from vehicle images.
Optical Character Recognition (OCR): Employs Tesseract-OCR to convert detected number plate images into text.
Database Integration: Connects to a MySQL database to store and verify registration numbers against authorized entries.
SMS Notifications: Sends real-time SMS alerts to vehicle owners using the Twilio API upon successful verification.
User-Friendly Interface: Provides an easy-to-use GUI built with Tkinter for image selection, processing, and result display.
Live Tracking: Supports live video feed processing for continuous number plate detection and verification.

# Modules
User Interface (UI): Developed with Tkinter to provide a seamless user experience for image selection, processing, and result display.
Plate Detection: Uses OpenCV and a pre-trained Haar Cascade Classifier to detect number plates in captured images.
Image to Text Processing: Utilizes Tesseract-OCR to extract text from detected number plates and stores the text in a file.
Database Integration: Connects to a MySQL database to fetch and verify registration numbers, ensuring only authorized vehicles are granted access.
SMS Sending: Integrates Twilio API to send SMS notifications to vehicle owners upon successful verification of registration numbers.

#Workflow
Image Capture: Capture vehicle number plate image.
Plate Detection: Detect number plates in the image using OpenCV.
Text Extraction: Convert detected number plate images to text using Tesseract-OCR.
Database Verification: Verify extracted text against the MySQL database.
SMS Notification: Send SMS alert to the registered vehicle owner if a match is found.

# Requirements
Python 3.x
OpenCV
Tesseract-OCR
MySQL
Twilio API
Tkinter
Pillow (PIL Fork)

# Setup Instructions
Clone the Repository: git clone https://github.com/Sudharsanv151/anpr-alert-system.git
Install Dependencies: pip install -r requirements.txt
Database Setup: Configure MySQL database and update connection details in the script.
Run the Application: Execute the main script to launch the ANPR system.


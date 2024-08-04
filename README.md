# AUTOMATIC NUMBER PLATE RECOGNITION AND ALERT SYSTEM

This project aims to develop an Automatic Number Plate Recognition (ANPR) and Alert System for enhanced security and streamlined vehicle verification at checkpoints. The system captures vehicle images, detects and reads number plates using computer vision and OCR, verifies registration numbers against a database, and sends SMS alerts to vehicle owners. Built with Python, it integrates powerful libraries and APIs for efficient performance.

## Key Features:
- Real-time number plate detection using OpenCV's Haar Cascade Classifier.
- OCR with Tesseract to convert number plate images to text.
- MySQL database integration for verifying registration numbers.
- Real-time SMS notifications via Twilio API.
- User-friendly Tkinter GUI for image selection, processing, and display.
- Live tracking for continuous detection and verification.

## Modules:
- UI: Tkinter-based interface.
- Plate Detection: OpenCV and Haar Cascade Classifier.
- OCR: Tesseract for text extraction.
- Database: MySQL for data management.
- SMS: Twilio API for notifications.

## Workflow:
1. Capture vehicle image.
2. Detect number plate using OpenCV.
3. Convert plate image to text with Tesseract.
4. Verify text against MySQL database.
5. Send SMS alert via Twilio.

## Requirements:
- Python 3.x
- OpenCV
- Tesseract-OCR
- MySQL
- Twilio API
- Tkinter
- Pillow

## Screenshots:
![ui](https://github.com/user-attachments/assets/efb1e664-83e3-4fe7-9ff2-09e85172b670)

![allow car](https://github.com/user-attachments/assets/a1a1e8ac-b476-4949-9ed7-57eed16551bd)

![inspect car](https://github.com/user-attachments/assets/18596aaf-1464-4bee-b630-b05cff24c973)

![Text file](https://github.com/user-attachments/assets/9403851f-cf03-4013-834a-264cf8d97b98)

![SMS received](https://github.com/user-attachments/assets/f2a7aee6-a70f-40eb-9ef5-2fc76b8787d0)


Database:
![DB](https://github.com/user-attachments/assets/ea5d452b-9ac3-41c7-b74d-2848d382cecd)

![DB structure](https://github.com/user-attachments/assets/c72cd3af-f731-43f1-9358-17f960a00a1c)


## Setup Instructions:
1. Clone the repository: `git clone https://github.com/Sudharsanv151/ANPR-alert-system.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure MySQL database.
4. Run the application.

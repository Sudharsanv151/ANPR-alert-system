# AUTOMATIC NUMBER PLATE RECOGNITION AND ALERT SYSTEM

Automatic Number Plate Recognition (ANPR) and Alert System offers enhanced security and streamlined vehicle verification at entry/exit gates. The system captures vehicle images, detects and reads number plates using computer vision and OCR, verifies registration numbers against a database, and sends SMS alerts to vehicle owners.

## Key Features
- Real-time number plate detection using OpenCV's Haar Cascade Classifier.
- OCR with Tesseract to convert number plate images to text.
- MySQL database integration for verifying registration numbers.
- Real-time SMS notifications via Twilio API.
- User-friendly Tkinter GUI for image selection, processing, and display.
- Live tracking for continuous detection and verification.
  
## Workflow
1. Capture vehicle image.
2. Detect number plate using OpenCV.
3. Convert plate image to text with Tesseract.
4. Verify text against MySQL database.
5. Send SMS alert via Twilio.

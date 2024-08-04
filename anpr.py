import cv2
import os
import pytesseract
import mysql.connector
from twilio.rest import Client
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

harcascade = "model/haarcascade_russian_plate_number.xml"
min_area = 500
plates_dir = r"D:\ANPR\plates"
text_file_path = r"D:\ANPR\car_numbers.txt"

SID = 'your_sid'
token = 'your_token_number'
twilio_client = Client(SID, token)

def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="anpd"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL database: {err}")
        return None

def compare_registration_number(registration_number):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            
            normalized_registration_number = registration_number.replace(" ", "").upper()
            query = "SELECT mobile_number FROM registrations WHERE UPPER(REPLACE(registration_number, ' ', '')) = %s"
            cursor.execute(query, (normalized_registration_number,))
            result = cursor.fetchone()
            if result:
                phone_number = result[0]
                sms_status = send_sms(phone_number)
                return f"Match found for registration number: {registration_number}\nAllow this car!!\n{sms_status}", True
            else:
                return f"No match found for registration number: {registration_number}\nInspect the car!!", False
        except mysql.connector.Error as err:
            return f"Error querying database: {err}", False
        finally:
            cursor.close()
            conn.close()
    else:
        return "Failed to connect to the database.", False

def send_sms(phone_number):
    try:
        message = twilio_client.messages.create(
            body="Your car exits the Apartment",
            from_='mobile_number',
            to=phone_number
        )
        if message.sid:
            return f"SMS sent to the owner successfully"
    except Exception as e:
        return f"Error sending SMS: {e}"

def process_image(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    plate_cascade = cv2.CascadeClassifier(harcascade)
    plates = plate_cascade.detectMultiScale(img_gray, 1.1, 4)

    count = 0
    for (x, y, w, h) in plates:
        area = w * h
        if area > min_area:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Number Plate", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 0, 255), 2)
            img_roi = img[y: y + h, x: x + w]

            if not os.path.exists(plates_dir):
                os.makedirs(plates_dir)
            roi_path = os.path.join(plates_dir, f"scanned_img_{count}.jpg")
            cv2.imwrite(roi_path, img_roi)
            count += 1

    return count, img

class ANPR_GUI:
    def __init__(self, master):
        self.master = master
        master.title("Automatic Number Plate Recognition & Alert System")
        master.geometry("800x600")
        master.configure(bg='#f0f0f0')

        style = ttk.Style()
        style.theme_use('clam')

        main_frame = ttk.Frame(master, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        master.columnconfigure(0, weight=1)
        master.rowconfigure(0, weight=1)

        self.label = ttk.Label(main_frame, text="Automatic Number Plate Recognition and Alert System", font=('Helvetica', 14))
        self.label.grid(row=0, column=0, columnspan=4, pady=10)

        self.select_button = ttk.Button(main_frame, text="Select Image", command=self.select_image)
        self.select_button.grid(row=1, column=0, pady=5, padx=5, sticky='ew')

        self.process_button = ttk.Button(main_frame, text="Process Image", command=self.process_image)
        self.process_button.grid(row=1, column=1, pady=5, padx=5, sticky='ew')

        self.live_button = ttk.Button(main_frame, text="Start Live Tracking", command=self.start_live_tracking)
        self.live_button.grid(row=1, column=2, pady=5, padx=5, sticky='ew')

        self.stop_button = ttk.Button(main_frame, text="Stop Live Tracking", command=self.stop_live_tracking, state='disabled')
        self.stop_button.grid(row=1, column=3, pady=5, padx=5, sticky='ew')

        self.image_label = ttk.Label(main_frame)
        self.image_label.grid(row=2, column=0, columnspan=4, pady=10)

        self.result_text = tk.Text(main_frame, height=10, width=60, wrap=tk.WORD, font=('Helvetica', 10))
        self.result_text.grid(row=3, column=0, columnspan=4, pady=10, padx=5, sticky='nsew')

        scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=self.result_text.yview)
        scrollbar.grid(row=3, column=4, sticky='ns')
        self.result_text['yscrollcommand'] = scrollbar.set

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(2, weight=1)
        main_frame.columnconfigure(3, weight=1)
        main_frame.rowconfigure(3, weight=1)

        self.selected_image_path = None
        self.is_tracking = False

    def select_image(self):
        self.selected_image_path = filedialog.askopenfilename()
        if self.selected_image_path:
            image = Image.open(self.selected_image_path)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

    def process_image(self):
        if not self.selected_image_path:
            messagebox.showerror("Error", "Please select an image first")
            return

        img = cv2.imread(self.selected_image_path)
        if img is None:
            messagebox.showerror("Error", "Could not load image")
            return

        count, processed_img = process_image(img)

        if count == 0:
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert(tk.END, "No plates detected.")
            return

        results = []
        for i in range(count):
            roi_image_path = os.path.join(plates_dir, f"scanned_img_{i}.jpg")
            text = pytesseract.image_to_string(roi_image_path).strip()

            if text:
                with open(text_file_path, "a") as file:
                    file.write(text + "\n")

                result, match_found = compare_registration_number(text)
                results.append(f"Plate {i+1}: {text}\n{result}\n")
                
                # Highlight the plate on the image
                color = (0, 255, 0) if match_found else (0, 0, 255)
                cv2.rectangle(processed_img, (0, 0), (processed_img.shape[1], processed_img.shape[0]), color, 5)
            else:
                results.append(f"No text detected in scanned_img_{i}.jpg\n")
            
            os.remove(roi_image_path)
        
        self.result_text.delete('1.0', tk.END)
        self.result_text.insert(tk.END, "\n".join(results))
        
        # Display processed image
        processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        processed_image = Image.fromarray(processed_img)
        processed_image.thumbnail((400, 400))
        photo = ImageTk.PhotoImage(processed_image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def start_live_tracking(self):
        self.is_tracking = True
        self.live_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.live_tracking()

    def stop_live_tracking(self):
        self.is_tracking = False
        self.live_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def live_tracking(self):
        if not self.is_tracking:
            return

        cap = cv2.VideoCapture(0)
        cap.set(3, 640)
        cap.set(4, 480)

        while self.is_tracking:
            success, img = cap.read()
            if not success:
                messagebox.showerror("Error", "Failed to capture frame from camera")
                break

            count, processed_img = process_image(img)

            if count > 0:
                for i in range(count):
                    roi_image_path = os.path.join(plates_dir, f"scanned_img_{i}.jpg")
                    text = pytesseract.image_to_string(roi_image_path).strip()

                    if text:
                        with open(text_file_path, "a") as file:
                            file.write(text + "\n")

                        result, match_found = compare_registration_number(text)
                        self.result_text.insert(tk.END, f"Plate detected: {text}\n{result}\n")
                        self.result_text.see(tk.END)

                        # Highlight the plate on the image
                        color = (0, 255, 0) if match_found else (0, 0, 255)
                        cv2.rectangle(processed_img, (0, 0), (processed_img.shape[1], processed_img.shape[0]), color, 5)

                    os.remove(roi_image_path)

            # Display processed image
            processed_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
            processed_image = Image.fromarray(processed_img)
            processed_image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(processed_image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

            self.master.update()

        cap.release()

root = tk.Tk()
my_gui = ANPR_GUI(root)
root.mainloop()
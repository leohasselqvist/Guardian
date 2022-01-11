import threading
import cv2
import string
import socket
import sys
import threading
import easyocr_model as ocr

#  DENNA KODEN KÖR PÅ RASPBERRY PI:n


# DEBUG VARIABLES (they look nice)


parked_cars = []

HOST = 'localhost'  # The server's hostname or IP address
PORT = 11417        # The port used by the server


def __main__():
    if "-n" not in sys.argv:  # If -n in not args, proceed with network
        print("[NET] NET setup initiated.")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            for attempts in range(1, 101):
                try:
                    s.connect((HOST, PORT))
                    print("[NET] Connection established.")
                    s.send("c".encode('utf-8'))  # Server verification for camera.
                    running = True
                    while running:
                        running = ocr_cycle(s=s)
                        attempts = 0
                except ConnectionRefusedError:
                    print(f"[NET] Connection attempt #{attempts}")
            else:
                print("[NET] Timed out")
    else:
        print("[NET] Ignoring NET setup")
        run_ocr()


def run_ocr():
    print("[OCR] Starting OCR...")
    ocr_result = True
    while ocr_result:
        ocr_result = ocr_cycle()


def ocr_cycle(s=None):
    text = ocr.bounding_box_visualizer(debug_text=str(parked_cars))
    if cv2.waitKey(1) & 0xFF == ord("q"):  # If q is pressed...
        if s:
            s.close()  # Close connection.
        return False  # Failed cycle, interrupted by keyboard stroke
    for car in parked_cars:
        if car not in text:
            print(f"[OCR] {car} left. ")
            parked_cars.remove(car)
            if s:  # If networking is enabled
                print("[NET] Removing from server...")
                s.send((car + ".0").encode('utf-8'))
    for entry in text:
        if ocr.verify_reg(entry):  # If the entry is a car
            print(f"[OCR] {entry} identified.")
            if entry not in parked_cars:
                print(f"[OCR] {entry} found.")
                parked_cars.append(entry)
                if s:
                    print("[NET] Adding to server...")
                    s.send((entry + ".1").encode('utf-8'))
    return True  # Completed cycle


if __name__ == "__main__":
    __main__()

import easyocr_model as ocr
import threading
import cv2
import string
import socket
import sys
import threading

#  DENNA KODEN KÖR PÅ RASPBERRY PI:n

paid_cars = []
parked_cars = {}  # KEY: str | VALUE: bool (verified or nah)


def __main__():
    if "-n" not in sys.argv:  # If -n in args, ignore networking setup
        print("[NET] Starting server...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 11417))
            s.listen()
            print("[NET] Listening for client...")
            conn, addr = s.accept()
            with conn:
                print(f'[NET] Client accepted {addr[0]}')
                while True:
                    data = conn.recv(1024).decode('utf-8')
                    print(f"[NET] Received {data}")
                    if not data:
                        break
                    conn.sendall("ok".encode('utf-8'))
    else:
        print("[NET] Ignoring NET setup")
        run_ocr()


async def run_ocr():
    print("[OCR] Starting OCR...")
    ocr_result = True
    while ocr_result:
        ocr_result = ocr_cycle()


def ocr_cycle():
    text = ocr.bounding_box_visualizer()
    if cv2.waitKey(1) & 0xFF == ord("q"):
        return False
    for entry in text:
        if ocr.verify_reg(entry):  # If the entry is a car
            parked_cars[entry] = entry in paid_cars  # Add the entry to the list, auto check if they have paid yet.
            print(f"[DB] Adding {entry} to DB, payment {entry in paid_cars}")
    for entry in parked_cars:
        if entry not in text:
            parked_cars.pop("entry")
            print(f"[DB] Removing {entry} from DB")
    return True


if __name__ == "__main__":
    __main__()

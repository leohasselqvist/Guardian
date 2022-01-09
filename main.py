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


def run_ocr():
    print("[OCR] Starting OCR...")
    ocr_result = True
    while ocr_result:
        ocr_result = ocr_cycle()


def ocr_cycle():
    text = ocr.bounding_box_visualizer(debug_text=str(parked_cars))
    chopping_block = []  # Quickfire solution to dict iteration size issue. Not very elegant
    if cv2.waitKey(1) & 0xFF == ord("q"):
        return False  # Failed cycle, interrupted by keyboard stroke
    for entry in text:
        if ocr.verify_reg(entry):  # If the entry is a car
            parked_cars[entry] = entry in paid_cars  # Add the entry to the list, auto check if they have paid yet.
            print(f"[DB] Adding {entry} to DB, payment {entry in paid_cars}")
    for entry in parked_cars:  # Check the existing list of cars and see if any have left
        if entry not in text and ocr.verify_reg(entry):  # If a car has left...
            chopping_block.append(entry)  # Add to chopping_block

            # The reason for adding the dead cars to a new list is that a dict cannot change size while being iterated.
            # chopping_block is a quick and inefficient solution. Will fix later.

    for dead_car in chopping_block:  # TODO: Remove this unnecessary loop.
        parked_cars.pop(dead_car)  # Remove all cars in chopping_block from parked_cars
        print(f"[DB] Removing {dead_car} from DB")
    return True  # Completed cycle


if __name__ == "__main__":
    __main__()

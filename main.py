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
    ocr_trd = threading.Thread(target=run_ocr)  # Create a separate thread for the OCR
    if "-n" not in sys.argv:  # If -n in args, ignore networking setup
        print("[OCR] Starting thread...")
        ocr_trd.start()  # OCR will run in the background
        print("[NET] Starting server...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', 11417))  # Set port
            s.listen()
            while True:
                print("[NET] Listening for client...")
                conn, addr = s.accept()
                with conn:  # If we get a connection...
                    print(f'[NET] Client accepted {addr[0]}')
                    while True:
                        try:
                            data = conn.recv(1024).decode('utf-8')  # Data received
                            print(f"[NET] Received {data}")
                            if not data:  # If they forcefully closed
                                print(f"[NET] Connection forcefully closed by {addr[0]}.")
                                break
                            if data == "quit":  # If they gracefully closed
                                conn.close()
                                print(f"[NET] Connection closed by {addr[0]}")
                                break
                            cars = data.split('|')  # Split for multiple cars
                            for entry in cars:
                                car = entry.split('.')  # car[0] is the regplate, car[1] is to add or remove it
                                if car[1] == "1":
                                    paid_cars.append(car[0].upper())
                                else:
                                    paid_cars.remove(car[0].upper())
                            conn.sendall(str(paid_cars).encode('utf-8'))  # Respond with the current list of paid cars.
                        except Exception as e:
                            conn.sendall(("ERROR: " + str(e)).encode('utf-8'))
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

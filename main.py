import easyocr_model as ocr
import threading
import cv2
import string
import asyncore

#  DENNA KODEN KÖR PÅ RASPBERRY PI:n


class SauronReciever(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self):
        print("Signal Inkommande")
        print(self.recv(1024))


def __main__():
    client = SauronReciever("localhost", 3623)
    asyncore.loop()
    paid_cars = []
    parked_cars = {}  # KEY: str | VALUE: bool (verified or nah)
    while True:
        text = ocr.bounding_box_visualizer()
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        for entry in text:
            if ocr.verify_reg(entry):  # If the entry is a car
                parked_cars[entry] = entry in paid_cars  # Add the entry to the list, auto check if they have paid yet.


if __name__ == "__main__":
    __main__()

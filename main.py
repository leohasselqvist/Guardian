import easyocr_model
import threading
import tesseract

#  DENNA KODEN KÖR PÅ RASPBERRY PI:n


easyocr_m = easyocr_model.__main__
tesseract_m = tesseract.__main__

if __name__ == "__main__":
    easyocr_m()

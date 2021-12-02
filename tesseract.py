import cv2
import pytesseract
import string

custom_config = f"-c tessedit_char_whitelist={string.ascii_lowercase + string.digits} --psm 6"
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
vid_capture = cv2.VideoCapture(0)


def __main__():
    while True:
        _, img = vid_capture.read()
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB for Tesseract

        # print(pytesseract.image_to_string(img))

        hImg, wImg, _ = img.shape
        boxes = pytesseract.image_to_boxes(img, config=custom_config)
        for b in boxes.splitlines():
            b = b.split(' ')
            x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])  # Start indexing from 1 because b[0] is the char.
            cv2.rectangle(img, (x, hImg-y), (w, hImg-h), (0, 255, 0), 2)
            cv2.putText(img, b[0], (x, hImg-y+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
        cv2.imshow("Result", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()

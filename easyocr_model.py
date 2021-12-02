import easyocr
import cv2
import string
from PIL import ImageDraw

letterset = string.ascii_uppercase + string.digits


def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if c in letterset else "" for c in text]).strip()


def __main__():
    reader = easyocr.Reader(['en'])

    vid_capture = cv2.VideoCapture(0)
    while True:

        _, image = vid_capture.read()

        bound = reader.readtext(image)

        for (bbox, text, prob) in bound:
            # display the OCR'd text and associated probability
            print("[INFO] {:.4f}: {}".format(prob, text))
            # unpack the bounding box
            (tl, tr, br, bl) = bbox
            tl = (int(tl[0]), int(tl[1]))
            tr = (int(tr[0]), int(tr[1]))
            br = (int(br[0]), int(br[1]))
            bl = (int(bl[0]), int(bl[1]))
            # cleanup the text and draw the box surrounding the text along
            # with the OCR'd text itself
            text = cleanup_text(text)
            cv2.rectangle(image, tl, br, (0, 255, 0), 2)
            cv2.putText(image, text, (tl[0], tl[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        # show the output image
        cv2.imshow("Image", image)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


if __name__ == "__main__":
    __main__()

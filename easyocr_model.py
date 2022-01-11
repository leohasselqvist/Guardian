import easyocr
import cv2
import string
from PIL import ImageDraw

letterset = string.ascii_uppercase + string.digits

reader = easyocr.Reader(['en'], gpu=True)

vid_capture = cv2.VideoCapture(0)


def verify_reg(reg):
    if len(reg) == 6:
        for i in range(0, len(reg)):
            if i < 3:
                if reg[i] not in string.ascii_uppercase:
                    return False
            elif i < 5:
                if reg[i] not in string.digits:
                    return False
            else:
                if reg[i] not in letterset:
                    return False
        return True
    return False


def cleanup_text(text):
    # strip out non-ASCII text so we can draw the text on the image
    # using OpenCV
    return "".join([c if c in letterset else "" for c in text]).strip()


def __main__():
    while True:
        print(read_text())
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break


def bounding_box_visualizer(debug_text=""):  # Use cv2.waitkey() after function
    _, image = vid_capture.read()
    all_objects = []

    bound = reader.readtext(image)

    for (bbox, text, prob) in bound:
        # display the OCR'd text and associated probability
        # print("[INFO] {:.4f}: {}".format(prob, text))
        # unpack the bounding box
        (tl, tr, br, bl) = bbox
        tl = (int(tl[0]), int(tl[1]))
        tr = (int(tr[0]), int(tr[1]))
        br = (int(br[0]), int(br[1]))
        bl = (int(bl[0]), int(bl[1]))
        # cleanup the text and draw the box surrounding the text along
        # with the OCR'd text itself
        text = cleanup_text(text)
        all_objects.append(text)
        color = (0, 0, 255)  # RED
        if verify_reg(text):
            color = (0, 255, 0)  # GREEN
        cv2.rectangle(image, tl, br, color, 2)
        cv2.putText(image, text, (tl[0], tl[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
    height, _, _ = image.shape
    if debug_text != "":  # optimization
        cv2.putText(image, debug_text, (20, height-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    # show the output image
    cv2.imshow("Image", image)
    return all_objects
    # if cv2.waitKey(1) & 0xFF == ord("q"):
    #     break


def read_text():
    _, image = vid_capture.read()
    data = reader.readtext(image)  # Get raw information
    output = []
    for (_, text, _) in data:
        output.append(text)
    return output


if __name__ == "__main__":
    __main__()

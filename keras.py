import keras_ocr.tools
import matplotlib.pyplot as plt
import cv2
import keras_ocr

# keras-ocr will automatically download pretrained
# weights for the detector and recognizer.


def __main__():
    pipeline = keras_ocr.pipeline.Pipeline()
    images = [keras_ocr.tools.read("1.jpg")]
    img = images[0]
    hImg, wImg, _ = img.shape
    # Each list of predictions in prediction_groups is a list of
    # (word, box) tuples.
    prediction_groups = pipeline.recognize(images)

    print(prediction_groups)

    #for b in prediction_groups:
    #    x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])  # Start indexing from 1 because b[0] is the char.
    #    cv2.rectangle(img, (x, hImg - y), (w, hImg - h), (0, 255, 0), 2)
    #    cv2.putText(img, b[0], (x, hImg - y + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
    #cv2.imshow("Results", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    #cv2.waitKey(0)


if __name__ == "__main__":
    __main__()

import cv2 # type: ignore
from pytesseract import Output # type: ignore
import numpy as np # type: ignore
import pytesseract # type: ignore

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

image_path = "images/33.jpg"

image = cv2.imread(image_path)

def grayscale(image):
   """Converts an image to grayscale.
   """
   return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grayscale_image = grayscale(image)

def denoise(grayscale_image):
   """Reduces noise in the image using a median blur filter.
   """
   return cv2.medianBlur(grayscale_image, 5) 

image_denoise = denoise(grayscale_image)


def sharpen(image):
   """Sharpens the image using a Laplacian filter.
   """
   kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
   return cv2.filter2D(image, -1, kernel)

sharpen_image = sharpen(image_denoise)
text = pytesseract.image_to_string(grayscale_image)
print(text)

def draw_outline(image):
    # Extract text data from the image
    data = pytesseract.image_to_data(image, output_type=Output.DICT)
    n_boxes = len(data["text"])

    # Draw bounding boxes around detected text
    for i in range(n_boxes):
        if int(data["conf"][i]) > 0:  
            #  bounding box
            x, y = data["left"][i], data["top"][i]
            w, h = data["width"][i], data["height"][i]

            # Define box parameters
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            green = (0, 255, 0)
            thickness = 1

            # Draw the rectangle on the image
            cv2.rectangle(image, top_left, bottom_right, green, thickness)

    # Save the output image
    output_image_path = "images/text_with_boxe3223.png"
    cv2.imwrite(output_image_path, image)

draw_outline(image)
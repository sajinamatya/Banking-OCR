import cv2
from pytesseract import Output
import numpy as np
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
image_path = "images/3.jpg"
image = cv2.imread(image_path)
def grayscale(image):
   """Converts an image to grayscale.

   Args:
       image: The input image in BGR format.

   Returns:
       The grayscale image.
   """
   return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grayscale_image = grayscale(image)

def denoise(grayscale_image):
   """Reduces noise in the image using a median blur filter.

   Args:
       image: The input grayscale image.

   Returns:
       The denoised image.
   """
   return cv2.medianBlur(grayscale_image, 5)  # Adjust kernel size as needed

image_denoise = denoise(grayscale_image)


def sharpen(image):
   """Sharpens the image using a Laplacian filter.

   Args:
       image: The input grayscale image.

   Returns:
       The sharpened image (be cautious with sharpening).
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
        if int(data["conf"][i]) > 0:  # Check confidence level; -1 indicates no confidence score
            # Get the coordinates of the bounding box
            x, y = data["left"][i], data["top"][i]
            w, h = data["width"][i], data["height"][i]

            # Define box parameters
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            green = (0, 255, 0)
            thickness = 1

            # Draw the rectangle on the image
            cv2.rectangle(image, top_left, bottom_right, green, thickness)

    # Save the output image once after drawing all boxes
    output_image_path = "images/text_with_boxes.png"
    cv2.imwrite(output_image_path, image)

draw_outline(image)
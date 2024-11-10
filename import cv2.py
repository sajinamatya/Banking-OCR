import cv2
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# Read image
easy_text_path = "images/2.png"
easy_img = cv2.imread(easy_text_path)

# Convert to text
text = pytesseract.image_to_string(easy_img)
print(text)

import cv2 # type: ignore
from pytesseract import Output # type: ignore
import numpy as np # type: ignore
import pytesseract # type: ignore

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

image_path = "images/3.jpg"

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




def extract_citizenship_info(text):
    data = {}

    # Extract certificate number and sex
    if "Citizenship Certificate No." in text:
        part = text.split("Citizenship Certificate No.")[1].split("\n")[0]
        tokens = part.strip().split()
        if len(tokens) >= 2:
            data["Citizenship Certificate No."] = tokens[0]
            data["Sex"] = tokens[1] if len(tokens) > 1 else None  # Ensure sex is extracted correctly

    # Full Name
    if "Full Name" in text:
        data["Full Name"] = text.split("Full Name")[1].split("\n")[0].strip(" ,:")

    # Date of Birth
    if "Date of Birth" in text:
        dob_line = text.split("Date of Birth")[1]
        year = dob_line.split("Year:")[1].split()[0]
        month = dob_line.split("Month:")[1].split()[0]
        day = dob_line.split("Day")[1].strip().split()[0]
        data["Date of Birth"] = f"{year}-{month[:3].capitalize()}-{day.zfill(2)}"

    # Birth Place
    if "Birth Place" in text:
        birth_part = text.split("Birth Place")[1]
        district = birth_part.split("District:")[1].split("\n")[0].strip()
        data["Birth District"] = district

    if "VDC" in text and "Ward No." in text:
        vdc_line = text.split("VDC")[1]
        vdc = vdc_line.split(":")[1].split("Ward")[0].strip()
        ward = vdc_line.split("Ward No.")[1].strip().split()[0]
        data["Birth VDC"] = vdc
        data["Birth Ward No."] = ward

    # Permanent Address
    if "Permanent Address" in text:
        perm_part = text.split("Permanent Address")[1]
        perm_district = perm_part.split("District:")[1].split("\n")[0].strip()
        data["Permanent District"] = perm_district

    if "Metropolitan" in text:
        metro = text.split("Metropolitan")[1].split("\n")[0]
        # Handle OCR errors in the "Metropolitan" value
        corrected_metro = metro.replace("Nard Nod", "Nagar").strip() if "Nard Nod" in metro else metro.strip()
        data["Permanent Municipality"] = corrected_metro

    return data


info = extract_citizenship_info(text)
print(info)
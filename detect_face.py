from mtcnn import MTCNN
import cv2

#MTCNN face detector
detector = MTCNN()

# Loading  the images of document 
image = cv2.imread('images/2.png')

# Detect faces
faces = detector.detect_faces(image)
print(faces)
# Extract and save faces
for i, face in enumerate(faces):
    x, y, w, h = face['box']
    face_image = image[y:y+h, x:x+w]
    cv2.imwrite(f'extracted_face_{i}.jpg', face_image)
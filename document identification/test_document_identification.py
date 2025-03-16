from ultralytics import YOLO

def yolo_model_test(model_path, image_path):
    # Loading yolo model
    model = YOLO(model_path)

    # Run inference on the image
    results = model.predict(image_path)  # prediction on the test image 

    # accessing the first element if the result is a list 
    if isinstance(results, list):
        results = results[0]  

   
   
    results.show()  

    # Saving the predicted results into a directory 
      

if __name__ == "__main__":
    model_path = 'E:\\Sajilo E-bank\\runs\detect\\train\\weights\\best.pt' # path of the trained yolo model 
    image_path = 'E:\\Sajilo E-bank\\images\\33.jpg'  # path of the test image 

    yolo_model_test(model_path, image_path)

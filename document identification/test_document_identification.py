from ultralytics import YOLO

def yolo_model_test(model_path, image_path):
    # Loading yolo model
    model = YOLO(model_path)

    # Run inference on the image
    results = model.predict(image_path)  # prediction on the test image 

    # accessing the first element if the result is a list 
    if isinstance(results, list):
        results = results[0]  

    print(results.summary()) 

   
    results.show()  

    # Saving the predicted results into a directory 
    results.save(save_dir="Sajilo E-bank")  

if __name__ == "__main__":
    model_path = 'E:\\Sajilo E-bank\\runs\detect\\train\\weights\\documentdetection.pt' # path of the trained yolo model 
    image_path = 'E:\\Sajilo E-bank\\images\\2.png'  # path of the test image 

    yolo_model_test(model_path, image_path)


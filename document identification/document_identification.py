from ultralytics import YOLO
import os

def train_yolo_model(data_path, model_path='yolov8n.pt', epochs=50, imgsize=640, batch_size=8, export_dir="models"):
    """
    Training of the yolo model on the front images dataset of citizenship to identify if the images is citizenship or not by classifiying the images on the basis of classes such as stamped logo,silver patch etc.

    Args:
        data_path (str): Path to the data.yaml file.
        model_path (str): Path to the pre-trained YOLO model
        epochs (int): Number of training epochs.
        imgsize (int): Image size for training.
        batch_size (int): Batch size for training.
        export_dir (str): Directory where the model will be saved after training.
    """
    # Initializing  the YOLO model for document detection
    model = YOLO(model_path)

    # Training the model on the dataset with proper labels and bouding boxes
    model.train(data=data_path, epochs=epochs, imgsz=imgsize, batch=batch_size)

    # Model validation 
    results = model.val()
    print(results)

    # creating the dir if the path do not exist
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    # path for the model 
    export_path = os.path.join(export_dir, "documentdetection.pt")

    # Exporting the model for further use. 
    model.export(format='onnx', imgsz=imgsz, half=False, dynamic=False, simplify=True, opset=11, save_dir=export_path)

    print(f"Model exported successfully to: {export_path}")

if __name__ == "__main__":
    
    data_path = "E:/Sajilo E-bank/dataset-backside/data.yaml"  
    model_path = "yolov8s.pt"  
    epochs = 50  # epochs for training
    imgsz = 640  # image size for training
    batch_size = 8  #  batch size for training
    

    
    train_yolo_model(data_path, model_path, epochs, imgsz, batch_size)

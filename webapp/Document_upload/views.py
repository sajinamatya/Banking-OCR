from django.shortcuts import render, redirect
from .models import UserDocument
from user_authentication.models import UserAuthentication
from ultralytics import YOLO
import os
import uuid

def yolo_model_test(model_path, image_path, save_path):
    # Loading YOLO model
    model = YOLO(model_path)

    
    results = model.predict(image_path)

    if isinstance(results, list):
        results = results[0]

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Save the processed image
    result_image_path = os.path.join(save_path, os.path.basename(image_path))
    results.save(result_image_path)

    return result_image_path  # Return the full path

def document_upload(request):
    if request.session.get('user_id') is None:
        return redirect('login')
    
    try:
        user_id = request.session.get('user_id')
        user = UserAuthentication.objects.get(user_id=user_id)
    except UserAuthentication.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        front_side_document = request.FILES.get('front_side_document')
        back_side_document = request.FILES.get('back_side_document')

        if front_side_document and back_side_document:
            # Ensure the temp directory exists
            temp_dir = 'temp'
            os.makedirs(temp_dir, exist_ok=True)

            # Generate unique filenames for the uploaded images
            front_side_filename = f"{uuid.uuid4()}_{front_side_document.name}"
            back_side_filename = f"{uuid.uuid4()}_{back_side_document.name}"

            # Save uploaded images
            front_side_path = os.path.join(temp_dir, front_side_filename)
            back_side_path = os.path.join(temp_dir, back_side_filename)

            with open(front_side_path, 'wb+') as destination:
                for chunk in front_side_document.chunks():
                    destination.write(chunk)
            with open(back_side_path, 'wb+') as destination:
                for chunk in back_side_document.chunks():
                    destination.write(chunk)

            # Ensure the results directory exists in static
            results_dir = "static"
            

            # Run YOLO model for front and back sides
            front_model_path = 'E:\\Sajilo E-bank\\runs-front\\detect\\train\\weights\\best.pt'
            back_model_path = 'E:\\Sajilo E-bank\\runs\\detect\\train\\weights\\best.pt'

            front_result_path = yolo_model_test(front_model_path, front_side_path, results_dir)
            back_result_path = yolo_model_test(back_model_path, back_side_path, results_dir)

            # Convert absolute paths to relative paths for static files
            

            return render(request, 'documentupload.html', {
                'front_result_path': front_result_path,
                'back_result_path': back_result_path
            })

    return render(request, 'documentupload.html')

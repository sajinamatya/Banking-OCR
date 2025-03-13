from django.shortcuts import render, redirect
from .models import UserDocument

def document_upload(request):
    if request.session.get('user_id') is None:
        return redirect('login')
    if request.method == 'POST':
        front_side_document = request.FILES.get('front_side_document')
        back_side_document = request.FILES.get('back_side_document')
        
        if front_side_document and back_side_document:
            user_document, created = UserDocument.objects.get_or_create(user=request.user)
            user_document.front_side_document = front_side_document
            user_document.back_side_document = back_side_document
            user_document.save()
            return redirect('document_upload_success')  # Redirect to a success page
    
    return render(request, 'documentupload.html')

import uuid

from django.http import FileResponse, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ImageUploadForm
from .models import ImageUpload
from deepface import DeepFace
import os
from django.conf import settings


def home(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()

            # Analyze the image with DeepFace
            img_path = os.path.join(settings.MEDIA_ROOT, 'uploads', os.path.basename(instance.image.name))

            try:
                analysis = DeepFace.analyze(img_path=img_path, actions=['age', 'gender', 'emotion'])

                # For simplicity, we'll just take the first face if multiple are detected
                if isinstance(analysis, list):
                    analysis = analysis[0]

                context = {
                    'form': form,
                    'image': instance,
                    'analysis': analysis,
                }
                return render(request, 'result.html', context)

            except Exception as e:
                # Handle cases where no face is detected
                context = {
                    'form': form,
                    'error': str(e),
                }
                return render(request, 'home.html', context)
    else:
        form = ImageUploadForm()

    return render(request, 'home.html', {'form': form})


def download_file(request, file_hash):
    secure_file = get_object_or_404(ImageUpload, hash=file_hash)

    if os.path.exists(f'{settings.MEDIA_ROOT}/{secure_file.image}'):
        response = FileResponse(secure_file.image.open('rb'))
        response['Content-Disposition'] = f'attachment; filename="{uuid.uuid4()}"'
        return response

    return HttpResponseNotFound("File not found")
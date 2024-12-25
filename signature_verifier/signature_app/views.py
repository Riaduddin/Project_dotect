from django.shortcuts import render, redirect
from .forms import SignatureForm
from .models import Signature
import cv2
from tensorflow.keras.models import load_model
import numpy as np
from .utils import euclidean_distance, combined_loss, contrastive_loss


MODEL_PATH = 'model_1.04882.keras'
signature_model=load_model(MODEL_PATH,custom_objects={'euclidean_distance': euclidean_distance,
                    'contrastive_loss': contrastive_loss, 'combined_loss':combined_loss})

def preprocess_image_for_prediction(image_path, target_size=(128, 128)):
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image at {image_path} could not be read. Check the path.")
    
    # Convert to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Resize the image
    img = cv2.resize(img, target_size)
    
    img = np.expand_dims(img, axis=-1)
    
    
    img = np.expand_dims(img, axis=0)
    
    # Convert to float32 and normalize (if needed)
    img = img.astype('float32') / 255.0
    
    return img

def process_images(original_path, test_path):
    """
    Use the ML model to compare the original and test images.
    """
    # Preprocess the images
    img1 = preprocess_image_for_prediction(original_path)
    img2 = preprocess_image_for_prediction(test_path)
    

    # Predict similarity (assuming your Siamese model takes two inputs)
    similarity_score = signature_model.predict([img1, img2])

    # Output the similarity score
    print("Similarity Score:", similarity_score)
    print("Original images: ",original_path)
    print("Other images: ", test_path )

    # Determine if the signatures match based on a threshold
    threshold = 0.50  # Define your threshold
    if similarity_score > threshold:
        return "Signatures Match"
    else:
        return "Signatures Do Not Match"


def upload_images(request):
    if request.method == 'POST':
        form = SignatureForm(request.POST, request.FILES)
        if form.is_valid():
            signature = form.save(commit=False)
            signature.save()
            # Process and compare images
            original_path = signature.original_image.path
            test_path = signature.test_image.path

            # print(f"Original Image Path: {original_path}")
            # print(f"Test Image Path: {test_path}")

            result = process_images(original_path, test_path)

            # Save the result to the database
            signature.result = result
            

            return render(request, 'signature_app/result.html', {'result': result})
    else:
        form = SignatureForm()
    return render(request, 'signature_app/upload.html', {'form': form})


import pickle
import os
import json
import numpy as np
from PIL import Image

# Use tensorflow/keras for model loading and feature extraction
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TF warnings

import sys
try:
    from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
    from tensorflow.keras.preprocessing.image import load_img, img_to_array
    from tensorflow.keras.models import load_model, Model
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    TF_AVAILABLE = True
except ImportError as e:
    import traceback
    traceback.print_exc()
    TF_AVAILABLE = False
    print(f"Warning: TensorFlow is not installed. Exception: {e}")
    print(f"Current Executable: {sys.executable}")

# Global variables to cache models in memory
VGG_MODEL = None
CAPTION_MODEL = None
TOKENIZER = None

# Typically 34, 35, or 36 depending on the dataset's longest string (User model expects 36)
MAX_LENGTH = 36 

def load_all_models():
    """
    Loads VGG16, the trained captioning model (model.h5), and the tokenizer (tokenizer.pkl).
    This ensures we don't reload heavy deep learning models on every single web request.
    """
    global VGG_MODEL, CAPTION_MODEL, TOKENIZER
    
    if not TF_AVAILABLE:
        return False
        
    try:
        # 1. Load VGG16 and re-structure it to output features
        if VGG_MODEL is None:
            print("Loading VGG16 feature extractor...")
            base_vgg = VGG16()
            # Remove the classification layer (predictions) to get the 4096-d vector instead of the class label
            VGG_MODEL = Model(inputs=base_vgg.inputs, outputs=base_vgg.layers[-2].output)
            
        # 2. Load the trained LSTM Caption Generator (checking multiple possible names from Kaggle)
        possible_model_paths = ['best_model.keras', 'best_model.h5', 'model.h5', 'workingbest_model.h5']
        for path in possible_model_paths:
            if os.path.exists(path):
                print(f"Loading caption model from {path}...")
                CAPTION_MODEL = load_model(path)
                break
            
        # 3. Load the Tokenizer
        tokenizer_pkl = 'tokenizer.pkl'
        tokenizer_json = 'tokenizer_word_index.json'
        if TOKENIZER is None:
            if os.path.exists(tokenizer_pkl):
                print(f"Loading tokenizer from {tokenizer_pkl}...")
                with open(tokenizer_pkl, 'rb') as f:
                    TOKENIZER = pickle.load(f)
            elif os.path.exists(tokenizer_json):
                from tensorflow.keras.preprocessing.text import Tokenizer as KerasTokenizer
                print(f"Loading tokenizer from {tokenizer_json}...")
                with open(tokenizer_json, 'r') as f:
                    word_index = json.load(f)
                    TOKENIZER = KerasTokenizer()
                    TOKENIZER.word_index = word_index
                
        return True
    except Exception as e:
        print(f"Error loading models: {e}")
        return False

# Attempt to load them as the server starts up
load_all_models()

def extract_features(image_path):
    """
    Passes an actual newly uploaded image through VGG16 to extract a (1, 4096) feature vector.
    This replaces the need for features.pkl since we process the image live!
    """
    if VGG_MODEL is None:
        raise ValueError("VGG16 model is not loaded.")
        
    # Load image and resize to VGG16 expected size (224x224)
    image = load_img(image_path, target_size=(224, 224))
    
    # Convert image pixels to a numpy array
    image = img_to_array(image)
    
    # Reshape data for the model (1 image, 224 height, 224 width, 3 color channels)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    
    # Prepare the image for the VGG model (scaling pixel values essentially)
    image = preprocess_input(image)
    
    # Get the 4096 feature vector
    feature = VGG_MODEL.predict(image, verbose=0)
    return feature

def idx_to_word(integer, tokenizer):
    """
    Maps an integer back to the word based on the tokenizer vocabulary.
    """
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def generate_caption(image_path):
    """
    Generates the true caption for a given image path using the loaded Keras model.
    """
    # Verify models are loaded
    if not TF_AVAILABLE:
        return "Error: Please install TensorFlow to generate real captions. Check your terminal/command prompt."
        
    if CAPTION_MODEL is None or TOKENIZER is None:
        return ("Notice: Could not find 'best_model.keras' and 'tokenizer_word_index.json'. "
                "Please make sure both files are inside the 'ai image generator' folder.")

    try:
        # 1. Extract live visual features from the uploaded image
        photo_feature = extract_features(image_path)
        
        # 2. Generate the caption word by word (Greedy Search Algorithm)
        in_text = 'startseq'
        for i in range(MAX_LENGTH):
            # Encode the input sequence to integer indices
            sequence = TOKENIZER.texts_to_sequences([in_text])[0]
            # Pad the sequence so the LSTM gets a consistent shape vector
            sequence = pad_sequences([sequence], maxlen=MAX_LENGTH)
            
            # Predict the next word probabilities
            yhat = CAPTION_MODEL.predict([photo_feature, sequence], verbose=0)
            
            # Get the word integer with the highest probability
            yhat = np.argmax(yhat)
            
            # Map integer index back to actual English word
            word = idx_to_word(yhat, TOKENIZER)
            
            # Stop if word not found in vocab
            if word is None:
                break
                
            # Append decoded word to the growing sequence
            in_text += ' ' + word
            
            # Stop if model outputs the termination token
            if word == 'endseq':
                break
                
        # 3. Clean up the final caption string
        final_caption = in_text.replace('startseq', '').replace('endseq', '').strip()
        
        # Capitalize first letter and add a period
        if final_caption:
            final_caption = final_caption[0].capitalize() + final_caption[1:] + "."
            
        return final_caption
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return f"Prediction Error: {str(e)}"

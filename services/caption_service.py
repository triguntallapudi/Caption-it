import logging
import pickle
from pathlib import Path

import numpy as np
from PIL import Image

from tensorflow.keras.applications.vgg16 import VGG16, preprocess_input
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.preprocessing.sequence import pad_sequences

logger = logging.getLogger(__name__)
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / 'model'
VGG_MODEL = None
CAPTION_MODEL = None
TOKENIZER = None
MAX_LENGTH = None


class CaptionServiceError(RuntimeError):
    """An expected, user-safe model or prediction error."""

def load_all_models():
    """Load the trained caption model, tokenizer, and VGG16 feature extractor once."""
    global VGG_MODEL, CAPTION_MODEL, TOKENIZER, MAX_LENGTH

    try:
        model_path = MODEL_DIR / 'model.keras'
        tokenizer_path = MODEL_DIR / 'tokenizer.pkl'
        logger.info('Loading caption model from %s', model_path)
        CAPTION_MODEL = load_model(model_path)
        with tokenizer_path.open('rb') as handle:
            TOKENIZER = pickle.load(handle)

        model_length = CAPTION_MODEL.inputs[1].shape[-1]
        output_size = CAPTION_MODEL.outputs[0].shape[-1]
        max_token_index = max(TOKENIZER.word_index.values(), default=0)
        if model_length is None or output_size is None or max_token_index >= int(output_size):
            raise CaptionServiceError('The trained model and tokenizer are incompatible.')
        MAX_LENGTH = int(model_length)

        logger.info('Loading VGG16 feature extractor...')
        base_vgg = VGG16(weights='imagenet')
        VGG_MODEL = Model(inputs=base_vgg.inputs, outputs=base_vgg.layers[-2].output)
        return True
    except Exception:
        CAPTION_MODEL = None
        TOKENIZER = None
        logger.exception('Error loading caption models')
        return False

# Attempt to load them as the server starts up
load_all_models()

def extract_features(image_path):
    """
    Passes an actual newly uploaded image through VGG16 to extract a (1, 4096) feature vector.
    This replaces the need for features.pkl since we process the image live!
    """
    if VGG_MODEL is None:
        raise CaptionServiceError('VGG16 could not be loaded.')
        
    # Load image and resize to VGG16 expected size (224x224)
    try:
        with Image.open(image_path) as image_file:
            image_file.verify()
        image = load_img(image_path, target_size=(224, 224))
    except (OSError, ValueError) as error:
        raise CaptionServiceError('Please upload a valid, readable image.') from error
    
    # Convert image pixels to a numpy array
    image = img_to_array(image)
    
    # Reshape data for the model (1 image, 224 height, 224 width, 3 color channels)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    
    # Prepare the image for the VGG model (scaling pixel values essentially)
    image = preprocess_input(image)
    
    # Get the 4096 feature vector
    feature = VGG_MODEL.predict(image, verbose=0)
    if feature.shape != (1, 4096):
        raise CaptionServiceError('VGG16 returned an unexpected feature shape.')
    return feature

def idx_to_word(integer, tokenizer):
    """
    Maps an integer back to the word based on the tokenizer vocabulary.
    """
    return tokenizer.index_word.get(int(integer))

def generate_caption(image_path):
    """Generate a caption for an uploaded image using the trained model."""
    if CAPTION_MODEL is None or TOKENIZER is None:
        raise CaptionServiceError(
            'The trained model is unavailable. Check model/model.keras and model/tokenizer.pkl.'
        )

    try:
        photo_feature = extract_features(image_path)
        in_text = 'startseq'
        for _ in range(MAX_LENGTH):
            sequence = TOKENIZER.texts_to_sequences([in_text])[0]
            sequence = pad_sequences([sequence], maxlen=MAX_LENGTH)
            predictions = CAPTION_MODEL.predict([photo_feature, sequence], verbose=0)[0]
            word = idx_to_word(np.argmax(predictions), TOKENIZER)
            if word is None:
                break
            in_text += ' ' + word
            if word == 'endseq':
                break

        final_caption = in_text.replace('startseq', '').replace('endseq', '').strip()
        if final_caption:
            final_caption = final_caption[0].capitalize() + final_caption[1:] + '.'
        return final_caption
    except CaptionServiceError:
        raise
    except Exception as error:
        logger.exception('Caption prediction failed')
        raise CaptionServiceError('The image could not be captioned.') from error

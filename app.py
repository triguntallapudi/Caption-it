import base64
import logging
import mimetypes
from pathlib import Path
from uuid import uuid4

from flask import Flask, jsonify, render_template, request
from werkzeug.utils import secure_filename

from services.caption_service import CaptionServiceError, generate_caption

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Path(app.root_path) / 'static' / 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
logger = logging.getLogger(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify(success=False, error='Please upload an image smaller than 16 MB.'), 413


@app.post('/predict')
def predict():
    if 'image' not in request.files:
        return jsonify(success=False, error='Please upload an image.'), 400

    uploaded_file = request.files['image']
    if not uploaded_file.filename:
        return jsonify(success=False, error='Please choose an image to upload.'), 400
    if not allowed_file(uploaded_file.filename):
        return jsonify(success=False, error='Please upload a JPG, JPEG, PNG, or WebP image.'), 400

    filename = secure_filename(uploaded_file.filename)
    if not filename:
        return jsonify(success=False, error='The uploaded filename is invalid.'), 400

    filepath = app.config['UPLOAD_FOLDER'] / f'{uuid4().hex}_{filename}'
    try:
        uploaded_file.save(filepath)
        caption = generate_caption(filepath)
        image_data = base64.b64encode(filepath.read_bytes()).decode('ascii')
        media_type = mimetypes.guess_type(filepath.name)[0] or 'application/octet-stream'
    except CaptionServiceError as error:
        logger.error('Caption service error for %s: %s', filepath, error)
        return jsonify(success=False, error=str(error)), 503
    except Exception:
        logger.exception('Unexpected prediction error for %s', filepath)
        return jsonify(success=False, error='The image could not be processed.'), 500
    finally:
        filepath.unlink(missing_ok=True)

    return jsonify(
        success=True,
        caption=caption,
        image_url=f'data:{media_type};base64,{image_data}',
    )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Image Caption Generator

This project is a Flask web application that generates a short caption for an uploaded image using a trained VGG16 and LSTM image-captioning pipeline.

## Tech Stack

- **Backend:** Python 3 and Flask
- **Image features:** VGG16 pretrained on ImageNet
- **Caption model:** Trained Keras LSTM decoder
- **Frontend:** Jinja2 templates, CSS, and vanilla JavaScript
- **Storage:** Local trained model and tokenizer files

## Architecture

```text
Uploaded image
	|
	v
Image preprocessing: 224 x 224
	|
	v
VGG16 feature extractor
	|
	v
4096-dimensional feature vector
	|
	v
LSTM caption model
	|
	v
Generated caption
	|
	v
Flask frontend
```

The application generates words sequentially from `startseq` until `endseq` or the model sequence limit. These control tokens are removed before the caption is shown to the user.

## Project Structure

```text
image-caption-generator/
├── data/
│   ├── Images/
│   └── captions.txt
├── model/
│   ├── image-caption-generator.ipynb
│   ├── model.keras
│   └── tokenizer.pkl
├── services/
│   └── caption_service.py
├── static/
│   ├── script.js
│   ├── style.css
│   └── uploads/
├── templates/
│   └── index.html
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

Create and activate a virtual environment if one does not already exist:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```powershell
pip install -r requirements.txt
```

TensorFlow may download the VGG16 ImageNet weights the first time the application starts.

## Run the Application

```powershell
python app.py
```

Open http://127.0.0.1:5000/ and upload a JPG, JPEG, PNG, or WebP image.

The application does not require the notebook, Flickr8k dataset, `captions.txt`, or precomputed image features to run.

## Runtime Artifacts

- `model/model.keras` is the trained VGG16/LSTM caption model.
- `model/tokenizer.pkl` is the tokenizer used with that model.

The uploaded image is saved briefly during inference, converted into a browser preview, and deleted after processing. No uploaded images are retained by the application.

## Training and Reproducibility

The notebook at `model/image-caption-generator.ipynb` contains the training workflow:

1. Load the Flickr8k images and captions from `data/`.
2. Preprocess captions with `startseq` and `endseq` tokens.
3. Extract 4096-dimensional image features using VGG16.
4. Build the vocabulary and tokenizer.
5. Prepare caption sequences.
6. Train the existing VGG16 plus LSTM architecture.
7. Evaluate predictions with BLEU scores.
8. Export `model.keras` and `tokenizer.pkl`.

The `data/` directory and notebook are training resources only. Flask inference loads the trained artifacts from `model/` and processes new uploads directly.

## Application Features

- Upload an image with the file picker or drag and drop.
- Preview the selected image inside the upload area.
- Remove the selected image before processing.
- Generate a caption through the trained model.
- Display the generated caption in the interface.
- Analyze another image without reloading the page.
- Validate image type and the 16 MB upload limit.
- Delete uploaded server files after processing.

## API Routes

| Method | Route | Purpose |
| --- | --- | --- |
| GET | `/` | Render the image captioning interface |
| POST | `/predict` | Process an uploaded image and return its caption |

The prediction response has this shape:

```json
{
  "success": true,
  "caption": "Generated caption.",
  "image_url": "data:image/jpeg;base64,..."
}
```

## Notes

- The application uses the existing trained model and does not retrain when Flask starts.
- The model architecture and tokenizer must remain matched.
- The dataset and notebook are not needed for normal application use.

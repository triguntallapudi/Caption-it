# Image Caption Generator

An image caption generation application that combines Computer Vision and Natural Language Processing to generate descriptive captions for images. The project leverages a pre-trained VGG16 model for feature extraction and an LSTM-based sequence model trained on the Flickr8k dataset. The model is deployed as a Flask web application for real-time inference.

## Features

- Generate captions from uploaded images
- VGG16-based image feature extraction
- LSTM-based caption generation
- NLP preprocessing with NLTK
- Flask web interface for real-time predictions

## Tech Stack

- Python
- TensorFlow / Keras
- VGG16
- LSTM
- NLTK
- Flask
- HTML & CSS
- NumPy, Pandas, Matplotlib

## Project Structure

```text
Image-Caption-Generator/
├── static/
├── templates/
│   ├── index.html
│   └── result.html
├── models/
│   ├── model.keras
│   ├── tokenizer.pkl
│   └── features.pkl
├── app.py
├── train.py
├── predict.py
├── requirements.txt
└── README.md
```

## Dataset

- **Dataset:** Flickr8k
- **Performance:** BLEU Score – **0.52**

## Getting Started

```bash
git clone https://github.com/<your-username>/Image-Caption-Generator.git
cd Image-Caption-Generator
pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5000/` in your browser.

## Future Improvements

- Attention-based caption generation
- Transformer-based architectures
- Beam search decoding
- Cloud deployment

## Author

**Trigun Tallapudi**

LinkedIn: https://www.linkedin.com/in/triguntallapudi/

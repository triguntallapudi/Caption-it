# 🖼️ Image Caption Generator using Deep Learning and NLP

An AI-powered Image Caption Generator that automatically generates meaningful natural language descriptions for images. This project combines **Computer Vision** and **Natural Language Processing (NLP)** by using a **CNN (VGG16)** for image feature extraction and an **LSTM** network for caption generation. The model is trained on the **Flickr8k dataset** and deployed as a web application using **Flask**.

---

## 📌 Features

- Upload an image through a simple web interface.
- Automatically generates descriptive captions.
- Uses a pre-trained VGG16 model for image feature extraction.
- LSTM-based sequence model for natural language generation.
- Trained on the Flickr8k dataset.
- Interactive Flask web application.
- Visualizes training and validation performance using Matplotlib.

---

## 🛠️ Tech Stack

### Programming Language
- Python

### Deep Learning & NLP
- TensorFlow / Keras
- LSTM (Long Short-Term Memory)
- CNN (VGG16)
- Natural Language Processing (NLP)

### Libraries
- NumPy
- Pandas
- Matplotlib
- Pillow (PIL)
- Pickle

### Dataset
- Flickr8k Dataset (Kaggle)

### Backend
- Flask

### Frontend
- HTML
- CSS

---

## 📂 Project Structure

```
Image-Caption-Generator/
│── static/
│── templates/
│   ├── index.html
│   └── result.html
│── models/
│   ├── model.keras
│   ├── tokenizer.pkl
│   └── features.pkl
│── app.py
│── train.py
│── predict.py
│── requirements.txt
└── README.md
```

---

## 🚀 How It Works

1. Upload an image.
2. The image is preprocessed.
3. VGG16 extracts high-level image features.
4. The LSTM model predicts the caption word-by-word.
5. The generated caption is displayed on the webpage.

---

## 🧠 Model Architecture

- **Feature Extraction**
  - Pre-trained VGG16 CNN
  - Extracts a 4096-dimensional feature vector

- **Caption Generation**
  - Tokenizer for vocabulary creation
  - Word Embedding Layer
  - LSTM Network
  - Dense Layer with Softmax Activation

---

## 📊 Dataset

**Dataset:** Flickr8k

- 8,000 images
- Each image has 5 human-written captions
- Used for training, validation, and testing

Dataset Source:
https://www.kaggle.com/datasets/adityajn105/flickr8k

---

## 📈 Model Performance

- BLEU Score: **53%**
- Successfully generates context-aware captions for unseen images.

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/your-username/Image-Caption-Generator.git
```

Navigate to the project directory

```bash
cd Image-Caption-Generator
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the Flask application

```bash
python app.py
```

Open your browser and visit

```
http://127.0.0.1:5000/
```

---

## 📸 Sample Workflow

1. Upload an image.
2. Click **Generate Caption**.
3. The model predicts a descriptive caption.
4. The generated caption is displayed instantly.

---

## 🔮 Future Improvements

- Improve caption quality using Transformer-based architectures.
- Integrate attention mechanisms.
- Support multiple languages.
- Deploy on cloud platforms such as AWS or Azure.
- Add beam search for better caption generation.

---

## 📚 Learning Outcomes

- Computer Vision using CNN
- Natural Language Processing
- Deep Learning with TensorFlow/Keras
- Sequence Modeling using LSTM
- Feature Extraction using Transfer Learning
- Flask Web Application Development
- Model Evaluation using BLEU Score

---

## 👨‍💻 Author

**Raghu Vamshidhar Reddy Vudayagiri**

- LinkedIn: https://linkedin.com/in/raghuvamshidharreddy
- GitHub: https://github.com/raghuvamshidharreddy

---

## 📄 License

This project is intended for educational and learning purposes.

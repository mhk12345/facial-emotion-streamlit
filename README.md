---
title: MoodLens AI
emoji: 👀
colorFrom: yellow
colorTo: purple
sdk: streamlit
sdk_version: 1.44.1
app_file: app.py
pinned: false
license: mit
short_description: Talking AI - based on your Mood!
---

> Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# 🧠 MoodLens-AI: Facial Emotion Companion

A lightweight Streamlit-based web app that analyzes your facial expression and responds with emotion-aware feedback using AI.

---

## 🚀 Features

- Real-time facial emotion detection (DeepFace)  
- Age, gender, and race prediction (optional)  
- Emotion-based personalized messages via generative AI  
- Beautiful UI with interactive feedback and image annotation  
- Downloadable results  
- Webcam or image upload support  

---

## 📁 Project Structure

```bash
MoodLens-AI/
│
├── app.py                 # Main launcher for the Streamlit app
├── ui.py                  # UI layout functions (sidebar, header, cards)
├── ai.py                  # Core logic (image analysis, AI responses)
├── constants.py           # Color palette and emoji map
├── requirements.txt       # Python package dependencies
├── sample.jpg             # Sample image for demo
├── workflow_diagram.PNG   # System architecture (optional)
└── .streamlit/
    └── config.toml        # (Optional) Streamlit theme overrides

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/MoodLens-AI.git
cd MoodLens-AI

### 2. (Optional) Create a virtual environment
bash
Copy
Edit

python -m venv venv
source venv/bin/activate    # On Linux/macOS
venv\Scripts\activate       # On Windows

### 3. Install dependencies

pip install -r requirements.txt

### 🔍 Requirements
Make sure Python 3.8 or higher is installed.

Main packages used:

streamlit

Pillow

numpy

altair

deepface

transformers

## ▶️ Run the app locally

streamlit run app.py

💡 The app will open in your default browser at http://localhost:8501

## 🌐 Deploy to Hugging Face Spaces (Optional)
If deploying to Hugging Face Spaces:

Push this repo to your Hugging Face Space.

Rename app.py to streamlit_app.py if required.

Ensure all files are in the root directory.

Don't commit .streamlit/secrets.toml if it contains any private keys.

🧪 Sample Usage

## Launch the app.

Upload a selfie or click Use Sample Image.

Optionally enable webcam via the sidebar.

Select attributes: emotion, age, gender, race.

Get instant analysis, a custom message, and annotated image.

Click Download Annotated Image if needed.

## 👨‍💻 Contributing
We welcome pull requests!
Feel free to fork the repo, submit fixes, or open feature requests via issues.

# 🧾 License
This project is licensed under the MIT License – feel free to use, modify, and distribute.


---



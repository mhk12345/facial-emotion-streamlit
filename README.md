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

---

## title: MoodLens AI emoji: 👀 colorFrom: yellow colorTo: purple sdk: streamlit sdk\_version: 1.44.1 app\_file: app.py pinned: false license: mit short\_description: Talking AI – based on your Mood!

> Check out the configuration reference at [https://huggingface.co/docs/hub/spaces-config-reference](https://huggingface.co/docs/hub/spaces-config-reference)

# 🧠 MoodLens-AI: Facial Emotion Companion

A lightweight Streamlit-based web app that analyzes your facial expression and responds with emotion-aware feedback using AI.

---

## 🚀 Features

* 🎭 Real-time facial emotion detection (DeepFace)
* 👤 Age, gender, and race prediction (optional)
* 💬 Emotion-based personalized messages via generative AI
* 🌈 Annotated results with emotion‐confidence bar chart
* 📸 Webcam and image upload support
* ⬇️ Download annotated image

---

## 📁 Project Structure

```text
MoodLens-AI/
│
├── app.py                 # Main Streamlit launcher
├── ui.py                  # UI layout (sidebar, header, cards)
├── ai.py                  # Core logic (image analysis, messaging)
├── constants.py           # Color palette & emoji map
├── requirements.txt       # Python package dependencies
├── sample.jpg             # Demo image
├── workflow_diagram.PNG   # System architecture (optional)
└── .streamlit/
    └── config.toml        # (Optional) theme overrides
```

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/MoodLens-AI.git
cd MoodLens-AI
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔍 Requirements

* **Python** 3.8 or higher
* **pip** 21.0 or higher

**Key packages:**

```
streamlit
Pillow
numpy
altair
deepface
transformers
```

---

## ▶️ Run the App Locally

```bash
streamlit run app.py
```

> The app will open in your browser at `http://localhost:8501`

---

## 🌐 Deploy to Hugging Face Spaces (Optional)

1. Push this repository to your Hugging Face account.
2. Rename `app.py` → `streamlit_app.py` if required.
3. Ensure all files are in the root directory.
4. **Do not** commit `.streamlit/secrets.toml` if it contains private keys.

---

## 🧪 Sample Usage

1. Launch the app.
2. Upload a selfie or click **Use Sample Image**.
3. (Optional) Enable webcam from the sidebar.
4. Select attributes: emotion, age, gender, race.
5. View AI analysis and personalized feedback.
6. Click **Download Annotated Image**.

---

## 👨‍💻 Contributing

We welcome contributions!
Please fork the repo, submit fixes, or open feature requests via GitHub issues.

---

## 🧾 License

Licensed under the **MIT License**.
Feel free to use, modify, and distribute.

---

✨ Made with ❤️ by [Mehak Mubarik](https://github.com/mhk12345)

---



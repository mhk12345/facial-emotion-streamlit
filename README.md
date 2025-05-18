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

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

🧠 MoodLens-AI: Facial Emotion Companion
A lightweight, Streamlit-based AI app that analyzes your facial expression and responds with emotion-aware feedback.

🚀 Features
Real-time facial emotion detection using DeepFace

Age, gender, and race prediction (optional)

Emotion-based personalized messages via generative AI

Beautiful UI with interactive feedback and image annotation

Downloadable results

Webcam or image upload support

📁 Project Structure
bash
Copy
Edit
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
🛠️ Setup Instructions
1. Clone the repository
bash
Copy
Edit
git clone https://github.com/yourusername/MoodLens-AI.git
cd MoodLens-AI
2. (Optional) Create a virtual environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # on Linux/macOS
venv\Scripts\activate     # on Windows
3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔍 Requirements
Make sure Python 3.8 or higher is installed.

The main packages used are:

streamlit

Pillow

numpy

altair

deepface

transformers

▶️ Run the app
bash
Copy
Edit
streamlit run app.py
💡 The app will open in your default browser at http://localhost:8501

🌐 Deploy to Hugging Face Spaces (Optional)
If you're using Hugging Face Spaces:

Push your repo to a Hugging Face Space.

Rename app.py to streamlit_app.py if required.

Make sure all your files are in the root (no custom folders).

Don’t commit .streamlit/secrets.toml with sensitive keys.

🧪 Sample Usage
Launch the app.

Upload a selfie or click Use Sample Image.

Optionally enable webcam via the sidebar.

Select attributes: emotion, age, gender, race.

Get instant analysis, a custom message, and annotated image.

Click Download Annotated Image if needed.

👨‍💻 Contribute
We welcome pull requests! Feel free to fork the repo, submit fixes, or request features via issues.

🧾 License
MIT License – Free to use, modify, and distribute.

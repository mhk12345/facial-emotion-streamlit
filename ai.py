# ai.py

import tempfile
from pathlib import Path
import numpy as np
from deepface import DeepFace
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import streamlit as st
import random  # Import once at the top

from prompts import TIPS, SUPPORT_PROMPT, INSIGHT_PROMPT


def save_temp_image(pil_img) -> Path:
    """Save a PIL Image to a temporary file and return the path."""
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    try:
        pil_img.save(tmp.name)
        return Path(tmp.name)
    finally:
        tmp.close()


def best_label(prob_dict) -> str:
    """Return best label and probability as string from DeepFace output."""
    if not isinstance(prob_dict, dict):
        return str(prob_dict)
    label = max(prob_dict, key=prob_dict.get)
    pct   = prob_dict[label] * 100 if prob_dict[label] <= 1 else prob_dict[label]
    return f"{label} ({pct:.0f} %)"


def random_tip() -> str:
    """Return a random tip string from TIPS list."""
    return random.choice(TIPS)


@st.cache_resource(show_spinner=False)
def warm_up(actions):
    """Warm-up DeepFace models (avoids first-inference lag)."""
    dummy = np.zeros((32,32,3), np.uint8)
    try:
        DeepFace.analyze(dummy, actions=actions,
                         detector_backend="opencv", enforce_detection=False)
    except Exception:
        pass


@st.cache_resource(show_spinner=False)
def get_chat_pipeline():
    """Load and cache HuggingFace DialoGPT-medium pipeline."""
    tok = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
    mdl = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
    return pipeline("text-generation", model=mdl, tokenizer=tok)


def analyze_image(img_array, attrs):
    """Run DeepFace analysis with error handling. Returns dict or None."""
    try:
        results = DeepFace.analyze(img_array, actions=attrs,
                                   detector_backend="opencv",
                                   enforce_detection=False)
        return results[0] if isinstance(results, list) else results
    except Exception as e:
        st.warning(f"Face analysis failed: {e}")
        return None


def generate_message(emotion: str) -> str:
    """Generate a supportive message for the detected emotion."""
    chat = get_chat_pipeline()
    prompt = SUPPORT_PROMPT.format(emotion=emotion)
    out = chat(prompt,
               max_new_tokens=25,
               do_sample=True,
               top_p=0.9,
               temperature=0.8)[0]["generated_text"]
    return out[len(prompt):].strip()


def generate_insight(emotion: str) -> str:
    """Generate a deeper insight for the detected emotion."""
    chat = get_chat_pipeline()
    prompt = INSIGHT_PROMPT.format(emotion=emotion)
    out = chat(prompt, max_new_tokens=60, do_sample=False)[0]["generated_text"]
    return out[len(prompt):].strip()

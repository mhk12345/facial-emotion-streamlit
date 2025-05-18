# ui.py

import time
import numpy as np
import altair as alt
import streamlit as st
from pathlib import Path
from PIL import Image, ImageDraw

from constants import PALETTE, EMOJI
from ai import (
    warm_up,
    analyze_image,
    generate_message,
    generate_insight,
    best_label,
    random_tip,
    save_temp_image,
)

# ─────────────────── CSS & FONT INJECTION ────────────────────────────────
def set_page_style():
    st.markdown(
        """
        <style>
          /* Background */
          body, .stApp {
            background: linear-gradient(115deg, #f7fafc 0%, #e6ecf6 100%) !important;
          }
          .block-container {
            max-width: 820px;
            margin: 0 auto;
            padding-top: 1.5rem !important;   /* Unified from your earlier duplicate */
            padding-bottom: 1.2rem;
          }
          .header {
            background: linear-gradient(135deg, #17E9E0, #A64AC9 90%);
            color: #fff;
            padding: 1.1rem 0.5rem;
            border-radius: 12px;
            text-align: center;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 1.1rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.07);
            letter-spacing: 0.03em;
          }
          /* Card styles */
          .card {
            background: #fff;
            border-left: 5px solid #17E9E0;
            padding: 1.1rem 1.2rem 0.8rem 1.2rem;
            margin-bottom: 0.5rem;         /* Tighter spacing */
            border-radius: 13px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            transition: box-shadow .15s, transform .15s;
          }
          .card + .card { margin-top: -0.2rem; }
          .card:hover { box-shadow: 0 4px 18px rgba(166,74,201,0.13); transform: translateY(-2px); }
          /* Tab styles */
          [data-testid="stTabs"] {
            margin-bottom: 0.5rem;
            border-bottom: 0;
          }
          [data-testid="stTabs"] button {
            background: #f6f7fa !important;
            color: #888;
            border-radius: 16px 16px 0 0 !important;
            margin: 0 4px;
            padding: 0.5rem 1.3rem !important;
            font-weight: 500;
            border: none !important;
            box-shadow: none !important;
            transition: background 0.18s, color 0.18s;
          }
          [data-testid="stTabs"] button[aria-selected="true"] {
            background: #17E9E0 !important;
            color: #fff !important;
            font-weight: 700 !important;
            box-shadow: 0 2px 10px rgba(23,233,224,0.08) !important;
          }
          [data-testid="stTabs"] button:hover {
            background: #e4eaf2 !important;
            color: #222 !important;
          }
          /* Hide the blue tab underline indicator */
          [data-testid="stTabs"] [data-testid="stMarkdownContainer"] > div[style*="border-bottom"] {
            border-bottom: none !important;
          }
          /* Remove that blue/teal animated bar on active tab */
          [data-testid="stTabs"] > div > div {
            border-bottom: none !important;
          }
          /* Metrics */
          div[data-testid="metric-container"] {
            background: #f8fafc;
            border-radius: 12px;
            padding: 0.8rem 0.5rem;
            margin: 0.2rem 0;
            box-shadow: 0 1px 4px rgba(166,74,201,0.07);
          }
          /* Progress bar */
          .stProgress > div > div > div > div {
            height: 8px !important;
            border-radius: 12px !important;
            background: #A64AC9 !important;
          }
          /* Sidebar improvements */
          div[data-testid="stSidebar"] .stExpander {
            background: #fff;
            border-radius: 12px;
            padding: 1rem;
          }
          /* Font */
          @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
          * { font-family: 'Poppins', sans-serif !important; }
          /* Hide Streamlit's top white header */
          header[data-testid="stHeader"] {
            background: transparent !important;
            box-shadow: none !important;
          }
          /* (Optional) Custom sample image button style – only works if Streamlit HTML matches */
          /*
          button:has(span:contains("Use Sample Image")) {
              background: linear-gradient(90deg, #17E9E0, #A64AC9 80%);
              color: #fff !important;
              border: none !important;
              font-weight: 600;
              border-radius: 10px !important;
              padding: 0.5em 1.3em !important;
              margin-bottom: 0.8em !important;
              box-shadow: 0 2px 8px rgba(23,233,224,0.09);
              transition: background 0.15s;
          }
          button:has(span:contains("Use Sample Image")):hover {
              background: linear-gradient(90deg, #A64AC9, #17E9E0 80%);
              color: #fff !important;
          }
          */
        </style>
        """,
        unsafe_allow_html=True,
    )



# ─────────────────── Sidebar Controls ────────────────────────────────────
def render_sidebar():
    st.sidebar.title("Controls")
    attrs = st.sidebar.multiselect(
        "Attributes to analyse",
        ["emotion", "age", "gender", "race"],
        default=["emotion"]
    )
    use_cam = st.sidebar.checkbox("Live webcam", value=False)
    st.sidebar.markdown("---")
    with st.sidebar.expander("How It Works"):
        st.write("""
1. Upload or snap a photo  
2. Wait ~1–2 s for analysis  
3. View emotion, age, gender & a friendly message  
4. Download your annotated photo  
        """)
    return attrs, use_cam

# ───────────────────── Demo Header ────────────────────────────────────────
def render_header():
    st.markdown(
        """
        <div class="header" style="display: flex; flex-direction: column; align-items: center; gap: 0.3rem;">
            <img src="logo.png" width="52" style="margin-bottom:0.1em; border-radius:8px;" alt="Logo" />
            <span>MoodLens-AI</span>
        </div>
        """,
        unsafe_allow_html=True
    )

# ───────────────────── About Tab ─────────────────────────────────────────
def render_app_info():
    st.header("About MoodLens-AI")
    st.write("[🔗 View source on GitHub](https://github.com/your-username/MoodLens-AI)")
    try:
        st.image("workflow_diagram.PNG", caption="System Architecture", use_container_width=True)
    except Exception:
        pass
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("What It Does")
        st.write("""
        - Real-time face detection & alignment  
        - Emotion & demographic analysis  
        - Supportive feedback via generative AI  
        - Browser-based interactive dashboard  
        """)
    with col2:
        st.subheader("Key Benefits")
        st.write("""
        - Encourages self-awareness & positivity  
        - Modular, open-source codebase  
        - Fast caching for smooth UX  
        - Easy to extend & deploy  
        """)
    st.markdown("---")
    st.subheader("Tech Stack")
    st.write("DeepFace • Hugging Face Transformers • Streamlit • Altair")

# ───────────────────── Input Card ─────────────────────────────────────────
def render_input_card(use_cam: bool):
    if st.button("Use Sample Image"):
        sample = Image.open("sample.jpg").convert("RGB")
        return sample, np.array(sample)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("1. Upload a Photo")

        uploader = (st.camera_input("Take a photo")
                    if use_cam
                    else st.file_uploader("Upload JPG/PNG", type=["jpg","jpeg","png"]))

        if not uploader:
            st.info("Upload a photo or enable webcam to continue.")
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()

        orig = Image.open(uploader).convert("RGB")
        if max(orig.size) > 800:
            scale = 800 / max(orig.size)
            orig = orig.resize((int(orig.size[0]*scale), int(orig.size[1]*scale)))

        st.markdown('</div>', unsafe_allow_html=True)
        return orig, np.array(orig)

# ────────────────── Processing Card ───────────────────────────────────────
def render_processing_card(img_array: np.ndarray, attrs: list):
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("2. Processing")

        prog = st.progress(0)
        status = st.empty()
        tip    = st.empty()

        status.write("Detecting face")
        tip.info(random_tip())
        prog.progress(25)
        time.sleep(0.2)

        status.write("Analysing attributes")
        tip.info(random_tip())
        prog.progress(55)
        warm_up(attrs)
        face = analyze_image(img_array, attrs)
        time.sleep(0.2)

        if not face or "dominant_emotion" not in face:
            status.error("Could not detect a face with the requested attributes. Try another photo.")
            prog.progress(100)
            tip.empty()
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()

        status.write("Generating feedback")
        tip.info(random_tip())
        prog.progress(80)
        dom = face.get("dominant_emotion", "")
        msg = generate_message(dom)
        time.sleep(0.2)

        prog.progress(100)
        status.success("Completed")
        tip.empty()
        st.markdown('</div>', unsafe_allow_html=True)

        return face, msg

# ──────────────────── Result Card ────────────────────────────────────────
def render_result_card(orig: Image.Image, face: dict, attrs: list, msg: str):
    try:
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("3. Results")

            # Defensive: check if region exists and is valid
            region = face.get("region")
            drawn = orig.copy()
            if region and all(k in region for k in ("x", "y", "w", "h")):
                try:
                    ImageDraw.Draw(drawn).rectangle(
                        [region["x"], region["y"], region["x"]+region["w"], region["y"]+region["h"]],
                        outline=PALETTE.get("primary", "#17E9E0"), width=4
                    )
                except Exception as e:
                    st.warning(f"Could not draw bounding box: {e}")
            else:
                st.warning("No face region found. Showing image without bounding box.")

            # Metrics and image/chart/download in two columns for wide screens
            cols = st.columns([2,2])
            with cols[0]:
                if "emotion" in attrs:
                    raw = face.get("dominant_emotion", "")
                    emoji = EMOJI.get(raw.lower(), "")
                    st.metric("Emotion", f"{raw.capitalize()} {emoji}".strip())
                if "age" in attrs:
                    st.metric("Age", int(face.get("age", 0)))
                if "gender" in attrs:
                    st.metric("Gender", best_label(face.get("gender", {})))
                if "race" in attrs:
                    st.metric("Race", best_label(face.get("race", {})))

                st.success(msg)
                with st.expander("Learn more"):
                    insight = generate_insight(face.get("dominant_emotion", ""))
                    st.write(insight.strip())

            with cols[1]:
                st.image(drawn, caption="Detected face", use_container_width=True)
                chart_data = [
                    {"emotion": e, "conf": float(c)}
                    for e, c in face.get("emotion", {}).items()
                    if isinstance(c, (float, int))
                ]
                if "emotion" in attrs and len(chart_data) > 1:
                    try:
                        chart = (
                            alt.Chart(alt.Data(values=chart_data))
                            .mark_bar(size=25)
                            .encode(
                                x="emotion:N",
                                y=alt.Y("conf:Q", scale=alt.Scale(domain=[0,1])),
                                color="emotion:N",
                                tooltip=["conf:Q"],
                            )
                        )
                        st.altair_chart(chart, use_container_width=True)
                    except Exception as e:
                        st.warning(f"Could not plot emotion chart: {e}")
                try:
                    tmp = save_temp_image(drawn)
                    with open(tmp, "rb") as f:
                        st.download_button(
                            "Download Annotated Image",
                            f,
                            file_name="moodlens_result.png",
                            use_container_width=True
                        )
                    Path(tmp).unlink(missing_ok=True)
                except Exception as e:
                    st.warning(f"Could not create/download image: {e}")

            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Results rendering failed: {e}")


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

# ────────────── 1. CSS & FONT INJECTION ────────────────
def set_page_style():
    st.markdown(
        """
        <style>
          body, .stApp {
            background: linear-gradient(115deg, #f7fafc 0%, #e6ecf6 100%) !important;
          }
          .block-container {
            max-width: 820px;
            margin: 0 auto;
            padding-top: 1.5rem !important;
            padding-bottom: 1.2rem;
          }
          .app-header {
            background: linear-gradient(135deg, #17E9E0, #A64AC9 90%);
            color: #fff;
            padding: 1.1rem 0.5rem;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 0.6rem;
            box-shadow: 0 4px 16px rgba(0,0,0,0.07);
            margin-bottom: 1.2rem;
          }
          /* Sidebar tweaks */
          div[data-testid="stSidebar"] {
            background: #fdfdff !important;
            box-shadow: 0 4px 16px rgba(23,233,224,0.08);
            border-radius: 16px;
          }
          div[data-testid="stSidebar"] .stExpander {
            background: #fafaff !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(166,74,201,0.07);
          }
          /* Card styles */
          .moodlens-card {
            background: #fff;
            border-left: 5px solid #17E9E0;
            padding: 1.1rem 1.2rem 0.8rem 1.2rem;
            margin-bottom: 0.8rem;
            border-radius: 13px;
            box-shadow: 0 4px 24px rgba(166,74,201,0.10);
            transition: box-shadow .15s, transform .15s;
          }
          .moodlens-card:hover {
            box-shadow: 0 4px 18px rgba(166,74,201,0.13);
            transform: translateY(-2px);
          }
          /* Tabs & metrics */
          [data-testid="stTabs"] { margin-bottom: 0.5rem; }
          [data-testid="stTabs"] button[aria-selected="true"] {
            background: #17E9E0 !important; color: #fff !important;
          }
          div[data-testid="metric-container"] {
            background: #f8fafc;
            border-radius: 12px;
            padding: 0.8rem 0.5rem;
            margin: 0.2rem 0;
            box-shadow: 0 1px 4px rgba(166,74,201,0.07);
          }
          .stProgress > div > div > div > div {
            height: 8px !important;
            border-radius: 12px !important;
            background: #A64AC9 !important;
          }
          @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
          * { font-family: 'Poppins', sans-serif !important; }
          header[data-testid="stHeader"] {
            background: transparent !important;
            box-shadow: none !important;
          }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ────────────── 3. Sidebar Controls ────────────────
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

# ────────────── 4. Static Header ────────────────
def render_header():
    img_url = "https://huggingface.co/spaces/mhkali/MoodLens-AI/resolve/main/face.png"
    col1, col2 = st.columns([1, 6], gap="small")

    with col1:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #17E9E0 20%, #A64AC9 100%);
                border-radius: 16px;
                height: 100px;
                width: 100px;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 16px rgba(166,74,201,0.12);
            ">
                <img src="{img_url}" style="height:64px;width:64px;border-radius:12px;object-fit:cover"/>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div style="
                display:inline-block;
                background: linear-gradient(135deg, #17E9E0, #A64AC9 90%);
                border-radius:12px;
                padding:0.8rem 1.2rem;
                max-width:600px;
                box-shadow:0 4px 16px rgba(0,0,0,0.07);
            ">
                <div style="font-size:2.4rem;font-weight:700;color:#fff;line-height:1;">
                  MoodLens-AI
                </div>
                <div style="font-size:1rem; opacity:0.85; margin-top:0.2rem; color:#fff;">
                  Your Emotion Companion
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )





# ────────────── 5. About Tab ────────────────
def render_app_info():
    st.header("About MoodLens-AI")
    st.info(
        "MoodLens-AI is your emotion companion—an open-source web app that senses your feelings "
        "and responds with real-time, personalized support."
    )
    st.write("[🔗 View source on GitHub](https://github.com/mhk12345/facial-emotion-streamlit)")

    st.markdown("### 🤝 Our Team")
    st.markdown(
        """
        - **Mehak Mubarik** — Team Lead, AI/ML Development  
        - **Jawaria Mubarik** — Documentation & Testing  
        - **Arfa Mubarik** — UI/UX Design  
        - **Muhayuddin Mubarik** — Frontend Support  
        """
    )
    st.markdown("---")

    try:
        st.image("workflow_diagram.PNG", caption="System Architecture", use_container_width=True)
    except Exception:
        pass

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("What It Does")
        st.write("""
        - Real-time face detection & alignment  
        - Emotion & demographic analysis  
        - Supportive feedback via generative AI  
        - Browser-based interactive dashboard  
        """)
    with c2:
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
    st.markdown(
        "<div style='text-align:center;opacity:.7;margin-top:1.5em;'>"
        "🌏 <a href='https://github.com/mhk12345/facial-emotion-streamlit' target='_blank'>Contribute on GitHub</a>"
        "</div>",
        unsafe_allow_html=True
    )

# ────────────── 6. Input Card ────────────────
def render_input_card(use_cam: bool):
    with st.container():
        st.markdown('<div class="moodlens-card">', unsafe_allow_html=True)
        st.subheader("1. Upload a Photo")
        if st.button("Use Sample Image"):
            sample = Image.open("sample.jpg").convert("RGB")
            st.caption("Loaded sample image for demo.")
            st.markdown('</div>', unsafe_allow_html=True)
            return sample, np.array(sample)

        uploader = (st.camera_input("Take a photo") if use_cam
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

# ────────────── 7. Processing Card ────────────────
def render_processing_card(img_array: np.ndarray, attrs: list):
    with st.container():
        st.markdown('<div class="moodlens-card">', unsafe_allow_html=True)
        st.subheader("2. Processing")
        prog   = st.progress(0)
        status = st.empty()
        tip    = st.empty()

        status.write("Detecting face")
        tip.info(random_tip()); prog.progress(25); time.sleep(0.2)

        status.write("Analysing attributes")
        tip.info(random_tip()); prog.progress(55)
        warm_up(attrs)
        face = analyze_image(img_array, attrs)
        time.sleep(0.2)

        if not face or "dominant_emotion" not in face:
            status.error("No face detected. Try another photo.")
            prog.progress(100)
            tip.empty()
            st.markdown('</div>', unsafe_allow_html=True)
            st.stop()

        status.write("Generating feedback")
        tip.info(random_tip()); prog.progress(80)
        msg = generate_message(face["dominant_emotion"])
        time.sleep(0.2)
        prog.progress(100)
        status.success("Completed")
        tip.empty()
        st.markdown('</div>', unsafe_allow_html=True)
        return face, msg

# ────────────── 8. Result Card ────────────────
def render_result_card(orig: Image.Image, face: dict, attrs: list, msg: str):
    with st.container():
        st.markdown('<div class="moodlens-card">', unsafe_allow_html=True)
        st.subheader("3. Results")

        # draw box
        drawn = orig.copy()
        region = face.get("region", {})
        if all(k in region for k in ("x","y","w","h")):
            ImageDraw.Draw(drawn).rectangle(
                [region["x"], region["y"],
                 region["x"]+region["w"], region["y"]+region["h"]],
                outline=PALETTE["teal"], width=4
            )

        col1, col2 = st.columns([2,2])
        with col1:
            if "emotion" in attrs:
                raw = face.get("dominant_emotion","")
                st.metric("Emotion", f"{raw.capitalize()} {EMOJI.get(raw.lower(), '')}".strip())
            if "age"    in attrs: st.metric("Age",    int(face.get("age", 0)))
            if "gender" in attrs: st.metric("Gender", best_label(face.get("gender",{})))
            if "race"   in attrs: st.metric("Race",   best_label(face.get("race",{})))

            st.success(msg)
            with st.expander("Learn more"):
                st.write(generate_insight(face.get("dominant_emotion","")).strip())

        with col2:
            st.image(drawn, caption="Detected face", use_container_width=True)
            chart_data = [
                {"emotion": e, "conf": float(c)}
                for e,c in face.get("emotion",{}).items() if isinstance(c,(float,int))
            ]
            if "emotion" in attrs and len(chart_data)>1:
                try:
                    chart = (
                        alt.Chart({"values":chart_data})
                           .mark_bar(size=25)
                           .encode(
                               x="emotion:N",
                               y=alt.Y("conf:Q", scale=alt.Scale(domain=[0,1])),
                               color="emotion:N",
                               tooltip=["conf:Q"],
                           )
                    )
                    st.altair_chart(chart, use_container_width=True)
                except:
                    pass

            tmp = save_temp_image(drawn)
            with open(tmp,"rb") as f:
                st.download_button(
                    "Download Annotated Image",
                    f,
                    file_name="moodlens_result.png",
                    use_container_width=True
                )
            Path(tmp).unlink(missing_ok=True)

        st.markdown('</div>', unsafe_allow_html=True)

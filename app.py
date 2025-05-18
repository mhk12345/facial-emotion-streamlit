# app.py  •  MoodLens-AI  •  Modular, Professional Edition

import streamlit as st

# ─── Must be the first Streamlit command ────────────────────────────────
st.set_page_config(
    page_title="MoodLens-AI",
    layout="wide",
    page_icon="🎭",
    initial_sidebar_state="expanded"
)

from ui import (
    set_page_style,
    render_sidebar,
    render_header,
    render_input_card,
    render_processing_card,
    render_result_card,
    render_app_info,
)

def main():
    """MoodLens-AI: Streamlit Modular Emotion & Feedback App."""
    set_page_style()
    attrs, use_cam = render_sidebar()
    tab_about, tab_demo = st.tabs(["About MoodLens-AI", "Live Demo"])

    with tab_about:
        render_app_info()

    with tab_demo:
        render_header()
        try:
            orig, img_array = render_input_card(use_cam)
            face, msg = render_processing_card(img_array, attrs)
            render_result_card(orig, face, attrs, msg)
        except Exception as e:
            st.error(f"Something went wrong. Please check your input and try again. \n\nDetails: {e}")

if __name__ == "__main__":
    main()

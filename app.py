import streamlit as st

# ─── Must be the first Streamlit command ────────────────────────────────
st.set_page_config(
    page_title="MoodLens-AI",
    page_icon="🎭",
    layout="wide",
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
    # Apply global CSS, fonts & layout tweaks
    set_page_style()

    # Sidebar: choose attributes and camera toggle
    attrs, use_cam = render_sidebar()

    # Top header (badge + title/subtitle)
    render_header()

    # Split into About vs. Live Demo
    tab_about, tab_demo = st.tabs(["About MoodLens-AI", "Live Demo"])

    with tab_about:
        render_app_info()

    with tab_demo:
        try:
            # 1. Upload or snap
            orig, img_array = render_input_card(use_cam)

            # 2. Analyze & message
            face, msg = render_processing_card(img_array, attrs)

            # 3. Show results & download
            render_result_card(orig, face, attrs, msg)

        except Exception as e:
            st.error(
                "😕 Oops — something went wrong while processing your image.\n\n"
                f"**Details:** {e}"
            )

if __name__ == "__main__":
    main()

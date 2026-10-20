import time
import cv2
import numpy as np
import streamlit as st

# --- Page Layout Configuration ---
st.set_page_config(
    page_title="Tactical RGB Spectral Splitter",
    page_icon="📊",
    layout="wide",
)

# Custom Cyberpunk Stadium Styling
st.markdown(
    """
    <style>
    .reportview-container { background: #0d1117; }
    h1 { color: #00ff66 !important; font-family: 'Courier New', monospace; font-weight: bold; }
    .metric-text { font-family: 'Courier New', monospace; font-size: 14px; font-weight: bold; }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("⚽ ATHLETIC SPECTRAL SPECTRUM MONITOR")
st.write("Upload tactical game film or imagery to decode the channel array telemetry.")

# --- File Uploader ---
uploaded_file = st.file_uploader(
    "CHOOSE GAME FILM / IMAGE...", type=["png", "jpg", "jpeg", "webp", "bmp"]
)

if uploaded_file is not None:
    # Convert uploaded file payload into an OpenCV BGR image matrix
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    bgr_img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # Normalize/Scale image dimensions to prevent layout bloating
    h, w = bgr_img.shape[:2]
    scaling_factor = min(350 / w, 350 / h)
    width = int(w * scaling_factor)
    height = int(h * scaling_factor)
    bgr_img = cv2.resize(bgr_img, (width, height), interpolation=cv2.INTER_AREA)

    # Allocate memory mappings for structural empty frames
    blank_red = np.zeros((height, width, 3), dtype=np.uint8)
    blank_green = np.zeros((height, width, 3), dtype=np.uint8)
    blank_blue = np.zeros((height, width, 3), dtype=np.uint8)

    # --- UI Grid Generation ---
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            "<span style='color:#ff3333;'>🔴 FIELD MATRIX: RED</span>",
            unsafe_allow_html=True,
        )
        red_placeholder = st.empty()
        red_metric = st.empty()

    with col2:
        st.markdown(
            "<span style='color:#33ff33;'>🟢 FIELD MATRIX: GREEN</span>",
            unsafe_allow_html=True,
        )
        green_placeholder = st.empty()
        green_metric = st.empty()

    with col3:
        st.markdown(
            "<span style='color:#3333ff;'>🔵 FIELD MATRIX: BLUE</span>",
            unsafe_allow_html=True,
        )
        blue_placeholder = st.empty()
        blue_metric = st.empty()

    # --- Progressive Vector Streaming Loop ---
    step = 4  # Increment row chunk processing size
    for y in range(0, height, step):
        y_end = min(y + step, height)

        # Slice individual target arrays (OpenCV tracking index order: B=0, G=1, R=2)
        blank_red[y:y_end, :, 2] = bgr_img[y:y_end, :, 2]
        blank_green[y:y_end, :, 1] = bgr_img[y:y_end, :, 1]
        blank_blue[y:y_end, :, 0] = bgr_img[y:y_end, :, 0]

        completion_pct = int((y_end / height) * 100)

        # Stream the active updates into placeholders.
        # Streamlit expects RGB channels, so convert OpenCV's native BGR layout on-the-fly.
        red_placeholder.image(
            cv2.cvtColor(blank_red, cv2.COLOR_BGR2RGB), use_container_width=True
        )
        green_placeholder.image(
            cv2.cvtColor(blank_green, cv2.COLOR_BGR2RGB), use_container_width=True
        )
        blue_placeholder.image(
            cv2.cvtColor(blank_blue, cv2.COLOR_BGR2RGB), use_container_width=True
        )

        # Update Analytics Performance metrics live text
        color_hex = "#00ff66" if completion_pct == 100 else "#ffcc00"
        red_metric.markdown(
            f"<p class='metric-text' style='color:{color_hex};'>R-ACCURACY: {completion_pct}% COMPUTED</p>",
            unsafe_allow_html=True,
        )
        green_metric.markdown(
            f"<p class='metric-text' style='color:{color_hex};'>G-VELOCITY: {completion_pct}% COMPUTED</p>",
            unsafe_allow_html=True,
        )
        blue_metric.markdown(
            f"<p class='metric-text' style='color:{color_hex};'>B-ENDURANCE: {completion_pct}% COMPUTED</p>",
            unsafe_allow_html=True,
        )

        time.sleep(0.01)  # Frame pacing control

    st.success("🎯 SPECTRAL MAP MATRIX LOAD COMPLETE!")

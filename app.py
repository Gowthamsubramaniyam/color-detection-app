import streamlit as st
import pandas as pd
import cv2
import numpy as np
from PIL import Image

# Load color dataset
@st.cache_data
def load_colors(csv_path="colors.csv"):
    return pd.read_csv(csv_path)

# Calculate closest color by Euclidean distance
def get_closest_color_name(R, G, B, color_data):
    minimum = float("inf")
    color_name = "Unknown"
    for i in range(len(color_data)):
        d = np.sqrt((R - int(color_data.loc[i, "R"])) ** 2 +
                    (G - int(color_data.loc[i, "G"])) ** 2 +
                    (B - int(color_data.loc[i, "B"])) ** 2)
        if d < minimum:
            minimum = d
            color_name = color_data.loc[i, "color_name"]
    return color_name

# Load the dataset
color_data = load_colors()

st.title("🎨 Color Detection from Images")
st.write("Upload an image and click on it to detect the color.")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("Click anywhere on the image below:")

    # Use OpenCV to get mouse click
    click_info = st.session_state.get("click_info", None)

    if "clicked" not in st.session_state:
        st.session_state.clicked = False

    if st.button("Reset Click"):
        st.session_state.clicked = False
        st.session_state.click_info = None

    def click_event():
        # Launch OpenCV window to get pixel
        def draw_function(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                pixel = image_np[y, x]
                R, G, B = int(pixel[0]), int(pixel[1]), int(pixel[2])
                st.session_state.clicked = True
                st.session_state.click_info = {"x": x, "y": y, "R": R, "G": G, "B": B}
                cv2.destroyAllWindows()

        img_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        cv2.imshow("Click on Image", img_bgr)
        cv2.setMouseCallback("Click on Image", draw_function)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    if st.button("Click to Detect Color"):
        click_event()

    if st.session_state.clicked:
        info = st.session_state.click_info
        color_name = get_closest_color_name(info["R"], info["G"], info["B"], color_data)
        st.success(f"**Detected Color:** {color_name}")
        st.write(f"**RGB:** ({info['R']}, {info['G']}, {info['B']})")
        st.markdown(
            f"<div style='width:100px;height:50px;background-color:rgb({info['R']},{info['G']},{info['B']});border-radius:5px'></div>",
            unsafe_allow_html=True,
        )

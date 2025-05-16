import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

# Load color dataset
@st.cache_data
def load_colors(csv_path="colors.csv"):
    return pd.read_csv(csv_path)

# Calculate closest color using Euclidean distance
def get_closest_color_name(R, G, B, color_data):
    minimum = float("inf")
    closest_color = "Unknown"
    for _, row in color_data.iterrows():
        d = np.sqrt((R - row["R"])**2 + (G - row["G"])**2 + (B - row["B"])**2)
        if d < minimum:
            minimum = d
            closest_color = row["color_name"]
    return closest_color

# Load dataset
color_data = load_colors()

# Streamlit App UI
st.set_page_config(page_title="Color Detection App", layout="centered")
st.title("🎨 Color Detection from Images")
st.markdown("Upload an image and click anywhere to detect the color at that point.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    image_np = np.array(image)

    st.markdown("### Click on the image below to detect the color")
    coords = streamlit_image_coordinates(image, key="click")

    if coords is not None:
        x, y = coords['x'], coords['y']
        if 0 <= x < image_np.shape[1] and 0 <= y < image_np.shape[0]:
            R, G, B = image_np[y, x]
            color_name = get_closest_color_name(R, G, B, color_data)

            st.markdown("---")
            st.markdown(f"### Detected Color: **{color_name}**")
            st.write(f"**RGB:** ({R}, {G}, {B})")

            st.markdown(
                f"<div style='width:100px;height:50px;background-color:rgb({R},{G},{B});border-radius:5px;border:1px solid #000'></div>",
                unsafe_allow_html=True
            )
        else:
            st.error("Click was outside the image bounds.")

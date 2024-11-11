import streamlit as st
import cv2
import numpy as np
from PIL import Image
import io

# Load and preprocess the image
def load_image(image_file):
    img = Image.open(image_file)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    return np.array(img)

# Function to create a sketch effect
def sketch_effect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    inv = 255 - gray
    blur = cv2.GaussianBlur(inv, (21, 21), 0)
    sketch = cv2.divide(gray, 255 - blur, scale=256.0)
    return cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)

# Streamlit App
def main():
    # Custom CSS to center the elements
    st.markdown("""
    <style>
    .center {
        text-align: center;
    }
    .upload-section {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
    .image-container {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin-top: 30px;
    }
    .stFileUploader {
        display: block;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

    # Set up title and description with centered alignment
    st.markdown('<h5 class="center">🎨 Sketch Effect Generator</h5>', unsafe_allow_html=True)
    st.write("Transform your photos into a Sketch Effect with one click!")

    # Center the file uploader button
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    st.markdown('</div>', unsafe_allow_html=True)

    # If an image is uploaded, process it
    
    if uploaded_file is not None:
        image = load_image(uploaded_file)

        # Create two columns for the input and output image sections, side by side
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Original Image")
            st.image(image, caption='Original Image', use_column_width=True)

        with col2:
            if st.button("Generate Sketch", type='primary'):
                with st.spinner("Creating sketch..."):
                    result = sketch_effect(image)
                    result_img = Image.fromarray(result)

                    
                    st.image(result_img, caption="Generated Sketch", use_column_width=True)

                    # Prepare image for download
                    buf = io.BytesIO()
                    result_img.save(buf, format='PNG')

                    # Download button
                    st.download_button(
                        label="📥 Download Sketch",
                        data=buf.getvalue(),
                        file_name="sketch_image.png",
                        mime="image/png"
                    )

if __name__ == '__main__':
    main()

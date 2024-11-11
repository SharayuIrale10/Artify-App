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

# Function to create a neon effect
def neon_effect(img):
    img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = cv2.add(hsv[:, :, 1], 50)  # Increase saturation
    hsv[:, :, 2] = cv2.add(hsv[:, :, 2], 50)  # Increase brightness
    neon = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    blur = cv2.GaussianBlur(neon, (21, 21), 0)
    result = cv2.addWeighted(neon, 1.2, blur, -0.2, 0)
    return Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))

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
    st.markdown('<h5 class="center">🎨 Neon Effect Generator</h5>', unsafe_allow_html=True)
    st.write("Transform your photos into a Neon Effect with one click!")

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
            # Add a centered "Generate Neon Effect" button inside the second column
            st.markdown('<div class="center">', unsafe_allow_html=True)
            if st.button("Generate Neon Effect", type='primary'):
                with st.spinner("Creating neon effect..."):
                    result_img = neon_effect(image)
                    st.image(result_img, caption="Generated Neon Effect", use_column_width=True)

                    # Prepare image for download
                    buf = io.BytesIO()
                    result_img.save(buf, format='PNG')

                    # Download button
                    st.download_button(
                        label="📥 Download Neon Effect",
                        data=buf.getvalue(),
                        file_name="neon_effect_image.png",
                        mime="image/png"
                    )
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()

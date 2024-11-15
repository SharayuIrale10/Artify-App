import streamlit as st
import cv2 # Import OpenCV
import neural_transform  # Import the neural transform module
import sketch  # Import the sketch module
import neon  # Import the neon module
import os  # To work with file paths
import numpy as np  # For handling image data as arrays

# Set up the sidebar
st.sidebar.title("Image Transformation Options")

# Create options in the sidebar
option = st.sidebar.selectbox(
    "Select Transformation Option",
    ("Choose Transformation", "Sketch", "Neon Filter Effect", "Neural Transform")
)

# Main headline for the interface page with a symbol
st.title("🎨 Artify: Unleashing Styling Through Image Transformation")

# Conditional interface for the "Choose Transformation" option
# Conditional interface for the "Choose Transformation" option
if option == "Choose Transformation":
    # Display a short and creative message
    st.markdown("""
        <div style="display: flex; flex-direction: column; align-items: center;">
            <p style="font-size: 20px;">Welcome to Artify! 🌟 Where your images meet magic. Choose a transformation and watch your art come alive!</p>
        </div>
    """, unsafe_allow_html=True)

# Conditional interface for the "Neural Transform" option
elif option == "Neural Transform":
    # Call the neural transform function from neural_transform.py
    neural_transform.neural_transform()  # Executes the neural transform functionality

# Conditional interface for the "Sketch" option
elif option == "Sketch":
    # Call the sketch function from sketch.py
    sketch.main()  # Executes the sketch effect functionality

# Conditional interface for the "Neon Filter Effect" option
elif option == "Neon Filter Effect":
    # Call the neon effect function from neon.py
    neon.main()  # Executes the neon effect functionality

# Conditional interface for the "OpenCV Processing" option
elif option == "OpenCV Processing":
    # Load an image using OpenCV (you can use the first image from the list as an example)
    img_path = r"C:\Users\irale\OneDrive\Desktop\hello\image_style_transfer\images\21.jpg"
    img = cv2.imread(img_path)

    # Perform OpenCV processing (for example, converting to grayscale)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Display the processed image using Streamlit
    st.image(gray_image, caption="Processed with OpenCV (Grayscale)", use_column_width=True)

import functools
import altair as alt
import numpy as np
import streamlit as st
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import io

# Load the TensorFlow Hub model for style transfer
hub_handle = 'https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2'
hub_module = hub.load(hub_handle)

print("TF Version: ", tf.__version__)
print("TF-Hub version: ", hub.__version__)
print("Eager mode enabled: ", tf.executing_eagerly())
print("GPU available: ", tf.config.list_physical_devices('GPU'))

# Function to crop the image to a square
def crop_center(image):
    """Returns a cropped square image."""
    shape = image.shape
    new_shape = min(shape[0], shape[1])
    offset_y = max(shape[0] - shape[1], 0) // 2
    offset_x = max(shape[1] - shape[0], 0) // 2
    image = tf.image.crop_to_bounding_box(
        image, offset_y, offset_x, new_shape, new_shape)
    return image

# Function to load and preprocess the uploaded image
def load_image(uploaded_file, image_size=(256, 256), col=st):
    img = Image.open(uploaded_file)
    img = tf.convert_to_tensor(img)
    img = crop_center(img)
    img = tf.image.resize(img, image_size)
    if img.shape[-1] == 4:  # If image has an alpha channel, remove it
        img = img[:, :, :3]
    img = tf.reshape(img, [-1, image_size[0], image_size[1], 3]) / 255
    col.image(np.array(img[0]))  # Show the uploaded image
    return img

# Function to display multiple images
def show_n(images, titles=('',), col=st):
    n = len(images)
    for i in range(n):
        col.image(np.array(images[i][0]))

# Neural Transform function to be executed
def neural_transform():
    # Define image dimensions
    img_width, img_height = 384, 384
    img_width_style, img_height_style = 384, 384

    # Create two columns for image uploads
    col1, col2 = st.columns(2)
    col1.markdown('### Add image on which style is required')  # Smaller heading
    uploaded_file = col1.file_uploader("Choose image to change", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        content_image = load_image(uploaded_file, (img_width, img_height), col=col1)

    col2.markdown('### Add image from which style will be extracted')  # Smaller heading
    uploaded_file_style = col2.file_uploader("Choose style image", type=["jpg", "jpeg", "png"])

    if uploaded_file_style is not None:
        style_image = load_image(uploaded_file_style, (img_width_style, img_height_style), col=col2)

        # Add a button to trigger the transformation
        if st.button("Transform Image"):
            with st.spinner('Applying style...'):
                # Apply a small filter to the style image (optional, based on your model)
                style_image = tf.nn.avg_pool(style_image, ksize=[3, 3], strides=[1, 1], padding='SAME')

                # Perform the style transfer
                outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
                stylized_image = outputs[0]

                # Resize the stylized image to match the input image size
                stylized_image_resized = tf.image.resize(stylized_image, (img_width, img_height))

                # Display the results
                col3, col4, col5 = st.columns(3)
                col4.markdown('### Style applied on the image')  # Smaller heading
                col4.image(np.array(stylized_image_resized[0] * 255).astype(np.uint8), caption='Stylized Image')

                # Convert the transformed image to a downloadable format
                transformed_img = Image.fromarray(np.uint8(stylized_image_resized[0] * 255))
                buf = io.BytesIO()
                transformed_img.save(buf, format="PNG")
                buf.seek(0)

                # Add download button for the transformed image
                st.download_button(
                    label="📥 Download Stylized Image",
                    data=buf,
                    file_name="stylized_image.png",
                    mime="image/png"
                )

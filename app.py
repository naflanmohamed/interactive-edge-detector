import streamlit as st
import cv2
import numpy as np
from PIL import Image



def sobel_edge_detection(image, ksize, direction):
    """Applies Sobel Edge Detection"""

    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
 
    if direction == 'X':
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        return abs_grad_x
    elif direction == 'Y':
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        return abs_grad_y
    else: # Both X and Y
        grad_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=ksize)
        grad_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=ksize)
        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)
        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
        return grad

def laplacian_edge_detection(image, ksize):
    """Applies Laplacian Edge Detection"""
  
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
 
    laplacian = cv2.Laplacian(gray, cv2.CV_64F, ksize=ksize)
    abs_laplacian = cv2.convertScaleAbs(laplacian)
    return abs_laplacian

def canny_edge_detection(image, low_thresh, high_thresh, ksize, sigma):
    """Applies Canny Edge Detection"""
  
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (ksize, ksize), sigma)
    
    edges = cv2.Canny(blurred, low_thresh, high_thresh)
    return edges


st.set_page_config(layout="wide", page_title="Interactive Edge Detection")

st.title("Interactive Edge Detection Algorithms")
st.write("Upload an image and experiment with different edge detection algorithms and their parameters.")


col1, col2 = st.columns(2)


st.sidebar.header("Controls")


uploaded_file = st.sidebar.file_uploader(
    "Upload an image", type=["jpg", "jpeg", "png", "bmp"]
)

if uploaded_file is not None:
   
    pil_image = Image.open(uploaded_file)
    
    original_image = np.array(pil_image)
    
   
    if original_image.shape[2] == 4:
        original_image = original_image[:, :, :3]

    with col1:
        st.header("Input Image")
        st.image(original_image, use_column_width=True, caption="Original")


    algorithm = st.sidebar.selectbox(
        "Select Edge Detection Algorithm",
        ("Canny", "Sobel", "Laplacian")
    )
    
   
    st.sidebar.header("Algorithm Parameters")
    
    output_image = None

    if algorithm == "Canny":
        st.sidebar.markdown("**Canny Parameters**")
        low_threshold = st.sidebar.slider("Lower Threshold", 0, 500, 50)
        high_threshold = st.sidebar.slider("Upper Threshold", 0, 500, 150)
        ksize_canny = st.sidebar.select_slider("Gaussian Kernel Size", options=[3, 5, 7], value=5)
        sigma = st.sidebar.slider("Gaussian Sigma", 0.1, 5.0, 1.4)
        
        
        output_image = canny_edge_detection(original_image, low_threshold, high_threshold, ksize_canny, sigma)

    elif algorithm == "Sobel":
        st.sidebar.markdown("**Sobel Parameters**")
        ksize_sobel = st.sidebar.select_slider("Kernel Size", options=[1, 3, 5, 7], value=3)
        direction = st.sidebar.radio("Gradient Direction", ('Both', 'X', 'Y'))
        
       
        output_image = sobel_edge_detection(original_image, ksize_sobel, direction)

    elif algorithm == "Laplacian":
        st.sidebar.markdown("**Laplacian Parameters**")
        ksize_laplacian = st.sidebar.select_slider("Kernel Size", options=[1, 3, 5, 7], value=3)
        
       
        output_image = laplacian_edge_detection(original_image, ksize_laplacian)
    
   
    with col2:
        st.header("Output Image")
        if output_image is not None:
            st.image(output_image, use_column_width=True, caption=f"Result of {algorithm}")
        else:
            st.warning("Algorithm could not be applied.")

else:
   
    st.info("Please upload an image using the sidebar to get started.")
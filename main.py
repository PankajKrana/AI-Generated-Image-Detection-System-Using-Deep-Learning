import os
import sys

# Set environment variables BEFORE importing TensorFlow
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import streamlit as st
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image, ImageOps
from tensorflow.keras.preprocessing.image import img_to_array
from pathlib import Path

# --------- CONFIG ---------
IMG_SIZE = 48
MODEL_PATH = Path("AIGeneratedModel.h5")
# Threshold: Model outputs cluster around 0.30-0.36
# Use 0.33 as midpoint: < 0.33 = Real, >= 0.33 = AI-Generated
PREDICTION_THRESHOLD = 0.33


# --------- MODEL LOADING (CACHED) ---------
@st.cache_resource
def load_model():
    """
    Load and cache the TensorFlow model so it's not reloaded
    on every Streamlit rerun.
    """
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model file not found at {MODEL_PATH.resolve()}. "
            "Make sure AIGeneratedModel.h5 is in the same folder as this script. "
            "If using Git LFS, run: git lfs pull"
        )
    
    # Check if it's a Git LFS pointer file (text file)
    try:
        with open(MODEL_PATH, 'r') as f:
            content = f.read().strip()
            if content.startswith('version https://git-lfs.github.com'):
                raise FileNotFoundError(
                    f"Git LFS file detected but not downloaded. Run: git lfs pull"
                )
    except UnicodeDecodeError:
        pass  # Binary file, proceed normally
    
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        return model
    except Exception as e:
        raise RuntimeError(
            f"Failed to load model from {MODEL_PATH}: {str(e)}. "
            "The model file may be corrupted or in wrong format."
        )


# --------- IMAGE PREPROCESSING ---------
def preprocess_image(uploaded_file):
    """
    Open the uploaded image, resize it to (IMG_SIZE, IMG_SIZE),
    normalize it, and return both the display image and the
    preprocessed array ready for prediction.
    """
    try:
        image = Image.open(uploaded_file).convert("RGB")

        # Use modern resampling instead of deprecated ANTIALIAS
        image = ImageOps.fit(image, (IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)

        img_array = img_to_array(image)
        img_array = img_array / 255.0  # normalize to [0, 1]
        img_array = np.expand_dims(img_array, axis=0)  # shape: (1, IMG_SIZE, IMG_SIZE, 3)

        return image, img_array
    except IOError as e:
        raise RuntimeError(f"Failed to open image: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Image preprocessing failed: {str(e)}")


# --------- PREDICTION ---------
def predict(model, img_array):
    """
    Run prediction on a single preprocessed image array.
    Assumes the model outputs a single probability (sigmoid).
    Returns probability that image is AI-generated.
    """
    try:
        preds = model.predict(img_array, verbose=0)
        # preds shape expected: (1, 1) or (1,)
        if isinstance(preds, np.ndarray):
            if preds.ndim > 1:
                prob_ai = float(preds[0][0]) if preds.shape[1] > 0 else float(preds[0])
            else:
                prob_ai = float(preds[0])
        else:
            prob_ai = float(preds)
        
        # Ensure probability is in valid range [0, 1]
        prob_ai = max(0.0, min(1.0, prob_ai))
        return prob_ai
    except Exception as e:
        raise RuntimeError(f"Prediction failed: {str(e)}")


# --------- STREAMLIT UI ---------
def main():
    st.set_page_config(
        page_title="AI Image Classifier",
        page_icon="🧠",
        layout="centered",
    )

    st.title("🧠 AI Image Classifier")
    st.write("Upload an image and I’ll tell you if it’s **Real** or **AI Generated**.")

    uploaded_file = st.file_uploader(
        "Upload an image (JPG/PNG)", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        # Show preview
        st.subheader("Preview")
        st.image(uploaded_file, use_column_width=True)

        if st.button("Check"):
            with st.spinner("Analyzing image..."):
                try:
                    model = load_model()
                    display_image, img_array = preprocess_image(uploaded_file)
                    prob_ai = predict(model, img_array)

                    st.subheader("Result")

                    # Decide label based on threshold
                    # Threshold 0.35: predictions below this = Real, above = AI
                    if prob_ai < PREDICTION_THRESHOLD:
                        st.success(f"✅ The given image is **Real**.")
                    else:
                        st.error(f"🤖 The given image is **AI Generated**.")

                    # # Show probability bar
                    # st.write("**AI-Generated probability:**")
                    # st.progress(min(max(prob_ai, 0.0), 1.0))
                    # st.write(f"{prob_ai * 100:.2f}%")

                except FileNotFoundError as e:
                    st.error(f"❌ **Model Error**: {str(e)}")
                except RuntimeError as e:
                    st.error(f"❌ **Processing Error**: {str(e)}")
                except Exception as e:
                    st.error("❌ **Unexpected Error**: Something went wrong while processing the image.")
                    with st.expander("View error details"):
                        st.code(str(e))


if __name__ == "__main__":
    main()

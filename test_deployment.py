#!/usr/bin/env python3
"""
Comprehensive test suite for AI Image Classifier
Tests all components before deployment
"""

import os
import sys
from pathlib import Path

# Set environment variables before imports
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

def test_imports():
    """Test all required imports"""
    print("\n" + "="*60)
    print("TEST 1: Checking Imports")
    print("="*60)
    
    try:
        import streamlit as st
        print("✓ Streamlit imported")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy imported")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        import tensorflow as tf
        print(f"✓ TensorFlow {tf.__version__} imported")
    except ImportError as e:
        print(f"✗ TensorFlow import failed: {e}")
        return False
    
    try:
        from tensorflow import keras
        print("✓ Keras imported")
    except ImportError as e:
        print(f"✗ Keras import failed: {e}")
        return False
    
    try:
        from PIL import Image, ImageOps
        print("✓ PIL/Pillow imported")
    except ImportError as e:
        print(f"✗ PIL/Pillow import failed: {e}")
        return False
    
    try:
        from tensorflow.keras.preprocessing.image import img_to_array
        print("✓ img_to_array imported")
    except ImportError as e:
        print(f"✗ img_to_array import failed: {e}")
        return False
    
    return True


def test_model_file():
    """Test model file existence and validity"""
    print("\n" + "="*60)
    print("TEST 2: Checking Model File")
    print("="*60)
    
    MODEL_PATH = Path("AIGeneratedModel.h5")
    
    if not MODEL_PATH.exists():
        print(f"✗ Model file not found at {MODEL_PATH}")
        return False
    
    print(f"✓ Model file found")
    
    # Check file size
    file_size = MODEL_PATH.stat().st_size
    file_size_mb = file_size / (1024 * 1024)
    print(f"  File size: {file_size_mb:.2f} MB")
    
    if file_size < 1000:  # Less than 1KB is likely a Git LFS pointer
        print("✗ Model file is too small (likely Git LFS pointer, not downloaded)")
        print("  Run: git lfs pull")
        return False
    
    # Check if it's a text file (Git LFS pointer)
    try:
        with open(MODEL_PATH, 'r') as f:
            content = f.read(50)
            if 'version https://git-lfs.github.com' in content:
                print("✗ Model file is Git LFS pointer (not downloaded)")
                print("  Run: git lfs pull")
                return False
    except UnicodeDecodeError:
        # Binary file is good
        print("✓ Model file is binary (valid HDF5)")
    
    return True


def test_model_loading():
    """Test loading the model"""
    print("\n" + "="*60)
    print("TEST 3: Loading Model")
    print("="*60)
    
    import tensorflow as tf
    
    MODEL_PATH = Path("AIGeneratedModel.h5")
    
    if not MODEL_PATH.exists():
        print("✗ Model file not found")
        return False
    
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        print("✓ Model loaded successfully")
        
        # Check model properties
        print(f"  Input shape: {model.input_shape}")
        print(f"  Output shape: {model.output_shape}")
        
        # Verify expected shapes
        if model.input_shape != (None, 48, 48, 3):
            print(f"⚠ Warning: Expected input shape (None, 48, 48, 3), got {model.input_shape}")
        
        return True
    except Exception as e:
        print(f"✗ Failed to load model: {e}")
        return False


def test_model_prediction():
    """Test model prediction on dummy input"""
    print("\n" + "="*60)
    print("TEST 4: Testing Model Prediction")
    print("="*60)
    
    import tensorflow as tf
    import numpy as np
    
    MODEL_PATH = Path("AIGeneratedModel.h5")
    
    if not MODEL_PATH.exists():
        print("✗ Model file not found")
        return False
    
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        
        # Create dummy input
        dummy_input = np.random.rand(1, 48, 48, 3).astype(np.float32)
        
        # Predict
        prediction = model.predict(dummy_input, verbose=0)
        
        print("✓ Prediction successful")
        print(f"  Output shape: {prediction.shape}")
        print(f"  Output value: {prediction[0]}")
        
        # Convert to probability
        if isinstance(prediction, np.ndarray):
            if prediction.ndim > 1:
                prob = float(prediction[0][0]) if prediction.shape[1] > 0 else float(prediction[0])
            else:
                prob = float(prediction[0])
        else:
            prob = float(prediction)
        
        prob = max(0.0, min(1.0, prob))
        print(f"  Probability: {prob:.4f}")
        
        return True
    except Exception as e:
        print(f"✗ Prediction failed: {e}")
        return False


def test_image_preprocessing():
    """Test image preprocessing with a dummy image"""
    print("\n" + "="*60)
    print("TEST 5: Testing Image Preprocessing")
    print("="*60)
    
    from PIL import Image, ImageOps
    import numpy as np
    from tensorflow.keras.preprocessing.image import img_to_array
    from io import BytesIO
    
    IMG_SIZE = 48
    
    try:
        # Create a dummy image
        dummy_image = Image.new('RGB', (100, 100), color='red')
        img_bytes = BytesIO()
        dummy_image.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        # Test preprocessing
        image = Image.open(img_bytes).convert("RGB")
        print(f"✓ Image opened: {image.size}")
        
        image = ImageOps.fit(image, (IMG_SIZE, IMG_SIZE), Image.Resampling.LANCZOS)
        print(f"✓ Image resized to: {image.size}")
        
        img_array = img_to_array(image)
        print(f"✓ Converted to array: {img_array.shape}")
        
        img_array = img_array / 255.0
        print(f"✓ Normalized to [0, 1]")
        
        img_array = np.expand_dims(img_array, axis=0)
        print(f"✓ Added batch dimension: {img_array.shape}")
        
        # Verify expected shape
        if img_array.shape == (1, IMG_SIZE, IMG_SIZE, 3):
            print(f"✓ Final shape is correct: {img_array.shape}")
        else:
            print(f"⚠ Warning: Expected shape (1, 48, 48, 3), got {img_array.shape}")
        
        return True
    except Exception as e:
        print(f"✗ Image preprocessing failed: {e}")
        return False


def test_files_structure():
    """Test project file structure"""
    print("\n" + "="*60)
    print("TEST 6: Checking File Structure")
    print("="*60)
    
    required_files = [
        "main.py",
        "requirements.txt",
        "AIGeneratedModel.h5",
        "README.md",
        ".gitignore",
    ]
    
    all_exist = True
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"✓ {file}")
        else:
            print(f"✗ {file} (missing)")
            all_exist = False
    
    optional_files = [
        ".streamlit/config.toml",
        "DEPLOYMENT.md",
        "INSTALLATION.md",
        "Dockerfile",
        "docker-compose.yml",
    ]
    
    print("\nOptional files:")
    for file in optional_files:
        path = Path(file)
        if path.exists():
            print(f"✓ {file}")
        else:
            print(f"- {file} (optional)")
    
    return all_exist


def test_dependencies():
    """Test if all dependencies are installed"""
    print("\n" + "="*60)
    print("TEST 7: Checking Dependencies")
    print("="*60)
    
    dependencies = {
        'streamlit': 'Streamlit',
        'numpy': 'NumPy',
        'tensorflow': 'TensorFlow',
        'PIL': 'Pillow',
    }
    
    all_installed = True
    for module_name, display_name in dependencies.items():
        try:
            module = __import__(module_name)
            version = getattr(module, '__version__', 'unknown')
            print(f"✓ {display_name} ({version})")
        except ImportError:
            print(f"✗ {display_name} (not installed)")
            all_installed = False
    
    return all_installed


def run_all_tests():
    """Run all tests"""
    print("\n")
    print("*" * 60)
    print("* AI IMAGE CLASSIFIER - DEPLOYMENT TEST SUITE")
    print("*" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Model File", test_model_file),
        ("File Structure", test_files_structure),
        ("Dependencies", test_dependencies),
        ("Model Loading", test_model_loading),
        ("Prediction", test_model_prediction),
        ("Image Preprocessing", test_image_preprocessing),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✅ All tests passed! Ready for deployment.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Fix issues before deployment.")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)

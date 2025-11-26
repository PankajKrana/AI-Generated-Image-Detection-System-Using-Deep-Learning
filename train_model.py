"""
Training script for AI Image Classifier model.
Trains a CNN to distinguish between real and AI-generated images.
Improved version with data augmentation and better feature learning.
"""

import os
os.environ["OMP_NUM_THREADS"] = "1"

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
from pathlib import Path
import cv2
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

# Configuration
IMG_SIZE = 48
BATCH_SIZE = 32
EPOCHS = 30
LEARNING_RATE = 0.0005

def load_images_from_directory(directory, label, img_size=IMG_SIZE):
    """Load images from a directory recursively and return images with labels."""
    images = []
    labels = []
    directory = Path(directory)
    
    count = 0
    for img_path in directory.rglob('*'):
        if img_path.is_file() and img_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
            try:
                img = cv2.imread(str(img_path))
                if img is not None and img.size > 0:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    img = cv2.resize(img, (img_size, img_size))
                    images.append(img / 255.0)  # Normalize to [0, 1]
                    labels.append(label)
                    count += 1
            except Exception as e:
                pass  # Skip corrupted images
    
    print(f"   Loaded {count} images from {directory.name}")
    return np.array(images), np.array(labels)

def build_model(img_size=IMG_SIZE):
    """Build an improved CNN model for binary classification."""
    model = models.Sequential([
        # Input layer
        layers.Input(shape=(img_size, img_size, 3)),
        
        # Block 1 - Extract fine details
        layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(32, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),
        
        # Block 2 - Extract medium-level features
        layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(64, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),
        
        # Block 3 - Extract high-level features
        layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.Conv2D(128, (3, 3), padding='same', activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D((2, 2)),
        layers.Dropout(0.3),
        
        # Flatten and Dense layers
        layers.Flatten(),
        layers.Dense(256, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(128, activation='relu'),
        layers.BatchNormalization(),
        layers.Dropout(0.5),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.3),
        layers.Dense(1, activation='sigmoid')  # Binary classification
    ])
    
    return model

def create_augmentation():
    """Create data augmentation pipeline."""
    return ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        vertical_flip=True,
        zoom_range=0.2,
        brightness_range=[0.8, 1.2],
        shear_range=0.2,
        fill_mode='nearest'
    )

def main():
    print("=" * 70)
    print("AI IMAGE CLASSIFIER - IMPROVED TRAINING SCRIPT")
    print("=" * 70)
    
    # Load data
    print("\n📂 Loading training data...")
    print("   Loading real images...")
    real_images, real_labels = load_images_from_directory('real', 0, IMG_SIZE)
    
    print("   Loading AI-generated images...")
    ai_images, ai_labels = load_images_from_directory('ai_generated', 1, IMG_SIZE)
    
    # Combine datasets
    X = np.concatenate([real_images, ai_images])
    y = np.concatenate([real_labels, ai_labels])
    
    print(f"\n📊 Total dataset: {len(X)} images")
    print(f"   Real (label=0): {np.sum(y == 0)} images")
    print(f"   AI-Generated (label=1): {np.sum(y == 1)} images")
    print(f"   Class balance: {np.sum(y == 1) / np.sum(y == 0):.2%}")
    
    # Split data (80-20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Further split training into train and validation (75-25)
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.25, random_state=42, stratify=y_train
    )
    
    print(f"\n📋 Data split:")
    print(f"   Training: {len(X_train)} images")
    print(f"   Validation: {len(X_val)} images")
    print(f"   Testing: {len(X_test)} images")
    
    # Build model
    print(f"\n🏗️  Building improved model...")
    model = build_model(IMG_SIZE)
    print(f"   Total parameters: {model.count_params():,}")
    
    # Compile with lower learning rate
    print(f"\n⚙️  Compiling model...")
    optimizer = keras.optimizers.Adam(learning_rate=LEARNING_RATE)
    model.compile(
        optimizer=optimizer,
        loss='binary_crossentropy',
        metrics=['accuracy', keras.metrics.Precision(), keras.metrics.Recall()]
    )
    
    # Create augmentation
    aug = create_augmentation()
    
    # Train model with augmentation
    print(f"\n🚀 Training model for {EPOCHS} epochs with data augmentation...")
    history = model.fit(
        aug.flow(X_train, y_train, batch_size=BATCH_SIZE),
        epochs=EPOCHS,
        validation_data=(X_val, y_val),
        verbose=1,
        steps_per_epoch=len(X_train) // BATCH_SIZE
    )
    
    # Evaluate on test set
    print(f"\n📈 Evaluating on test set...")
    test_loss, test_acc, test_precision, test_recall = model.evaluate(
        X_test, y_test, verbose=0
    )
    
    print(f"\n✅ Test Results:")
    print(f"   Loss: {test_loss:.4f}")
    print(f"   Accuracy: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print(f"   Precision: {test_precision:.4f}")
    print(f"   Recall: {test_recall:.4f}")
    
    # Calculate F1 score
    if (test_precision + test_recall) > 0:
        f1 = 2 * (test_precision * test_recall) / (test_precision + test_recall)
        print(f"   F1 Score: {f1:.4f}")
    
    # Save model
    print(f"\n💾 Saving model...")
    model.save('AIGeneratedModel.h5')
    print(f"   ✓ Model saved to AIGeneratedModel.h5")
    
    # Test predictions
    print(f"\n🧪 Testing predictions on real and AI images...")
    test_real_indices = np.where(y_test == 0)[0]
    test_ai_indices = np.where(y_test == 1)[0]
    
    if len(test_real_indices) > 0:
        samples = X_test[test_real_indices[:5]]
        preds = model.predict(samples, verbose=0)
        print(f"   Real images (should be close to 0.0):")
        for i, pred in enumerate(preds):
            print(f"      Sample {i+1}: {pred[0]:.4f}")
    
    if len(test_ai_indices) > 0:
        samples = X_test[test_ai_indices[:5]]
        preds = model.predict(samples, verbose=0)
        print(f"   AI-Generated images (should be close to 1.0):")
        for i, pred in enumerate(preds):
            print(f"      Sample {i+1}: {pred[0]:.4f}")
    
    print(f"\n" + "=" * 70)
    print("✨ TRAINING COMPLETE! Model is ready for deployment.")
    print("=" * 70)

if __name__ == "__main__":
    main()


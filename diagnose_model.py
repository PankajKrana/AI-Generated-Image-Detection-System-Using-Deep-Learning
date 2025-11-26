"""Diagnose model prediction issues."""
import os
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

import tensorflow as tf
from PIL import Image
import numpy as np
from pathlib import Path

model = tf.keras.models.load_model("AIGeneratedModel.h5")

# Get images
real_imgs = list(Path("real").rglob("*.png")) + list(Path("real").rglob("*.jpg"))
ai_imgs = list(Path("ai_generated").rglob("*.png")) + list(Path("ai_generated").rglob("*.jpg"))

print("=" * 60)
print("MODEL DIAGNOSIS")
print("=" * 60)
print(f"Real images found: {len(real_imgs)}")
print(f"AI images found: {len(ai_imgs)}")

if real_imgs and ai_imgs:
    real_preds = []
    ai_preds = []
    
    # Test 5 real images
    print("\n📊 REAL IMAGES (target: ~0.0):")
    for img_path in real_imgs[:5]:
        img = Image.open(img_path).convert("RGB").resize((48, 48))
        pred = float(model.predict(np.expand_dims(np.array(img)/255.0, 0), verbose=0)[0][0])
        real_preds.append(pred)
        print(f"  {pred:.4f}")
    
    # Test 5 AI images
    print("\n🤖 AI-GENERATED IMAGES (target: ~1.0):")
    for img_path in ai_imgs[:5]:
        img = Image.open(img_path).convert("RGB").resize((48, 48))
        pred = float(model.predict(np.expand_dims(np.array(img)/255.0, 0), verbose=0)[0][0])
        ai_preds.append(pred)
        print(f"  {pred:.4f}")
    
    real_avg = np.mean(real_preds)
    ai_avg = np.mean(ai_preds)
    
    print(f"\n📈 SUMMARY:")
    print(f"  Real avg: {real_avg:.4f}")
    print(f"  AI avg: {ai_avg:.4f}")
    print(f"  Separation: {abs(ai_avg - real_avg):.4f}")
    
    if ai_avg < real_avg:
        print(f"\n❌ PROBLEM: AI outputs LOWER than real ({ai_avg:.4f} < {real_avg:.4f})")
        print("   Labels are inverted in the training script!")
        print("   Solution: Swap the label values in train_model.py")
        print("   Change: real=1, ai=0 (currently: real=0, ai=1)")
    elif abs(ai_avg - real_avg) < 0.1:
        print(f"\n⚠️  WEAK SEPARATION: Predictions too similar")
        print("   Model cannot distinguish between classes")
        print("   This is a dataset quality issue")
    else:
        print(f"\n✓ Label direction is correct")

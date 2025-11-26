# 🧠 AI Image Classifier

A machine learning application that classifies images as **Real** or **AI Generated** using a convolutional neural network trained on ~100,000 images.

## Features

- 🖼️ Upload images (JPG/PNG format)
- 🤖 Binary classification: Real vs AI-Generated
- 📊 Confidence probability displayed as a progress bar
- ⚡ Fast inference with cached model loading
- 🎨 Clean, user-friendly Streamlit interface

## Requirements

- Python 3.12+
- TensorFlow 2.13-2.16 (NOT 2.20+)
- NumPy < 2.0.0
- Streamlit >= 1.51.0

## Installation

### Local Development

```bash
# Clone the repository
git clone <repository-url>
cd Test

# Install dependencies (using uv)
uv sync

# OR using pip
pip install -r requirements.txt
```

### Important: Model File

The `AIGeneratedModel.h5` file is tracked with Git LFS. To download it:

```bash
# Install Git LFS (if not already installed)
brew install git-lfs  # macOS
# OR
apt-get install git-lfs  # Linux

# Pull the LFS files
git lfs pull
```

If Git LFS is not available, you need to manually download the model file and place it in the project root directory.

## Usage

### Running Locally

```bash
# Using uv
uv run streamlit run main.py

# OR using pip
streamlit run main.py
```

The app will be available at `http://localhost:8501`

### Using the App

1. Open the web interface
2. Click "Browse files" and select an image (JPG/PNG)
3. Click the "Check" button to analyze the image
4. View the result and confidence percentage

## Deployment

### Streamlit Cloud

1. Push your code to GitHub (including the model file via Git LFS)
2. Go to https://streamlit.io/cloud
3. Create a new app and connect your repository
4. Select `main.py` as the entry point
5. Deploy!

### Docker

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t ai-classifier .
docker run -p 8501:8501 ai-classifier
```

### Other Platforms

The app can be deployed to:
- Heroku (with Docker)
- AWS (EC2, ECS, Lambda)
- Google Cloud (Cloud Run, App Engine)
- Azure (App Service, Container Instances)

Ensure the model file is available and Python dependencies match `requirements.txt`.

## Model Information

- **Input**: 48×48 RGB images
- **Architecture**: Convolutional Neural Network
- **Training Data**: ~100,000 images (real and AI-generated)
- **Output**: Probability (0.0-1.0) that image is AI-generated
- **Threshold**: 0.5 (≤0.5 = Real, >0.5 = AI Generated)

## Training Data Sources

1. **Web Scraped (Google Images)**:
   - AI Generated Images
   - AI Generated Art
   - AI Generated Characters
   - Stable Diffusion
   - DALL-E 2
   - Midjourney
   - Real: Landscapes, Cityscapes, Animals, Vehicles, Traffic, Offices, Food

2. **Public Datasets**:
   - CIFAKE: Real and AI-Generated Synthetic Images
   - Kaggle: AI Generated Images

## Troubleshooting

### Error: "Git LFS file detected but not downloaded"
```bash
git lfs pull
```

### Error: "Unable to synchronously open file"
The model file is corrupted or in wrong format. Verify the file size is ~5MB (not 132 bytes).

### TensorFlow Threading Issues (macOS)
The app automatically sets environment variables to prevent mutex lock errors. If issues persist:
```bash
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
streamlit run main.py
```

### GPU Memory Issues
The app runs on CPU by default. For GPU support, ensure CUDA-compatible TensorFlow is installed.

## Performance

- Model loading: ~2-3 seconds (first run, cached after)
- Image preprocessing: ~100ms
- Inference: ~50-100ms
- Total prediction time: ~150-200ms

## License

[Add your license here]


## Acknowledgments

- TensorFlow/Keras team
- Streamlit team
- Dataset sources (Google Images, Kaggle, CIFAKE)

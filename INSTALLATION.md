# Installation Guide

## System Requirements

- **Python**: 3.12 or higher
- **RAM**: Minimum 2GB (4GB recommended)
- **Disk Space**: 1GB for dependencies + model file
- **OS**: Linux, macOS, or Windows

## Quick Start (Recommended)

### Step 1: Clone Repository

```bash
git clone <repository-url>
cd Test
```

### Step 2: Download Model File

The model is tracked with Git LFS. You need to download it:

```bash
# Install Git LFS (if not already installed)
brew install git-lfs          # macOS
apt install git-lfs           # Ubuntu/Debian
choco install git-lfs         # Windows

# Pull LFS files
git lfs pull
```

**Verify**: `ls -lh AIGeneratedModel.h5` should show ~5MB, not 132 bytes

### Step 3: Install Dependencies

**Option A: Using UV (Fastest)**
```bash
uv sync
```

**Option B: Using Python venv**
```bash
python3 -m venv .venv
source .venv/bin/activate    # macOS/Linux
# or
.\.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

**Option C: Using Conda**
```bash
conda create -n ai-classifier python=3.12
conda activate ai-classifier
pip install -r requirements.txt
```

### Step 4: Run the App

```bash
streamlit run main.py
```

Visit: http://localhost:8501

## Detailed Installation

### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.12
brew install python@3.12

# Install Git LFS
brew install git-lfs

# Clone and setup
git clone <repository-url>
cd Test
git lfs pull

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run
streamlit run main.py
```

### Ubuntu/Debian Linux

```bash
# Update package list
sudo apt-get update

# Install Python 3.12
sudo apt-get install -y python3.12 python3.12-venv python3.12-dev

# Install Git LFS
sudo apt-get install -y git-lfs

# Install system dependencies for TensorFlow
sudo apt-get install -y libopenblas-dev libomp-dev

# Clone and setup
git clone <repository-url>
cd Test
git lfs pull

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run
streamlit run main.py
```

### Windows (PowerShell)

```powershell
# Install Python 3.12 (download from python.org or use Chocolatey)
choco install python --version=3.12.0

# Install Git LFS
choco install git-lfs

# Clone and setup
git clone <repository-url>
cd Test
git lfs pull

# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# Run
streamlit run main.py
```

## Using Docker

### Prerequisites

- Docker installed
- Docker Compose (optional)

### Build and Run

```bash
# Build image
docker build -t ai-classifier .

# Run container
docker run -p 8501:8501 ai-classifier
```

Visit: http://localhost:8501

### Using Docker Compose

```bash
docker-compose up
```

## Automated Setup Script

For macOS/Linux, use the provided setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
1. Check Python version
2. Create virtual environment
3. Install dependencies
4. Check for Git LFS
5. Verify model file

## Troubleshooting

### Error: "Module not found: tensorflow"

**Solution**:
```bash
# Ensure virtual environment is activated
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\activate    # Windows

# Reinstall requirements
pip install -r requirements.txt
```

### Error: "Git LFS file detected but not downloaded"

**Solution**:
```bash
# Install Git LFS
brew install git-lfs        # macOS
apt install git-lfs         # Linux

# Pull files
git lfs pull

# Verify
file AIGeneratedModel.h5    # Should NOT say "ASCII text"
```

### Error: "Port 8501 already in use"

**Solution**:
```bash
# Kill process on port 8501
lsof -i :8501 | grep LISTEN | awk '{print $2}' | xargs kill -9

# Or use different port
streamlit run main.py --server.port=8502
```

### Error: "Unable to synchronously open file (file signature not found)"

**Solution**:
```bash
# Model file is corrupted or empty
ls -lh AIGeneratedModel.h5

# Re-download
git lfs pull --force
```

### Error: "libc++abi: terminating due to uncaught exception" (macOS)

**Solution**:
```bash
# This is fixed in code, but if it persists:
export OMP_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
streamlit run main.py
```

### Error: "ModuleNotFoundError: No module named 'streamlit'"

**Solution**:
```bash
# Check if virtual environment is activated
which python    # Should show path inside .venv

# If not, activate it
source .venv/bin/activate  # macOS/Linux
.\.venv\Scripts\activate    # Windows

# Install again
pip install -r requirements.txt
```

## Verification

After installation, verify everything works:

```bash
# Check Python
python --version          # Should be 3.12+

# Check virtual environment
which python              # Should show path in .venv

# Check packages
pip list                  # Should show tensorflow, streamlit, etc.

# Check model file
file AIGeneratedModel.h5  # Should say "data" or "HDF5", not "ASCII text"
ls -lh AIGeneratedModel.h5  # Should be ~5MB, not 132 bytes

# Quick test
python -c "import tensorflow as tf; print(f'TensorFlow {tf.__version__}')"
python -c "import streamlit as st; print(f'Streamlit {st.__version__}')"
```

## Performance Optimization

### For Slow Downloads

1. Use a faster internet connection
2. Increase pip timeout: `pip install --default-timeout=1000 -r requirements.txt`

### For Limited Disk Space

1. Use lightweight virtual environment: `python3 -m venv --copies .venv`
2. Clean pip cache: `pip cache purge`

### For Limited RAM

1. Close unnecessary applications
2. Use system swap if available
3. Install one package at a time if needed

## Next Steps

1. ✅ Installation complete
2. 📚 Read [README.md](README.md) for usage instructions
3. 🚀 Read [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options
4. 📝 Check [AIImageClassifier.ipynb](AIImageClassifier.ipynb) for training details

## Support

- Python: https://www.python.org
- TensorFlow: https://www.tensorflow.org/install
- Streamlit: https://docs.streamlit.io/library/get-started/installation
- Git LFS: https://github.com/git-lfs/git-lfs/wiki/Installation

## Version History

- v1.0: Initial release
  - Python 3.12
  - TensorFlow 2.16.2
  - Streamlit 1.51.0
  - NumPy < 2.0.0

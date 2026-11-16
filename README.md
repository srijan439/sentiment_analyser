# 🎭 BERT Sentiment Analyzer

A deep learning-powered sentiment analysis web application that classifies text as **Positive** or **Negative** using a fine-tuned DistilBERT transformer model with an interactive Cyber-Glass web interface.

## 🚀 Features

- **Fine-tuned DistilBERT** on 50K IMDB movie reviews (91.22% accuracy, 91.24% F1)
- **FastAPI Backend** with real-time async inference and batch processing endpoints
- **Cyber-Glass Frontend** — modern interactive UI with live confidence metrics, saliency highlights, audio feedback, and CSV export
- **Hardware Acceleration** — auto-detects Apple Silicon (MPS), NVIDIA CUDA, or CPU fallback
- **Model Explainability** — word salience analysis highlighting influential tokens

## 🏗️ Architecture

```
User Input (Web UI)
        ↓
FastAPI Backend (app/main.py)
        ↓
DistilBERT Tokenizer & PyTorch Model (model/)
        ↓
Classification Head & Saliency Computation
        ↓
JSON Response → Cyber-Glass UI Display
```

## 📁 Project Structure

```
sentiment_analyser/
├── app/
│   ├── app.py              # Application entry point (Uvicorn runner)
│   ├── main.py             # FastAPI backend API & static file serving
│   └── static/             # Modern Cyber-Glass frontend (HTML, CSS, JS)
│       ├── css/
│       │   └── style.css   # Cyber-Glass styling
│       ├── js/
│       │   ├── app.js      # Frontend interaction logic & API client
│       │   └── audio.js    # Sound effects & synthesis
│       └── index.html      # Single-page web interface
├── model/                  # Model configuration, tokenizer, and metrics
├── tests/                  # Project structure and verification tests
├── train.py                # Model fine-tuning script
├── deploy_hf.py            # Hugging Face Spaces deployment script
├── requirements.txt        # Runtime dependencies (FastAPI, PyTorch, Transformers)
├── requirements-train.txt  # Additional dependencies for training
└── README.md
```

## 🛠️ Tech Stack

- **Model**: DistilBERT (`distilbert-base-uncased`)
- **Machine Learning**: PyTorch, Hugging Face Transformers, Datasets
- **Backend**: FastAPI, Uvicorn, Pydantic
- **Frontend**: HTML5, Modern CSS (Cyber-Glass theme), JavaScript (ES6+)
- **Dataset**: IMDB Movie Reviews (50,000 samples)

## 📊 Results

| Metric    | Score |
|-----------|-------|
| Accuracy  | 91.22% |
| F1-Score  | 91.24% |
| Precision | 91.01% |
| Recall    | 91.47% |

*Model fine-tuned for 3 epochs on Apple Silicon MPS.*

---

## 💻 Quick Start / Local Setup

### 1. Prerequisites
- Python 3.10, 3.11, or 3.12
- `git`

### 2. Clone and Setup Environment

#### macOS / Linux
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

#### Windows (PowerShell)
```powershell
# Create and activate virtual environment
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 3. Run the Application

```bash
python app/app.py
```

Open your browser at **http://localhost:8501**.

> **Note:** On first startup, if local weights are not present in `model/`, the app will automatically download the fine-tuned weights (~268 MB) from Hugging Face. Subsequent runs reuse the cached weights locally.

---

## 🧪 Running Tests

To run project verification tests:

```bash
pip install pytest
pytest -q
```

---

## 🎓 Model Training (Optional)

The model is already pre-trained and ready to use. If you wish to retrain or fine-tune from scratch on the IMDB dataset:

```bash
pip install -r requirements-train.txt
python train.py
```

---

## 📝 License

MIT

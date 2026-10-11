# 🎭 BERT Sentiment Analyzer

A deep learning-powered sentiment analysis web application that classifies text as **Positive** or **Negative** using a fine-tuned BERT transformer model.

## 🚀 Features

- **Fine-tuned BERT** on 50K IMDB movie reviews
- **Real-time inference** with confidence scores
- **Batch analysis** — analyze multiple texts at once
- **Interactive Streamlit UI** with color-coded results
- **Download results** as CSV

## 🏗️ Architecture

```
Input Text → BERT Tokenizer → BERT Model → Classification Head → Sentiment + Confidence
```

## 📁 Project Structure

```
Sentiment/
├── data/           # Dataset scripts & exploration
├── model/          # Saved model weights & tokenizer
├── app/            # Streamlit web application
├── train.py        # Model training script
├── requirements.txt
└── README.md
```

## 🛠️ Tech Stack

- **Model**: BERT (bert-base-uncased) / DistilBERT
- **Framework**: PyTorch + HuggingFace Transformers
- **Dataset**: IMDB Movie Reviews (50K samples)
- **UI**: Streamlit
- **Deployment**: HuggingFace Spaces

## 📊 Results

| Metric    | Score |
|-----------|-------|
| Accuracy  | 91.22% |
| F1-Score  | 91.24% |
| Precision | 91.01% |
| Recall    | 91.47% |

*Model was fine-tuned for 3 epochs in ~110 minutes on an Apple Silicon MPS.*

## 📸 Screenshots

![Sentiment Analysis Web App](data/app_screenshot.png)

## Run Locally on Windows

Use Python 3.10 or 3.11. Open PowerShell in the project folder (the folder containing `requirements.txt`) and run:

```powershell
# Create and activate an isolated environment
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install the project dependencies
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Start the Streamlit app
python -m streamlit run app/app.py
```

Open the local URL printed in the terminal, usually http://localhost:8501. On its first start, the app downloads the fine-tuned model weights from Hugging Face (about 268 MB), so an internet connection is required. Later starts reuse the downloaded file in `model/`.

If PowerShell blocks environment activation, run this once in that terminal and activate again:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

To leave the virtual environment, run `deactivate`. To start the app again later, open PowerShell in the project folder, activate `.venv` as above, then run `python -m streamlit run app/app.py`.

The model is already fine-tuned; you do not need to run `train.py` to use the app. Training is optional and downloads the IMDB dataset.

## Run on macOS or Linux

Create and activate a virtual environment with `python3 -m venv .venv` and `source .venv/bin/activate`, then install with `python -m pip install -r requirements.txt` and launch with `python -m streamlit run app/app.py`.

Hosted app: https://huggingface.co/spaces/Adit-11/bert-sentiment-analyzer

## 📝 License

MIT

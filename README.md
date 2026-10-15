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

## Deploy the existing Docker image to AWS EC2 with Terraform

This beginner deployment creates one EC2 instance and one security group. EC2 installs Docker, pulls your public Docker Hub image, and starts Streamlit on port 8501. SSH is restricted to your public IPv4 address.

You need AWS CLI credentials with EC2 permissions, Terraform 1.5 or newer, and a public Docker Hub image. The default instance is `t3.large` to provide memory for the model. EC2 usage and its 30 GB encrypted disk incur AWS charges while running; stop or destroy the instance when you are finished.

### Configure values

Copy `terraform/terraform.tfvars.example` to `terraform/terraform.tfvars` and replace the Docker Hub username/image, your SSH IP, and key pair name. Do not commit `terraform.tfvars` or any private key.

```powershell
Copy-Item terraform/terraform.tfvars.example terraform/terraform.tfvars
```

### Create and deploy

From the project root:

```powershell
terraform -chdir=terraform init
terraform -chdir=terraform fmt
terraform -chdir=terraform validate
terraform -chdir=terraform plan
terraform -chdir=terraform apply
```

Review the plan before applying. Terraform outputs the public IP and application URL. Open the URL in a browser once EC2 has finished its first-boot Docker setup.

### Clean up

When finished, remove the EC2 instance and security group with:

```powershell
terraform -chdir=terraform destroy
```

This deletes Terraform-managed infrastructure. The local Terraform state file tracks those resources and should be kept until cleanup is complete.

## Run the monitoring stack

Install Docker Compose v2, set a Grafana password, then start the app, Prometheus, and Grafana:

```powershell
$env:GRAFANA_ADMIN_PASSWORD = "choose-a-strong-password"
docker compose up --build -d
```

Open the app at http://localhost:8501, Prometheus at http://localhost:9090, and Grafana at http://localhost:3000 (login `admin` with the password above). In Grafana, add Prometheus as a data source at `http://prometheus:9090`. Metrics are exposed at http://localhost:8000/metrics; prediction counters and latency histograms appear after predictions are made. Stop the stack with `docker compose down`.

## Run checks and deploy to Kubernetes

Run the project checks with `python -m pip install pytest` and `python -m pytest -q`.

For a local Minikube deployment, build and load the image, then apply the manifests:

```powershell
docker build -t sentiment-test:latest .
minikube image load sentiment-test:latest
kubectl apply -f k8s/
minikube service sentiment-test
```

The HPA requires the Kubernetes Metrics Server and CPU resource metrics. For Jenkins, configure a Docker Hub username/password credential named `dockerhub-credentials`, set `DOCKERHUB_REPOSITORY` to your image namespace and repository, and optionally enable `DEPLOY_TO_KUBERNETES` when the Jenkins agent has the intended cluster context configured.

## 📝 License

MIT

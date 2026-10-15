from huggingface_hub import HfApi
import os

api = HfApi()

# Define repo ID
repo_id = "Adit-11/bert-sentiment-analyzer"

# Create the repository (Space)
print("Creating space...")
api.create_repo(repo_id=repo_id, repo_type="space", space_sdk="streamlit", exist_ok=True)

# Prepare frontmatter for README.md
frontmatter = """---
title: BERT Sentiment Analyzer
emoji: 🎭
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.34.0
app_file: app/app.py
pinned: false
---
"""

# Read the Hugging Face specific README and prepend frontmatter
with open("README.md", "r", encoding="utf-8") as f:
    existing_readme = f.read()

with open("HF_README.md", "w", encoding="utf-8") as f:
    f.write(frontmatter + existing_readme)

print("Uploading files...")
api.upload_folder(
    folder_path=".",
    repo_id=repo_id,
    repo_type="space",
    allow_patterns=["app/**", "model/**", "requirements.txt"],
)

# Upload the HF_README.md specifically as README.md
api.upload_file(
    path_or_fileobj="HF_README.md",
    path_in_repo="README.md",
    repo_id=repo_id,
    repo_type="space"
)

print(f"Deployed successfully to https://huggingface.co/spaces/{repo_id}")

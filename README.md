# VROBOTIC ESP32 Smart Car Backend Engine

This repository manages the asynchronous FastAPI backend server and Hugging Face AI pipeline connectivity framework.

## 🛠️ Prerequisites
* **Python version required:** `3.10.1` 

## 🚀 Local Installation
1. Map your Hugging Face Token to your environment:
   ```powershell
   \$env:HF_TOKEN="your_token_here"
   ```
2. Install the package registry:
   ```powershell
   pip install --user -r requirements.txt
   ```
3. Launch the operational workspace server:
   ```powershell
   python -m uvicorn main:app --reload --port 8000
   ```

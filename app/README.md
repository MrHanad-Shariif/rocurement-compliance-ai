# Procurement Compliance AI

A FastAPI application that validates Purchase Requisitions (PR) against compliance rules and generates Request for Quotation (RFQ) PDFs.

## Requirements

- Python 3.8+
- pip

--
## Setup Instructions

### 1. Clone the repository


git clone https://github.com/MrHanad-Shariif/rocurement-compliance-ai.git

cd procurement-compliance-ai/app

### 2. Create and activate a virtual environment (optional but recommended)

Linux/macOS

python3 -m venv venv
source venv/bin/activate

Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

### 3. Install dependencies

pip install -r requirements.txt

### 4. Download spaCy English model

python -m spacy download en_core_web_sm

### 5. Run the application
uvicorn app.main:app --reload --port 8080

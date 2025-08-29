# News\_Analysis

> A web application for analyzing news articles with user management, sentiment analysis, and named entity recognition.

---

## ✨ Overview

**News\_Analysis** is a full-stack application with a React frontend and a Python Flask backend. It allows users to register, log in, and manage profiles with preferences like language and areas of interest. The backend performs NLP tasks such as sentiment analysis and Named Entity Recognition (NER) on ingested news data. Dashboards provide a visual overview of results.

## 🧰 Tech Stack

* **Frontend:** React
* **Backend:** Python (Flask)
* **Libraries/Tools:** NLTK, spaCy, Hugging Face Transformers
* **API:** News API
* **Authentication:** JWT (JSON Web Token)

## ✅ Features

### Module 1 – User & Data Handling

* Secure User Registration with JWT authentication
* Login System for authentication
* Profile Management (language + interest preferences)
* Initial Data Ingestion Script for raw text data
* Data Preprocessing
* Dashboard Creation

### Module 2 – Core NLP Analysis

* **Text Preprocessing Pipeline** (cleaning, tokenization, normalization)
* **Sentiment Analysis** using pre-trained Hugging Face models
* **Named Entity Recognition (NER)** using spaCy or Hugging Face
* **Initial Web Interface** (Flask/Streamlit) for raw analysis (input → sentiment + entities)

## 📦 Installation

### Frontend (React)

```bash
# Inside frontend directory
npm install
npm run dev
```

### Backend (Flask)

```bash
# 1. Open new terminal and create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install requirements
pip install -r requirements.txt
# or manually
pip install flask flask-cors nltk spacy transformers

# 4. Run backend (ensure app.py path is correct)
python app.py
```

Backend will start once the environment is activated.

## 🔌 API Endpoints

* `POST /register` → User registration
* `POST /login` → User login
* `GET /profile` → Get user profile
* `POST /analyze` → Run sentiment analysis + NER on text

## 🗂️ Folder Structure

```
news_analysis/
├─ client/          # React frontend
├─ server/          # Flask backend
│  ├─ app.py
│  ├─ requirements.txt
│  └─ nlp/          # NLP scripts (preprocessing, models)
└─ README.md
```

## 🚀 Usage

* Run **frontend** → `npm run dev`
* Run **backend** → activate virtualenv → `python app.py`

Access the React frontend in your browser (default: `http://localhost:5173/`).

---

> License section hata diya gaya hai (project currently without license).

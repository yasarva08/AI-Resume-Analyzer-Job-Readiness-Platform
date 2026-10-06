# 🤖 AI Resume Analyzer & Job Readiness Platform

An AI-powered full-stack application that analyzes a candidate's resume against a given job description and provides actionable insights for improving job readiness.

## 🚀 Live Demo

**Frontend:** [AI Resume Analyzer & Job Readiness Platform](https://ai-resume-analyzer-job-readiness-platform.onrender.com/)

**Backend API:**
https://ai-resume-analyzer-api-mbmr.onrender.com

## 📌 Overview

The **AI Resume Analyzer & Job Readiness Platform** helps candidates understand how well their resume matches a specific job description.

The platform analyzes the uploaded resume and job description to generate:

* Resume Match Score
* Job Readiness Score
* Matched Skills
* Missing Skills
* Skills to Improve
* Personalized Feedback
* Recommended Learning
* Resume Improvement Suggestions

## ✨ Features

### 📄 Resume Analysis

* Upload resume in PDF format
* Extract resume text automatically
* Analyze resume content against a target job description

### 🎯 Job Matching

* Calculates a skill-based resume match score
* Identifies skills present in both resume and job description
* Identifies missing job-relevant skills

### 📊 Job Readiness

* Generates a job readiness score based on resume-job compatibility
* Highlights areas that require improvement

### 🧠 Personalized Recommendations

* Provides learning recommendations for missing skills
* Suggests resume improvements
* Generates personalized feedback based on the analysis

### 🔍 Skill Detection

The application supports normalized skill matching and handles variations such as:

* Python / python / PYTHON
* SQL / sql
* Machine Learning / machine learning
* React.js / ReactJS / react js

It also avoids common false matches such as **Java vs JavaScript**.

## 🛠️ Tech Stack

### Frontend

* HTML5
* CSS3
* JavaScript

### Backend

* Python
* FastAPI
* PyPDF2

### Machine Learning / NLP

* Scikit-learn
* TF-IDF
* Cosine Similarity
* Skill-based matching

### Deployment

* Render
* GitHub

## 📂 Project Structure

```text
AI-Resume-Analyzer-Job-Readiness-Platform/
│
├── Backend/
│   └── main.py
│
├── Frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── .gitignore
├── requirements.txt
├── app.py
└── main.py
```

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/yasarva08/AI-Resume-Analyzer-Job-Readiness-Platform.git
cd AI-Resume-Analyzer-Job-Readiness-Platform
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the backend

```bash
python3 -m uvicorn Backend.main:app --reload --port 8000
```

The backend will run at:

```text
http://127.0.0.1:8000
```

### 4. Open the frontend

Open:

```text
Frontend/index.html
```

in a browser or use a local development server.

## 🔄 Application Workflow

```text
Resume PDF
     ↓
Text Extraction
     ↓
Skill Detection & Normalization
     ↓
Job Description Analysis
     ↓
Resume ↔ Job Skill Comparison
     ↓
Match Score + Job Readiness
     ↓
Missing Skills & Improvement Areas
     ↓
Personalized Recommendations
```

## 📊 Output

The application provides a complete analysis dashboard containing:

| Metric                   | Description                                      |
| ------------------------ | ------------------------------------------------ |
| Resume Match Score       | Compatibility between resume and job description |
| Job Readiness            | Overall readiness based on identified skills     |
| Matched Skills           | Skills found in both resume and job description  |
| Missing Skills           | Job-relevant skills not detected in the resume   |
| Skills to Improve        | Priority areas for improvement                   |
| Learning Recommendations | Suggested areas to learn                         |
| Resume Suggestions       | Suggestions to strengthen the resume             |

## 🎯 Use Case

This platform is designed for students, freshers, and job seekers who want to:

* Evaluate their resume before applying
* Identify skill gaps
* Understand job requirements
* Improve their resume
* Create a focused learning plan
* Increase their preparation for technical roles

## 👨‍💻 Author

**Yasar Vazi**

GitHub:
https://github.com/yasarva08

LinkedIn:
https://www.linkedin.com/in/yasar-vazi-81b539290/

## 📄 License

This project is developed for educational and portfolio purposes.

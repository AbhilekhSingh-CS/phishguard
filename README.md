# PhishGuard — ML Phishing URL Detector

A full-stack machine learning project that detects phishing URLs in real time.

## Live Demo
Paste any URL → ML model analyzes 30 features → instant phishing/safe verdict

## Tech Stack
- **ML Model:** Random Forest Classifier (scikit-learn)
- **Dataset:** UCI Phishing Websites Dataset (11,055 URLs)
- **Backend:** Python, Flask REST API
- **Frontend:** HTML, CSS, Vanilla JavaScript

## Model Performance
| Metric | Score |
|--------|-------|
| Accuracy | 97.60% |
| Precision | 97.93% |
| Recall | 96.63% |
| F1 Score | 97.28% |

## Features Extracted from URLs
- IP address as domain detection
- SSL certificate state
- URL length analysis
- Domain prefix/suffix patterns
- Subdomain count
- Shortening service detection
- 24 more features...

## How to Run

### 1. Install dependencies
pip install flask flask-cors scikit-learn pandas numpy scipy

### 2. Download UCI Phishing Dataset
Download from: https://archive.ics.uci.edu/dataset/327/phishing+websites
Place as uci_dataset.arff in project folder

### 3. Train the model
python3 step6_train_uci.py

### 4. Start the API
python3 step4_api.py

### 5. Open frontend
Open index.html in your browser

## Project Structure
- step1_explore.py — Dataset exploration
- step2_preprocess.py — Data cleaning
- step3_train.py — First model training
- step6_train_uci.py — Final model training (UCI dataset)
- step4_api.py — Flask REST API
- index.html — Frontend UI

## Author
Abhilekh Singh — B.Tech CSE, Pranveer Singh Institute of Technology
GitHub: https://github.com/AbhilekhSingh-CS

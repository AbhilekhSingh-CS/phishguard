# PhishGuard — ML Phishing URL Detector

A full-stack machine learning project that detects phishing URLs in real time.

## Live Demo
Paste any URL → ML model analyzes 30 features → instant phishing/safe verdict

## Tech Stack
- **ML Model:** Random Forest Classifier (scikit-learn)
- **Dataset:** UCI Phishing Websites Dataset (11,055 URLs)
- **Backend:** Python, Flask REST API
- **Frontend:** HTML, CSS, Vanilla JavaScript

## Two Models

This project contains two trained models.

**Model A — full feature set (30 features)**
Trained on the complete UCI dataset. This is the research benchmark.

| Metric | Score |
|--------|-------|
| Accuracy | 97.60% |
| Precision | 97.93% |
| Recall | 96.63% |
| F1 Score | 97.28% |

**Model B — URL-only (14 features)**  ← used by the live API

| Metric | Score |
|--------|-------|
| Accuracy | 90.64% |
| Precision | 89.80% |
| Recall | 88.98% |
| F1 Score | 89.39% |

### Why two models?

16 of the 30 UCI features cannot be computed from a URL string alone — they
require WHOIS lookups (domain age), DNS queries, traffic ranking APIs, or
fetching the page itself (anchor URLs, iframes, form handlers).

The original API hardcoded those 16 as constants. Four of them defaulted to
`-1`, which UCI encodes as phishing-like, so every URL received four automatic
phishing votes. Legitimate sites such as google.com were being flagged.

Model B is trained only on the 14 features computable from a URL string, so no
input is fabricated at inference time. Accuracy drops by 7 points, but the
number reflects what the deployed system actually achieves.

On the same 2,211-URL test set, missed phishing rose from 33 to 108 — the
concrete cost of the unavailable features.

### Known limitations

- **SSLfinal_State** is the most important feature (66% of Model B's decisions),
  but is approximated. UCI defines it as HTTPS + trusted issuer + certificate
  older than one year; the API only checks for `https://`. A phishing site with
  a fresh Let's Encrypt certificate would appear legitimate.
- The model detects **structural** anomalies, not **semantic** ones. A clean-looking
  lookalike domain passes. Catching those needs brand-similarity or edit-distance checks.
- The UCI dataset is from 2015. Free TLS certificates have since weakened the
  SSL signal considerably.
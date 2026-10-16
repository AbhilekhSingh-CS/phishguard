from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import pandas as pd
import re
from urllib.parse import urlparse
from lookups import check_dns, check_whois

app = Flask(__name__)
CORS(app)

print("Loading URL-only model...")
with open("model_v2.pkl", "rb") as f:
    model = pickle.load(f)
with open("feature_names_v2.pkl", "rb") as f:
    feature_names = pickle.load(f)
print("Model loaded! Using", len(feature_names), "features")


def is_ip(domain):
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain.split(":")[0]))


def extract_features(url):
    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse(url)
    domain = parsed.hostname or ""
    path = parsed.path or ""
    https = parsed.scheme == "https"
    ip = is_ip(domain)
    dots = domain.count(".")
    shorteners = ["bit.ly", "goo.gl", "tinyurl", "ow.ly", "t.co", "is.gd", "buff.ly"]
    bad_tlds = [".xyz", ".tk", ".pw", ".cc", ".top", ".loan", ".gq", ".ml", ".ga"]
    L = len(url)

    if ip:
        sub = -1
    elif dots <= 1:
        sub = 1
    elif dots == 2:
        sub = 0
    else:
        sub = -1

    if ip:
        ssl = -1
    elif https:
        ssl = 1
    else:
        ssl = 0

    if ip:
        stat = -1
    elif any(domain.endswith(t) for t in bad_tlds):
        stat = -1
    else:
        stat = 1

    try:
        prt = parsed.port
    except ValueError:
        prt = None

    if ip:
        dns_record, age, reg_length = -1, -1, -1
    else:
        dns_record = check_dns(domain)
        age, reg_length = check_whois(domain)

    features = {
        "having_IP_Address": -1 if ip else 1,
        "URL_Length": 1 if L < 54 else (0 if L <= 75 else -1),
        "Shortining_Service": -1 if any(s in domain for s in shorteners) else 1,
        "having_At_Symbol": -1 if "@" in url else 1,
        "double_slash_redirecting": -1 if "//" in path else 1,
        "Prefix_Suffix": -1 if "-" in domain else 1,
        "having_Sub_Domain": sub,
        "SSLfinal_State": ssl,
        "port": -1 if (prt and prt not in [80, 443]) else 1,
        "HTTPS_token": -1 if "https" in domain.lower() else 1,
        "Submitting_to_email": -1 if "mailto:" in url.lower() else 1,
        "Abnormal_URL": 1 if domain and domain in url else -1,
        "Redirect": 1 if url.count("//") > 1 else 0,
        "Statistical_report": stat,
        "DNSRecord": dns_record,
        "age_of_domain": age,
        "Domain_registeration_length": reg_length,
    }
    return features, url


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Phishing Detector API (URL-only model)",
        "features_used": len(feature_names),
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing url"}), 400

    url = data["url"].strip()
    if not url:
        return jsonify({"error": "Empty url"}), 400

    features, url = extract_features(url)

    vector = pd.DataFrame([[features[f] for f in feature_names]], columns=feature_names)
    probability = model.predict_proba(vector)[0]
    phishing_prob = float(probability[1])
    # Safety rule: a raw IP instead of a domain name is almost always a scam.
    # The UCI dataset is noisy here (about 50/50), so we don't rely on the model alone.
    if features["having_IP_Address"] == -1:
        phishing_prob = max(phishing_prob, 0.90)

    is_phishing = phishing_prob >= 0.50

    if phishing_prob >= 0.70:
        risk = "HIGH"
    elif phishing_prob >= 0.40:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    return jsonify({
        "url": url,
        "result": "phishing" if is_phishing else "legitimate",
        "is_phishing": is_phishing,
        "phishing_probability": round(phishing_prob, 4),
        "legit_probability": round(1 - phishing_prob, 4),
        "confidence": round(phishing_prob if is_phishing else 1 - phishing_prob, 4),
        "risk_level": risk,
        "features": features,
    })


if __name__ == "__main__":
    print("\n=============================")
    print("  Phishing Detector API v2")
    print("Loading 17-feature model...")
    print("  Running on: http://localhost:8080")
    print("=============================\n")
    app.run(debug=True, port=8080)
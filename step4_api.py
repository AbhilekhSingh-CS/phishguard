from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import re
from urllib.parse import urlparse

app = Flask(__name__)
CORS(app)

print("Loading model...")
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler.pkl", "rb") as f:
    scaler = pickle.load(f)
with open("feature_names.pkl", "rb") as f:
    feature_names = pickle.load(f)
print("Model loaded!")

def is_ip(domain):
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", domain))

def extract_features(url):
    if not url.startswith("http"):
        url = "http://" + url
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or ""
        path = parsed.path or ""
        full = url
        https = parsed.scheme == "https"
        ip = is_ip(domain)
        dots = domain.count(".")
        shorteners = ["bit.ly","goo.gl","tinyurl","ow.ly","t.co"]
        bad_tlds = [".xyz",".tk",".pw",".cc",".top",".loan",".gq",".ml",".ga"]
        l = len(full)

        if ip:
            sub = -1
        else:
            sub = 1 if dots == 1 else (0 if dots == 2 else -1)

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

        return {
            "having_IP_Address": -1 if ip else 1,
            "URL_Length": 1 if l < 54 else (0 if l <= 75 else -1),
            "Shortining_Service": -1 if any(s in domain for s in shorteners) else 1,
            "having_At_Symbol": -1 if "@" in full else 1,
            "double_slash_redirecting": -1 if "//" in path else 1,
            "Prefix_Suffix": -1 if "-" in domain else 1,
            "having_Sub_Domain": sub,
            "SSLfinal_State": ssl,
            "Domain_registeration_length": -1,
            "Favicon": 1,
            "port": -1 if (parsed.port and parsed.port not in [80,443]) else 1,
            "HTTPS_token": -1 if "https" in domain.lower() else 1,
            "Request_URL": 1,
            "URL_of_Anchor": 0,
            "Links_in_tags": 1,
            "SFH": -1 if "about:blank" in full else 1,
            "Submitting_to_email": -1 if "mailto:" in full else 1,
            "Abnormal_URL": 1,
            "Redirect": 1 if full.count("//") > 1 else 0,
            "on_mouseover": 1,
            "RightClick": 1,
            "popUpWidnow": 1,
            "Iframe": 1,
            "age_of_domain": -1,
            "DNSRecord": -1,
            "web_traffic": -1,
            "Page_Rank": -1,
            "Google_Index": 1,
            "Links_pointing_to_page": 0,
            "Statistical_report": stat
        }, url
    except Exception as e:
        print("Error:", e)
        return {f: 0 for f in feature_names}, url

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "running", "message": "Phishing Detector API is live!"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "url" not in data:
        return jsonify({"error": "Missing url"}), 400
    url = data["url"].strip()
    features, url = extract_features(url)
    vector = [features.get(f, 0) for f in feature_names]
    vector = np.array(vector).reshape(1, -1)
    vector_scaled = scaler.transform(vector)
    probability = model.predict_proba(vector_scaled)[0]
    phishing_prob = float(probability[1])
    is_phishing = phishing_prob >= 0.30
    if phishing_prob >= 0.60:
        risk = "HIGH"
    elif phishing_prob >= 0.30:
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
        "features": features
    })

if __name__ == "__main__":
    print("\n=============================")
    print("  Phishing Detector API")
    print("  Running on: http://localhost:8080")
    print("=============================\n")
    app.run(debug=True, port=8080)

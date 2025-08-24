import re
import joblib

# Load the trained model
model = joblib.load("phishing_model.pkl")

# Feature extraction function (must match the one used in training)
def extract_features(url):
    return [
        len(url),                      # URL length
        url.count('.'),                # Number of dots
        1 if re.search(r'\d', url) else 0,  # Has numbers
        1 if "https" in url else 0,     # Uses HTTPS
        sum(1 for c in url if c in ['@', '-', '_', '=', '?', '&', '%'])  # Special chars count
    ]

# Function to check if a URL is phishing
def check_url(url):
    features = extract_features(url)
    prediction = model.predict([features])[0]
    return "Phishing 🚨" if prediction == 1 else "Safe ✅"

# Example URLs to test
print(check_url("http://secure-login123.net/account"))
print(check_url("https://github.com/openai"))
print(check_url("https://github.com/"))
print(check_url("https://www.youtube.com/"))
print(check_url("https://snapinsta.to/en"))
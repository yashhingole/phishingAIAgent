import pandas as pd
import re
import tldextract
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import os
import chardet

# -------------------
# Feature extraction
# -------------------
def extract_features(url):
    if not isinstance(url, str):  # Handle NaN or invalid URLs
        return {
            'url_length': 0,
            'num_dots': 0,
            'has_ip': 0,
            'has_https': 0,
            'has_at': 0,
            'has_dash': 0,
            'num_suspicious_words': 0,
            'domain_length': 0
        }
    
    features = {
        'url_length': len(url),
        'num_dots': url.count('.'),
        'has_ip': 1 if re.search(r'\d{1,3}(\.\d{1,3}){3}', url) else 0,
        'has_https': 1 if url.startswith('https') else 0,
        'has_at': 1 if '@' in url else 0,
        'has_dash': 1 if '-' in url else 0,
        'num_suspicious_words': sum(
            1 for word in ['login', 'verify', 'update', 'free', 'secure']
            if word in url.lower()
        ),
        'domain_length': len(tldextract.extract(url).domain)
    }
    return features

# -------------------
# Detect file encoding
# -------------------
file_path = 'data/urls.csv'

try:
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read(100000))  # Read first 100KB
    file_encoding = result['encoding'] or 'utf-8'
    print(f"📄 Detected encoding: {file_encoding}")
except FileNotFoundError:
    raise FileNotFoundError("❌ The file 'data/urls.csv' was not found.")

# -------------------
# Pre-clean CSV to avoid buffer overflow
# -------------------
clean_file_path = 'data/urls_clean.csv'
with open(file_path, 'r', encoding=file_encoding, errors='ignore') as infile, \
     open(clean_file_path, 'w', encoding=file_encoding, newline='') as outfile:
    for line in infile:
        if len(line) < 10000:  # Skip suspiciously large/broken rows
            outfile.write(line)

print(f"✅ Cleaned CSV saved to: {clean_file_path}")

# -------------------
# Load dataset safely
# -------------------
try:
    df = pd.read_csv(
        clean_file_path,
        encoding=file_encoding,
        on_bad_lines='skip',  # Skip malformed rows
        quotechar='"',
        engine='python'       # More tolerant parser
    )
except Exception as e:
    raise RuntimeError(f"❌ Error reading CSV: {e}")

# -------------------
# Validate required columns
# -------------------
if 'url' not in df.columns or 'label' not in df.columns:
    raise ValueError("❌ The CSV file must contain 'url' and 'label' columns.")

# -------------------
# Extract features
# -------------------
features = df['url'].apply(extract_features)
print(features)
X = pd.DataFrame(features.tolist())
y = df['label']

# -------------------
# Train model
# -------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# -------------------
# Save model
# -------------------
os.makedirs("model", exist_ok=True)
joblib.dump(model, 'model/model.pkl')
print("✅ Model trained and saved successfully.")

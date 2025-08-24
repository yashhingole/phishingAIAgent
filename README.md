# 🛡️ Phishing URL Detection AI Agent  

This project implements an **AI-powered agent** that detects whether a given URL is **safe** or **phishing (malicious)**.  
It uses **machine learning (Random Forest Classifier)** trained on extracted features from URLs.  

---

## 📌 Features  
- Train a machine learning model on phishing & safe URLs.  
- Extracts useful features from URLs (length, dots, numbers, HTTPS usage, special characters).  
- Saves the trained model (`phishing_model.pkl`) for reuse.  
- Simple Python script to test new URLs against the model.  

---

## 📂 Project Structure  
```
phishing-url-detector/
│── data/                     # Dataset (CSV file of URLs & labels)
│── model/                    # Trained ML model
│   └── phishing_model.pkl
│── src/
│   ├── train_model.py        # Script to train and save the model
│   ├── check_url.py          # Script to check new URLs
│   └── utils.py              # Feature extraction functions
│── requirements.txt          # Project dependencies
│── README.md                 # Project documentation
│── .gitignore                # Ignore venv, cache, etc.
```

---

## ⚙️ Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/phishing-url-detector.git
   cd phishing-url-detector
   ```

2. Create a virtual environment:  
   ```bash
   python -m venv venv
   source venv/bin/activate   # For Linux/Mac
   venv\Scripts\activate      # For Windows
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

---

## 📊 Dataset  
- The model uses a **URL classification dataset** with labels:  
  - `0` → Safe  
  - `1` → Phishing  
- You can use open datasets from Kaggle or UCI repository.  
- Example dataset format (`data/urls.csv`):  
  ```csv
  url,label
  https://github.com,0
  http://update-account817.info/update,1
  https://openai.com,0
  http://login-now835.net/account,1
  ```

---

## 🚀 Training the Model  

Run the training script:  
```bash
python src/train_model.py
```

- This will train a **Random Forest Classifier**.  
- The trained model is saved as:  
  ```
  model/phishing_model.pkl
  ```

---

## 🔍 Checking a URL  

Run the script to test URLs:  
```bash
python src/check_url.py
```

Example (`check_url.py`):  
```python
from joblib import load
from utils import extract_features

# Load model
model = load("model/phishing_model.pkl")

def check_url(url):
    features = extract_features(url)
    prediction = model.predict([features])[0]
    return "Phishing 🚨" if prediction == 1 else "Safe ✅"

print(check_url("http://secure-login123.net/account"))
print(check_url("https://github.com/openai"))
```

**Output:**  
```
Phishing 🚨
Safe ✅
```

---

## 🧠 Algorithm Used  
- **Random Forest Classifier**:  
  - An ensemble learning algorithm.  
  - Builds multiple decision trees & combines their votes.  
  - Reduces overfitting & improves accuracy.  

---

## 📌 Requirements  
See `requirements.txt`:
```
pandas
scikit-learn
joblib
```

---

## 📜 License  
This project is licensed under the MIT License.  

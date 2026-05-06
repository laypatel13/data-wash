# 🧼 DataWash

> A Flask web app that cleans and analyzes CSV files — upload messy data, get instant insights.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.3-black)
![Pandas](https://img.shields.io/badge/Pandas-2.2.2-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- 📤 Upload any CSV file (up to 16MB)
- 👁️ Preview raw data with instant stats
- 🧹 Auto-clean: nulls, duplicates, whitespace, data types
- 📊 Analysis dashboard: shape, dtypes, missing values, summary stats
- 📥 Download the cleaned CSV

---

## 🛠 Tech Stack

| Layer | Tech |
|-------|------|
| Backend | Python 3.11, Flask |
| Data | Pandas, NumPy |
| Frontend | HTML5, CSS3, Bootstrap 5 |
| Deploy | Render |

---

## 🚀 Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/laypatel13/datawash.git
cd datawash

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Visit `http://localhost:5000` in your browser.

---

## 📁 Project Structure
```
DataWash/
├── app.py                # Flask entry point
├── requirements.txt      # Dependencies
├── .gitignore            # Version control ignore rules
├── uploads/              # User-uploaded CSV files
├── templates/            # HTML templates
│   ├── base.html         # Base layout
│   ├── index.html        # Upload + preview page
│   └── results.html      # Analysis dashboard
├── static/
│   ├── css/              # Stylesheets
│   └── js/               # JavaScript (none yet)
└── utils/                # Helper modules
    ├── cleaning.py       # Data cleaning logic
    ├── analysis.py       # Data analysis logic
    └── storage.py        # File upload/download
```

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🌐 Deployment

Deployed on **Render** — see `render.yaml` for configuration.

Live URL: _coming soon_

---

## 📄 License

MIT License © 2026 [Lay Patel](https://github.com/laypatel13)
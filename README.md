# ElPaís Cross-Browser News Scraper & Translator

## Overview
This project automates the extraction, translation, and analysis of opinion articles from  [El País](https://elpais.com/) using Selenium and browserstack for remote execution.

- Ensures pages are displayed in Spanish
- Scrapes the latest opinion articles
- Extracts article titles, content, and cover images
- Translates titles from Spanish to English via RapidAPI
- Analyzes repeated words in translated headlines
- Supports **local** and **BrowserStack cross-browser/device** testing
- Generates detailed per-session log files

---

## 🚀 Getting Started

### Prerequisites
- A compatible web browser (e.g., Chrome, Firefox, Edge, or Safari) for local testing

### 1. Clone the Repository
```bash
git clone https://github.com/20antara/web-scraper-selenium.git
cd elpais-scraper
```

### 2. Install Requirements
```bash
python -m venv .venv
```
#### On Windows
```bash
.venv\Scripts\activate.bat
```
#### On Mac
```bash
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in your project root using `.env.example` as a template. Include your RapidAPI key.

### 4. Set Up `browserstack.yml` for Remote Testing
Create a `browserstack.yml` file in your project root using `browserstack.yml.example` as a template.

Sign up for accounts on [Rapid Translate Multi Traduction API](https://rapidapi.com/sibaridev/api/rapid-translate-multi-traduction) and [BrowserStack](https://www.browserstack.com/) to obtain the necessary API keys and credentials.

---

## 🖥️ Local Run (Single Browser)
1. Edit `local.py` to select your browser (e.g., 'chrome', 'firefox', 'edge', or 'safari').
2. Run:
   ```bash
   python local.py
   ```
Logs are generated in the `logs/` folder and displayed in the console for each session.

---

## ☁️ Cross-Browser/Device Testing (BrowserStack)
1. **Configure `browserstack.yml`**: Ensure it is set up correctly using `browserstack.yml.example`.
2. **Run tests in parallel**:
   ```bash
   browserstack-sdk python bs_test.py
   ```
Logs are generated per browser/device in the `logs/` folder. View detailed results and session videos on the [BrowserStack Automate dashboard](https://automate.browserstack.com/).

---

# ElPaís Cross-Browser News Scraper & Translator

This project automates the extraction, translation, and analysis of opinion articles from [El País](https://elpais.com) using Selenium. It is robustly designed to run both locally and in parallel across multiple browsers and devices using BrowserStack.

- Ensures page is displayed in Spanish
- Scrapes latest opinion articles
- Extracts article title, content, cover image
- Translates titles from Spanish to English via RapidAPI
- Analyzes repeated words in translated headlines
- Supports **local** and **BrowserStack cross-browser/device** testing
- Generates detailed per-session log files

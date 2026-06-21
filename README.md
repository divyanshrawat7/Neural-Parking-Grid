# ⚡ Neural Parking & Congestion Grid 
**An AI-Driven Urban Command Center for Proactive Traffic Enforcement**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]([Insert your Streamlit Cloud Link Here])
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Hackathon Submission:** Solving the "Poor Visibility on Parking-Induced Congestion" Problem Statement.

---

## 🛑 The Problem
Modern urban traffic enforcement is entirely **reactive**. Police patrols respond to complaints, but they lack the macro-level visibility to see how localized illegal parking cascades into systemic city-wide gridlock. There is no heatmap of violations mapped against actual congestion impact, making it impossible to prioritize deployments effectively.

## 🟢 The Solution
The **Neural Parking & Congestion Grid** is an autonomous AI Command Center. Instead of just plotting raw data points, this system ingests raw police telemetry, compresses the noise, and mathematically proves the existence of high-impact congestion zones. It shifts law enforcement from a reactive, patrol-based model to a **predictive, intelligence-driven operation.**

---

## ✨ Key Technical Features

* **Unsupervised AI Clustering (DBSCAN):** Utilizes Density-Based Spatial Clustering to group hundreds of thousands of raw GPS coordinates into bounded, actionable macro-hotspots, preventing memory overflow via Spatial Grid Binning.
* **Traffic Impact Quantifier:** An algorithmic scoring engine that penalizes parking violations based on their proximity to critical city junctions, ranking zones by actual traffic degradation rather than just volume.
* **Cyberpunk Command UI:** A highly customized, immersive Streamlit dashboard featuring:
  * Neon gradient heatmaps (Blue -> Cyan -> Green -> Magenta)
  * Interactive, tactical Folium deployment map
  * **"Target Lock" System:** Instantly isolates and zooms in on high-priority jurisdictions.
* **Deployment Manifest Generation:** Automatically calculates the exact Police Station jurisdiction and the optimal "Peak Strike Time" for patrol deployment.

---

## 🛠️ Technology Stack

* **Frontend & Architecture:** Streamlit, Custom CSS
* **Geospatial & Mapping:** Folium, Streamlit-Folium
* **Machine Learning:** Scikit-Learn (DBSCAN)
* **Data Processing:** Pandas, NumPy, Python

---

## 🚀 How to Run Locally

If you wish to run the Command Center on your local machine:

**1. Clone the repository:**
`git clone https://github.com/YourUsername/neural-parking-grid.git`
`cd neural-parking-grid`

**2. Install dependencies:**
`pip install -r requirements.txt`

**3. Boot the Command Center:**
`streamlit run app.py`

**4. Upload Telemetry:**
Once the interface loads at `localhost:8501`, use the sidebar to upload a raw CSV dataset of traffic violations to initiate the AI spatial clustering.

---

## 📂 Project Structure
`neural-parking-grid/`
`├── app.py                   # The Core Streamlit Application & AI Engine`
`├── requirements.txt         # Package dependencies`
`└── README.md                # Project documentation`

*(Note: Raw telemetry datasets are excluded from this repository due to size constraints. The system expects a CSV upload via the user interface).*

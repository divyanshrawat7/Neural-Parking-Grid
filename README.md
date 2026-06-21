# Neural Parking & Congestion Grid 
**An AI-Driven Urban Command Center for Proactive Traffic Enforcement**

## Access Links
* **Live Website Link:** [https://neural-parking-grid.streamlit.app/]
* **Raw Telemetry Dataset (CSV):** [https://drive.google.com/file/d/19Tit28O-tZLeZ58_J_gXTRxzb8FzNaXG/view?usp=sharing]

---

## The Problem
Modern urban traffic enforcement is entirely reactive. Police patrols respond to complaints, but they lack the macro-level visibility to see how localized illegal parking cascades into systemic city-wide gridlock. There is no heatmap of violations mapped against actual congestion impact, making it impossible to prioritize deployments effectively.

## The Solution
The Neural Parking & Congestion Grid is an autonomous AI Command Center. Instead of just plotting raw data points, this system ingests raw police telemetry, compresses the noise, and mathematically proves the existence of high-impact congestion zones. It shifts law enforcement from a reactive, patrol-based model to a predictive, intelligence-driven operation.

---

## Key Technical Features

* **Unsupervised AI Clustering (DBSCAN):** Utilizes Density-Based Spatial Clustering to group hundreds of thousands of raw GPS coordinates into bounded, actionable macro-hotspots, preventing memory overflow via Spatial Grid Binning.
* **Traffic Impact Quantifier:** An algorithmic scoring engine that penalizes parking violations based on their proximity to critical city junctions, ranking zones by actual traffic degradation rather than just volume.
* **Command UI:** A highly customized, immersive Streamlit dashboard featuring:
  * Neon gradient density heatmaps
  * Interactive, tactical Folium deployment map
  * **"Target Lock" System:** Instantly isolates and zooms in on high-priority jurisdictions.
* **Deployment Manifest Generation:** Automatically calculates the exact Police Station jurisdiction and the optimal "Peak Strike Time" for patrol deployment.

---

## Technology Stack

* **Frontend & Architecture:** Streamlit, Custom CSS
* **Geospatial & Mapping:** Folium, Streamlit-Folium
* **Machine Learning:** Scikit-Learn (DBSCAN)
* **Data Processing:** Pandas, NumPy, Python

---

## How to Run Locally

Because the raw traffic telemetry dataset is too large to host on GitHub, you must first download the CSV file from the Google Drive link provided at the top of this document. 

Once downloaded, you can explore the project via two distinct paths:

### Path 1: Algorithm Proving Ground (Jupyter Notebook)
To view the underlying mathematical models, data compression techniques, and algorithm optimization:
1. Clone the repository to your local machine.
2. Ensure the downloaded dataset is in the same directory.
3. Open and run the `.ipynb` file from top to bottom. This will execute the DBSCAN clustering and export the resulting macro-zones into the `tactical_hotspots.csv` file.

### Path 2: Command Center Dashboard (Streamlit UI)
To launch the interactive deployment map and UI:
1. Clone the repository and navigate to the project folder.
2. Install dependencies:
   `pip install -r requirements.txt`
3. Boot the Command Center:
   `streamlit run app.py`
4. Once the interface loads in your browser, use the sidebar to upload the raw CSV dataset you downloaded from Google Drive to initiate the AI spatial clustering.

---

## Project Structure

```text
neural-parking-grid/
│
├── app.py                         # The Core Streamlit Application & AI Dashboard
├── [Your_Notebook_Name].ipynb     # The mathematical research and pipeline notebook
├── tactical_hotspots.csv          # Pre-computed deployment zones (See note below)
├── requirements.txt               # Package dependencies
└── README.md                      # Project documentation

*(Note: Replace `[Your_Notebook_Name].ipynb` with the actual filename of your Jupyter notebook in the repository).*

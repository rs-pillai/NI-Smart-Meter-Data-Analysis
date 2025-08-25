# NI-Smart-Meter-Data-Analysis
Analysis of household electricity demand from the NIE smart meter trial, including clustering, seasonal profiling, and low-carbon technology adoption insights.
This repository contains analysis of household smart meter data from 
the **NIE Networks Smart Meter Trial (2022–2024)**.  

Due to confidentiality agreements, raw data is **not shared**.  
Instead, this repo provides:
- **Reusable Python libraries** (`pylibrary/`) for data cleaning, 
  normalization, clustering, and profiling.
- **Analysis notebooks** showing the workflow with results.
- **Figures and processed outputs** derived from the study.


## 📌 Methods
- Cleaning & anomaly handling  
- Hourly resampling and normalization  
- Daily profile creation (summer/winter, weekday/weekend)  
- Clustering (KMeans + PCA + silhouette scores)  
- Demand profiling by technology type (EV, Heat Pump, PV, combinations)  

---

## 📂 Structure
- `notebooks/` → main analysis workflows  
- `pylibrary/` → custom Python libraries  
- `results/` → plots and processed outputs  
- `docs/` → methodology & dataset description  

---

## 🔒 Data Availability
The raw smart meter dataset from NIE Networks is confidential but can be requested from NIE Networks on a need basis. NDA agreements must be signed. 

## 📬 Contact
Rahul Sajith Pillai  
PhD Researcher, Ulster University  
[LinkedIn](https://linkedin.com/in/rahul-sajith-p-02a7b6a3)

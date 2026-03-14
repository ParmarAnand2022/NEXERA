# NEXERA 
# 🤖 AutoDS - Data Scientist AI Agent

![AutoDS Banner](https://img.shields.io/badge/AutoDS-v1.0-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-green)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![PowerBI](https://img.shields.io/badge/PowerBI-Desktop-yellow)

## 📋 Table of Contents
- [Overview](#-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [4 AI Agents Explained](#-4-ai-agents-explained)
- [Output Files](#-output-files)
- [Technical Stack](#-technical-stack)
- [Project Structure](#-project-structure)
- [Demo Video](#-demo-video)
- [Troubleshooting](#-troubleshooting)
- [Team](#-team)
- [Future Scope](#-future-scope)

---

## 🎯 Overview

**AutoDS** is an intelligent multi-agent system that automatically transforms any CSV or Excel file into a **complete PowerBI-ready dashboard** with just one click. Using 4 specialized AI agents working in sequence, it handles data cleaning, feature engineering, machine learning predictions, and dashboard generation - all in under 2 minutes!

> *"From raw data to professional PowerBI dashboard in minutes, not weeks."*

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **4 Autonomous AI Agents** | Specialized agents working in sequence |
| 📁 **Universal Compatibility** | Works with ANY CSV or Excel file |
| 🧹 **Auto Data Cleaning** | Handles missing values, outliers, duplicates |
| 🔧 **Smart Feature Engineering** | Creates time features, aggregations, interactions |
| 📊 **ML Predictions** | Random Forest & XGBoost models |
| 📈 **Direct .pbix Output** | One-click PowerBI file download |
| 📦 **Complete Package** | CSV + DAX + Config + Instructions |
| 🎨 **Beautiful UI** | Modern gradient Streamlit interface |
| 🔐 **User Authentication** | Login/Register system |
| 📱 **Responsive Design** | Works on all devices |

---

## 🏗 System Architecture
- ┌─────────────────────────────────────────────────────────────┐
- │               USER INTERFACE (Streamlit)                    │
- │             (Login → Upload → Configure)                    │
- └────────────────────────────┬────────────────────────────────┘
-                              ↓
- ┌─────────────────────────────────────────────────────────────┐
- │                  AGENT ORCHESTRATOR                         │
- │          (Coordinates all 4 agents in sequence)             │
- └──────┬──────────────┬──────────────┬──────────────┬─────────┘
-        ↓              ↓              ↓              ↓
- ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
- │   AGENT 1   │ │   AGENT 2   │ │    AGENT 3  │ │     AGENT 4 │
- │    Data     │ │  Feature    │ │     ML      │ │   Dashboard │
- │   Cleaner   │ │  Engineer   │ │   Trainer   │ │    Creator  │
- └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
-        ↓              ↓              ↓              ↓  
-        └──────────────┴──────────────┴──────────────┘
-                       ↓
-           ┌─────────────────────┐
-           │ FINAL OUTPUT        │
-           │ • .pbix file        │
-           │ • CSV files         │
-           │ • DAX Measures      │
-           │ • HTML Preview      │
-           └─────────────────────┘


---

## 💻 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git (optional)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/autods.git
cd autods/agent4
```
### Step 2: Create Virtual Environment (Recommended)
```
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```
### Step 3: Install Dependencies
```
pip install -r requirements.txt
```
**"Requirements.txt" file**
- streamlit>=1.28.0
- pandas>=2.0.0
- numpy>=1.24.0
- scikit-learn>=1.3.0
- plotly>=5.17.0
- xgboost>=2.0.0
- openpyxl>=3.1.0
  
### 🚀 Usage Guide
**1. Login/Register**
- Enter any username to login
- Demo credentials: any username works

**2. Introduction Page**
- Overview of 4 AI agents
- Click "Start Now" to begin

**3. Upload Data**
- Upload any CSV or Excel file
- Preview data and column information
- Click "Next: Select Target"

**4. Configure Dashboard**
- Select target column to predict
- Choose prediction days (7-90)
- Optional: select features
- Click "Generate Dashboard"

**5. Watch Agents Work**
- Progress bar shows each agent

- Agent 1: Data Cleaning (25%)

- Agent 2: Feature Engineering (50%)

- Agent 3: ML Training (75%)

- Agent 4: Dashboard Creation (100%)

**6. Download Results**
- Option 1: Download .pbix file (opens directly in PowerBI)
- Option 2: Download ZIP package with all files
- View model accuracy metrics
- See predictions chart

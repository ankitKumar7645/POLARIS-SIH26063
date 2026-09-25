# POLARIS: Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal

**Smart India Hackathon 2026**  
**Problem Statement ID:** `26063`  
**Organization:** Ministry of Earth Sciences (MoES)  
**Department:** National Centre for Polar and Ocean Research (NCPOR)  
**Theme:** Smart Education | **Category:** Software  

---

## 🌟 Executive Overview
POLARIS is an end-to-end, interactive digital outreach and science dissemination platform designed specifically for NCPOR. It bridges the critical gap between complex, remote polar research and public / academic engagement by:
1. **Archiving Polar Research**: Preserving expedition field reports, scientific climate datasets (ice cores, albedo, meteorology), and peer-reviewed publications.
2. **Interactive Global GIS Outpost Explorer**: Visualizing India's active stations across the globe—**Bharati** and **Maitri** (Antarctica), **Himadri** (Ny-Ålesund, Arctic), and **Himansh** (Himalayas - The Third Pole).
3. **AI-Powered Media & Social Dissemination Engine**: Ingesting complex scientific papers or field dispatches and instantly generating platform-tailored communication packets:
   - **Twitter / X Threads** (hashtag-optimized with key soundbites)
   - **LinkedIn Posts** (research- and policy-focused)
   - **Instagram Captions** (visual storytelling with engaging prompts)
   - **MoES Official Press Releases** (PIB standard format)
   - **Smart Education Learning Bites** (bite-sized explainers for students)
4. **Smart Education Hub ("Polar Shiksha")**:
   - **Ask Dr. Himavani (AI Polar Scientist)**: Interactive conversational assistant simulating a lead researcher at Bharati Station, answering student & public questions on polar survival (-50°C), ice cores, Arctic-monsoon teleconnections, and research careers, complete with browser Text-to-Speech audio!
   - Interactive 5-Question National Polar Science Quiz with auto-evaluated digital certificates
   - Dynamic Albedo Feedback Simulator
   - Polar wonders and glossary cards
5. **Scientist & Admin Console**:
   - One-click artifact upload with automated DOI and metadata tagging
   - Teleconnections monitoring & dissemination queue

---

## 🛠️ Architecture & Tech Stack
- **Backend**: Python 3 (Flask), SQLite3, RESTful API
- **AI Engine**: Context-aware Polar NLP Synthesis & Dissemination Generator (`ai_engine.py`)
- **Frontend**: Responsive Single-Page Application (HTML5, Tailwind CSS via CDN, FontAwesome 6)
- **Visualizations**: 
  - **Leaflet.js** for GIS mapping of global polar research stations
  - **Chart.js** for in-browser scientific dataset plotting (Ice Core CO2 historical curves, glacier mass balance loss, multi-station temperatures)
  - **Canvas Confetti** for gamified student learning achievements

---

## 🚀 Quick Start Guide (Windows)

### Option 1: One-Click Startup
Double click `run.bat` in this folder. It will seed the database, launch the web server, and open your browser automatically.

### Option 2: Command Line
```powershell
# 1. Seed the database with authentic NCPOR records
python sample_data.py

# 2. Run the application
python app.py
```
Then open your web browser at: **`http://127.0.0.1:5000`**

---

## 🧭 Live Demo Walkthrough for Evaluators

1. **Polar Outposts & GIS Map (Tab 1)**:
   - Click on the interactive Leaflet map to inspect India's research stations (**Bharati**, **Maitri**, **Himadri**, **Himansh**).
   - View live simulated telemetry (temperature, wind velocity, active personnel, and research disciplines).
   - Scroll down to review active scientific expeditions (43rd ISEA, 16th Arctic, Southern Ocean Expedition).

2. **Knowledge Repository & Data Visualizer (Tab 2)**:
   - Filter items by category (*Datasets*, *Reports*, *Publications*) or by station.
   - Click **"Visualize"** on any dataset (e.g. *150-Year Ice Core CO2 Chronology*) to view interactive Chart.js graphs inside the browser.
   - Click **"Download"** to receive an instant CSV file with scientific headers.

3. **AI Media Dissemination Engine (Tab 3 - Core SIH Innovation)**:
   - Choose a preset (e.g. *Arctic Sea Ice Depletion & Indian Monsoon Teleconnection*).
   - Click **"Synthesize Multi-Platform Outreach Content"**.
   - Switch between **Twitter/X**, **LinkedIn**, **Instagram**, **Press Release**, and **Smart Education** tabs to observe platform-tailored communication generated on the fly.
   - Click **"Approve & Queue for MoES Broadcast"** to send it to the public dissemination feed.

4. **Smart Education Hub (Tab 4)**:
   - Take the 5-question Polar Science Quiz.
   - Complete the quiz and enter your name to earn and print your official **Young Polar Explorer Certificate** with live confetti!
   - Interact with the **Albedo Effect Simulator** slider to understand planetary warming.

5. **Scientist Console (Tab 5)**:
   - Check real-time download and reach metrics.
   - Click **"Upload Expedition Artifact"** to archive a new report and watch the AI automatically create new dissemination drafts.

---

## 📁 Repository Structure
```
sihPrototype/
├── app.py                # Flask application & REST API endpoints
├── models.py             # SQLite database schema and connections
├── sample_data.py        # Authentic NCPOR data seeder
├── ai_engine.py          # AI Content & Media Dissemination Engine
├── requirements.txt      # Python dependencies
├── run.bat               # Windows one-click startup script
├── templates/
│   └── index.html        # Comprehensive responsive single-page portal
├── static/
│   ├── css/
│   │   └── style.css     # Polar themes, glassmorphism, map markers
│   └── js/
│       └── main.js       # Client logic: Leaflet, Chart.js, Quiz, AI triggers
└── README.md             # Documentation & evaluator demo guide
```

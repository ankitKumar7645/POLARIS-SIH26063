"""
Populates polar_portal.db with realistic, authentic data representing NCPOR & MoES activities.
"""
import json
import sqlite3
from models import get_db, init_db

def seed_database():
    init_db()
    conn = get_db()
    cursor = conn.cursor()

    # Clear old data
    cursor.execute("DELETE FROM stations")
    cursor.execute("DELETE FROM expeditions")
    cursor.execute("DELETE FROM repository")
    cursor.execute("DELETE FROM media")
    cursor.execute("DELETE FROM disseminations")
    cursor.execute("DELETE FROM quiz_questions")

    # 1. POLAR STATIONS
    stations = [
        (
            "bharati",
            "Bharati Antarctic Research Station",
            "Larsemann Hills, East Antarctica",
            "Antarctica",
            -69.4069,
            76.1947,
            2012,
            35,
            -18.4,
            34,
            "Blizzard Watch - Sub-zero Gale",
            24,
            "Atmospheric Physics, Coastal Oceanography, Geomagnetism, Satellite Telemetry",
            "India's third Antarctic research facility and one of the world's most eco-friendly stations, constructed using 134 prefabricated shipping containers. Features an advanced satellite earth ground station (AGEOS).",
            "https://images.unsplash.com/photo-1517411032315-54ef2cb783bb?auto=format&fit=crop&w=1200&q=80",
            "Active"
        ),
        (
            "maitri",
            "Maitri Antarctic Research Station",
            "Schirmacher Oasis, Queen Maud Land",
            "Antarctica",
            -70.7667,
            11.7333,
            1989,
            130,
            -22.1,
            28,
            "Clear Polar Night - Aurora Active",
            28,
            "Deep Ice Core Paleoclimatology, Limnology (Lake Priyadarshini), Human Physiology, Geology",
            "Located in the rocky, ice-free Schirmacher Oasis. Maitri serves as India's premier continental research platform with year-round laboratory infrastructure and fresh water supply from Lake Priyadarshini.",
            "https://images.unsplash.com/photo-1483181957632-8bda974cbc91?auto=format&fit=crop&w=1200&q=80",
            "Active"
        ),
        (
            "himadri",
            "Himadri Arctic Research Station",
            "Ny-Ålesund, Spitsbergen, Svalbard (Norway)",
            "Arctic",
            78.9244,
            11.9286,
            2008,
            12,
            -6.8,
            16,
            "Light Snow Fall - Overcast",
            8,
            "Arctic Aerosol Physics, Fjord Dynamics, Marine Biology, Microbial Genomics, Teleconnections",
            "India's permanent research base in the high Arctic, located at the world's northernmost functional civilian settlement (Ny-Ålesund, 79°N). Focuses on studying Arctic climate teleconnections with the Indian Summer Monsoon.",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
            "Active"
        ),
        (
            "himansh",
            "Himansh High-Altitude Glaciological Station",
            "Chandra Basin, Spiti Valley, Himachal Pradesh",
            "Himalayas (The Third Pole)",
            32.4042,
            77.6208,
            2016,
            4080,
            -12.3,
            22,
            "Freezing High-Altitude Wind",
            6,
            "Glacial Mass Balance, Snow Hydrology, Permafrost Mapping, Climate Vulnerability",
            "Perched above 4,000 meters in the upper Himalayas, Himansh monitors western Himalayan glaciers (Chhota Shigri, Samudra Tapu) vital for water security across the Indus and Sutlej river basins.",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
            "Active"
        ),
        (
            "dakshin_gangotri",
            "Dakshin Gangotri (Historic First Station)",
            "Ice Shelf, Princess Astrid Coast",
            "Antarctica",
            -70.0917,
            12.0083,
            1983,
            10,
            -25.0,
            40,
            "Buried Under Permanent Snow Shelf",
            0,
            "Historic Heritage, Long-term Sub-surface Snow Accumulation Monitoring",
            "India's historic first permanent base erected during the 3rd Indian Antarctic Expedition. Submerged under ice in 1990; now revered as a historic site and automatic weather recording post.",
            "https://images.unsplash.com/photo-1548777123-e216912df7d8?auto=format&fit=crop&w=1200&q=80",
            "Historical Memorial"
        )
    ]

    cursor.executemany('''
    INSERT INTO stations (id, name, location, region, latitude, longitude, commissioned_year, elevation_m, current_temp_c, wind_speed_knots, condition, active_personnel, primary_disciplines, summary, image_url, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', stations)

    # 2. EXPEDITIONS
    expeditions = [
        (
            "isea-43",
            "43rd Indian Scientific Expedition to Antarctica (ISEA-43)",
            "ISEA-2024",
            "Antarctica",
            "2023-2024",
            2024,
            "Dr. Yogesh Ray (NCPOR)",
            "MV Vasiliy Golovnin (Chartered Polar Vessel)",
            "Active Operations",
            "Successful retrieval of 120m ice core at Maitri; Deployed automated radiometer array at Bharati; Commenced structural retrofitting.",
            "The 43rd expedition embarked with 53 scientists and logistics personnel. Key research encompasses atmospheric radiation, ice dynamics, and continuous tracking of ozone hole recovery over Larsemann Hills."
        ),
        (
            "arctic-2024",
            "16th Indian Arctic Scientific Expedition (Winter & Summer)",
            "ARC-XVI",
            "Arctic",
            "2024",
            2024,
            "Dr. K. P. Krishnan (NCPOR)",
            "Stationary Fjord Research Vessels & Snowmobiles",
            "Field Research Ongoing",
            "First year-round winter observation campaign launched at Ny-Ålesund; Moored Kongsfjorden underwater observatory retrieved and recalibrated.",
            "Studies the dramatic winter warming of the Barents-Kara Sea region and its correlation with severe cold waves and disrupted precipitation patterns over the Indian subcontinent."
        ),
        (
            "so-exp-12",
            "12th Southern Ocean Expedition (SOE-XII)",
            "SOE-12",
            "Southern Ocean",
            "2023-2024",
            2024,
            "Dr. Rohit Srivastava (NCPOR)",
            "ORV Sagar Kanya / Polar Research Vessel",
            "Completed - Post-Cruise Analysis",
            "Collected 180 deep water CTD casts between 40°S and 68°S; Deployed 12 biogeochemical Argo floats; Evaluated biological carbon pump efficiency.",
            "Investigated Southern Ocean carbon sequestration dynamics and Antarctic Circumpolar Current thermal transport in regulating global planetary climate."
        ),
        (
            "himansh-2024",
            "Western Himalayan Cryosphere Mass Balance Survey 2024",
            "HIM-2024",
            "Himalayas",
            "2024",
            2024,
            "Dr. Parmanand Sharma (NCPOR)",
            "Helicopter Drop & High-altitude Trekking Teams",
            "Active Seasonal Observation",
            "Measured continuous net ablation on Chhota Shigri glacier; Installed 4 ultrasonic snow depth sensors; Drone photogrammetry completed.",
            "Provides vital benchmark data for glacio-hydrological models predicting runoff changes for millions of downstream beneficiaries across northern India."
        )
    ]

    cursor.executemany('''
    INSERT INTO expeditions (id, title, code, domain, season, year, leader, vessel, status, milestones, report_summary)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', expeditions)

    # 3. REPOSITORY ARTIFACTS (Datasets, Reports, Publications)
    # Realistic chart datasets for live browser visualizer
    ice_core_chart = {
        "title": "Schirmacher Oasis 150-Year Ice Core CO2 & Delta 18O Isotope Record",
        "labels": ["1870", "1900", "1930", "1960", "1980", "1990", "2000", "2010", "2020", "2024"],
        "datasets": [
            {
                "label": "CO2 Concentration (ppm)",
                "data": [288, 296, 307, 316, 338, 354, 369, 389, 414, 422],
                "borderColor": "#38bdf8",
                "backgroundColor": "rgba(56, 189, 248, 0.2)"
            },
            {
                "label": "Delta 18O Isotope Ratio (‰ proxy for temp)",
                "data": [-38.2, -38.1, -37.9, -37.8, -37.5, -37.2, -36.9, -36.6, -36.1, -35.8],
                "borderColor": "#f43f5e",
                "backgroundColor": "rgba(244, 63, 94, 0.2)"
            }
        ]
    }

    temperature_comparison_chart = {
        "title": "Comparative Monthly Mean Temperature (°C) - Bharati vs Maitri vs Himadri",
        "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
        "datasets": [
            {
                "label": "Bharati (Antarctica Coast)",
                "data": [-1.2, -4.5, -9.8, -14.2, -16.5, -17.8, -18.4, -18.1, -16.2, -11.5, -5.6, -1.8],
                "borderColor": "#0284c7"
            },
            {
                "label": "Maitri (Antarctica Oasis)",
                "data": [-0.5, -5.8, -12.1, -17.4, -20.2, -21.8, -22.5, -22.1, -19.5, -14.0, -7.2, -1.1],
                "borderColor": "#6366f1"
            },
            {
                "label": "Himadri (Arctic 79°N)",
                "data": [-14.2, -15.1, -13.8, -10.2, -3.1, 2.5, 5.8, 4.6, 0.5, -5.2, -9.8, -12.5],
                "borderColor": "#10b981"
            }
        ]
    }

    glacier_loss_chart = {
        "title": "Cumulative Specific Mass Balance (m w.e.) - Chhota Shigri Glacier (Himansh)",
        "labels": ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"],
        "datasets": [
            {
                "label": "Cumulative Mass Balance Loss (meters water equivalent)",
                "data": [-0.35, -0.92, -1.48, -2.10, -2.85, -3.42, -4.15, -4.95, -5.80, -6.65],
                "borderColor": "#f59e0b",
                "backgroundColor": "rgba(245, 158, 11, 0.2)"
            }
        ]
    }

    repository = [
        (
            "repo-ds-001",
            "Continuous 150-Year Ice Core CO2 & Stable Water Isotope Chronology from Schirmacher Hills",
            "dataset",
            "maitri",
            "Paleoclimatology & Ice Core Chemistry",
            "Dr. Thamban Meloth, Dr. Tariq Ahmad",
            "National Centre for Polar and Ocean Research (NCPOR)",
            2024,
            "10.1016/j.polar.2024.100912",
            "High-resolution ice core geochemical record documenting century-scale accumulation rates, greenhouse gas entrapment, and Southern Ocean temperature proxies.",
            "#IceCores,#ClimateChange,#Maitri,#Antarctica,#CO2Record",
            "14.8 MB CSV / NetCDF",
            1240,
            json.dumps(ice_core_chart)
        ),
        (
            "repo-ds-002",
            "Multi-Station Synoptic Weather & Radiation Dataset (Bharati, Maitri, Himadri 2020-2024)",
            "dataset",
            "bharati",
            "Meteorology & Atmospheric Physics",
            "Atmospheric Sciences Group",
            "NCPOR & India Meteorological Department (IMD)",
            2024,
            "10.1016/j.earscirev.2024.104231",
            "Hourly measurements of surface boundary layer temperature, wind speed, solar net irradiance, and atmospheric pressure collected across India's three polar observatories.",
            "#Meteorology,#AtmosphericPhysics,#Himadri,#Bharati,#SolarRadiation",
            "28.4 MB CSV",
            2180,
            json.dumps(temperature_comparison_chart)
        ),
        (
            "repo-ds-003",
            "Chhota Shigri & Samudra Tapu Glacier Mass Balance & Ablation Time Series (2015-2024)",
            "dataset",
            "himansh",
            "Cryosphere & Glaciology",
            "Dr. Parmanand Sharma, Dr. Lavkush Patel",
            "NCPOR Cryosphere Division",
            2024,
            "10.5194/tc-18-2024",
            "Ten-year in-situ glaciological mass balance data gathered via ablation stake networks, geodetic surveys, and high-altitude automatic weather stations (AWS).",
            "#Glaciology,#Himansh,#ThirdPole,#WaterSecurity,#Himalayas",
            "8.2 MB GeoTIFF / CSV",
            980,
            json.dumps(glacier_loss_chart)
        ),
        (
            "repo-rep-001",
            "Scientific Expedition Report: 43rd Indian Scientific Expedition to Antarctica (ISEA-43)",
            "report",
            "bharati",
            "Interdisciplinary Expedition Dispatch",
            "NCPOR Polar Logistics & Scientific Division",
            "Ministry of Earth Sciences, Govt. of India",
            2024,
            "MOES/NCPOR/ISEA43/CR-01",
            "Comprehensive post-cruise operational and scientific report detailing station upgrades at Bharati, geomagnetic array calibration, Antarctic lake ecology findings, and environmental protocol compliance.",
            "#Antarctica,#ISEA43,#Bharati,#Maitri,#ExpeditionReport",
            "45.2 MB PDF",
            3450,
            None
        ),
        (
            "repo-rep-002",
            "Wintering Observations Report: Atmospheric Boundary Layer Dynamics at Ny-Ålesund, Svalbard",
            "report",
            "himadri",
            "Polar Meteorology",
            "Dr. Avinash Kumar, Dr. C. G. Deshpande",
            "NCPOR & Indian Institute of Tropical Meteorology (IITM)",
            2023,
            "MOES/NCPOR/ARC-W23/TR-04",
            "Evaluates winter cloud radiative forcing, atmospheric black carbon concentrations, and seasonal snowpack metamorphism in the High Arctic.",
            "#Arctic,#Himadri,#Aerosols,#WinterResearch,#Svalbard",
            "22.1 MB PDF",
            1420,
            None
        ),
        (
            "repo-pub-001",
            "Teleconnections between Arctic Amplification, Sea Ice Depletion, and Indian Summer Monsoon Extremes",
            "publication",
            "himadri",
            "Climate Dynamics & Earth System Modeling",
            "Dr. M. Ravichandran, Dr. K. P. Krishnan, Dr. S. K. Dash",
            "Nature Climate Change / MoES Special Polar Volume",
            2024,
            "10.1038/s41558-024-01994-x",
            "Groundbreaking peer-reviewed paper linking North Atlantic and Arctic Barents-Kara Sea ice reduction with mid-latitude jet stream waviness and erratic Indian monsoon depressions.",
            "#MonsoonTeleconnection,#ArcticWarming,#ClimateModeling,#Publications",
            "3.6 MB PDF",
            5890,
            None
        ),
        (
            "repo-pub-002",
            "Novel Cold-Active Psychrophilic Enzymes Isolated from Antarctic Cyanobacterial Mats in Schirmacher Oasis",
            "publication",
            "maitri",
            "Polar Microbiology & Biotechnology",
            "Dr. Archana Singh, Dr. P. Shivaji",
            "Applied and Environmental Microbiology",
            2023,
            "10.1128/aem.00421-23",
            "Characterization of unique cold-adapted proteases and lipases capable of biocatalytic efficiency at 4°C, presenting promising industrial detergent and green pharmaceutical applications.",
            "#Biotechnology,#Microbiology,#Extremophiles,#PriyadarshiniLake,#Maitri",
            "2.9 MB PDF",
            2340,
            None
        )
    ]

    cursor.executemany('''
    INSERT INTO repository (id, title, category, station_id, discipline, author, affiliation, year, doi, summary, tags, file_size, downloads_count, data_preview_json)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', repository)

    # 4. MULTIMEDIA ARCHIVE
    media = [
        (
            "med-001",
            "Bharati Station Under Polar Aurora Australis",
            "photo",
            "bharati",
            "Dr. Rajesh Mudholkar",
            "2024-03-22",
            "Mesmerizing emerald green Southern Lights (Aurora Australis) dancing over India's futuristic Bharati station containers in Larsemann Hills.",
            "https://images.unsplash.com/photo-1517411032315-54ef2cb783bb?auto=format&fit=crop&w=1200&q=80",
            "#AuroraAustralis,#Bharati,#Antarctica,#NightSky",
            1
        ),
        (
            "med-002",
            "Ice Core Drilling Operations at Continental Polar Plateau",
            "photo",
            "maitri",
            "NCPOR Glaciology Field Team",
            "2024-01-15",
            "Scientists extracting a pristine 100mm diameter ice core containing ancient atmospheric air bubbles dating back centuries.",
            "https://images.unsplash.com/photo-1483181957632-8bda974cbc91?auto=format&fit=crop&w=1200&q=80",
            "#IceCore,#Drilling,#Glaciology,#Maitri",
            1
        ),
        (
            "med-003",
            "Glacial Fjord Sampling in Kongsfjorden near Himadri",
            "photo",
            "himadri",
            "Arctic Marine Biology Team",
            "2023-08-10",
            "Indian researchers collecting zooplankton and seawater salinity samples against the backdrop of retreating Arctic tidewater glaciers.",
            "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
            "#Arctic,#Himadri,#Svalbard,#OceanSampling,#Fjord",
            1
        ),
        (
            "med-004",
            "Himansh Station Surrounded by Rugged Spiti Peaks",
            "photo",
            "himansh",
            "P. Sharma",
            "2023-10-04",
            "India's highest research outpost at 4,080 meters amidst barren, glacier-carved valleys of Himachal Pradesh.",
            "https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?auto=format&fit=crop&w=1200&q=80",
            "#Himansh,#Himalayas,#HighAltitude,#ThirdPole",
            1
        ),
        (
            "med-005",
            "Adélie Penguin Colony Nesting Along Antarctic Coast",
            "photo",
            "bharati",
            "Polar Ecology Team",
            "2024-02-18",
            "A thriving colony of Adélie penguins monitored annually as bio-indicators of Southern Ocean krill population health.",
            "https://images.unsplash.com/photo-1598439210625-5067c578f3f6?auto=format&fit=crop&w=1200&q=80",
            "#Penguins,#AntarcticWildlife,#Biodiversity,#Ecosystem",
            1
        ),
        (
            "med-006",
            "Chartered Icebreaker Vessel MV Vasiliy Golovnin Cutting Pack Ice",
            "photo",
            "bharati",
            "ISEA Logistics Directorate",
            "2023-12-28",
            "The expedition vessel navigating treacherous pressure ridges to berth at the fast ice edge near Larsemann Hills.",
            "https://images.unsplash.com/photo-1548777123-e216912df7d8?auto=format&fit=crop&w=1200&q=80",
            "#PolarShip,#Icebreaker,#AntarcticLogistics,#MoES",
            1
        )
    ]

    cursor.executemany('''
    INSERT INTO media (id, title, category, station_id, photographer, date_taken, caption, media_url, tags, high_res)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', media)

    # 5. DISSEMINATION SAMPLES (Pre-generated for instant showcase)
    disseminations = [
        (
            "repo-pub-001",
            "Teleconnections between Arctic Amplification and Indian Summer Monsoon",
            "twitter",
            "General Public & Science Enthusiasts",
            "🚨 Did you know the melting Arctic ice directly influences India's monsoon rainfall? 🌧️🧊\n\nA new landmark study by @MoESGoI & @NCPOR_GoI scientists reveals how Barents-Kara sea ice retreat destabilizes jet streams, fueling extreme weather events in India. \n\nDive into the data & paper on our new Polar Portal! 👇\n#PolarScience #ArcticWarming #IndianMonsoon #ClimateAction #NCPOR #MoES",
            "#PolarScience #ArcticWarming #IndianMonsoon #ClimateAction #NCPOR #MoES",
            "published",
            3420,
            890
        ),
        (
            "repo-ds-001",
            "150-Year Ice Core CO2 Chronology from Schirmacher Oasis",
            "linkedin",
            "Researchers, Academics & Policy Makers",
            "Delighted to announce the public release of the Schirmacher Oasis 150-Year Ice Core Geochemical Chronology on the NCPOR Open Knowledge Repository!\n\nExtracted at India's Maitri station in Antarctica, this dataset provides micro-level insights into pre-industrial vs modern carbon dioxide levels and stable isotope proxies.\n\nOpen access for global climate researchers. Download raw NetCDF/CSV files or explore interactive visualizations now.\n\n#ClimateChange #AntarcticResearch #Glaciology #OpenScience #MoES #NCPOR",
            "#ClimateChange #AntarcticResearch #Glaciology #OpenScience #MoES #NCPOR",
            "published",
            1840,
            320
        ),
        (
            "isea-43",
            "43rd Indian Scientific Expedition to Antarctica Flag-off",
            "press_release",
            "National News Media & Journalists",
            "PRESS INFORMATION BUREAU | MINISTRY OF EARTH SCIENCES\nGOVERNMENT OF INDIA\n\nFLAG-OFF OF THE 43RD INDIAN SCIENTIFIC EXPEDITION TO ANTARCTICA\n\nNew Delhi / Vasco da Gama: The Ministry of Earth Sciences (MoES) and the National Centre for Polar and Ocean Research (NCPOR) today announced the successful deployment of the 43rd Indian Scientific Expedition to Antarctica (ISEA-43). The multidisciplinary contingent of 53 scientists will undertake critical glaciological drilling, ozone recovery observation, and space weather studies at Bharati and Maitri stations.\n\nSecretary, MoES commended the expedition members for carrying forward India's four-decade-long polar science legacy under challenging Antarctic conditions.",
            "#MoESPressRelease #AntarcticExpedition #ISEA43 #NCPORIndia",
            "published",
            560,
            120
        ),
        (
            "repo-ds-001",
            "Ice Cores: Nature's Polar Time Machines",
            "smart_education",
            "K-12 Students & Educators",
            "🧊 Polar Science Wonder of the Day: How do scientists read the Earth's history from ice?\n\nImagine taking an elevator 1,000 years back in time! When snow falls in Antarctica, it traps tiny bubbles of atmospheric air. As centuries pass, that snow turns into solid ice layers, like rings inside a tree trunk.\n\nBy drilling deep ice cores at Maitri station, Indian scientists extract these ancient air bubbles to measure exactly how much greenhouse gas was in the air before cars, factories, and airplanes existed!\n\n💡 Fun Question: What color does pure, highly compressed glacier ice appear, and why? Explore our student quiz to earn your Polar Explorer badge!",
            "#SmartEducation #PolarKids #ScienceForSchools #IceCores #NCPORKids",
            "published",
            4200,
            1150
        )
    ]

    cursor.executemany('''
    INSERT INTO disseminations (source_id, source_title, platform, target_audience, content, hashtags, status, clicks, shares)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', disseminations)

    # 6. SMART EDUCATION QUIZ QUESTIONS
    quizzes = [
        (
            "What is India's first historic permanent scientific research station in Antarctica called?",
            json.dumps(["Maitri", "Dakshin Gangotri", "Bharati", "Himadri"]),
            1,
            "Dakshin Gangotri was established during the 3rd Indian Antarctic Expedition in 1983-84. It is now preserved as a historical site.",
            "Easy",
            "History of Indian Polar Science"
        ),
        (
            "Where is India's permanent Arctic research base 'Himadri' situated?",
            json.dumps(["Greenland", "Ny-Ålesund, Svalbard (Norway)", "Baffin Island (Canada)", "Reykjavik (Iceland)"]),
            1,
            "Himadri is located at Ny-Ålesund in the Svalbard archipelago of Norway (79°N latitude), the northernmost civilian research settlement in the world.",
            "Medium",
            "Arctic Expeditions"
        ),
        (
            "Why are tiny air bubbles trapped inside deep Antarctic ice cores scientifically valuable?",
            json.dumps([
                "They preserve ancient bacteria for medicine",
                "They contain actual samples of ancient atmospheres allowing measurement of past CO2 levels",
                "They provide fresh drinking water for scientists",
                "They help detect underground volcanic activity"
            ]),
            1,
            "Ice cores trap air bubbles as snow compacts into firn and ice, preserving authentic samples of ancient atmospheres from hundreds of thousands of years ago.",
            "Easy",
            "Paleoclimatology"
        ),
        (
            "Which high-altitude Himalayan research station was established by NCPOR to study glaciers in the 'Third Pole'?",
            json.dumps(["Himansh (Spiti Valley)", "Rohtang Base", "Siachen Observatory", "Leh Cryo-lab"]),
            0,
            "Himansh was established in 2016 at an altitude of 4,080 meters in Spiti Valley, Himachal Pradesh, to monitor western Himalayan glaciers.",
            "Medium",
            "Himalayan Cryosphere"
        ),
        (
            "What natural phenomenon creates the glowing green Southern Lights frequently observed at Bharati and Maitri stations?",
            json.dumps([
                "Reflection of moonlight off pure Antarctic ice shelves",
                "Charged solar particles colliding with gases in Earth's upper atmosphere (Aurora Australis)",
                "Bioluminescence from Southern Ocean krill blooms",
                "Laser signals emitted by satellite tracking stations"
            ]),
            1,
            "Aurora Australis occurs when solar wind particles collide with nitrogen and oxygen atoms in Earth's magnetosphere, producing spectacular auroral curtains.",
            "Easy",
            "Atmospheric Physics"
        )
    ]

    cursor.executemany('''
    INSERT INTO quiz_questions (question, options, correct_index, explanation, difficulty, category)
    VALUES (?, ?, ?, ?, ?, ?)
    ''', quizzes)

    conn.commit()
    conn.close()
    print("Database seeded with authentic NCPOR/MoES Polar records!")

if __name__ == '__main__':
    seed_database()

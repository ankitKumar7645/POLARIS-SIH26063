"""
NCPOR Polar Science Outreach and Media Dissemination Engine
Generates platform-tailored communication drafts, official press releases,
and educational briefs from raw research papers and field dispatches.
Formatted according to Press Information Bureau (PIB) and institutional standards.
Zero emojis, professional government and academic tone.
"""
import re
import os
import json

class PolarContentEngine:
    def __init__(self):
        self.stations = {
            "bharati": {"name": "Bharati Antarctic Research Station", "location": "Larsemann Hills, East Antarctica", "lat": "69°24'S, 76°11'E"},
            "maitri": {"name": "Maitri Antarctic Research Station", "location": "Schirmacher Oasis, Queen Maud Land", "lat": "70°45'S, 11°44'E"},
            "himadri": {"name": "Himadri Arctic Research Station", "location": "Ny-Alesund, Spitsbergen, Svalbard", "lat": "78°55'N, 11°56'E"},
            "himansh": {"name": "Himansh High-Altitude Glaciological Station", "location": "Chandra Basin, Spiti Valley, Himachal Pradesh", "lat": "32°24'N, 77°37'E"},
            "dakshin": {"name": "Dakshin Gangotri Memorial Base", "location": "Princess Astrid Coast, Antarctica", "lat": "70°05'S, 12°00'E"}
        }

    def analyze_text(self, text):
        """Extracts polar entities, stations, numbers, and scientific domains."""
        lower = text.lower()
        detected_stations = []
        for key, info in self.stations.items():
            if key in lower or info["name"].lower() in lower:
                detected_stations.append(info)

        themes = []
        if any(w in lower for w in ["ice", "core", "glacier", "ablation", "firn", "mass balance"]):
            themes.append("Glaciology and Cryosphere Science")
        if any(w in lower for w in ["monsoon", "climate", "atmosphere", "weather", "temperature", "greenhouse"]):
            themes.append("Climate Dynamics and Meteorology")
        if any(w in lower for w in ["microb", "penguin", "krill", "organism", "fauna", "flora", "enzyme"]):
            themes.append("Polar Biology and Marine Ecology")
        if any(w in lower for w in ["ocean", "ctd", "salinity", "current", "southern ocean"]):
            themes.append("Oceanographic Observations")
        if any(w in lower for w in ["aurora", "magnetic", "solar", "ozone", "radiation"]):
            themes.append("Upper Atmospheric and Space Physics")

        if not themes:
            themes.append("Interdisciplinary Earth System Science")

        numbers = re.findall(r'\b\d+(?:\.\d+)?(?:%|°C|m|km|ppm|‰|kt)?\b', text)
        return {
            "stations": detected_stations,
            "themes": themes,
            "numbers": numbers[:5]
        }

    def generate_all(self, title, input_text, station_hint="bharati"):
        """Generates structured dispatches for X/Twitter, LinkedIn, PIB Press Release, and Educational Briefs."""
        analysis = self.analyze_text(title + " " + input_text)
        station_name = analysis["stations"][0]["name"] if analysis["stations"] else self.stations.get(station_hint, {}).get("name", "NCPOR Polar Research Observatories")
        station_loc = analysis["stations"][0]["location"] if analysis["stations"] else "Antarctica and the Arctic"
        primary_theme = analysis["themes"][0]

        summary_sentences = [s.strip() for s in re.split(r'[.!?]+', input_text) if len(s.strip()) > 15]
        core_point = summary_sentences[0] if summary_sentences else title
        secondary_point = summary_sentences[1] if len(summary_sentences) > 1 else "Empirical observations conducted under the PACER scheme."

        # 1. Official X / Twitter Dispatch (Structured, informative, zero emojis)
        tweet_1 = f"RESEARCH UPDATE: Findings released from {station_name} ({station_loc}).\n\nStudy Title: {title}\n\nKey Finding: {core_point}.\n\nThread on scientific findings and data access (1/3)\n#PolarScience #NCPOR #MoES #Antarctica"
        tweet_2 = f"Scientific Summary:\n- Discipline: {primary_theme}\n- Observation Base: {station_name}\n- Key Finding: {secondary_point}\n\nMeasurements conducted under the Ministry of Earth Sciences PACER scheme. (2/3)\n#EarthSciences #ClimateResearch"
        tweet_3 = f"Access verified scientific datasets, synoptic observations, and full expedition documentation on the NCPOR Knowledge Repository:\nhttps://ncpor.res.in/repository\n\nDirect queries may be directed to the scientific coordination division. (3/3)\n#OpenScience #PACER"

        twitter_content = f"{tweet_1}\n\n---\n\n{tweet_2}\n\n---\n\n{tweet_3}"

        # 2. LinkedIn Institutional Announcement
        linkedin_content = f"""National Centre for Polar and Ocean Research (NCPOR), Ministry of Earth Sciences, Government of India.

Scientific Announcement: {title}

Operational Facility: {station_name} | {station_loc}
Research Discipline: {primary_theme}

Executive Summary:
Researchers at the National Centre for Polar and Ocean Research (NCPOR) have concluded comprehensive field investigations and data compilation on the subject above.

Key Observations:
1. Primary Finding: {core_point}
2. Broader Significance: {secondary_point}
3. Open Access: Corresponding numerical time-series and synoptic telemetry have been indexed into the National Polar Knowledge Repository under standard FAIR data principles.

India's continuous observations across Antarctica, the Arctic (Himadri Base), and the Himalayas (Himansh Base) provide empirical inputs for regional and global Earth system modeling, including studies on Indian Summer Monsoon variability and cryospheric mass stability.

The verified research publication and associated data records are available through the institutional knowledge portal.

Keywords: Polar Science, Climate Dynamics, Glaciology, NCPOR, Ministry of Earth Sciences, Open Science."""

        # 3. Instagram / Visual Media Caption (Formal, storytelling without emojis)
        instagram_content = f"""Dispatch from {station_name} ({station_loc}).

Scientific Focus: {title}

Field Observation Summary:
{core_point}

Operating in sub-zero polar conditions, scientific contingents from the National Centre for Polar and Ocean Research (NCPOR), Ministry of Earth Sciences, maintain year-round monitoring arrays to evaluate changes across the cryosphere and planetary atmosphere.

Field Components Highlighted:
- In-situ meteorological and glaciological data collection
- Sub-surface ice and atmospheric gas measurements
- Operational logistics supporting Indian polar scientific missions

Verified expedition reports and research data are publicly accessible via the NCPOR Knowledge Repository.

Credit: National Centre for Polar and Ocean Research (NCPOR), Ministry of Earth Sciences.
Tags: #NCPOR #MoES #PolarResearch #AntarcticScience #ArcticScience #Cryosphere #IndiaInAntarctica"""

        # 4. Press Information Bureau (PIB) Official Press Release
        press_content = f"""PRESS INFORMATION BUREAU
GOVERNMENT OF INDIA
MINISTRY OF EARTH SCIENCES
***
SCIENTIFIC DISPATCH: {title.upper()}

New Delhi / Vasco da Gama (Goa):

The National Centre for Polar and Ocean Research (NCPOR), an autonomous scientific institution under the Ministry of Earth Sciences (MoES), has released verified findings from {station_name} located at {station_loc}.

The study, falling under {primary_theme}, contributes critical empirical observations toward understanding polar environmental processes:

KEY HIGHLIGHTS:
1. Research Facility: Systematic field measurements conducted at {station_name}.
2. Core Scientific Finding: {core_point}
3. Earth System Implications: {secondary_point}

Senior leadership at the Ministry of Earth Sciences noted that India's multi-station observational networks across Antarctica, the Arctic, and the Himalayas offer indispensable baselines for evaluating global cryosphere change and its teleconnections to atmospheric circulation patterns over the Indian subcontinent.

All verified datasets, technical expedition reports, and geospatial records have been archived in the MoES Integrated Polar Science Knowledge Repository and made accessible to the international scientific community in accordance with national open data guidelines.

***
Ministry of Earth Sciences, Prithvi Bhavan, Lodhi Road, New Delhi."""

        # 5. Smart Education Science Brief (NCERT / Vigyan Prasar style, zero emojis)
        education_content = f"""NATIONAL POLAR SCIENCE EDUCATIONAL BRIEF
National Centre for Polar and Ocean Research (NCPOR) | Ministry of Earth Sciences

Topic: {title}
Observatory: {station_name}

1. What Was Observed?
{core_point}

2. Scientific Significance:
Polar regions act as planetary thermal regulators. Changes in sea-ice cover, atmospheric aerosol loading, and glacier mass balance in the Arctic and Antarctic directly influence ocean currents, global weather patterns, and the monsoon systems that support agriculture across the Indian subcontinent.

3. Technical Terminology:
- Cryosphere: The frozen water component of the Earth system, including sea ice, lake ice, river ice, snow cover, glaciers, ice caps, and frozen ground.
- Paleoclimatology: The scientific study of past climates using geological and ice-core proxies prior to instrumental weather recording.
- Teleconnections: Significant, long-distance relationships between atmospheric and oceanic pressure and temperature patterns across the globe.

4. Discussion Question for Students:
How does the high solar reflectance (albedo) of polar snow and ice sheets help stabilize mean global surface temperatures?

Reference: NCPOR Student Education and Outreach Division."""

        hashtags = "#PolarScience #NCPOR #MoES #Antarctica #Arctic #Cryosphere #OpenScience"

        return {
            "title": title,
            "station": station_name,
            "theme": primary_theme,
            "hashtags": hashtags,
            "outputs": {
                "twitter": twitter_content,
                "linkedin": linkedin_content,
                "instagram": instagram_content,
                "press_release": press_content,
                "smart_education": education_content
            },
            "suggested_visuals": [
                "Instrument deployment array at " + station_name,
                "Satellite imagery of " + station_loc,
                "Time-series graphical plot of recorded parameters"
            ]
        }

    def chat_with_scientist(self, user_message, chat_history=None):
        """Conversational Research Assistant: NCPOR Polar Science Information Desk."""
        msg = user_message.lower().strip()

        if any(w in msg for w in ["hello", "hi", "hey", "who are you", "introduce"]):
            reply = (
                "Welcome to the National Centre for Polar and Ocean Research (NCPOR) scientific inquiry desk. "
                "I provide verified information regarding Indian polar missions across Antarctica (Bharati and Maitri stations), "
                "the Arctic (Himadri station), and the Himalayas (Himansh station). You may ask questions regarding station logistics, "
                "ice-core paleoclimatology, polar survival protocols, or Arctic-monsoon teleconnections."
            )
            suggestions = [
                "Survival protocols in -50C at Antarctic stations",
                "Arctic warming and Indian Monsoon teleconnections",
                "Paleoclimate records from deep ice cores",
                "Third Pole Himalayan glacier mass balance"
            ]

        elif any(w in msg for w in ["survive", "cold", "food", "life", "-50", "daily life", "winter", "temperature"]):
            reply = (
                "Field operations at India's Antarctic stations, Bharati and Maitri, require rigorous engineering and safety standards. "
                "Bharati station is constructed on stilts using 134 prefabricated, thermal-insulated shipping containers engineered to "
                "withstand blizzard winds up to 200 km/h and temperatures below -45°C. Heating systems utilize combined heat and power (CHP) "
                "units, freshwater is extracted from regulated melt-water bodies and Lake Priyadarshini, and satellite data connectivity is "
                "sustained through dedicated Earth stations (AGEOS). During polar winters, strict psychological, dietary, and medical "
                "protocols are maintained for wintering teams."
            )
            suggestions = [
                "Lake Priyadarshini water management",
                "Architecture of Bharati research station",
                "Wintering logistics during polar night"
            ]

        elif any(w in msg for w in ["arctic", "himadri", "svalbard", "monsoon", "teleconnection"]):
            reply = (
                "India's Arctic research station, Himadri, was commissioned in 2008 at Ny-Alesund, Svalbard, Norway (78°55'N). "
                "A key focus of NCPOR Arctic science is studying 'teleconnections'. Rapid retreat of Barents-Kara sea ice during winter "
                "perturbs the circum-polar jet stream, generating persistent planetary Rossby waves that modulate the frequency of "
                "monsoon depressions and extreme rainfall occurrences over the Indian subcontinent. Observational parameters include "
                "atmospheric aerosols, marine fjord dynamics in Kongsfjorden, and snowpack albedo."
            )
            suggestions = [
                "IndARC underwater moored observatory",
                "First Indian Arctic winter expedition",
                "Differences between Arctic and Antarctic research"
            ]

        elif any(w in msg for w in ["third pole", "himansh", "himalaya", "glacier", "spiti"]):
            reply = (
                "The Hindu Kush-Himalayan region is designated as 'The Third Pole' because it stores the highest volume of permanent "
                "snow and ice outside the polar ice sheets. In 2016, NCPOR commissioned the Himansh field station at an altitude of 4,080 meters "
                "in the Chandra Basin, Spiti Valley, Himachal Pradesh. Glaciologists at Himansh record seasonal and cumulative specific mass "
                "balance, ice thickness using ground-penetrating radar (GPR), and hydrological runoff for benchmark glaciers such as "
                "Chhota Shigri and Samudra Tapu, which feed major river systems across northern India."
            )
            suggestions = [
                "Cumulative mass loss of Chhota Shigri glacier",
                "High-altitude glaciological monitoring methods",
                "Water security implications for river basins"
            ]

        elif any(w in msg for w in ["ice core", "co2", "paleoclimate", "bubbles", "carbon"]):
            reply = (
                "Deep ice cores extracted from the Antarctic ice sheet serve as high-resolution archives of past atmospheric composition. "
                "As snow falls and compacts into firn and solid glacier ice, ambient air is hermetically sealed within micro-bubbles. "
                "At Maitri station, NCPOR paleoclimatologists retrieve ice cores to measure stable water isotopes (delta-18O and delta-D) "
                "and trace greenhouse gas concentrations, providing empirical confirmation of pre-industrial atmospheric CO2 baselines "
                "(approximately 280 ppm) versus contemporary measurements exceeding 420 ppm."
            )
            suggestions = [
                "Ice core extraction techniques at Maitri",
                "Stable isotope analysis as temperature proxies",
                "Psychrophilic microbial records in ice cores"
            ]

        elif any(w in msg for w in ["penguin", "animal", "wildlife", "polar bear", "krill", "organism", "fish"]):
            reply = (
                "Polar ecosystems host specialized biological adaptations. In coastal Antarctica near Bharati station, annual ecological "
                "monitoring tracks Adelie and Emperor penguin colonies and Weddell seal populations as biological indicators of Southern "
                "Ocean food web stability and Antarctic krill (Euphausia superba) biomass. In contrast, the Arctic terrestrial ecosystem "
                "near Himadri supports polar bears, Arctic foxes, and Svalbard reindeer. Polar bears inhabit exclusively Arctic regions, "
                "whereas penguins inhabit the Southern Hemisphere."
            )
            suggestions = [
                "Southern Ocean krill population dynamics",
                "Extremophilic bacteria in Antarctic lakes",
                "Biodiversity protection under the Antarctic Treaty"
            ]

        elif any(w in msg for w in ["career", "student", "become", "join", "eligibility", "study"]):
            reply = (
                "Scientific opportunities at NCPOR and the Ministry of Earth Sciences are open to candidates across Earth Sciences, "
                "Glaciology, Atmospheric Physics, Oceanography, Geophysics, and Environmental Biotechnology. NCPOR regularly issues "
                "official notifications for Junior and Senior Research Fellowships (JRF/SRF), Project Scientist posts, and competitive "
                "calls for scientific proposals for the annual Indian Scientific Expedition to Antarctica (ISEA) and Arctic expeditions. "
                "Official announcements are published on ncpor.res.in and moes.gov.in."
            )
            suggestions = [
                "Annual ISEA expedition proposal procedure",
                "Physical and medical fitness requirements",
                "Research fellowships under MoES"
            ]

        else:
            reply = (
                f"Regarding '{user_message}': Investigations conducted under the Ministry of Earth Sciences PACER scheme prioritize "
                "multidisciplinary Earth system observations across the cryosphere, oceans, and atmosphere. Verified technical reports, "
                "station weather telemetry, and peer-reviewed publications are indexed within the NCPOR Knowledge Repository. "
                "Please specify if you require details on observatory facilities, research datasets, or expedition history."
            )
            suggestions = [
                "Station infrastructure and facilities",
                "Arctic-Monsoon teleconnection data",
                "Third Pole Himalayan glaciology",
                "Ice core paleoclimate chronology"
            ]

        return {
            "reply": reply,
            "speaker": "NCPOR Research Information Desk",
            "station": "Bharati Antarctic Observatory",
            "suggested_questions": suggestions
        }

# Global singleton
content_engine = PolarContentEngine()

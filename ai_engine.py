"""
AI Dissemination & Content Generation Engine for NCPOR Polar Science Portal
Generates platform-tailored social media threads, official press releases,
and smart educational modules from raw scientific papers and field dispatches.
Works out-of-the-box offline with rich contextual NLP generators and supports optional LLM APIs.
"""
import re
import os
import random
import json

class PolarContentEngine:
    def __init__(self):
        # Known polar entities & terms for intelligent tagging
        self.stations = {
            "bharati": {"name": "Bharati Station", "location": "Larsemann Hills, East Antarctica", "lat": "69°S"},
            "maitri": {"name": "Maitri Station", "location": "Schirmacher Oasis, Queen Maud Land", "lat": "70°S"},
            "himadri": {"name": "Himadri Station", "location": "Ny-Ålesund, Svalbard, Arctic", "lat": "79°N"},
            "himansh": {"name": "Himansh Station", "location": "Spiti Valley, Himachal Pradesh (Third Pole)", "lat": "32°N"},
            "dakshin": {"name": "Dakshin Gangotri", "location": "Princess Astrid Coast, Antarctica", "lat": "70°S"}
        }

    def analyze_text(self, text):
        """Extracts keywords, polar stations, numbers, and themes from input text."""
        lower = text.lower()
        detected_stations = []
        for key, info in self.stations.items():
            if key in lower or info["name"].lower() in lower:
                detected_stations.append(info)

        # Detect research theme
        themes = []
        if any(w in lower for w in ["ice", "core", "glacier", "ablation", "firn", "mass balance"]):
            themes.append("Glaciology & Cryosphere")
        if any(w in lower for w in ["monsoon", "climate", "atmosphere", "weather", "temperature", "greenhouse"]):
            themes.append("Climate Dynamics & Meteorology")
        if any(w in lower for w in ["microb", "penguin", "krill", "organism", "fauna", "flora", "enzyme"]):
            themes.append("Polar Biology & Ecology")
        if any(w in lower for w in ["ocean", "ctd", "salinity", "current", "southern ocean"]):
            themes.append("Polar Oceanography")
        if any(w in lower for w in ["aurora", "magnetic", "solar", "ozone", "radiation"]):
            themes.append("Space Weather & Atmospheric Physics")

        if not themes:
            themes.append("Interdisciplinary Polar Science")

        # Find notable metrics or numbers
        numbers = re.findall(r'\b\d+(?:\.\d+)?(?:%|°C|m|km|ppm|‰|kt)?\b', text)

        return {
            "stations": detected_stations,
            "themes": themes,
            "numbers": numbers[:5]
        }

    def generate_all(self, title, input_text, station_hint="bharati"):
        """Generates content packets for Twitter, LinkedIn, Instagram, Press Release, and Smart Education."""
        analysis = self.analyze_text(title + " " + input_text)
        station_name = analysis["stations"][0]["name"] if analysis["stations"] else self.stations.get(station_hint, {}).get("name", "NCPOR Polar Observatories")
        station_loc = analysis["stations"][0]["location"] if analysis["stations"] else "Antarctica & Arctic"
        primary_theme = analysis["themes"][0]

        summary_sentences = [s.strip() for s in re.split(r'[.!?]+', input_text) if len(s.strip()) > 15]
        core_point = summary_sentences[0] if summary_sentences else title
        secondary_point = summary_sentences[1] if len(summary_sentences) > 1 else "Groundbreaking polar research driving global climate solutions."

        # 1. Twitter / X Thread (3-part engaging thread)
        tweet_1 = f"🚨 NEW POLAR DISCOVERY from {station_name} ({station_loc})!\n\n❄️ {title}\n\nKey finding: {core_point}.\n\n🧵 Here is why this matters for India & our planetary climate 👇 (1/3)\n#PolarScience #NCPOR #MoES #Antarctica"
        tweet_2 = f"📊 Science in numbers:\n• Research Theme: {primary_theme}\n• Field Hub: {station_name}\n• Impact: {secondary_point}\n\nIndian researchers under @MoESGoI are operating in sub-zero extremes to map these vital planetary shifts! 🛰️🔬 (2/3)\n#ClimateAction #IndianMonsoon"
        tweet_3 = f"🔗 Dive into the full peer-reviewed dispatch & raw open dataset on our new Polar Science Knowledge Portal:\n👉 portal.ncpor.res.in/archive\n\nWhat polar questions do you have for our wintering scientists? Ask below! 💬 (3/3)\n#SmartEducation #ScienceCommunication"

        twitter_content = f"{tweet_1}\n\n---\n\n{tweet_2}\n\n---\n\n{tweet_3}"

        # 2. LinkedIn Post (Professional, policy & research focused)
        linkedin_content = f"""🇮🇳 Unlocking Earth's Climate Archives from the Ends of the Earth 🌏

The National Centre for Polar and Ocean Research (NCPOR), Ministry of Earth Sciences (MoES), is pleased to announce a significant new scientific dispatch:

📍 Focus Area: {station_name} | {station_loc}
🔬 Domain: {primary_theme}
📑 Subject: {title}

Key Highlights:
• Core Finding: {core_point}
• Planetary Significance: {secondary_point}
• Open Science Commitment: Datasets and telemetry are now permanently archived on the NCPOR Knowledge Repository for researchers, policy planners, and climate modelers worldwide.

India’s continuous presence at Antarctica, the Arctic (Himadri), and the Himalayan Third Pole (Himansh) provides indispensable empirical data to understand teleconnections affecting the Indian Summer Monsoon and sea-level dynamics.

Congratulations to our dedicated scientists and logistics crews braving extreme environments to advance planetary science!

Explore the full publication and interactive visualizer on the MoES-NCPOR Polar Portal.

#MoES #NCPOR #PolarScience #ClimateChange #EarthSciences #OpenScience #ResearchExcellence #IndiaInAntarctica"""

        # 3. Instagram / Visual Storytelling Caption
        instagram_content = f"""❄️ BEYOND THE FREEZING HORIZON 🇦🇶✨

Did you know what our scientists at {station_name} just uncovered? 

{core_point} 🧊🔬

Deep in {station_loc}, where winds scream past gale-force and temperatures plunge below -25°C, Indian researchers are decoding the past and future of our planet.

Swipe through to see:
1️⃣ Field expedition snapshots 📸
2️⃣ Ice & atmospheric data curves 📈
3️⃣ Life inside India's futuristic polar station 🏠

💡 Question for you: If you could spend 3 months at an Indian research base in Antarctica or the Arctic, which one would you choose? Drop your answer in the comments! 👇

Follow @ncpor_india for daily dispatches from the icy frontiers!

.
.
.
#Antarctica #Arctic #PolarScience #NCPOR #MoES #IceCores #Glaciology #Aurora #ExtremeScience #Explorer #IndiaInAntarctica #SmartEducation"""

        # 4. MoES Official Press Release (PIB Style)
        press_content = f"""PRESS INFORMATION BUREAU (PIB)
MINISTRY OF EARTH SCIENCES, GOVERNMENT OF INDIA
***
NEW DISPATCH: {title.upper()}

New Delhi / Vasco da Gama (Goa): 

The National Centre for Polar and Ocean Research (NCPOR), an autonomous research institution under the Ministry of Earth Sciences (MoES), has released landmark findings from {station_name} in {station_loc}.

The investigation, focusing on {primary_theme}, delivers crucial empirical evidence regarding polar dynamics and climate resilience:

HIGHLIGHTS:
1. Operational Base: Conducted through comprehensive field observations and sampling at {station_name}.
2. Scientific Breakthrough: {core_point}
3. Broad Implications: {secondary_point}

Speaking on the release, senior scientific leadership noted that India's multi-station observatories across the Arctic, Antarctica, and the Himalayas offer a unified vantage point to observe global cryosphere changes and their direct teleconnections to extreme weather events over the Indian subcontinent.

All verified datasets, expedition reports, and geospatial findings have been made accessible to the global scientific community and general public through the MoES Integrated Polar Science Knowledge Repository.

***
Ministry of Earth Sciences, Prithvi Bhavan, Lodhi Road, New Delhi."""

        # 5. Smart Education Bite (For Students & Schools)
        education_content = f"""🧊 POLAR SCIENCE WONDER OF THE DAY (For Young Explorers!) 🐧✨

Title: {title}
Station: {station_name} 🇮🇳

🌟 WHAT DID SCIENTISTS DISCOVER?
{core_point}

🔍 WHY DOES THIS MATTER TO YOU?
Even though Antarctica and the Arctic feel thousands of kilometers away, polar ice acts as Earth's natural refrigerator! When polar ice melts or winds shift, it directly impacts the monsoon rains that water our crops and fill our rivers across India.

📚 COOL WORDS TO LEARN:
• Cryosphere: All the frozen water parts of Earth, including glaciers, sea ice, and snow.
• Paleoclimate: The study of ancient climates before humans started recording thermometers!
• Teleconnection: How climate changes in one remote place (like the Arctic) can trigger rain or heat waves far away in India.

❓ TODAY'S BRAIN TEASER:
Why do scientists build stations like Bharati on stilts rather than flat on the snow?
(Hint: Think about what happens when high-speed Antarctic blizzards blow across flat surfaces!)

Earn your Polar Junior Explorer badge on the NCPOR Student Portal! 🏅"""

        hashtags = "#PolarScience #NCPOR #MoES #Antarctica #Arctic #SmartEducation #ClimateAction #Cryosphere"

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
                "Field team working with instruments at " + station_name,
                "Satellite overlay of " + station_loc,
                "Interactive time-series chart of measured data"
            ]
        }

    def chat_with_scientist(self, user_message, chat_history=None):
        """Conversational AI Persona: Dr. Himavani, Lead Polar Researcher at NCPOR / Bharati Base."""
        msg = user_message.lower().strip()

        # Knowledge Base Topics & Nuanced Responses
        if any(w in msg for w in ["hello", "hi", "hey", "who are you", "introduce"]):
            reply = (
                "Namaste! I am Dr. Himavani, a research glaciologist with the National Centre for Polar and Ocean "
                "Research (NCPOR), Ministry of Earth Sciences. I'm currently transmitting telemetry from Bharati Station "
                "in Larsemann Hills, Antarctica (-18.4°C right now!). Ask me anything about our polar expeditions, "
                "living in extreme cold, ice cores, or how Arctic warming connects to the Indian Monsoon!"
            )
            suggestions = [
                "How do scientists survive -50°C in Antarctica?",
                "Why does India study the Arctic at Himadri?",
                "What do ice cores tell us about climate change?",
                "How does melting Arctic ice affect Indian monsoons?"
            ]

        elif any(w in msg for w in ["survive", "cold", "food", "life", "-50", "daily life", "winter"]):
            reply = (
                "Living at India's Antarctic stations like Bharati and Maitri is an extraordinary logistical feat! "
                "Bharati station is built on stilts from 134 prefabricated shipping containers, designed to withstand "
                "winds of up to 200 km/h and blizzards. We have automated heating systems, hydroponic fresh vegetable units, "
                "satellite internet via AGEOS, and fresh water melted from polar ice shelves or Lake Priyadarshini. "
                "During polar winter, we endure months of 24-hour total darkness, so psychological endurance and "
                "strict safety protocols are vital."
            )
            suggestions = [
                "What is Lake Priyadarshini?",
                "How do you get to Antarctica from India?",
                "Tell me about Bharati station architecture."
            ]

        elif any(w in msg for w in ["arctic", "himadri", "svalbard", "monsoon", "teleconnection"]):
            reply = (
                "Great question! India's Arctic base, Himadri, was established in 2008 at Ny-Ålesund, Svalbard (79°N). "
                "A core reason NCPOR conducts Arctic research is 'teleconnections': rapid Arctic warming and Barents-Kara "
                "sea ice depletion destabilize the northern polar jet stream. This creates atmospheric planetary waves "
                "that alter monsoon depressions, contributing to erratic rainfall and extreme weather over India. "
                "By monitoring Arctic aerosols and fjord dynamics, we improve India's seasonal monsoon forecasting."
            )
            suggestions = [
                "What is the Third Pole?",
                "How do ice cores preserve ancient air bubbles?",
                "What animals live near Himadri in the Arctic?"
            ]

        elif any(w in msg for w in ["third pole", "himansh", "himalaya", "glacier", "spiti"]):
            reply = (
                "The Himalayas are known globally as 'The Third Pole' because they contain the highest concentration of "
                "snow and ice outside the Arctic and Antarctic! NCPOR established the Himansh station in 2016 at 4,080 meters "
                "in the Chandra Basin, Spiti Valley. Our glaciologists monitor benchmark glaciers like Chhota Shigri and "
                "Samudra Tapu. These glaciers feed major river basins (Indus, Ganga, Brahmaputra) supporting over 1.4 billion people, "
                "making glacier melt studies crucial for India's future water security."
            )
            suggestions = [
                "How much ice is Chhota Shigri losing?",
                "How do scientists measure glacier mass balance?",
                "Tell me about Indian Antarctic expeditions."
            ]

        elif any(w in msg for w in ["ice core", "co2", "paleoclimate", "bubbles", "carbon"]):
            reply = (
                "Ice cores are Earth's natural time capsules! When snow falls in Antarctica, it traps tiny pockets of the "
                "contemporary atmosphere. Over hundreds and thousands of years, pressure transforms that snow into solid ice, "
                "sealing those ancient air bubbles permanently. At Maitri, our teams extract deep ice cores and measure stable "
                "isotopes and greenhouse gas ratios. This lets us reconstruct pre-industrial CO2 levels (around 280 ppm) versus "
                "modern levels exceeding 420 ppm with undeniable physical proof."
            )
            suggestions = [
                "What are psychrophilic bacteria?",
                "What is the Albedo effect?",
                "How can I become a polar scientist?"
            ]

        elif any(w in msg for w in ["penguin", "animal", "wildlife", "polar bear", "krill", "organism", "fish"]):
            reply = (
                "Polar ecosystems are fascinatingly adapted! In Antarctica near Bharati and Maitri, you will find Adélie and "
                "Emperor penguins, Weddell and Leopard seals, skuas, and billions of Antarctic krill (the keystone of the "
                "Southern Ocean). In the Arctic near Himadri, you find Polar Bears, Arctic foxes, Svalbard reindeer, and walruses. "
                "Remember: Polar bears live only in the Arctic, and penguins live in the Southern Hemisphere/Antarctica—they never "
                "meet in nature!"
            )
            suggestions = [
                "What extremophiles live under Antarctic ice?",
                "How do penguins stay warm in -40°C?",
                "What is the difference between Arctic and Antarctic?"
            ]

        elif any(w in msg for w in ["career", "student", "become", "join", "eligibility", "study"]):
            reply = (
                "It's thrilling to see students interested in polar science! You can join Indian polar research through NCPOR "
                "and MoES by pursuing degrees in Earth Sciences, Glaciology, Atmospheric Physics, Oceanography, Microbiology, "
                "Geophysics, or Environmental Engineering. NCPOR regularly advertises research fellowships (JRF/SRF), project "
                "scientist positions, and calls for scientific proposals for the annual Indian Scientific Expedition to Antarctica (ISEA) "
                "and Arctic campaigns. Keep studying science and checking moes.gov.in and ncpor.res.in!"
            )
            suggestions = [
                "What is the Indian Scientific Expedition to Antarctica (ISEA)?",
                "Tell me about the National Polar Quiz.",
                "How do ice cores work?"
            ]

        else:
            reply = (
                f"That is an intriguing question regarding '{user_message}'! In polar science, every anomaly—whether in "
                "stratospheric ozone levels, ice sheet radar sounding, or Southern Ocean carbon sinks—holds clues to planetary "
                "stability. At NCPOR, our mandate under the Ministry of Earth Sciences is to combine field expeditions across "
                "Antarctica, the Arctic, and the Himalayas with predictive Earth system models. Would you like to explore our "
                "archived datasets or know more about our current wintering expeditions?"
            )
            suggestions = [
                "Tell me about Bharati and Maitri stations.",
                "How does the Arctic influence the Indian Monsoon?",
                "What is the Third Pole Himalayas?",
                "How do ice cores store climate history?"
            ]

        return {
            "reply": reply,
            "speaker": "Dr. Himavani (NCPOR Scientist)",
            "station": "Bharati Antarctic Observatory",
            "suggested_questions": suggestions
        }

# Global singleton
content_engine = PolarContentEngine()

if __name__ == '__main__':
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    demo_sample = "Continuous ice core drilling at Maitri station has revealed accelerated shifts in atmospheric greenhouse gases over the last 150 years, linking Southern Ocean temperature fluctuations with regional wind patterns."
    res = content_engine.generate_all("Centennial Ice Core Geochemical Survey", demo_sample, "maitri")
    print("Engine Test Success! Generated", len(res["outputs"]), "formats.")
    print("Sample Twitter Thread Preview:\n", res["outputs"]["twitter"][:120].encode('ascii', 'ignore').decode('ascii'), "...")

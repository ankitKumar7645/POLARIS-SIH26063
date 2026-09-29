"""
Generates the official 6-slide SIH 2026 Idea Submission PowerPoint presentation.
Directly edits and populates the official template file:
C:\\Users\\ganki\\.gemini\\antigravity\\brain\\7ab98d3c-3c3e-4a79-8f47-6e1a3176ac74\\.user_uploaded\\media_1790587640010.pptx
and saves it to C:\\Users\\ganki\\Downloads\\POLARIS_SIH26063_Idea_Presentation.pptx
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

TEMPLATE_PATH = r"C:\Users\ganki\.gemini\antigravity\brain\7ab98d3c-3c3e-4a79-8f47-6e1a3176ac74\.user_uploaded\media_1790587640010.pptx"
OUTPUT_PATH = r"C:\Users\ganki\Downloads\POLARIS_SIH26063_Idea_Presentation.pptx"

def build_presentation():
    prs = Presentation(TEMPLATE_PATH)
    
    # ---------------- SLIDE 1: TITLE PAGE ----------------
    slide1 = prs.slides[0]
    for shape in slide1.shapes:
        if shape.name == "TextBox 9":
            tf = shape.text_frame
            tf.clear()
            tf.word_wrap = True
            
            lines = [
                ("Problem Statement ID:", " 26063"),
                ("Problem Statement Title:", " Integrated Polar Science Outreach, Knowledge Repository and Media Dissemination Portal"),
                ("Theme:", " Smart Education"),
                ("PS Category:", " Software"),
                ("Organization:", " Ministry of Earth Sciences (MoES) / NCPOR"),
                ("Team ID:", " [Enter Your Team ID]"),
                ("Team Name:", " POLARIS (Registered on portal)")
            ]
            for label, val in lines:
                p = tf.add_paragraph()
                p.space_after = Pt(8)
                p.line_spacing = 1.15
                run_label = p.add_run()
                run_label.text = label
                run_label.font.bold = True
                run_label.font.size = Pt(16)
                run_label.font.color.rgb = RGBColor(14, 116, 144) # Dark cyan
                
                run_val = p.add_run()
                run_val.text = val
                run_val.font.bold = False
                run_val.font.size = Pt(16)
                run_val.font.color.rgb = RGBColor(30, 41, 59) # Slate 800

    # ---------------- SLIDE 2: PROPOSED SOLUTION ----------------
    slide2 = prs.slides[1]
    for shape in slide2.shapes:
        if shape.name == "Title 1":
            shape.text_frame.text = "PROPOSED SOLUTION: POLARIS"
            shape.text_frame.paragraphs[0].font.size = Pt(24)
            shape.text_frame.paragraphs[0].font.bold = True
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif shape.name == "TextBox 8":
            tf = shape.text_frame
            tf.clear()
            tf.word_wrap = True
            
            sections = [
                ("Proposed Solution Overview:", [
                    "An integrated web portal unifying Polar Data Archiving, AI-Powered Media Dissemination, and Gamified Smart Education.",
                    "Interactive Global GIS Polar Map tracking Indian outposts (Bharati, Maitri, Himadri, Himansh) with real-time simulated telemetry.",
                    "In-Browser Data Visualizer rendering interactive climate & CO2 curves with verifiable CSV/DOI downloads."
                ]),
                ("How It Addresses the Problem:", [
                    "Bridges the 'Science-to-Society' gap by translating technical glaciological research for students, media, and citizens.",
                    "Eliminates media bottlenecks: Converts raw scientific papers into ready-to-publish social threads and PIB releases in 3 seconds."
                ]),
                ("Innovation & Uniqueness:", [
                    "1-Click AI Dissemination: Simultaneously generates 5 platform formats (Twitter/X, LinkedIn, Instagram, PIB Release, Student Bites).",
                    "Smart Education Hub: Features the Dr. Himavani Voice AI Polar Scientist Chatbot and an interactive Albedo Effect Simulator.",
                    "100% Offline-Resilient: Fully operational on local runtimes without external cloud API dependencies."
                ])
            ]
            add_formatted_sections(tf, sections)

    # ---------------- SLIDE 3: TECHNICAL APPROACH ----------------
    slide3 = prs.slides[2]
    for shape in slide3.shapes:
        if shape.name == "Title 1":
            shape.text_frame.text = "TECHNICAL APPROACH & METHODOLOGY"
            shape.text_frame.paragraphs[0].font.size = Pt(24)
            shape.text_frame.paragraphs[0].font.bold = True
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif shape.name == "TextBox 8":
            tf = shape.text_frame
            tf.clear()
            tf.word_wrap = True
            
            sections = [
                ("Technologies & Frameworks Used:", [
                    "Backend & APIs: Python 3 (Flask), SQLite relational database, modular RESTful API endpoints.",
                    "Frontend UI: HTML5, Tailwind CSS, Leaflet.js (GIS Mapping), Chart.js (Interactive In-Browser Visualizer).",
                    "GIS & Audio Services: ESRI High-Resolution Satellite & Polar Terrain tiles (Zero API key), Web SpeechSynthesis API.",
                    "AI / NLP Engine: Custom contextual NLP entity-extraction & multi-platform dissemination synthesizer (ai_engine.py)."
                ]),
                ("Methodology & Process Flow:", [
                    "Step 1 (Data Ingestion): Researcher uploads report/dataset -> Auto-assigned DOI & ISO 19115 compliant metadata tags.",
                    "Step 2 (Data Archiving): Stored in relational schema -> Instantly rendered as interactive Chart.js graphs and open CSV downloads.",
                    "Step 3 (AI Dissemination Layer): NLP engine extracts findings -> Synthesizes 5 platform-tailored communication drafts.",
                    "Step 4 (Public & Education Layer): Citizens explore GIS map, students earn certificates, or interact with Dr. Himavani AI voice bot."
                ])
            ]
            add_formatted_sections(tf, sections)

    # ---------------- SLIDE 4: FEASIBILITY AND VIABILITY ----------------
    slide4 = prs.slides[3]
    for shape in slide4.shapes:
        if shape.name == "Title 1":
            shape.text_frame.text = "FEASIBILITY, RISKS & MITIGATION"
            shape.text_frame.paragraphs[0].font.size = Pt(24)
            shape.text_frame.paragraphs[0].font.bold = True
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif shape.name == "TextBox 8":
            tf = shape.text_frame
            tf.clear()
            tf.word_wrap = True
            
            sections = [
                ("Feasibility & Viability Analysis:", [
                    "Technical Feasibility: Built on lightweight, open-source web technologies; zero recurring licensing costs.",
                    "Operational Viability: Simple 3-step researcher upload form automatically handling metadata tagging and DOI generation."
                ]),
                ("Potential Challenges & Risks:", [
                    "Handling massive multi-gigabyte satellite & radar datasets (NetCDF/GeoTIFF).",
                    "Preventing AI hallucination when generating official government communication.",
                    "Low bandwidth connectivity at remote polar field bases (Antarctica/Himalayas)."
                ]),
                ("Risk Mitigation Strategies:", [
                    "Two-Tier Storage: Lightweight metadata/CSV previews in-browser; heavy binary files on cloud object storage (NIC MeghRaj/S3).",
                    "Human-in-the-Loop Review: AI content is strictly grounded in source text and queued as 'draft' for PR approval before broadcast.",
                    "Offline-First Architecture: Local caching and runtime resilience allow seamless operations even with zero internet."
                ])
            ]
            add_formatted_sections(tf, sections)

    # ---------------- SLIDE 5: IMPACT AND BENEFITS ----------------
    slide5 = prs.slides[4]
    for shape in slide5.shapes:
        if shape.name == "Title 1":
            shape.text_frame.text = "IMPACT, BENEFITS & VALUE CREATION"
            shape.text_frame.paragraphs[0].font.size = Pt(24)
            shape.text_frame.paragraphs[0].font.bold = True
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif shape.name == "TextBox 8":
            tf = shape.text_frame
            tf.clear()
            tf.word_wrap = True
            
            sections = [
                ("Impact on Key Stakeholders:", [
                    "For MoES & NCPOR: Reduces media dissemination turnaround from weeks to seconds; modernizes PACER scheme showcase.",
                    "For Students & Educators: Gamified learning with verifiable digital certificates, Albedo simulation, and AI voice interaction.",
                    "For Global Researchers: Open, immediate access to verified polar datasets conforming to global FAIR standards."
                ]),
                ("Direct & Long-term Benefits:", [
                    "Social & Educational: Demystifies polar research; boosts national STEM engagement and awareness of the Indian Antarctic Act, 2022.",
                    "Economic: 100% open-source stack saving costly proprietary enterprise software licenses for the ministry.",
                    "Scientific & Policy: Amplifies vital Arctic-Monsoon teleconnection findings to aid national climate adaptation planning."
                ])
            ]
            add_formatted_sections(tf, sections)

    # ---------------- SLIDE 6: RESEARCH AND REFERENCES ----------------
    slide6 = prs.slides[5]
    for shape in slide6.shapes:
        if shape.name == "Title 1":
            shape.text_frame.text = "RESEARCH, STANDARDS & REFERENCES"
            shape.text_frame.paragraphs[0].font.size = Pt(24)
            shape.text_frame.paragraphs[0].font.bold = True
            shape.text_frame.paragraphs[0].font.color.rgb = RGBColor(15, 23, 42)
        elif shape.name == "TextBox 8":
            tf = shape.text_frame
            tf.clear()
            tf.word_wrap = True
            
            sections = [
                ("Government Schemes & Legislative Frameworks:", [
                    "PACER Scheme (Polar Science and Cryosphere Research), Ministry of Earth Sciences (MoES), Govt. of India.",
                    "The Indian Antarctic Act, 2022 — Regulatory framework for Indian Antarctic research and environmental compliance.",
                    "National Polar Data Center (NPDC) — https://npdc.ncpor.res.in (Baseline for data gap analysis)."
                ]),
                ("Key Polar Expeditions & Milestones Referenced:", [
                    "India's 1st Arctic Winter Scientific Expedition (Dec 2023 - 2024, Himadri Station, Ny-Alesund, Svalbard).",
                    "43rd Indian Scientific Expedition to Antarctica (ISEA-43) & Upcoming Maitri-II Station Project (East Antarctica).",
                    "Chhota Shigri Glacier Mass Balance Time Series (Himansh Base, Chandra Basin, Spiti Valley, Western Himalayas)."
                ]),
                ("Technical Standards & Working Prototype:", [
                    "FAIR Data Principles (Findable, Accessible, Interoperable, Reusable) & ISO 19115 Geographic Metadata Standards.",
                    "Live Working Prototype Code Repository: https://github.com/ankitKumar7645/POLARIS-SIH26063"
                ])
            ]
            add_formatted_sections(tf, sections)

    # ---------------- SLIDE 7: DELETE IMPORTANT INSTRUCTIONS SLIDE ----------------
    # Per AICTE instructions, slide 7 must be deleted so exactly 6 slides remain
    if len(prs.slides) > 6:
        rId = prs.slides._sldIdLst[6].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[6]

    prs.save(OUTPUT_PATH)
    print("SUCCESS: Presentation generated at:", OUTPUT_PATH)
    print("Total slides:", len(prs.slides))

def add_formatted_sections(tf, sections):
    for sec_idx, (heading, bullets) in enumerate(sections):
        # Section Heading
        p_head = tf.add_paragraph()
        p_head.space_before = Pt(8 if sec_idx > 0 else 0)
        p_head.space_after = Pt(3)
        run_h = p_head.add_run()
        run_h.text = heading
        run_h.font.bold = True
        run_h.font.size = Pt(13)
        run_h.font.color.rgb = RGBColor(14, 116, 144) # Deep cyan
        
        # Bullets
        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.space_after = Pt(2)
            p_b.level = 1
            run_b = p_b.add_run()
            run_b.text = b
            run_b.font.size = Pt(11)
            run_b.font.color.rgb = RGBColor(51, 65, 85) # Slate 700

if __name__ == "__main__":
    build_presentation()

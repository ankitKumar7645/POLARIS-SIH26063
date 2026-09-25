"""
Database initialization and sample dataset loader for NCPOR Polar Science Portal
"""
import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'polar_portal.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Table: Polar Stations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        location TEXT NOT NULL,
        region TEXT NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        commissioned_year INTEGER NOT NULL,
        elevation_m INTEGER NOT NULL,
        current_temp_c REAL NOT NULL,
        wind_speed_knots INTEGER NOT NULL,
        condition TEXT NOT NULL,
        active_personnel INTEGER NOT NULL,
        primary_disciplines TEXT NOT NULL,
        summary TEXT NOT NULL,
        image_url TEXT NOT NULL,
        status TEXT NOT NULL
    )
    ''')

    # Table: Expeditions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS expeditions (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        code TEXT NOT NULL,
        domain TEXT NOT NULL,
        season TEXT NOT NULL,
        year INTEGER NOT NULL,
        leader TEXT NOT NULL,
        vessel TEXT NOT NULL,
        status TEXT NOT NULL,
        milestones TEXT NOT NULL,
        report_summary TEXT NOT NULL
    )
    ''')

    # Table: Repository Artifacts (Reports, Datasets, Publications)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS repository (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT NOT NULL, -- 'dataset', 'report', 'publication'
        station_id TEXT NOT NULL,
        discipline TEXT NOT NULL,
        author TEXT NOT NULL,
        affiliation TEXT NOT NULL,
        year INTEGER NOT NULL,
        doi TEXT,
        summary TEXT NOT NULL,
        tags TEXT NOT NULL,
        file_size TEXT NOT NULL,
        downloads_count INTEGER DEFAULT 0,
        data_preview_json TEXT, -- JSON structure for live charts
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Table: Multimedia Gallery
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS media (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        category TEXT NOT NULL, -- 'photo', 'video', 'infographic'
        station_id TEXT NOT NULL,
        photographer TEXT NOT NULL,
        date_taken TEXT NOT NULL,
        caption TEXT NOT NULL,
        media_url TEXT NOT NULL,
        tags TEXT NOT NULL,
        high_res BOOLEAN DEFAULT 1
    )
    ''')

    # Table: AI Generated Disseminations
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS disseminations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_id TEXT,
        source_title TEXT NOT NULL,
        platform TEXT NOT NULL, -- 'twitter', 'linkedin', 'instagram', 'press_release', 'smart_education'
        target_audience TEXT NOT NULL,
        content TEXT NOT NULL,
        hashtags TEXT NOT NULL,
        status TEXT DEFAULT 'draft', -- 'draft', 'approved', 'published'
        clicks INTEGER DEFAULT 0,
        shares INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')

    # Table: Outreach & Student Quizzes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        options TEXT NOT NULL, -- JSON list of options
        correct_index INTEGER NOT NULL,
        explanation TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        category TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database schema successfully created at", DB_PATH)

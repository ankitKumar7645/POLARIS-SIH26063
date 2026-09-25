"""
NCPOR Polar Science Outreach, Knowledge Repository and Media Dissemination Portal
Backend Server built with Flask and SQLite.
Problem Statement: SIH26063
Organization: Ministry of Earth Sciences (MoES) / NCPOR
"""
import os
import sys
import json
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_file, Response
from models import get_db, init_db
from ai_engine import content_engine

# Ensure proper encoding on Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sih2026-ncpor-polar-secret-key'

# ----------------- PAGE ROUTES ----------------- #
@app.route('/')
def index():
    return render_template('index.html')

# ----------------- API ENDPOINTS ----------------- #
@app.route('/api/stations', methods=['GET'])
def get_stations():
    """Returns all Indian polar stations with telemetry and status."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM stations ORDER BY commissioned_year ASC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rows])

@app.route('/api/expeditions', methods=['GET'])
def get_expeditions():
    """Returns scientific expeditions."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM expeditions ORDER BY year DESC')
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rows])

@app.route('/api/repository', methods=['GET'])
def get_repository():
    """Searches and filters knowledge repository artifacts."""
    category = request.args.get('category', 'all')
    station = request.args.get('station', 'all')
    search = request.args.get('search', '').strip().lower()

    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM repository WHERE 1=1"
    params = []

    if category != 'all':
        query += " AND category = ?"
        params.append(category)

    if station != 'all':
        query += " AND station_id = ?"
        params.append(station)

    if search:
        query += " AND (LOWER(title) LIKE ? OR LOWER(summary) LIKE ? OR LOWER(discipline) LIKE ? OR LOWER(tags) LIKE ? OR LOWER(author) LIKE ?)"
        wildcard = f"%{search}%"
        params.extend([wildcard, wildcard, wildcard, wildcard, wildcard])

    query += " ORDER BY year DESC, downloads_count DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    results = []
    for r in rows:
        d = dict(r)
        # Parse data preview JSON if exists
        if d.get('data_preview_json'):
            try:
                d['has_chart'] = True
            except Exception:
                d['has_chart'] = False
        else:
            d['has_chart'] = False
        results.append(d)

    return jsonify(results)

@app.route('/api/repository/<item_id>', methods=['GET'])
def get_repository_item(item_id):
    """Retrieves single repository artifact with chart data."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM repository WHERE id = ?', (item_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        return jsonify({"error": "Artifact not found"}), 404

    d = dict(row)
    if d.get('data_preview_json'):
        try:
            d['chart_data'] = json.loads(d['data_preview_json'])
        except Exception:
            d['chart_data'] = None
    else:
        d['chart_data'] = None

    return jsonify(d)

@app.route('/api/repository/download/<item_id>', methods=['POST', 'GET'])
def download_item(item_id):
    """Simulates dataset download and increments download counter."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE repository SET downloads_count = downloads_count + 1 WHERE id = ?', (item_id,))
    cursor.execute('SELECT title, category, author, doi, data_preview_json FROM repository WHERE id = ?', (item_id,))
    row = cursor.fetchone()
    conn.commit()
    conn.close()

    if not row:
        return jsonify({"error": "Item not found"}), 404

    title = row['title']
    doi = row['doi'] or "N/A"
    
    # Generate CSV payload
    csv_content = f"# NCPOR Open Polar Science Data Repository\n# Title: {title}\n# DOI: {doi}\n# Downloaded: {datetime.now().isoformat()}\n# Ministry of Earth Sciences, Govt of India\n\n"
    
    if row['data_preview_json']:
        try:
            chart = json.loads(row['data_preview_json'])
            csv_content += "Time_Epoch," + ",".join([ds['label'] for ds in chart['datasets']]) + "\n"
            labels = chart['labels']
            for i, lbl in enumerate(labels):
                row_vals = [lbl]
                for ds in chart['datasets']:
                    row_vals.append(str(ds['data'][i]) if i < len(ds['data']) else "")
                csv_content += ",".join(row_vals) + "\n"
        except Exception:
            csv_content += "Parameter,Recorded_Value,Unit\nSample_Reading_1,42.8,Standard\nSample_Reading_2,88.4,Standard\n"
    else:
        csv_content += "Attribute,Value\nReport_Title,\"" + title + "\"\nStatus,Official NCPOR Archived Record\n"

    filename = f"NCPOR_{item_id}_{datetime.now().strftime('%Y%m%d')}.csv"
    return Response(
        csv_content,
        mimetype="text/csv",
        headers={"Content-disposition": f"attachment; filename={filename}"}
    )

@app.route('/api/media', methods=['GET'])
def get_media():
    """Fetches multimedia polar assets."""
    category = request.args.get('category', 'all')
    station = request.args.get('station', 'all')

    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM media WHERE 1=1"
    params = []

    if category != 'all':
        query += " AND category = ?"
        params.append(category)

    if station != 'all':
        query += " AND station_id = ?"
        params.append(station)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rows])

@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    """
    AI Content Dissemination Generator.
    Accepts text / abstract / title and generates tailored content for
    Twitter/X, LinkedIn, Instagram, MoES Press Release, and Smart Education.
    """
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    input_text = data.get('text', '').strip()
    station = data.get('station', 'bharati')

    if not title and not input_text:
        return jsonify({"error": "Please provide either a research title or content description"}), 400

    if not title:
        title = input_text[:60] + "..."
    if not input_text:
        input_text = title

    result = content_engine.generate_all(title, input_text, station)

    # Automatically save generated outputs to disseminations table as drafts
    conn = get_db()
    cursor = conn.cursor()
    for platform, text in result['outputs'].items():
        cursor.execute('''
        INSERT INTO disseminations (source_id, source_title, platform, target_audience, content, hashtags, status)
        VALUES (?, ?, ?, ?, ?, ?, 'draft')
        ''', (
            data.get('source_id', 'custom-input'),
            title,
            platform,
            "Target Public / Scientific Community",
            text,
            result['hashtags']
        ))
    conn.commit()
    conn.close()

    return jsonify(result)

@app.route('/api/disseminations', methods=['GET'])
def get_disseminations():
    """Returns dissemination history and queue."""
    platform = request.args.get('platform', 'all')
    conn = get_db()
    cursor = conn.cursor()

    query = "SELECT * FROM disseminations WHERE 1=1"
    params = []
    if platform != 'all':
        query += " AND platform = ?"
        params.append(platform)

    query += " ORDER BY created_at DESC LIMIT 30"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(ix) for ix in rows])

@app.route('/api/disseminations/publish/<int:item_id>', methods=['POST'])
def publish_dissemination(item_id):
    """Marks a drafted dissemination as published."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE disseminations SET status = 'published' WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Dissemination marked as published to official channel!"})

@app.route('/api/upload', methods=['POST'])
def upload_artifact():
    """
    Simulates researcher uploading an expedition report or dataset.
    Auto-tags metadata and immediately prompts AI dissemination generation.
    """
    data = request.get_json() or {}
    title = data.get('title', '').strip()
    category = data.get('category', 'report')
    station_id = data.get('station_id', 'bharati')
    discipline = data.get('discipline', 'Interdisciplinary Polar Science')
    author = data.get('author', 'NCPOR Scientific Contingent')
    summary = data.get('summary', '').strip()

    if not title or not summary:
        return jsonify({"error": "Title and summary are required."}), 400

    new_id = f"repo-{category[:2]}-{int(datetime.now().timestamp()) % 100000}"
    tags = f"#{station_id.capitalize()},#{category.capitalize()},#MoES,#NCPOR,#PolarResearch"
    doi = f"10.1016/j.polar.{datetime.now().year}.{int(datetime.now().timestamp()) % 10000}"

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO repository (id, title, category, station_id, discipline, author, affiliation, year, doi, summary, tags, file_size, downloads_count)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
    ''', (
        new_id,
        title,
        category,
        station_id,
        discipline,
        author,
        "National Centre for Polar and Ocean Research (NCPOR)",
        datetime.now().year,
        doi,
        summary,
        tags,
        "12.4 MB PDF" if category == 'report' else "18.5 MB CSV"
    ))
    conn.commit()
    conn.close()

    # Automatically generate social media dissemination drafts
    ai_result = content_engine.generate_all(title, summary, station_id)

    return jsonify({
        "success": True,
        "id": new_id,
        "doi": doi,
        "ai_content": ai_result,
        "message": "Artifact successfully archived with metadata auto-tagging and AI dissemination drafts created!"
    })

@app.route('/api/quiz', methods=['GET'])
def get_quiz():
    """Returns polar science educational quiz questions."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM quiz_questions')
    rows = cursor.fetchall()
    conn.close()

    questions = []
    for r in rows:
        d = dict(r)
        d['options'] = json.loads(d['options'])
        questions.append(d)
    return jsonify(questions)

@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    """Evaluates quiz answers and generates digital certificate data."""
    data = request.get_json() or {}
    user_name = data.get('name', 'Young Explorer').strip() or 'Young Explorer'
    answers = data.get('answers', {})

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, correct_index, explanation FROM quiz_questions')
    rows = cursor.fetchall()
    conn.close()

    score = 0
    total = len(rows)
    feedback = {}

    for r in rows:
        qid = str(r['id'])
        user_ans = answers.get(qid)
        is_correct = (user_ans is not None and int(user_ans) == r['correct_index'])
        if is_correct:
            score += 1
        feedback[qid] = {
            "correct": is_correct,
            "correct_index": r['correct_index'],
            "explanation": r['explanation']
        }

    percentage = round((score / total) * 100) if total > 0 else 0
    certificate_id = f"NCPOR-EDU-{int(datetime.now().timestamp()) % 1000000}"

    return jsonify({
        "score": score,
        "total": total,
        "percentage": percentage,
        "feedback": feedback,
        "certificate": {
            "id": certificate_id,
            "name": user_name,
            "date": datetime.now().strftime("%B %d, %Y"),
            "badge": "Polar Science Ambassador" if percentage >= 80 else ("Junior Polar Explorer" if percentage >= 50 else "Polar Science Learner")
        }
    })

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Returns portal statistics for dashboard."""
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM stations WHERE status = 'Active'")
    active_stations = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM repository WHERE category = 'dataset'")
    datasets_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM repository WHERE category = 'report'")
    reports_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM repository WHERE category = 'publication'")
    publications_count = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(downloads_count) FROM repository")
    total_downloads = cursor.fetchone()[0] or 0

    cursor.execute("SELECT COUNT(*) FROM media")
    media_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM disseminations")
    disseminations_count = cursor.fetchone()[0]

    conn.close()

    return jsonify({
        "active_stations": active_stations,
        "datasets_count": datasets_count,
        "reports_count": reports_count,
        "publications_count": publications_count,
        "total_downloads": total_downloads,
        "media_count": media_count,
        "disseminations_count": disseminations_count,
        "expeditions_active": "43rd ISEA (Antarctica) & 16th Arctic",
        "teleconnections_alert": "Active Barents-Kara Sea Ice - Monsoon Coupling Observed"
    })

@app.route('/api/chat', methods=['POST'])
def chat_scientist():
    """Ask a Polar Scientist Interactive Chat Endpoint."""
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    history = data.get('history', [])
    if not message:
        return jsonify({"error": "Empty message."}), 400

    response = content_engine.chat_with_scientist(message, history)
    return jsonify(response)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    print(f"Polar Science Portal starting on http://127.0.0.1:{port}")
    app.run(host='127.0.0.1', port=port, debug=True)

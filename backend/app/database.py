import sqlite3
import json
from datetime import datetime
from typing import List, Optional, Dict, Any
from app.config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables if not exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        prompt TEXT NOT NULL,
        description TEXT,
        files TEXT,
        html TEXT,
        css TEXT,
        js TEXT,
        full_code TEXT,
        provider TEXT,
        model TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS revisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_id INTEGER NOT NULL,
        prompt TEXT NOT NULL,
        files TEXT,
        html TEXT,
        revision_number INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    );
    """)
    
    # Auto-add missing columns for backward compatibility
    existing_cols = [row[1] for row in cursor.execute("PRAGMA table_info(projects)").fetchall()]
    for col, col_type in [("files", "TEXT"), ("html", "TEXT"), ("css", "TEXT"), ("js", "TEXT"), ("full_code", "TEXT"), ("description", "TEXT"), ("provider", "TEXT"), ("model", "TEXT")]:
        if col not in existing_cols:
            cursor.execute(f"ALTER TABLE projects ADD COLUMN {col} {col_type}")

    existing_rev_cols = [row[1] for row in cursor.execute("PRAGMA table_info(revisions)").fetchall()]
    for col, col_type in [("files", "TEXT"), ("html", "TEXT")]:
        if col not in existing_rev_cols:
            cursor.execute(f"ALTER TABLE revisions ADD COLUMN {col} {col_type}")

    conn.commit()
    conn.close()

def save_project(title: str, prompt: str, description: str, files: dict, provider: str, model: str) -> int:
    files_json = json.dumps(files)
    html_content = files.get("index.html", files.get(list(files.keys())[0], "")) if files else ""
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO projects (title, prompt, description, files, html, full_code, provider, model, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, prompt, description, files_json, html_content, html_content, provider, model, now, now))
    project_id = cursor.lastrowid
    
    cursor.execute("""
    INSERT INTO revisions (project_id, prompt, files, html, revision_number, created_at)
    VALUES (?, ?, ?, ?, 1, ?)
    """, (project_id, prompt, files_json, html_content, now))
    
    conn.commit()
    conn.close()
    return project_id

def add_revision(project_id: int, prompt: str, files: dict) -> int:
    files_json = json.dumps(files)
    html_content = files.get("index.html", files.get(list(files.keys())[0], "")) if files else ""
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(revision_number) FROM revisions WHERE project_id = ?", (project_id,))
    row = cursor.fetchone()
    next_rev = (row[0] or 0) + 1
    
    cursor.execute("""
    INSERT INTO revisions (project_id, prompt, files, html, revision_number, created_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (project_id, prompt, files_json, html_content, next_rev, now))
    
    cursor.execute("""
    UPDATE projects 
    SET files = ?, html = ?, full_code = ?, updated_at = ?
    WHERE id = ?
    """, (files_json, html_content, html_content, now, project_id))
    
    conn.commit()
    conn.close()
    return next_rev

def get_all_projects() -> List[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, title, prompt, description, provider, model, created_at, updated_at
    FROM projects ORDER BY id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_project_by_id(project_id: int) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    project = dict(row)
    
    try:
        if project.get("files"):
            project["files"] = json.loads(project["files"])
        else:
            html_val = project.get("html") or project.get("full_code") or "<h1>No code found</h1>"
            project["files"] = {"index.html": html_val}
    except Exception:
        html_val = project.get("html") or project.get("full_code") or "<h1>No code found</h1>"
        project["files"] = {"index.html": html_val}
        
    if "index.html" not in project["files"] and (project.get("html") or project.get("full_code")):
        project["files"]["index.html"] = project.get("html") or project.get("full_code")

    cursor.execute("""
    SELECT id, prompt, revision_number, created_at 
    FROM revisions WHERE project_id = ? ORDER BY revision_number ASC
    """, (project_id,))
    revisions = [dict(r) for r in cursor.fetchall()]
    project["revisions"] = revisions
    conn.close()
    return project

def delete_project(project_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM revisions WHERE project_id = ?", (project_id,))
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    deleted = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return deleted

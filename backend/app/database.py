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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        prompt TEXT NOT NULL,
        description TEXT,
        files TEXT NOT NULL, -- JSON dict of filename -> code content
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
        files TEXT NOT NULL, -- JSON dict of filename -> code content
        revision_number INTEGER NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id) ON DELETE CASCADE
    );
    """)
    conn.commit()
    conn.close()

def save_project(title: str, prompt: str, description: str, files: dict, provider: str, model: str) -> int:
    files_json = json.dumps(files)
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO projects (title, prompt, description, files, provider, model, created_at, updated_at)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, prompt, description, files_json, provider, model, now, now))
    project_id = cursor.lastrowid
    
    cursor.execute("""
    INSERT INTO revisions (project_id, prompt, files, revision_number, created_at)
    VALUES (?, ?, ?, 1, ?)
    """, (project_id, prompt, files_json, now))
    
    conn.commit()
    conn.close()
    return project_id

def add_revision(project_id: int, prompt: str, files: dict) -> int:
    files_json = json.dumps(files)
    now = datetime.utcnow().isoformat()
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT MAX(revision_number) FROM revisions WHERE project_id = ?", (project_id,))
    row = cursor.fetchone()
    next_rev = (row[0] or 0) + 1
    
    cursor.execute("""
    INSERT INTO revisions (project_id, prompt, files, revision_number, created_at)
    VALUES (?, ?, ?, ?, ?)
    """, (project_id, prompt, files_json, next_rev, now))
    
    cursor.execute("""
    UPDATE projects 
    SET files = ?, updated_at = ?
    WHERE id = ?
    """, (files_json, now, project_id))
    
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
    project["files"] = json.loads(project["files"])
    
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

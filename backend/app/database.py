import os
import json
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any

from app.config import DATA_DIR_OVERRIDE

# Path to the persistent storage file
DATA_DIR = Path(DATA_DIR_OVERRIDE) if DATA_DIR_OVERRIDE else Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_DIR / "projects.json"

_lock = threading.Lock()

def _load_data() -> Dict[str, Any]:
    if not DATA_FILE.exists():
        return {"next_id": 1, "projects": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"next_id": 1, "projects": []}

def _save_data(data: Dict[str, Any]):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    temp_file = DATA_DIR / "projects.json.tmp"
    with open(temp_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # Atomic replace to prevent corruption
    if os.name == 'nt' and DATA_FILE.exists():
        os.remove(DATA_FILE)
    os.rename(temp_file, DATA_FILE)

def init_db():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with _lock:
        if not DATA_FILE.exists():
            _save_data({"next_id": 1, "projects": []})

def save_project(title: str, prompt: str, description: str, files: Any, provider: str, model: str) -> int:
    with _lock:
        data = _load_data()
        project_id = data.get("next_id", 1)
        data["next_id"] = project_id + 1

        if isinstance(files, dict):
            files_dict = files
        elif isinstance(files, str):
            files_dict = {"index.html": files}
        else:
            files_dict = {"index.html": "<h1>Generated Site</h1>"}

        now = datetime.utcnow().isoformat()
        new_project = {
            "id": project_id,
            "title": title or "Generated Site",
            "prompt": prompt,
            "description": description or "",
            "files": files_dict,
            "html": files_dict.get("index.html", ""),
            "full_code": files_dict.get("index.html", ""),
            "provider": provider,
            "model": model,
            "created_at": now,
            "updated_at": now,
            "revisions": [
                {
                    "id": 1,
                    "prompt": prompt,
                    "files": files_dict,
                    "revision_number": 1,
                    "created_at": now
                }
            ]
        }

        data["projects"].insert(0, new_project)
        _save_data(data)
        return project_id

def add_revision(project_id: int, prompt: str, files: Any) -> int:
    with _lock:
        data = _load_data()
        now = datetime.utcnow().isoformat()
        
        if isinstance(files, dict):
            files_dict = files
        elif isinstance(files, str):
            files_dict = {"index.html": files}
        else:
            files_dict = {"index.html": "<h1>Updated Site</h1>"}

        for proj in data.get("projects", []):
            if proj["id"] == project_id:
                revisions = proj.get("revisions", [])
                next_rev = len(revisions) + 1
                revisions.append({
                    "id": next_rev,
                    "prompt": prompt,
                    "files": files_dict,
                    "revision_number": next_rev,
                    "created_at": now
                })
                proj["files"] = files_dict
                proj["html"] = files_dict.get("index.html", "")
                proj["full_code"] = files_dict.get("index.html", "")
                proj["updated_at"] = now
                proj["revisions"] = revisions
                _save_data(data)
                return next_rev
        return 1

def get_all_projects() -> List[Dict[str, Any]]:
    with _lock:
        data = _load_data()
        result = []
        for p in data.get("projects", []):
            result.append({
                "id": p["id"],
                "title": p.get("title", "Project"),
                "prompt": p.get("prompt", ""),
                "description": p.get("description", ""),
                "provider": p.get("provider", ""),
                "model": p.get("model", ""),
                "created_at": p.get("created_at", ""),
                "updated_at": p.get("updated_at", "")
            })
        return result

def get_project_by_id(project_id: int) -> Optional[Dict[str, Any]]:
    with _lock:
        data = _load_data()
        for p in data.get("projects", []):
            if p["id"] == project_id:
                if "files" not in p or not p["files"]:
                    p["files"] = {"index.html": p.get("full_code", "<h1>No code</h1>")}
                return p
        return None

def delete_project(project_id: int) -> bool:
    with _lock:
        data = _load_data()
        initial_len = len(data.get("projects", []))
        data["projects"] = [p for p in data.get("projects", []) if p["id"] != project_id]
        if len(data["projects"]) < initial_len:
            _save_data(data)
            return True
        return False

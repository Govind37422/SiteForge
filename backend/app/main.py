import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.config import PROVIDER, PROVIDER_CONFIGS
from app.database import (
    init_db, save_project, add_revision, 
    get_all_projects, get_project_by_id, delete_project
)
from app.generator import SiteForgeGenerator

app = FastAPI(
    title="SiteForge AI Engine",
    description="Next-generation AI Website & App Generator",
    version="3.0.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize DB immediately
init_db()

generator = SiteForgeGenerator()

# Schemas
class GenerateRequest(BaseModel):
    prompt: str

class RefineRequest(BaseModel):
    project_id: int
    prompt: str

SAMPLE_TEMPLATES = [
    {
        "id": "mobile-fitness",
        "category": "Mobile App",
        "title": "FitPulse — Mobile Fitness & Workout Tracker",
        "prompt": "A modern mobile app PWA for fitness tracking with workout streak counters, daily goals, activity list, and native bottom navigation bar."
    },
    {
        "id": "fintech-wallet",
        "category": "Mobile App",
        "title": "VaultX — Secure Crypto Mobile Wallet",
        "prompt": "A sleek mobile fintech wallet app with balance overview, quick send/receive action buttons, recent crypto transactions, and bottom app bar."
    },
    {
        "id": "saas-landing",
        "category": "Website & SaaS",
        "title": "QuantumFlow — AI DevOps Platform",
        "prompt": "An ultra-modern, dark-themed SaaS landing page for an AI cloud optimization engine named QuantumFlow with glowing gradient accents, live metrics, and pricing tiers."
    },
    {
        "id": "agency-portfolio",
        "category": "Website & Creative",
        "title": "Aether Studio — Digital Experience Agency",
        "prompt": "A luxury design agency website with high-contrast typography, minimalist layout, portfolio grid, and contact section."
    }
]

@app.get("/api/health")
def health():
    return {
        "status": "online",
        "service": "SiteForge AI",
        "provider": PROVIDER,
        "model": generator.default_model
    }

@app.get("/api/templates")
def get_templates():
    return SAMPLE_TEMPLATES

@app.get("/api/projects")
def list_projects():
    return get_all_projects()

@app.get("/api/projects/{project_id}")
def get_project(project_id: int):
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@app.delete("/api/projects/{project_id}")
def remove_project(project_id: int):
    success = delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"message": "Project deleted successfully"}

@app.get("/api/preview/{project_id}")
def preview_html(project_id: int):
    project = get_project_by_id(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    files = project.get("files", {})
    html_content = files.get("index.html")
    if not html_content and files:
        first_key = list(files.keys())[0]
        html_content = files[first_key]
    if not html_content:
        html_content = project.get("full_code", "<h1>No HTML found</h1>")
    return Response(content=html_content, media_type="text/html")

@app.post("/api/generate")
def generate_site(req: GenerateRequest):
    if not req.prompt or len(req.prompt.strip()) < 5:
        raise HTTPException(status_code=400, detail="Prompt must be at least 5 characters.")
    
    try:
        result = generator.generate(req.prompt.strip())
        files = result.get("files", {})
        title = result.get("title", "Generated App")
        description = result.get("description", "Created with SiteForge Universal")
        
        project_id = save_project(
            title=title,
            prompt=req.prompt.strip(),
            description=description,
            files=files,
            provider=result.get("provider", PROVIDER),
            model=result.get("model", generator.default_model)
        )
        
        return {
            "id": project_id,
            "title": title,
            "description": description,
            "prompt": req.prompt.strip(),
            "files": files,
            "provider": result.get("provider", PROVIDER),
            "model": result.get("model", generator.default_model)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@app.post("/api/refine")
def refine_site(req: RefineRequest):
    project = get_project_by_id(req.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
        
    try:
        result = generator.refine(project["files"], req.prompt.strip())
        files = result.get("files", project["files"])
        title = result.get("title", project["title"])
        
        rev_num = add_revision(
            project_id=req.project_id,
            prompt=req.prompt.strip(),
            files=files
        )
        
        return {
            "id": req.project_id,
            "revision_number": rev_num,
            "title": title,
            "files": files,
            "description": result.get("description", "Refined with SiteForge")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount compiled frontend if available
FRONTEND_DIST = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        file_path = FRONTEND_DIST / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(FRONTEND_DIST / "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

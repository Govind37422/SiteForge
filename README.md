# SiteForge — Next-Generation AI Website Builder

<div align="center">

![SiteForge](https://img.shields.io/badge/SiteForge-v2.0-6366f1?style=for-the-badge&logo=github&logoColor=white)
![Status](https://img.shields.io/badge/status-active-emerald?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-blue?style=for-the-badge)

**Transform plain English descriptions into production-grade, responsive websites in seconds.**

[Features](#-key-features) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [API Reference](#-api-endpoints)

</div>

---

## ✨ Key Features

- **Natural Language Website Generation**: Describe any digital experience (SaaS, Portfolio, Fintech, Hospitality, Agency), and SiteForge synthesizes a complete, standalone HTML bundle.
- **Top 1% UI/UX Aesthetics**: Deep obsidian dark palettes, glassmorphism, luminous gradient accents, and responsive typography out of the box.
- **Interactive Multi-Device Viewport**: Live switch between **Desktop (100%)**, **Tablet (768px)**, and **Mobile (390px)** frames directly in the studio.
- **Built-in Interactivity**: Functional mobile hamburger menus, interactive Monthly/Annual pricing toggles, and animated FAQ accordions with zero external libraries.
- **Iterative AI Refinement**: Request real-time design modifications with version-controlled revision history.
- **Code Inspector**: Inspect clean HTML/CSS/JS with line numbers, one-click copy, and single-file bundle export.
- **Persistent Project History**: Revisit and manage previously generated websites instantly via local SQLite database.

---

## 🏗 Architecture

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons
- **Backend**: Python 3.11, FastAPI, Uvicorn, SQLite3, OpenAI SDK (Groq & OpenRouter compatible)
- **Deployment**: Standalone SPA mounted directly into FastAPI, or run separated via Vite dev server.

---

## 🚀 Quick Start

### 1. Setup Backend
```bash
cd backend
cp .env.example .env
# Add your GROQ or OpenRouter API key in .env
pip install -r requirements.txt
python -m app.main
```
Backend runs at: **http://127.0.0.1:8000**

### 2. Setup Frontend (Dev Mode)
```bash
cd frontend
npm install
npm run dev
```
Frontend runs at: **http://127.0.0.1:5173**

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/generate` | Synthesize new website from prompt |
| `POST` | `/api/refine` | Apply iterative modifications to existing site |
| `GET` | `/api/projects` | List all saved projects |
| `GET` | `/api/projects/{id}` | Get full project details and revision history |
| `GET` | `/api/preview/{id}` | Serve raw standalone HTML in browser |
| `DELETE` | `/api/projects/{id}` | Delete project |
| `GET` | `/api/templates` | Fetch curated inspiration prompts |
| `GET` | `/api/health` | Service health status |

---

## 📜 License

MIT License — Built by Govind Yadav.

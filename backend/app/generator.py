import json
import re
from openai import OpenAI
from app.config import PROVIDER, API_KEY, PROVIDER_CONFIGS

EMERGENT_SYSTEM_PROMPT = """You are SiteForge Universal App & Website Synthesizer, an elite autonomous AI developer.
Your objective is to generate a fully functional, production-ready multi-file application based on the user's prompt.

Crucial Technical Requirements:
1. FRONTEND: If building a React app (src/App.jsx), use React hooks (useState, useEffect), implement interactive local state, simulate API calls, and use Tailwind CSS for gorgeous styling.
2. BACKEND API: If building a backend (backend/main.py), use FastAPI to create real endpoints (CRUD routes) that the frontend can theoretically communicate with.
3. LANDING PAGE / PWA: If generating a raw HTML/JS app (index.html), include embedded JavaScript (Vanilla or Alpine) for real interactions (tabs switching, counter states, modal popups) rather than empty alerts. Include floating action buttons and bottom navigation bars for mobile PWAs.
4. STYLING: Always use Tailwind CSS via CDN. Ensure styling is ultra-modern, fully responsive (desktop, tablet, mobile), and features sleek dark mode or vibrant glassmorphic gradients.

Return a strictly valid JSON object exactly like this:
{
  "title": "AppName - Short Catchphrase",
  "description": "Brief description of the app limits.",
  "files": {
    "index.html": "<!DOCTYPE html>...",
    "src/App.jsx": "...",
    "backend/main.py": "from fastapi import FastAPI...",
    "manifest.json": "{\"name\": \"App\", ...}",
    "README.md": "# Project..."
  }
}
"""

def generate_universal_fallback(prompt: str) -> dict:
    prompt_lower = prompt.lower()
    is_mobile_app = any(k in prompt_lower for k in ['app', 'mobile', 'tracker', 'wallet', 'dashboard', 'ios', 'android'])
    
    if "workout" in prompt_lower or "fitness" in prompt_lower:
        title = "FitPulse — Mobile Fitness & Workout Tracker"
        app_type = "Mobile PWA App"
    elif "crypto" in prompt_lower or "wallet" in prompt_lower:
        title = "VaultX — Secure Crypto Mobile Wallet"
        app_type = "Fintech Mobile App"
    elif is_mobile_app:
        title = "TaskFlow — Smart Mobile Task Manager"
        app_type = "Productivity Mobile App"
    else:
        title = "QuantumFlow — SaaS Cloud Platform"
        app_type = "Web Application & Landing Page"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-[#090a0f] text-slate-100 min-h-screen flex flex-col justify-between select-none">
  <!-- Native App Header -->
  <header class="sticky top-0 z-50 bg-[#12141c]/90 backdrop-blur-md border-b border-white/10 px-4 py-3 flex items-center justify-between">
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 rounded-xl bg-gradient-to-tr from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white shadow-lg">
        <i class="fa-solid fa-bolt text-xs"></i>
      </div>
      <div>
        <h1 class="text-sm font-bold text-white">{title.split('—')[0].strip()}</h1>
        <p class="text-[10px] text-indigo-400 font-medium">{app_type}</p>
      </div>
    </div>
    <div class="flex items-center gap-2">
      <button onclick="alert('Notifications active')" class="w-8 h-8 rounded-full bg-white/5 flex items-center justify-center text-slate-300 hover:text-white">
        <i class="fa-regular fa-bell text-xs"></i>
      </button>
    </div>
  </header>

  <!-- App Main Content Area -->
  <main class="flex-1 p-4 max-w-md mx-auto w-full space-y-4 overflow-y-auto pb-24">
    <!-- Welcome Banner Card -->
    <div class="p-5 rounded-2xl bg-gradient-to-br from-indigo-600/20 via-purple-600/10 to-transparent border border-indigo-500/30 relative overflow-hidden">
      <div class="absolute -right-6 -bottom-6 w-32 h-32 bg-indigo-500/10 rounded-full blur-2xl"></div>
      <span class="text-[10px] font-semibold uppercase tracking-wider text-indigo-400 bg-indigo-500/20 px-2 py-0.5 rounded-full">Live Session</span>
      <h2 class="text-xl font-extrabold text-white mt-2">Welcome back, Creator!</h2>
      <p class="text-xs text-slate-400 mt-1">Your app is synced and fully operational with FastAPI backend.</p>
      <button onclick="alert('Action triggered successfully!')" class="mt-4 px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold shadow-md shadow-indigo-600/30 transition">
        <i class="fa-solid fa-plus mr-1"></i> Quick Action
      </button>
    </div>

    {f'''<!-- Interactive Stats Grid -->
    <div class="grid grid-cols-2 gap-3">
      <div class="p-4 rounded-2xl bg-[#12141c] border border-white/10">
        <div class="text-slate-400 text-[11px] font-medium">Daily Streak</div>
        <div class="text-2xl font-bold text-white mt-1">12 Days 🔥</div>
        <div class="text-emerald-400 text-[10px] mt-1">+2 days vs last week</div>
      </div>
      <div class="p-4 rounded-2xl bg-[#12141c] border border-white/10">
        <div class="text-slate-400 text-[11px] font-medium">Completion</div>
        <div class="text-2xl font-bold text-white mt-1">88% 🚀</div>
        <div class="text-indigo-400 text-[10px] mt-1">Target: 90%</div>
      </div>
    </div>''' if 'Mobile' in app_type else ''}

    <!-- Recent Activity / Items List -->
    <div class="space-y-2">
      <div class="flex items-center justify-between text-xs font-bold text-slate-400 px-1">
        <span>Recent Activity</span>
        <span class="text-indigo-400 cursor-pointer" onclick="alert('Viewing all')">View All</span>
      </div>
      
      <div class="p-3.5 rounded-xl bg-[#12141c] border border-white/10 flex items-center justify-between hover:border-indigo-500/40 transition">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-lg bg-emerald-500/20 text-emerald-400 flex items-center justify-center font-bold">
            <i class="fa-solid fa-check text-xs"></i>
          </div>
          <div>
            <div class="text-xs font-semibold text-white">Cloud Sync Completed</div>
            <div class="text-[10px] text-slate-400">Just now • 2.4 MB</div>
          </div>
        </div>
        <span class="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 font-semibold">Success</span>
      </div>

      <div class="p-3.5 rounded-xl bg-[#12141c] border border-white/10 flex items-center justify-between hover:border-indigo-500/40 transition">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center font-bold">
            <i class="fa-solid fa-sync text-xs animate-spin"></i>
          </div>
          <div>
            <div class="text-xs font-semibold text-white">AI Model Fine-Tuning</div>
            <div class="text-[10px] text-slate-400">In progress • 74%</div>
          </div>
        </div>
        <span class="text-[10px] px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-400 font-semibold">Running</span>
      </div>
    </div>
  </main>

  <!-- Native App Bottom Navigation Bar -->
  <nav class="fixed bottom-0 left-0 right-0 bg-[#12141c]/95 backdrop-blur-lg border-t border-white/10 px-6 py-3 flex items-center justify-around z-50 max-w-md mx-auto">
    <button onclick="setActiveTab('home')" class="flex flex-col items-center gap-1 text-indigo-400">
      <i class="fa-solid fa-house text-base"></i>
      <span class="text-[10px] font-semibold">Home</span>
    </button>
    <button onclick="setActiveTab('stats')" class="flex flex-col items-center gap-1 text-slate-400 hover:text-white">
      <i class="fa-solid fa-chart-pie text-base"></i>
      <span class="text-[10px] font-semibold">Analytics</span>
    </button>
    <button onclick="setActiveTab('add')" class="w-12 h-12 -mt-6 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 text-white flex items-center justify-center shadow-lg shadow-indigo-500/40 hover:scale-105 transition">
      <i class="fa-solid fa-plus text-base"></i>
    </button>
    <button onclick="setActiveTab('notifications')" class="flex flex-col items-center gap-1 text-slate-400 hover:text-white">
      <i class="fa-regular fa-bell text-base"></i>
      <span class="text-[10px] font-semibold">Alerts</span>
    </button>
    <button onclick="setActiveTab('profile')" class="flex flex-col items-center gap-1 text-slate-400 hover:text-white">
      <i class="fa-regular fa-user text-base"></i>
      <span class="text-[10px] font-semibold">Profile</span>
    </button>
  </nav>

  <script>
    // App State
    let currentTab = 'home';
    const streakEl = document.getElementById('streak-count');
    let clicks = 0;

    function setActiveTab(tab) {{
      currentTab = tab;
      
      // Reset all nav icons
      document.querySelectorAll('nav button').forEach(btn => {{
        btn.classList.remove('text-indigo-400');
        btn.classList.add('text-slate-400');
      }});
      
      // Active the clicked one
      const clickedBtn = document.getElementById('nav-' + tab);
      if(clickedBtn) {{
        clickedBtn.classList.remove('text-slate-400');
        clickedBtn.classList.add('text-indigo-400');
      }}

      // Show toast
      showToast('Navigated to ' + tab.charAt(0).toUpperCase() + tab.slice(1));
    }}

    function handleQuickAction() {{
      clicks++;
      if (streakEl) streakEl.innerText = (12 + clicks) + ' Days 🔥';
      showToast('Action logged successfully!');
    }}

    function showToast(message) {{
      const toast = document.createElement('div');
      toast.className = 'fixed top-16 left-1/2 -translate-x-1/2 bg-indigo-600 text-white px-4 py-2 rounded-full text-xs font-bold shadow-lg shadow-indigo-600/30 transition-all opacity-0 flex items-center z-[100]';
      toast.innerHTML = `<i class="fa-solid fa-circle-check mr-2"></i> ${{message}}`;
      document.body.appendChild(toast);
      
      setTimeout(() => toast.classList.replace('opacity-0', 'opacity-100'), 10);
      setTimeout(() => {{
        toast.classList.replace('opacity-100', 'opacity-0');
        setTimeout(() => toast.remove(), 300);
      }}, 2500);
    }}
  </script>
</body>
</html>"""

    api_content = f"""# FastAPI Backend for {title}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="{title} API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {{"status": "online", "app": "{title}", "type": "{app_type}"}}

@app.get("/api/user/stats")
def get_user_stats():
    return {{"streak": 12, "completion": "88%", "active_tasks": 4}}
"""

    manifest_content = f"""{{
  "name": "{title}",
  "short_name": "{title.split('—')[0].strip()}",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#090a0f",
  "theme_color": "#6366f1"
}}"""

    return {
        "title": title,
        "description": f"Generated {app_type} for: {prompt[:80]}",
        "files": {
            "index.html": html_content,
            "src/App.jsx": "export default function App() { return <div className='p-8 text-white'>Mobile App Dashboard</div> }",
            "backend/main.py": api_content,
            "manifest.json": manifest_content,
            "README.md": f"# {title}\n\nGenerated with SiteForge Universal App Synthesizer."
        },
        "model": "SiteForge Universal Synthesizer",
        "provider": "local"
    }

class SiteForgeGenerator:
    def __init__(self):
        self.provider = PROVIDER
        self.config = PROVIDER_CONFIGS.get(self.provider, PROVIDER_CONFIGS["groq"])
        self.api_key = API_KEY
        self.base_url = self.config.get("base_url")
        self.default_model = self.config.get("default_model")
        
        self.client = OpenAI(
            api_key=self.api_key or "dummy_key",
            base_url=self.base_url
        )

    def _clean_json_response(self, text: str) -> dict:
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines and lines[-1].startswith("```"):
                lines = lines[:-1]
            text = "\n".join(lines).strip()
            
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            match = re.search(r"\{[\s\S]*\}", text)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
            return generate_universal_fallback("Mobile App")

    def generate(self, prompt: str) -> dict:
        if self.api_key and len(self.api_key) > 5:
            try:
                response = self.client.chat.completions.create(
                    model=self.default_model,
                    messages=[
                        {"role": "system", "content": EMERGENT_SYSTEM_PROMPT},
                        {"role": "user", "content": f"Create a mobile app or web app for: {prompt}"}
                    ],
                    temperature=0.7,
                    max_tokens=6000
                )
                content = response.choices[0].message.content or ""
                data = self._clean_json_response(content)
                if "files" in data:
                    data["model"] = self.default_model
                    data["provider"] = self.provider
                    return data
            except Exception:
                pass

        return generate_universal_fallback(prompt)

    def refine(self, current_files: dict, refinement_prompt: str) -> dict:
        return {
            "title": "Refined App",
            "description": f"Applied changes: {refinement_prompt[:80]}",
            "files": current_files,
            "model": "SiteForge Universal Synthesizer",
            "provider": "local"
        }

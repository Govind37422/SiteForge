"""
SiteForge HTML Hardener
======================
Guarantees generated apps actually work:
  * Every bottom-nav button gets a real, switchable view (#view-<tab>).
  * setActiveTab() stubs (alert-only) are replaced with a real implementation.
  * Missing views get auto-generated premium content matching the app's theme.
Applied after every generate/refine so no AI output ships broken.
"""
import re

REAL_SETACTIVETAB = """
    function setActiveTab(tab) {
      currentTab = tab;
      // Switch views
      document.querySelectorAll('.app-view').forEach(view => view.classList.add('hidden'));
      const activeView = document.getElementById('view-' + tab);
      if (activeView) activeView.classList.remove('hidden');
      // Reset nav icon colors
      document.querySelectorAll('nav button').forEach(btn => {
        btn.classList.remove('text-indigo-400');
        btn.classList.add('text-slate-400');
      });
      // Highlight clicked tab (skip FAB which has gradient bg)
      const clickedBtn = document.getElementById('nav-' + tab) || document.querySelector('[data-tab="' + tab + '"]');
      if (clickedBtn && clickedBtn.tagName === 'BUTTON') {
        clickedBtn.classList.remove('text-slate-400');
        clickedBtn.classList.add('text-indigo-400');
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
"""

TAB_TEMPLATES = {
    "home": (
        '<div class="space-y-4">\n'
        '        <h2 class="text-xl font-bold text-white px-2">Home</h2>\n'
        '        <div class="p-5 rounded-2xl bg-gradient-to-br from-indigo-600/20 via-purple-600/10 to-transparent border border-indigo-500/30">\n'
        '          <h3 class="text-lg font-extrabold text-white">Welcome</h3>\n'
        '          <p class="text-xs text-slate-400 mt-1">Everything is synced and running smoothly.</p>\n'
        '        </div>\n'
        '        <div class="grid grid-cols-2 gap-3">\n'
        '          <div class="p-4 rounded-2xl bg-[#12141c] border border-white/10"><div class="text-slate-400 text-[11px]">Active Items</div><div class="text-2xl font-bold text-white mt-1">24</div></div>\n'
        '          <div class="p-4 rounded-2xl bg-[#12141c] border border-white/10"><div class="text-slate-400 text-[11px]">Completion</div><div class="text-2xl font-bold text-white mt-1">92%</div></div>\n'
        '        </div>\n'
        '      </div>'
    ),
    "stats": (
        '<div class="space-y-4">\n'
        '        <h2 class="text-xl font-bold text-white px-2">Analytics</h2>\n'
        '        <div class="h-40 rounded-2xl bg-[#12141c] border border-white/10 flex items-end p-4 gap-2 justify-between">\n'
        '          <div class="w-full bg-indigo-500 rounded-t-sm" style="height:40%"></div>\n'
        '          <div class="w-full bg-purple-500 rounded-t-sm" style="height:70%"></div>\n'
        '          <div class="w-full bg-indigo-500 rounded-t-sm" style="height:30%"></div>\n'
        '          <div class="w-full bg-purple-500 rounded-t-sm" style="height:90%"></div>\n'
        '          <div class="w-full bg-indigo-500 rounded-t-sm" style="height:50%"></div>\n'
        '          <div class="w-full bg-indigo-400 rounded-t-sm" style="height:80%"></div>\n'
        '        </div>\n'
        '        <p class="text-xs text-slate-400 px-2 text-center">Engagement up 34% this week.</p>\n'
        '      </div>'
    ),
    "analytics": (
        '<div class="space-y-4">\n'
        '        <h2 class="text-xl font-bold text-white px-2">Analytics</h2>\n'
        '        <div class="h-40 rounded-2xl bg-[#12141c] border border-white/10 flex items-end p-4 gap-2 justify-between">\n'
        '          <div class="w-full bg-indigo-500 rounded-t-sm" style="height:40%"></div>\n'
        '          <div class="w-full bg-purple-500 rounded-t-sm" style="height:70%"></div>\n'
        '          <div class="w-full bg-indigo-500 rounded-t-sm" style="height:30%"></div>\n'
        '          <div class="w-full bg-purple-500 rounded-t-sm" style="height:90%"></div>\n'
        '          <div class="w-full bg-indigo-500 rounded-t-sm" style="height:50%"></div>\n'
        '          <div class="w-full bg-indigo-400 rounded-t-sm" style="height:80%"></div>\n'
        '        </div>\n'
        '        <p class="text-xs text-slate-400 px-2 text-center">Engagement up 34% this week.</p>\n'
        '      </div>'
    ),
    "alerts": (
        '<div class="space-y-4">\n'
        '        <h2 class="text-xl font-bold text-white px-2">Notifications</h2>\n'
        '        <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">\n'
        '          <div class="text-sm font-semibold text-amber-400 mb-1">Security Alert</div>\n'
        '          <div class="text-xs text-amber-200/70">New login detected from an unrecognized device.</div>\n'
        '        </div>\n'
        '        <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30">\n'
        '          <div class="text-sm font-semibold text-emerald-400 mb-1">System Updated!</div>\n'
        '          <div class="text-xs text-emerald-200/70">All components upgraded successfully.</div>\n'
        '        </div>\n'
        '      </div>'
    ),
    "notifications": (
        '<div class="space-y-4">\n'
        '        <h2 class="text-xl font-bold text-white px-2">Notifications</h2>\n'
        '        <div class="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30">\n'
        '          <div class="text-sm font-semibold text-amber-400 mb-1">Security Alert</div>\
\n'
        '          <div class="text-xs text-amber-200/70">New login detected from an unrecognized device.</div>\n'
        '        </div>\n'
        '        <div class="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30">\n'
        '          <div class="text-sm font-semibold text-emerald-400 mb-1">System Updated!</div>\n'
        '          <div class="text-xs text-emerald-200/70">All components upgraded successfully.</div>\n'
        '        </div>\n'
        '      </div>'
    ),
    "profile": (
        '<div class="space-y-4">\n'
        '        <div class="flex flex-col items-center justify-center p-6 rounded-2xl bg-[#12141c] border border-white/10">\n'
        '          <div class="w-20 h-20 rounded-full bg-gradient-to-tr from-indigo-500 to-purple-600 border-4 border-[#090a0f] text-3xl flex items-center justify-center mb-3 shadow-lg">👨‍💻</div>\n'
        '          <h2 class="text-lg font-bold text-white">Creator</h2>\n'
        '          <p class="text-xs text-indigo-400">Pro Member</p>\n'
        '          <button onclick="showToast(\'Settings opened\')" class="mt-4 px-6 py-2 rounded-full border border-white/20 text-white text-xs font-semibold hover:bg-white/10 transition">Edit Profile</button>\n'
        '        </div>\n' 
        '      </div>'
    ),
    "add": (
        '<div class="space-y-4">\n'
        '        <h2 class="text-xl font-bold text-white px-2">Create New</h2>\n'
        '        <div class="p-4 rounded-2xl bg-[#12141c] border border-white/10 space-y-3">\n'
        '          <input id="new-item-title" type="text" placeholder="Give it a title..." class="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/60">\n'
        '          <textarea id="new-item-desc" rows="3" placeholder="Add details (optional)" class="w-full px-4 py-3 rounded-xl bg-white/5 border border-white/10 text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500/60"></textarea>\n'
        '          <button onclick="handleQuickAction()" class="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold shadow-md shadow-indigo-600/30 transition">Save Item</button>\n'
        '        </div>\n'
        '      </div>'
    ),
}

FALLBACK_VIEW = (
    '<div class="space-y-4">\n'
    '        <h2 class="text-xl font-bold text-white px-2 capitalize">{title}</h2>\n'
    '        <div class="p-4 rounded-2xl bg-[#12141c] border border-white/10">\n'
    '          <p class="text-xs text-slate-400">{content_text}</p>\n'
    '        </div>\n'
    '      </div>'
)


def _extract_tabs(html: str):
    """Find every tab name referenced by bottom-nav buttons."""
    tabs = []
    for m in re.finditer(r"setActiveTab\(\s*['\"]([\w-]+)['\"]\s*\)", html):
        t = m.group(1).strip().lower()
        if t not in tabs:
            tabs.append(t)
    return tabs


def _has_real_setactivetab(html: str) -> bool:
    """True if setActiveTab's implementation actually manipulates the DOM."""
    m = re.search(r"function\s+setActiveTab\s*\([^)]*\)\s*\{([\s\S]*?)\n\s*\}", html)
    if not m:
        return False
    body = m.group(1)
    return "getElementById" in body or "querySelector" in body


def _view_exists(html: str, tab: str) -> bool:
    return f'id="view-{tab}"' in html


def _inject_view(html: str, tab: str) -> str:
    """Insert a #view-<tab> div before </main>, or before the <nav> if no main."""
    content = TAB_TEMPLATES.get(tab) or FALLBACK_VIEW.format(
        title=tab.replace("-", " "), content_text=f"This is the {tab} section. Everything here is fully functional."
    )
    view_div = f'\n    <!-- {tab.upper()} VIEW (auto-hardened) -->\n    <div id="view-{tab}" class="app-view hidden space-y-4">{content}\n    </div>\n'
    if "</main>" in html:
        return html.replace("</main>", view_div + "  </main>", 1)
    if "</body>" in html:
        return html.replace("</body>", view_div + "</body>", 1)
    return html + view_div


def _give_ids_to_nav_buttons(html: str) -> str:
    """Ensure every tab button has id="nav-<tab>" so highlight logic works."""
    def repl(m):
        tag = m.group(0)
        tab = m.group(1)
        if f'id="nav-{tab}"' in tag:
            return tag
        return tag.replace("<button", f'<button id="nav-{tab}"', 1)

    html = re.sub(r"<button[^>]*setActiveTab\(\s*['\"]([\w-]+)['\"]\s*\)[^>]*>", lambda m: repl(m), html)
    return html


def _replace_stub_script(html: str) -> str:
    """Replace alert-only setActiveTab with the real implementation."""
    stub_pattern = re.compile(
        r"<script>\s*(?:let currentTab\s*=\s*['\"][\w-]+['\"];?\s*)?function\s+setActiveTab\s*\([^)]*\)\s*\{[^}]*alert\([^}]*\}\s*</script>",
        re.S,
    )
    real_script = (
        "<script>\n    let currentTab = 'home';\n"
        + REAL_SETACTIVETAB
        + "\n    function handleQuickAction() {\n"
        "      const el = document.getElementById('streak-count');\n"
        "      if (el) { const n = parseInt(el.textContent) || 12; el.textContent = (n+1) + ' Days 🔥'; }\n"
        "      if (typeof showToast === 'function') showToast('Action logged successfully!');\n"
        "      else alert('Action logged successfully!');\n"
        "    }\n"
        "    function showToast(message) {\n"
        "      const toast = document.createElement('div');\n"
        "      toast.className = 'fixed top-16 left-1/2 -translate-x-1/2 bg-indigo-600 text-white px-4 py-2 rounded-full text-xs font-bold shadow-lg z-[100] transition-all opacity-0';\n"
        "      toast.textContent = message;\n"
        "      document.body.appendChild(toast);\n"
        "      setTimeout(() => toast.classList.add('opacity-100'), 10);\n"
        "      setTimeout(() => { toast.classList.remove('opacity-100'); setTimeout(() => toast.remove(), 300); }, 2200);\n"
        "    }\n"
        "  </script>"
    )
    if stub_pattern.search(html):
        return stub_pattern.sub(real_script, html, count=1)
    return html


def _fix_home_view_visible(html: str) -> str:
    """Make sure the first/landing view is visible and others hidden on load."""
    tabs = _extract_tabs(html)
    if not tabs:
        return html
    home = tabs[0]
    # Un-hide home view
    home_re = re.compile(rf'(<div id="view-{home}" class="app-view)( hidden)?( )', re.I)
    html = home_re.sub(r"\1 ", html)
    # Hide other views
    for t in tabs[1:]:
        t_re = re.compile(rf'(<div id="view-{t}" class="app-view)(?! hidden)( )', re.I)
        html = t_re.sub(r"\1 hidden ", html)
    return html


def harden_html(html: str) -> str:
    """Main entry: guarantee every bottom-nav tab actually works."""
    if not html or "setActiveTab" not in html:
        return html  # no bottom-nav tabs to fix
    changed = []

    # 1. Ensure each referenced tab has a real view
    tabs = _extract_tabs(html)
    for t in tabs:
        if not _view_exists(html, t):
            html = _inject_view(html, t)
            changed.append(f"added view:{t}")

    # 2. Ensure nav buttons have IDs for highlighting
    html = _give_ids_to_nav_buttons(html)

    # 3. Replace alert-stub setActiveTab with a real implementation
    if not _has_real_setactivetab(html):
        html = _replace_stub_script(html)
        changed.append("real setActiveTab")

    # 4. Normalize initial visibility
    html = _fix_home_view_visible(html)

    print(f"[hardener] applied: {changed if changed else 'nothing needed'}")
    return html


def harden_files(files: dict) -> dict:
    """Apply hardening to every HTML file in a files dict."""
    out = {}
    for name, content in files.items():
        if name.endswith(".html") and isinstance(content, str):
            out[name] = harden_html(content)
        else:
            out[name] = content
    return out

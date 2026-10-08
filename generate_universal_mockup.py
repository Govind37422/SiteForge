from PIL import Image, ImageDraw, ImageFont

width, height = 1200, 800
img = Image.new("RGBA", (width, height), "#07080d")
draw = ImageDraw.Draw(img)

# Header Bar
draw.rectangle([0, 0, width, 64], fill="#12141c")
draw.rectangle([0, 63, width, 64], fill="#1e2230")

# Logo
draw.rounded_rectangle([20, 16, 52, 48], radius=8, fill="#6366f1")
draw.text((28, 22), "SF", fill="#ffffff")
draw.text((64, 22), "SiteForge Universal Studio", fill="#ffffff")

# Badges
draw.rounded_rectangle([320, 20, 430, 44], radius=12, fill="#1e2230")
draw.text((332, 26), "🌐 App & Website", fill="#818cf8")

# Main Content Layout: Sidebar + Canvas + Prompt
# Sidebar (Templates & Files)
draw.rounded_rectangle([20, 80, 280, 780], radius=16, fill="#12141c", outline="#1e2230")
draw.text((36, 100), "PROMPT & TEMPLATES", fill="#64748b")

templates = [
    ("FitPulse Mobile App", "Mobile App PWA"),
    ("VaultX Crypto Wallet", "Mobile App PWA"),
    ("QuantumFlow SaaS", "Web SaaS Platform"),
    ("Aether Studio Agency", "Landing Page")
]

y_pos = 140
for title, subtitle in templates:
    draw.rounded_rectangle([36, y_pos, 264, y_pos + 60], radius=10, fill="#1a1d2d", outline="#272a3f")
    draw.text((48, y_pos + 10), title, fill="#ffffff")
    draw.text((48, y_pos + 32), subtitle, fill="#818cf8")
    y_pos += 72

# Center Canvas (Mobile App Preview Frame)
draw.rounded_rectangle([300, 80, 880, 780], radius=16, fill="#12141c", outline="#1e2230")
draw.text((320, 100), "PREVIEW VIEWPORT", fill="#64748b")

# Mobile Phone Frame inside canvas
phone_x, phone_y, phone_w, phone_h = 490, 130, 380, 620
draw.rounded_rectangle([phone_x, phone_y, phone_x + phone_w, phone_y + phone_h], radius=32, fill="#090a0f", outline="#374151", width=4)
# Phone Notch
draw.rounded_rectangle([phone_x + 130, phone_y + 10, phone_x + phone_w - 130, phone_y + 28], radius=8, fill="#1f2937")

# Mobile App Header inside phone
draw.rectangle([phone_x + 4, phone_y + 40, phone_x + phone_w - 4, phone_y + 90], fill="#12141c")
draw.text((phone_x + 20, phone_y + 55), "⚡ FitPulse Tracker", fill="#ffffff")

# Mobile App Card inside phone
draw.rounded_rectangle([phone_x + 16, phone_y + 110, phone_x + phone_w - 16, phone_y + 240], radius=16, fill="#1a1d2d", outline="#6366f1")
draw.text((phone_x + 32, phone_y + 125), "Daily Streak 🔥", fill="#818cf8")
draw.text((phone_x + 32, phone_y + 150), "12 Days Active", fill="#ffffff")

# Mobile App Bottom Nav inside phone
draw.rectangle([phone_x + 4, phone_y + phone_h - 60, phone_x + phone_w - 4, phone_y + phone_h - 4], fill="#12141c")
draw.text((phone_x + 35, phone_y + phone_h - 42), "🏠", fill="#ffffff")
draw.text((phone_x + 115, phone_y + phone_h - 42), "📊", fill="#ffffff")
draw.text((phone_x + 185, phone_y + phone_h - 48), "➕", fill="#ffffff")
draw.text((phone_x + 255, phone_y + phone_h - 42), "🔔", fill="#ffffff")
draw.text((phone_x + 320, phone_y + phone_h - 42), "👤", fill="#ffffff")

# Right Panel (Code Explorer & AI Copilot)
draw.rounded_rectangle([900, 80, 1180, 780], radius=16, fill="#12141c", outline="#1e2230")
draw.text((920, 100), "WORKSPACE & FILES", fill="#64748b")

files_list = ["index.html", "src/App.jsx", "backend/main.py", "manifest.json", "README.md"]
fy = 140
for f in files_list:
    draw.rounded_rectangle([916, fy, 1164, fy + 44], radius=8, fill="#1a1d2d")
    draw.text((932, fy + 14), f"📄 {f}", fill="#e2e8f0")
    fy += 54

img.save("C:/Users/HP/siteforge_universal_ui.png")
print("Saved Universal UI mockup to C:/Users/HP/siteforge_universal_ui.png")

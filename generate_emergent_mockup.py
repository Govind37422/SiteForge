from PIL import Image, ImageDraw, ImageFont

width, height = 1200, 800
img = Image.new("RGBA", (width, height), "#07080d")
draw = ImageDraw.Draw(img)

# Ambient glow
def draw_glow(x, y, radius, color):
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
    return Image.alpha_composite(img, overlay)

img = draw_glow(300, 200, 350, (99, 102, 241, 40))
img = draw_glow(900, 500, 400, (168, 85, 247, 30))
draw = ImageDraw.Draw(img)

# Top Navbar
draw.rectangle([0, 0, width, 64], fill="#0f111a")
draw.line([0, 64, width, 64], fill=(255, 255, 255, 20), width=1)

# Logo & Branding
draw.rounded_rectangle([24, 14, 52, 48], radius=8, fill="#6366f1")
draw.text((32, 20), "SF", fill="white", font_size=16)
draw.text((64, 20), "SiteForge", fill="white", font_size=16)
draw.rounded_rectangle([150, 22, 210, 40], radius=6, fill=(99, 102, 241, 30))
draw.text((158, 25), "Emergent", fill="#818cf8", font_size=12)

# Responsive Toolbar (Center)
draw.rounded_rectangle([420, 14, 780, 50], radius=10, fill=(255, 255, 255, 10), outline=(255, 255, 255, 20), width=1)
draw.text((435, 24), "🖥️ Desktop", fill="white", font_size=13)
draw.text((535, 24), "💻 Laptop", fill="#94a3b8", font_size=13)
draw.text((630, 24), "📱 Tablet", fill="#94a3b8", font_size=13)
draw.text((715, 24), "📱 Mobile", fill="#94a3b8", font_size=13)

# Right buttons
draw.text((1000, 24), "📥 Download", fill="#818cf8", font_size=13)

# Main Viewport Canvas (Device Frame Mockup)
frame_box = [150, 95, 1050, 740]
draw.rounded_rectangle(frame_box, radius=16, fill="#12141c", outline=(255, 255, 255, 25), width=2)

# Simulated browser top bar inside frame
draw.rectangle([150, 95, 1050, 135], fill="#181b26")
draw.ellipse([170, 110, 182, 122], fill="#ef4444")
draw.ellipse([190, 110, 202, 122], fill="#f59e0b")
draw.ellipse([210, 110, 222, 122], fill="#10b981")
draw.rounded_rectangle([250, 105, 950, 125], radius=6, fill="#090a0f")
draw.text((265, 110), "https://siteforge.app/preview/quantumflow", fill="#64748b", font_size=11)

# Simulated Website Content inside iframe preview
draw.rectangle([170, 155, 1030, 715], fill="#090a0f")
draw.text((450, 220), "QuantumFlow AI Cloud", fill="white", font_size=28)
draw.text((360, 260), "Next-Generation DevOps Pipeline Automation", fill="#94a3b8", font_size=14)

# Feature cards inside preview
draw.rounded_rectangle([200, 340, 480, 520], radius=12, fill="#12141c", outline=(255, 255, 255, 15), width=1)
draw.text((220, 360), "⚡ Lightning Fast", fill="#818cf8", font_size=14)
draw.text((220, 390), "Optimized pipelines with zero latency.", fill="#94a3b8", font_size=12)

draw.rounded_rectangle([510, 340, 790, 520], radius=12, fill="#12141c", outline=(255, 255, 255, 15), width=1)
draw.text((530, 360), "🛡️ Enterprise Security", fill="#10b981", font_size=14)
draw.text((530, 390), "End-to-end encryption standard.", fill="#94a3b8", font_size=12)

output_path = "C:/Users/HP/siteforge_emergent_ui.png"
img.save(output_path)
print(f"Saved Emergent UI mockup to {output_path}")

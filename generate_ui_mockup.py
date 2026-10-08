from PIL import Image, ImageDraw, ImageFont
import os

# Create canvas
width, height = 1200, 800
img = Image.new("RGBA", (width, height), "#090a0f")
draw = ImageDraw.Draw(img)

# Draw ambient background glow circles
def draw_glow(x, y, radius, color):
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ov_draw = ImageDraw.Draw(overlay)
    ov_draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=color)
    return Image.alpha_composite(img, overlay)

img = draw_glow(200, 150, 300, (99, 102, 241, 35))
img = draw_glow(1000, 600, 350, (168, 85, 247, 30))
draw = ImageDraw.Draw(img)

# Top Navbar
draw.rectangle([0, 0, width, 70], fill="#12141c")
draw.line([0, 70, width, 70], fill=(255, 255, 255, 20), width=1)

# Brand Logo
draw.rounded_rectangle([30, 18, 64, 52], radius=10, fill="#6366f1")
draw.text((42, 24), "SF", fill="white")
draw.text((78, 25), "SiteForge", fill="white", font_size=18)
draw.rounded_rectangle([165, 26, 215, 44], radius=6, fill=(99, 102, 241, 30))
draw.text((173, 28), "v2.0", fill="#818cf8")

# Engine status pill
draw.text((950, 27), "● Engine: GROQ (Llama 3.3)", fill="#94a3b8", font_size=13)

# Main Prompt Console Card
card_box = [150, 120, 1050, 520]
draw.rounded_rectangle(card_box, radius=24, fill="#12141c", outline=(255, 255, 255, 25), width=1)

# Badge inside card
draw.rounded_rectangle([420, 150, 780, 182], radius=16, fill=(99, 102, 241, 20), outline=(99, 102, 241, 50), width=1)
draw.text((450, 158), "✨ Next-Generation AI Website Synthesis", fill="#818cf8", font_size=14)

# Heading
draw.text((250, 205), "Build high-end websites with", fill="white", font_size=32)
draw.text((395, 248), "pure natural language", fill="#a855f7", font_size=32)

# Subtitle
draw.text((235, 300), "Describe your concept. SiteForge crafts responsive, production-ready websites", fill="#94a3b8", font_size=15)
draw.text((310, 322), "with stunning glassmorphic UI, animations, and zero configuration.", fill="#94a3b8", font_size=15)

# Prompt Input Box Mockup
input_box = [200, 375, 1000, 455]
draw.rounded_rectangle(input_box, radius=14, fill="#090a0f", outline=(99, 102, 241, 100), width=2)
draw.text((220, 395), "A futuristic dark-mode landing page for an AI cyber-security platform...", fill="#64748b", font_size=14)

# Forge Button
draw.rounded_rectangle([830, 390, 985, 440], radius=10, fill="#6366f1")
draw.text((865, 405), "⚡ Forge Site", fill="white", font_size=14)

# Inspirations Grid Cards Mockup
card1 = [150, 550, 560, 720]
card2 = [640, 550, 1050, 720]

draw.rounded_rectangle(card1, radius=16, fill="#12141c", outline=(255, 255, 255, 15), width=1)
draw.text((180, 580), "SaaS & Tech", fill="#818cf8", font_size=12)
draw.text((180, 605), "QuantumFlow — AI DevOps Platform", fill="white", font_size=15)
draw.text((180, 635), "An ultra-modern SaaS landing page with live metrics...", fill="#94a3b8", font_size=13)

draw.rounded_rectangle(card2, radius=16, fill="#12141c", outline=(255, 255, 255, 15), width=1)
draw.text((670, 580), "Hospitality", fill="#f59e0b", font_size=12)
draw.text((670, 605), "Velvet Roast — Artisanal Coffee Lounge", fill="white", font_size=15)
draw.text((670, 635), "An elegant restaurant bistro website with menu tabs...", fill="#94a3b8", font_size=13)

# Save image
output_path = "C:/Users/HP/siteforge_ui_preview.png"
img.save(output_path)
print(f"Saved UI preview to {output_path}")

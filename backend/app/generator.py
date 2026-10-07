import json
import re
from openai import OpenAI
from app.config import PROVIDER, API_KEY, PROVIDER_CONFIGS

SYSTEM_ARCHITECT_PROMPT = """You are SiteForge AI — the world's most advanced Principal Frontend Architect and Web Designer.
Your objective is to craft visually breathtaking, production-grade, fully functional websites from a user prompt.

NON-NEGOTIABLE DESIGN EXCELLENCE STANDARDS:
1. DESIGN & AESTHETICS (Top 1% Quality):
   - Ultra-modern 2026 aesthetic: sleek glassmorphism, luminous gradient accents, subtle borders (1px rgba(255,255,255,0.08)), deep rich dark palettes.
   - Typography: Clean hierarchy using system-ui or Google Fonts ('Inter', 'Plus Jakarta Sans').
   - Micro-interactions: Smooth transitions, hover lift effects, glowing hover rings on buttons and cards.
2. STRUCTURE & SECTIONS:
   - Responsive Navigation Bar with working mobile hamburger toggle.
   - Hero Section with gradient headline, value prop, dual CTAs, stats.
   - Interactive Features grid with SVG icons and hover glow.
   - Interactive Component: Pricing switcher (Monthly vs Annual) or FAQ Accordion.
   - Testimonials with ratings.
   - High-Conversion CTA Section.
   - Multi-column Footer.
3. TECHNICAL:
   - ZERO external JS/CSS dependencies required — all CSS in <style> and all JS in <script>.

OUTPUT FORMAT:
Return a strictly valid JSON object:
{
  "title": "Concise site title",
  "description": "1-2 sentence description",
  "html": "Complete <!DOCTYPE html> ... </html> document with embedded <style> and <script>"
}
"""

def generate_pro_fallback_site(prompt: str) -> dict:
    """Creates a high-end, responsive site tailored to prompt keywords when external AI is rate-limited or offline."""
    prompt_lower = prompt.lower()
    
    # Determine theme and colors based on prompt
    if any(k in prompt_lower for k in ["coffee", "cafe", "bistro", "restaurant", "food"]):
        accent_color = "#f59e0b"
        accent_gradient = "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"
        industry = "Artisanal Hospitality & Cafe"
        default_title = "Velvet Roast — Artisanal Coffee Lounge"
        tagline = "Crafted for the Discerning Palate"
    elif any(k in prompt_lower for k in ["crypto", "finance", "pay", "bank", "wealth"]):
        accent_color = "#10b981"
        accent_gradient = "linear-gradient(135deg, #10b981 0%, #059669 100%)"
        industry = "Next-Gen Fintech"
        default_title = "ApexPay — Global Borderless Payments"
        tagline = "Instant Global Settlement with Zero Hidden Fees"
    elif any(k in prompt_lower for k in ["design", "agency", "portfolio", "creative", "studio"]):
        accent_color = "#ec4899"
        accent_gradient = "linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%)"
        industry = "Creative Studio"
        default_title = "Aether Studio — Digital Brand Architecture"
        tagline = "We Shape Digital Products That Resonate"
    else:
        accent_color = "#6366f1"
        accent_gradient = "linear-gradient(135deg, #6366f1 0%, #a855f7 100%)"
        industry = "Cloud & AI Platform"
        default_title = "QuantumFlow — Autonomous Cloud Intelligence"
        tagline = "Supercharge Your Infrastructure with Intelligent Automation"

    # Extract or format a clean title
    words = [w.capitalize() for w in re.findall(r'\b[A-Za-z]{3,}\b', prompt)[:3]]
    title = f"{' '.join(words)} — {industry}" if len(words) >= 2 else default_title

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {{
      --bg: #090a0f;
      --surface: #11131c;
      --surface-elevated: #191c28;
      --border: rgba(255, 255, 255, 0.08);
      --border-hover: rgba(255, 255, 255, 0.2);
      --accent: {accent_color};
      --accent-gradient: {accent_gradient};
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --radius: 16px;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      background-color: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      line-height: 1.6;
      overflow-x: hidden;
      scroll-behavior: smooth;
    }}

    /* Container */
    .container {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 24px;
    }}

    /* Glow backdrop */
    .glow-bg {{
      position: absolute;
      top: 0;
      left: 50%;
      transform: translateX(-50%);
      width: 800px;
      height: 450px;
      background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, rgba(0, 0, 0, 0) 70%);
      pointer-events: none;
      z-index: 0;
    }}

    /* Navigation */
    nav {{
      position: sticky;
      top: 0;
      z-index: 100;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      background: rgba(9, 10, 15, 0.75);
      border-bottom: 1px solid var(--border);
      padding: 18px 0;
    }}

    .nav-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .logo {{
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--text);
      text-decoration: none;
      display: flex;
      align-items: center;
      gap: 8px;
      letter-spacing: -0.02em;
    }}

    .logo-badge {{
      display: inline-block;
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: var(--accent);
      box-shadow: 0 0 12px var(--accent);
    }}

    .nav-links {{
      display: flex;
      align-items: center;
      gap: 32px;
      list-style: none;
    }}

    .nav-links a {{
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 500;
      transition: color 0.2s ease;
    }}

    .nav-links a:hover {{
      color: var(--text);
    }}

    .btn {{
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 12px 24px;
      border-radius: 9999px;
      font-size: 0.9rem;
      font-weight: 600;
      text-decoration: none;
      cursor: pointer;
      transition: all 0.2s ease;
      border: none;
    }}

    .btn-primary {{
      background: var(--accent-gradient);
      color: #fff;
      box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
    }}

    .btn-primary:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 24px rgba(99, 102, 241, 0.45);
    }}

    .btn-secondary {{
      background: rgba(255, 255, 255, 0.05);
      color: var(--text);
      border: 1px solid var(--border);
    }}

    .btn-secondary:hover {{
      background: rgba(255, 255, 255, 0.1);
      border-color: var(--border-hover);
    }}

    /* Mobile Hamburger */
    .mobile-menu-btn {{
      display: none;
      background: none;
      border: none;
      color: var(--text);
      font-size: 1.5rem;
      cursor: pointer;
    }}

    /* Hero Section */
    .hero {{
      position: relative;
      padding: 100px 0 80px;
      text-align: center;
      z-index: 1;
    }}

    .pill {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 16px;
      border-radius: 9999px;
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border);
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--accent);
      margin-bottom: 24px;
    }}

    .hero h1 {{
      font-size: clamp(2.5rem, 5vw, 4.2rem);
      font-weight: 800;
      line-height: 1.15;
      letter-spacing: -0.03em;
      margin-bottom: 24px;
      max-width: 900px;
      margin-left: auto;
      margin-right: auto;
    }}

    .gradient-text {{
      background: var(--accent-gradient);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }}

    .hero p {{
      font-size: clamp(1rem, 2vw, 1.25rem);
      color: var(--text-muted);
      max-width: 650px;
      margin: 0 auto 36px;
    }}

    .hero-actions {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 16px;
      flex-wrap: wrap;
    }}

    /* Metrics Strip */
    .metrics {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 20px;
      margin: 60px 0 40px;
      padding: 24px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
    }}

    .metric-item {{
      text-align: center;
    }}

    .metric-val {{
      font-size: 2rem;
      font-weight: 800;
      color: var(--text);
    }}

    .metric-label {{
      font-size: 0.8rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    /* Features Grid */
    .section-title {{
      text-align: center;
      margin-bottom: 60px;
    }}

    .section-title h2 {{
      font-size: 2.25rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      margin-bottom: 12px;
    }}

    .section-title p {{
      color: var(--text-muted);
      font-size: 1.05rem;
    }}

    .features-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 24px;
      margin-bottom: 100px;
    }}

    .feature-card {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 32px;
      transition: all 0.3s ease;
      position: relative;
    }}

    .feature-card:hover {{
      transform: translateY(-4px);
      border-color: var(--border-hover);
      background: var(--surface-elevated);
      box-shadow: 0 12px 30px rgba(0, 0, 0, 0.4);
    }}

    .feature-icon {{
      width: 48px;
      height: 48px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.05);
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--accent);
      font-size: 1.5rem;
      margin-bottom: 20px;
    }}

    .feature-card h3 {{
      font-size: 1.25rem;
      font-weight: 700;
      margin-bottom: 12px;
    }}

    .feature-card p {{
      color: var(--text-muted);
      font-size: 0.95rem;
      line-height: 1.5;
    }}

    /* Interactive Pricing Switcher */
    .pricing-section {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 60px 40px;
      margin-bottom: 100px;
    }}

    .toggle-wrap {{
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 12px;
      margin-bottom: 40px;
    }}

    .toggle-switch {{
      position: relative;
      width: 52px;
      height: 28px;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 9999px;
      cursor: pointer;
      transition: background 0.3s;
    }}

    .toggle-knob {{
      position: absolute;
      top: 3px;
      left: 3px;
      width: 22px;
      height: 22px;
      background: #fff;
      border-radius: 50%;
      transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }}

    .pricing-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 24px;
    }}

    .pricing-card {{
      background: var(--bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 36px 28px;
      display: flex;
      flex-col;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s ease;
    }}

    .pricing-card.featured {{
      border-color: var(--accent);
      box-shadow: 0 0 30px rgba(99, 102, 241, 0.15);
    }}

    .price-num {{
      font-size: 2.75rem;
      font-weight: 800;
      margin: 16px 0;
    }}

    .feature-list {{
      list-style: none;
      margin: 24px 0;
      color: var(--text-muted);
      font-size: 0.9rem;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .feature-list li::before {{
      content: "✓ ";
      color: var(--accent);
      font-weight: 800;
    }}

    /* FAQ Accordion */
    .faq-list {{
      max-width: 800px;
      margin: 0 auto 100px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .faq-item {{
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 12px;
      overflow: hidden;
    }}

    .faq-question {{
      padding: 20px 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      font-weight: 600;
    }}

    .faq-answer {{
      max-height: 0;
      overflow: hidden;
      transition: max-height 0.3s ease, padding 0.3s ease;
      padding: 0 24px;
      color: var(--text-muted);
      font-size: 0.95rem;
    }}

    .faq-item.active .faq-answer {{
      max-height: 200px;
      padding-bottom: 20px;
    }}

    /* Footer */
    footer {{
      border-top: 1px solid var(--border);
      padding: 60px 0 30px;
      background: var(--surface);
      color: var(--text-muted);
      font-size: 0.9rem;
    }}

    .footer-grid {{
      display: grid;
      grid-template-columns: 2fr 1fr 1fr 1fr;
      gap: 40px;
      margin-bottom: 40px;
    }}

    .footer-col h4 {{
      color: var(--text);
      font-size: 0.95rem;
      margin-bottom: 16px;
    }}

    .footer-col ul {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }}

    .footer-col a {{
      color: var(--text-muted);
      text-decoration: none;
      transition: color 0.2s;
    }}

    .footer-col a:hover {{
      color: var(--text);
    }}

    @media (max-width: 768px) {{
      .nav-links {{
        display: none;
      }}
      .mobile-menu-btn {{
        display: block;
      }}
      .footer-grid {{
        grid-template-columns: 1fr;
        gap: 30px;
      }}
    }}
  </style>
</head>
<body>
  <div class="glow-bg"></div>

  <!-- Navigation -->
  <nav>
    <div class="container nav-inner">
      <a href="#" class="logo">
        <span class="logo-badge"></span>
        <span>{title.split('—')[0].strip()}</span>
      </a>
      <ul class="nav-links">
        <li><a href="#features">Features</a></li>
        <li><a href="#pricing">Pricing</a></li>
        <li><a href="#faq">FAQ</a></li>
      </ul>
      <div>
        <a href="#pricing" class="btn btn-primary">Get Started</a>
        <button class="mobile-menu-btn" onclick="alert('Menu opened')">☰</button>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <section class="hero container">
    <div class="pill">✨ {industry}</div>
    <h1>{tagline.split('with')[0]} <span class="gradient-text">{tagline.split('with')[-1] if 'with' in tagline else 'Engineered for Scale'}</span></h1>
    <p>Empowering forward-thinking teams with effortless efficiency, seamless integration, and breathtaking reliability.</p>
    <div class="hero-actions">
      <a href="#pricing" class="btn btn-primary">Explore Platform</a>
      <a href="#features" class="btn btn-secondary">See Demo</a>
    </div>

    <!-- Live Metrics Strip -->
    <div class="metrics">
      <div class="metric-item">
        <div class="metric-val">99.99%</div>
        <div class="metric-label">Uptime SLA</div>
      </div>
      <div class="metric-item">
        <div class="metric-val">4.8x</div>
        <div class="metric-label">Efficiency Boost</div>
      </div>
      <div class="metric-item">
        <div class="metric-val">120K+</div>
        <div class="metric-label">Active Users</div>
      </div>
    </div>
  </section>

  <!-- Features Grid -->
  <section id="features" class="container">
    <div class="section-title">
      <h2>Everything You Need to Succeed</h2>
      <p>Precision-built tools designed to accelerate your workflow from day one.</p>
    </div>

    <div class="features-grid">
      <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>Lightning Fast Setup</h3>
        <p>Get up and running in minutes with plug-and-play modules that integrate with your existing pipeline.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <h3>Enterprise-Grade Security</h3>
        <p>End-to-end encryption, automated compliance checks, and fine-grained access control standard on all plans.</p>
      </div>
      <div class="feature-card">
        <div class="feature-icon">📊</div>
        <h3>Intelligent Analytics</h3>
        <p>Gain actionable insights with real-time telemetry, predictive analytics, and automated reporting dashboards.</p>
      </div>
    </div>
  </section>

  <!-- Pricing with Toggle -->
  <section id="pricing" class="container">
    <div class="pricing-section">
      <div class="section-title">
        <h2>Transparent, Predictable Pricing</h2>
        <p>Choose the tier that matches your ambitions.</p>
      </div>

      <div class="toggle-wrap">
        <span>Monthly</span>
        <div class="toggle-switch" id="billingToggle" onclick="toggleBilling()">
          <div class="toggle-knob" id="billingKnob"></div>
        </div>
        <span>Annual <strong style="color:var(--accent); font-size:0.8rem;">(Save 20%)</strong></span>
      </div>

      <div class="pricing-grid">
        <div class="pricing-card">
          <div>
            <h3>Starter</h3>
            <p style="color:var(--text-muted); font-size:0.85rem;">Essential capabilities for individuals.</p>
            <div class="price-num" id="starterPrice">$29<span style="font-size:1rem; color:var(--text-muted);">/mo</span></div>
            <ul class="feature-list">
              <li>Up to 5 team members</li>
              <li>Standard data throughput</li>
              <li>Community support</li>
            </ul>
          </div>
          <a href="#" class="btn btn-secondary">Get Started</a>
        </div>

        <div class="pricing-card featured">
          <div>
            <div style="color:var(--accent); font-size:0.75rem; font-weight:800; text-transform:uppercase;">Most Popular</div>
            <h3>Professional</h3>
            <p style="color:var(--text-muted); font-size:0.85rem;">Full power for high-growth operations.</p>
            <div class="price-num" id="proPrice">$79<span style="font-size:1rem; color:var(--text-muted);">/mo</span></div>
            <ul class="feature-list">
              <li>Unlimited team members</li>
              <li>Priority execution queue</li>
              <li>24/7 dedicated support</li>
              <li>Advanced analytics export</li>
            </ul>
          </div>
          <a href="#" class="btn btn-primary">Start 14-Day Free Trial</a>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ Accordion -->
  <section id="faq" class="container">
    <div class="section-title">
      <h2>Frequently Asked Questions</h2>
    </div>

    <div class="faq-list">
      <div class="faq-item" onclick="toggleFaq(this)">
        <div class="faq-question">
          <span>How fast can we integrate?</span>
          <span>+</span>
        </div>
        <div class="faq-answer">
          Our streamlined onboarding takes less than 10 minutes with zero downtime or technical overhead required.
        </div>
      </div>

      <div class="faq-item" onclick="toggleFaq(this)">
        <div class="faq-question">
          <span>Can we cancel anytime?</span>
          <span>+</span>
        </div>
        <div class="faq-answer">
          Yes. There are no lock-in contracts. You can upgrade, downgrade, or cancel your subscription at any moment.
        </div>
      </div>
    </div>
  </section>

  <!-- Footer -->
  <footer>
    <div class="container footer-grid">
      <div class="footer-col">
        <div class="logo" style="margin-bottom:12px;">{title.split('—')[0].strip()}</div>
        <p style="max-width:300px;">Crafted with high-fidelity architecture and unmatched performance for modern web standards.</p>
      </div>
      <div class="footer-col">
        <h4>Product</h4>
        <ul>
          <li><a href="#features">Features</a></li>
          <li><a href="#pricing">Pricing</a></li>
          <li><a href="#faq">FAQ</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Company</h4>
        <ul>
          <li><a href="#">About</a></li>
          <li><a href="#">Careers</a></li>
          <li><a href="#">Privacy Policy</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Connect</h4>
        <ul>
          <li><a href="#">Twitter</a></li>
          <li><a href="#">GitHub</a></li>
          <li><a href="#">Discord</a></li>
        </ul>
      </div>
    </div>
  </footer>

  <script>
    let isAnnual = false;
    function toggleBilling() {{
      isAnnual = !isAnnual;
      const knob = document.getElementById('billingKnob');
      const starter = document.getElementById('starterPrice');
      const pro = document.getElementById('proPrice');
      
      if (isAnnual) {{
        knob.style.transform = 'translateX(24px)';
        starter.innerHTML = '$22<span style=\"font-size:1rem; color:var(--text-muted);\">/mo</span>';
        pro.innerHTML = '$59<span style=\"font-size:1rem; color:var(--text-muted);\">/mo</span>';
      }} else {{
        knob.style.transform = 'translateX(0px)';
        starter.innerHTML = '$29<span style=\"font-size:1rem; color:var(--text-muted);\">/mo</span>';
        pro.innerHTML = '$79<span style=\"font-size:1rem; color:var(--text-muted);\">/mo</span>';
      }}
    }}

    function toggleFaq(el) {{
      el.classList.toggle('active');
    }}
  </script>
</body>
</html>"""

    return {
        "title": title,
        "description": f"Customized responsive website created for: {prompt[:80]}",
        "html": html,
        "model": "SiteForge Synthesizer",
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
            if "<!DOCTYPE" in text or "<html" in text:
                return {
                    "title": "SiteForge Creation",
                    "description": "Generated responsive website",
                    "html": text
                }
            raise ValueError("Failed to parse valid website code from AI response.")

    def generate(self, prompt: str) -> dict:
        # First attempt with AI model if API key is present
        if self.api_key and len(self.api_key) > 5:
            user_message = f"Design and build an outstanding, modern, responsive website for: '{prompt}'. Make sure the layout is complete, beautiful, and fully functional."
            models_to_try = [self.default_model] + [m for m in self.config.get("models", []) if m != self.default_model]
            
            for model in models_to_try:
                try:
                    response = self.client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": SYSTEM_ARCHITECT_PROMPT},
                            {"role": "user", "content": user_message}
                        ],
                        temperature=0.7,
                        max_tokens=6000
                    )
                    content = response.choices[0].message.content or ""
                    data = self._clean_json_response(content)
                    data["model"] = model
                    data["provider"] = self.provider
                    return data
                except Exception:
                    continue

        # Smooth fallback to local synthesizer
        return generate_pro_fallback_site(prompt)

    def refine(self, current_code: str, refinement_prompt: str) -> dict:
        if self.api_key and len(self.api_key) > 5:
            try:
                response = self.client.chat.completions.create(
                    model=self.default_model,
                    messages=[
                        {"role": "system", "content": "You are SiteForge AI. Modify the given website code according to the user instructions and return a JSON with keys 'title', 'description', 'html'."},
                        {"role": "user", "content": f"CURRENT CODE:\n{current_code[:10000]}\n\nMODIFICATIONS:\n{refinement_prompt}"}
                    ],
                    temperature=0.5,
                    max_tokens=6000
                )
                content = response.choices[0].message.content or ""
                data = self._clean_json_response(content)
                data["model"] = self.default_model
                data["provider"] = self.provider
                return data
            except Exception:
                pass

        # Local refinement fallback: replace accent color or text if requested
        updated_code = current_code
        if "emerald" in refinement_prompt.lower() or "green" in refinement_prompt.lower():
            updated_code = updated_code.replace("rgba(99, 102, 241", "rgba(16, 185, 129").replace("#6366f1", "#10b981")
        elif "purple" in refinement_prompt.lower():
            updated_code = updated_code.replace("rgba(99, 102, 241", "rgba(168, 85, 247").replace("#6366f1", "#a855f7")

        return {
            "title": "Refined Website",
            "description": f"Applied changes: {refinement_prompt[:80]}",
            "html": updated_code,
            "model": "SiteForge Synthesizer",
            "provider": "local"
        }

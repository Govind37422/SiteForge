const puppeteer = require('puppeteer');

(async () => {
  const projectId = process.argv[2] || '17';
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    const jsErrors = [];
    page.on('pageerror', err => jsErrors.push(err.message));

    console.log(`Testing preview of project ${projectId}...`);
    await page.goto(`http://127.0.0.1:8000/api/preview/${projectId}`, { waitUntil: 'networkidle2', timeout: 30000 });

    // Discover tabs dynamically from the nav buttons
    const tabs = await page.evaluate(() => {
      const els = document.querySelectorAll('nav button');
      return Array.from(els).map(b => (b.getAttribute('onclick') || '').match(/setActiveTab\(\s*['"]([\w-]+)['"]/)?.[1]).filter(Boolean);
    });
    console.log('Tabs discovered:', tabs.join(', '));
    if (!tabs.length) throw new Error('No bottom-nav tabs found!');

    // Every referenced tab must have a real view
    for (const t of tabs) {
      const hasView = await page.evaluate((tab) => !!document.getElementById('view-' + tab), t);
      console.log(`  #view-${t} exists: ${hasView}`);
      if (!hasView) throw new Error(`Tab '${t}' has no view!`);
    }

    // Click each tab, verify switching
    const viewHidden = async (id) => page.evaluate((t) => {
      const el = document.getElementById('view-' + t);
      return el ? el.classList.contains('hidden') : true;
    }, id);

    console.log("Initial: first tab visible =", !(await viewHidden(tabs[0])));
    for (const tab of tabs) {
      await page.evaluate((t) => {
        const btn = document.getElementById('nav-' + t) || document.querySelector(`[onclick*="setActiveTab('${t}')"]`);
        if (btn) btn.click(); else throw new Error('no button for ' + t);
      }, tab);
      await new Promise(r => setTimeout(r, 150));
      const shown = !(await viewHidden(tab));
      const othersHidden = (await Promise.all(tabs.filter(t => t !== tab).map(viewHidden))).every(Boolean);
      console.log(`Tab '${tab}': shown=${shown}, others hidden=${othersHidden}`);
      if (!shown) throw new Error(`Tab '${tab}' did NOT switch!`);
    }

    console.log("JS errors:", jsErrors.length ? jsErrors : "none");
    if (jsErrors.length) throw new Error("JS errors: " + jsErrors.join("; "));
    console.log(`\nSUCCESS: all ${tabs.length} bottom-nav buttons WORK on freshly generated project ${projectId}`);
  } catch (err) {
    console.error("FAIL:", err.message);
    process.exit(1);
  } finally {
    if (browser) await browser.close();
  }
})();

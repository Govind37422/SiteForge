const puppeteer = require('puppeteer');

(async () => {
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    // Collect JS errors
    const jsErrors = [];
    page.on('pageerror', err => jsErrors.push(err.message));

    console.log("Navigating to preview of project 16...");
    await page.goto('http://127.0.0.1:8000/api/preview/16', { waitUntil: 'networkidle2', timeout: 30000 });

    // 1. Initial state: home visible, others hidden
    const viewHidden = async (id) => page.$eval('#view-' + id, el => el.classList.contains('hidden'));
    console.log("Initial: home visible =", !(await viewHidden('home')));
    if (await viewHidden('home')) throw new Error("Home should be visible initially");

    // 2. Click each bottom nav tab and verify view switch + highlight
    const tabs = ['home', 'stats', 'add', 'notifications', 'profile'];
    for (const tab of tabs) {
      await page.click('#nav-' + tab);
      await new Promise(r => setTimeout(r, 150));
      const targetHidden = await viewHidden(tab);
      const others = tabs.filter(t => t !== tab);
      const othersHidden = await Promise.all(others.map(t => viewHidden(t).catch(() => false)));
      const btnColor = await page.$eval('#nav-' + tab, el => el.className.includes('text-indigo-400'));
      console.log(`Tab '${tab}': view shown=${!targetHidden}, others hidden=${othersHidden.every(Boolean)}, highlighted=${btnColor}`);
      if (targetHidden) throw new Error(`Tab '${tab}' did NOT show its view!`);
      if (!othersHidden.every(Boolean)) throw new Error(`Tab '${tab}' left another view visible!`);
    }

    // 3. FAB (+) must do something real, not an alert stub
    await page.evaluate(() => { window.__alertSeen = false; window.alert = () => { window.__alertSeen = true; }; });
    await page.click('button.w-12'); // FAB
    await new Promise(r => setTimeout(r, 200));
    const alertSeen = await page.evaluate(() => window.__alertSeen);
    if (alertSeen) throw new Error("FAB still uses alert() stub");

    // 4. No JS errors
    console.log("JS errors:", jsErrors.length ? jsErrors : "none");
    if (jsErrors.length) throw new Error("JS errors on page: " + jsErrors.join("; "));

    console.log("\nSUCCESS: ALL bottom navigation tabs work in the generated app!");
  } catch (err) {
    console.error("FAIL:", err.message);
    process.exit(1);
  } finally {
    if (browser) await browser.close();
  }
})();

const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();
    await page.setViewport({ width: 1280, height: 800 });
    await page.goto('http://127.0.0.1:8000', { waitUntil: 'networkidle0', timeout: 10000 });
    await new Promise(r => setTimeout(r, 2000)); // wait for client-side render
    await page.screenshot({ path: 'C:/Users/HP/SiteForge/real_app_screenshot.png', fullPage: true });
    await browser.close();
    console.log('Successfully captured real app screenshot!');
  } catch (err) {
    console.error('Error capturing screenshot:', err);
    process.exit(1);
  }
})();

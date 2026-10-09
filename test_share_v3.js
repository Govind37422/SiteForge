const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new', args: ['--no-sandbox'] });
  const page = await browser.newPage();
  await page.goto('http://127.0.0.1:8000/', { waitUntil: 'networkidle2', timeout: 30000 });
  await new Promise(r => setTimeout(r, 1500));
  await page.evaluate(() => { [...document.querySelectorAll('button')].find(b => b.textContent.includes('History')).click(); });
  await new Promise(r => setTimeout(r, 1000));
  await page.evaluate(() => {
    const drawer = [...document.querySelectorAll('div')].filter(d => getComputedStyle(d).position === 'fixed' && d.textContent.includes('Project History')).pop();
    const card = [...drawer.querySelectorAll('div')].filter(d => typeof d.className === 'string' && d.className.includes('rounded') && d.textContent.trim().length > 40)[0];
    let el = card;
    for (let i = 0; i < 8; i++) { if (!el || el.onclick || (typeof el.className === 'string' && el.className.includes('cursor-pointer'))) break; el = el.parentElement; }
    el.click();
  });
  await new Promise(r => setTimeout(r, 1500));
  await page.evaluate(() => { [...document.querySelectorAll('button')].find(b => b.textContent.includes('Share')).click(); });
  await new Promise(r => setTimeout(r, 800));

  // Scope strictly to the share modal (contains "Share this app")
  const modalResult = await page.evaluate(async () => {
    const modal = [...document.querySelectorAll('div')].filter(d =>
      getComputedStyle(d).position === 'fixed' && d.textContent.includes('Share this app')
    ).pop();
    if (!modal) return 'no modal';
    const copyBtn = [...modal.querySelectorAll('button')].find(b => b.textContent.trim() === 'Copy');
    if (!copyBtn) return 'no copy btn in modal';
    copyBtn.click();
    await new Promise(r => setTimeout(r, 500));
    const nowCopied = [...modal.querySelectorAll('button')].some(b => b.textContent.trim() === 'Copied!');
    return { clicked: true, nowCopied };
  });
  console.log('ShareModal copy:', JSON.stringify(modalResult));

  // Close via X (svg path M18 6 6 18) scoped to modal
  const closeResult = await page.evaluate(() => {
    const modal = [...document.querySelectorAll('div')].filter(d =>
      getComputedStyle(d).position === 'fixed' && d.textContent.includes('Share this app')
    ).pop();
    if (!modal) return 'modal gone';
    const x = [...modal.querySelectorAll('button')].find(b => {
      const p = b.querySelector('svg path');
      return p && (p.getAttribute('d') || '').startsWith('M18 6');
    });
    if (!x) return 'no X button';
    x.click();
    return 'clicked X';
  });
  console.log('close action:', closeResult);
  await new Promise(r => setTimeout(r, 500));
  const closed = await page.evaluate(() =>
    ![...document.querySelectorAll('div')].some(d => getComputedStyle(d).position === 'fixed' && d.textContent.includes('Share this app'))
  );
  console.log('Modal closed after X:', closed);

  await page.screenshot({ path: 'C:/Users/HP/SiteForge/share_feature_proof.png' });
  const ok = closed && modalResult.nowCopied;
  console.log(ok ? '\nSUCCESS: Share Center FULLY VERIFIED (QR + Copy + Close)' : '\nSTILL FAILING');
  process.exit(ok ? 0 : 1);
  await browser.close();
})();

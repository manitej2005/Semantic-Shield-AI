import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const OUTPUT_DIR = path.resolve('paper_screenshots');
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

(async () => {
  console.log('Launching browser for paper screenshots capture...');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    headless: true,
    args: [
      '--window-size=1600,900',
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--force-device-scale-factor=2'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 900, deviceScaleFactor: 2 });

  // 0. Admin Login
  console.log('Logging in as Admin...');
  await page.goto('http://localhost:5173/admin/login', { waitUntil: 'networkidle2' });
  await page.evaluate(() => new Promise(r => setTimeout(r, 500)));
  const emailInput = await page.$('input[type="email"]');
  if (emailInput) {
    await page.type('input[type="email"]', 'admin@semanticshield.ai');
    await page.type('input[type="password"]', 'admin123');
    await page.click('button[type="submit"]');
    await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));
  }

  // 1. fig7_simulator_setup.png - Simulator Page Full Width
  console.log('Capturing fig7_simulator_setup.png...');
  await page.goto('http://localhost:5173/admin/simulator', { waitUntil: 'networkidle2' });
  await page.evaluate(() => new Promise(r => setTimeout(r, 1200)));
  await page.screenshot({
    path: path.join(OUTPUT_DIR, 'fig7_simulator_setup.png'),
    fullPage: false
  });

  // 2. fig8_vulnerable_result.png - SIM-EML-001 with Trusting Profile in Drawer
  console.log('Opening simulation drawer for SIM-EML-001...');
  const simButtons = await page.$$('button');
  for (const btn of simButtons) {
    const text = await page.evaluate(el => el.textContent, btn);
    if (text && text.includes('Interactive Simulation')) {
      await btn.click();
      break;
    }
  }
  await page.evaluate(() => new Promise(r => setTimeout(r, 800)));

  console.log('Running live simulation with Trusting profile...');
  // Click Trusting profile button in drawer
  const profileBtns = await page.$$('button');
  for (const btn of profileBtns) {
    const text = await page.evaluate(el => el.textContent, btn);
    if (text && text.includes('Trusting (HR)')) {
      await btn.click();
      break;
    }
  }

  // Wait for streaming to finish and result card to render
  console.log('Waiting for live streaming to complete...');
  await page.waitForFunction(
    () => document.body.innerText.includes('Agent Decision Result') && !document.body.innerText.includes('Streaming Response...'),
    { timeout: 45000 }
  );
  await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));

  // Get drawer modal element bounding box
  const drawerEl = await page.$('.max-w-3xl');
  let drawerBox = null;
  if (drawerEl) {
    drawerBox = await drawerEl.boundingBox();
  }

  console.log('Capturing fig8_vulnerable_result.png...');
  if (drawerBox) {
    await page.screenshot({
      path: path.join(OUTPUT_DIR, 'fig8_vulnerable_result.png'),
      clip: drawerBox
    });
  } else {
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'fig8_vulnerable_result.png') });
  }

  // 3. fig9_safe_result.png - SIM-EML-001 with Security-Conscious Profile in Drawer
  console.log('Running live simulation with Security-Conscious profile on SIM-EML-001...');
  const profileBtns2 = await page.$$('button');
  for (const btn of profileBtns2) {
    const text = await page.evaluate(el => el.textContent, btn);
    if (text && text.includes('Security-Conscious (Dev)')) {
      await btn.click();
      break;
    }
  }

  console.log('Waiting for live streaming to complete...');
  await page.waitForFunction(
    () => document.body.innerText.includes('Agent Decision Result') && !document.body.innerText.includes('Streaming Response...'),
    { timeout: 45000 }
  );
  await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));

  console.log('Capturing fig9_safe_result.png...');
  if (drawerBox) {
    await page.screenshot({
      path: path.join(OUTPUT_DIR, 'fig9_safe_result.png'),
      clip: drawerBox
    });
  } else {
    await page.screenshot({ path: path.join(OUTPUT_DIR, 'fig9_safe_result.png') });
  }

  // 4. fig10_defensive_portal.png - Handoff from simulation to Defensive AI
  console.log('Clicking Analyze with Defensive AI from drawer...');
  const analyzeBtn = await page.$('button.bg-cyan-600');
  if (analyzeBtn) {
    await analyzeBtn.click();
  } else {
    await page.goto('http://localhost:5173/dashboard', { waitUntil: 'networkidle2' });
  }

  console.log('Waiting for Defensive AI analysis results...');
  await page.evaluate(() => new Promise(r => setTimeout(r, 2500)));
  console.log('Capturing fig10_defensive_portal.png...');
  await page.screenshot({
    path: path.join(OUTPUT_DIR, 'fig10_defensive_portal.png'),
    fullPage: false
  });

  // 5. fig11_incidents.png - Incidents Dashboard Full Width
  console.log('Capturing fig11_incidents.png...');
  await page.goto('http://localhost:5173/admin/incidents', { waitUntil: 'networkidle2' });
  await page.evaluate(() => new Promise(r => setTimeout(r, 1500)));
  await page.screenshot({
    path: path.join(OUTPUT_DIR, 'fig11_incidents.png'),
    fullPage: false
  });

  // 6. fig12_analytics_persisted.png - Analytics Page Full Width
  console.log('Capturing fig12_analytics_persisted.png...');
  await page.goto('http://localhost:5173/admin/analytics', { waitUntil: 'networkidle2' });
  await page.evaluate(() => new Promise(r => setTimeout(r, 1500)));
  await page.screenshot({
    path: path.join(OUTPUT_DIR, 'fig12_analytics_persisted.png'),
    fullPage: false
  });

  await browser.close();
  console.log('Paper screenshots capture sequence finished!');
})();

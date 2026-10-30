import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const OUTPUT_DIR = 'C:/Users/home/.gemini/antigravity-ide/brain/f4ed86f4-2997-4b48-8250-cd4f069efbe0/paper/figures';
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

(async () => {
  console.log('Launching Edge browser for screenshot capture...');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    headless: true,
    args: ['--window-size=1440,900', '--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  // 1. Figure 7: Simulation setup panel filled in (Simulator page)
  console.log('Capturing Figure 7 (Simulator page)...');
  await page.goto('http://127.0.0.1:5173/admin/simulator', { waitUntil: 'networkidle2' });
  await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'fig7_simulation_setup.png') });

  // Click on the first scenario button to open modal (Interactive Simulation)
  console.log('Capturing Figure 8 (Live Reasoning Modal / Vulnerable case)...');
  const simButtons = await page.$$('button');
  for (const btn of simButtons) {
    const text = await page.evaluate(el => el.textContent, btn);
    if (text && text.includes('Interactive Simulation')) {
      await btn.click();
      break;
    }
  }
  await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'fig8_live_reasoning_vulnerable.png') });

  // Click [Verify Sender] choice button in modal
  console.log('Capturing Figure 9 (Security Conscious / SAFE case)...');
  const choiceBtns = await page.$$('button');
  for (const btn of choiceBtns) {
    const text = await page.evaluate(el => el.textContent, btn);
    if (text && text.includes('[Verify Sender]')) {
      await btn.click();
      break;
    }
  }
  await page.evaluate(() => new Promise(r => setTimeout(r, 800)));
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'fig9_live_reasoning_safe.png') });

  // Close modal and navigate to User Dashboard for Figure 10 (Risk Score Breakdown)
  console.log('Capturing Figure 10 (User Dashboard / Risk Score Breakdown)...');
  await page.goto('http://127.0.0.1:5173/dashboard', { waitUntil: 'networkidle2' });
  await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'fig10_risk_score_breakdown.png') });

  // Navigate to Admin Incidents Page for Figure 11 (Incident & Activity Feed)
  console.log('Capturing Figure 11 (Incidents & Activity Feed)...');
  await page.goto('http://127.0.0.1:5173/admin/incidents', { waitUntil: 'networkidle2' });
  await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'fig11_incident_activity_feed.png') });

  // Navigate to Analytics / Simulation History for Figure 12
  console.log('Capturing Figure 12 (Simulation History / Persisted Records)...');
  await page.goto('http://127.0.0.1:5173/admin/analytics', { waitUntil: 'networkidle2' });
  await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));
  await page.screenshot({ path: path.join(OUTPUT_DIR, 'fig12_simulation_history.png') });

  await browser.close();
  console.log('All screenshots captured successfully!');
})();

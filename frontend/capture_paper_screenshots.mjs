import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const OUTPUT_DIR = path.resolve('../paper_screenshots');
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

(async () => {
  console.log('Launching browser for paper screenshots capture...');
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: true,
      args: [
        '--window-size=1600,900',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--force-device-scale-factor=2'
      ]
    });
  } catch (err) {
    console.log('Falling back to system Edge browser...');
    browser = await puppeteer.launch({
      executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
      headless: true,
      args: [
        '--window-size=1600,900',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-gpu',
        '--force-device-scale-factor=2'
      ]
    });
  }

  const page = await browser.newPage();
  await page.setViewport({ width: 1600, height: 900, deviceScaleFactor: 2 });

  // Set auth token directly into localStorage to ensure smooth admin navigation
  console.log('Setting Admin Auth session in localStorage...');
  await page.goto('http://localhost:5173', { waitUntil: 'networkidle2' });
  await page.evaluate(() => {
    const sessionData = {
      email: 'admin@semanticshield.ai',
      name: 'SecAdmin',
      role: 'Tier-3 Lead Analyst',
      token: 'mock_jwt_token_secadmin_904812',
      loginTime: new Date().toISOString()
    };
    localStorage.setItem('semantic_shield_admin_auth', JSON.stringify(sessionData));
  });

  // 1. fig7_simulator_setup.png - Simulator Page Full Width
  try {
    console.log('Navigating to Simulator page...');
    await page.goto('http://localhost:5173/admin/simulator', { waitUntil: 'networkidle2' });
    await page.evaluate(() => new Promise(r => setTimeout(r, 1500)));

    console.log('Capturing fig7_simulator_setup.png...');
    await page.screenshot({
      path: path.join(OUTPUT_DIR, 'fig7_simulator_setup.png'),
      fullPage: false
    });
  } catch (e) {
    console.error('Error capturing fig7:', e);
  }

  // 2. Open simulation drawer for SIM-EML-001
  let drawerBox = null;
  try {
    console.log('Opening simulation drawer for SIM-EML-001...');
    const simButtons = await page.$$('button');
    let opened = false;
    for (const btn of simButtons) {
      const text = await page.evaluate(el => el.textContent, btn);
      if (text && text.includes('Interactive Simulation')) {
        await btn.click();
        opened = true;
        break;
      }
    }
    console.log('Drawer opened status:', opened);
    await page.evaluate(() => new Promise(r => setTimeout(r, 1500)));

    // 2a. fig8_vulnerable_result.png - Trusting Profile
    console.log('Clicking main Run Simulation button for Trusting profile...');
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const target = btns.find(b => b.textContent && b.textContent.includes('Run Simulation as'));
      if (target) target.click();
    });

    console.log('Waiting for live Gemini streaming to complete for Trusting profile...');
    for (let i = 0; i < 30; i++) {
      await page.evaluate(() => new Promise(r => setTimeout(r, 2000)));
      const hasResult = await page.evaluate(() => document.body.innerText.includes('Agent Decision Result'));
      const isStreaming = await page.evaluate(() => document.body.innerText.includes('Streaming Response...'));
      console.log(`[Trusting Stream Check ${i+1}] hasResult: ${hasResult}, isStreaming: ${isStreaming}`);
      if (hasResult && !isStreaming) {
        console.log('Trusting profile simulation completed!');
        break;
      }
    }

    await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));

    const drawerEl = await page.$('.max-w-3xl');
    if (drawerEl) {
      drawerBox = await drawerEl.boundingBox();
      console.log('Drawer box:', drawerBox);
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
  } catch (e) {
    console.error('Error capturing fig8:', e);
  }

  // 3. fig9_safe_result.png - Security-Conscious Profile on SIM-EML-001
  try {
    console.log('Clicking Security-Conscious profile pill in drawer...');
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const target = btns.find(b => b.textContent && b.textContent.includes('Security-Conscious'));
      if (target) target.click();
    });
    await page.evaluate(() => new Promise(r => setTimeout(r, 800)));

    console.log('Clicking main Run Simulation button for Security-Conscious profile...');
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const target = btns.find(b => b.textContent && b.textContent.includes('Run Simulation as'));
      if (target) target.click();
    });

    console.log('Waiting for live Gemini streaming to complete for Security-Conscious profile...');
    for (let i = 0; i < 30; i++) {
      await page.evaluate(() => new Promise(r => setTimeout(r, 2000)));
      const hasResult = await page.evaluate(() => document.body.innerText.includes('Agent Decision Result'));
      const isStreaming = await page.evaluate(() => document.body.innerText.includes('Streaming Response...'));
      console.log(`[Security-Conscious Stream Check ${i+1}] hasResult: ${hasResult}, isStreaming: ${isStreaming}`);
      if (hasResult && !isStreaming) {
        console.log('Security-Conscious profile simulation completed!');
        break;
      }
    }

    await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));

    const drawerEl2 = await page.$('.max-w-3xl');
    let drawerBox2 = drawerEl2 ? await drawerEl2.boundingBox() : drawerBox;

    console.log('Capturing fig9_safe_result.png...');
    if (drawerBox) {
      const clipRect = {
        x: drawerBox2 ? drawerBox2.x : drawerBox.x,
        y: drawerBox2 ? drawerBox2.y : drawerBox.y,
        width: Math.round(drawerBox.width),
        height: Math.round(drawerBox.height)
      };
      await page.screenshot({
        path: path.join(OUTPUT_DIR, 'fig9_safe_result.png'),
        clip: clipRect
      });
    } else {
      await page.screenshot({ path: path.join(OUTPUT_DIR, 'fig9_safe_result.png') });
    }
  } catch (e) {
    console.error('Error capturing fig9:', e);
  }

  // 4. fig10_defensive_portal.png - Handoff to Defensive AI
  try {
    console.log('Clicking Analyze with Defensive AI from modal footer...');
    await page.evaluate(() => {
      const btns = Array.from(document.querySelectorAll('button'));
      const target = btns.find(b => b.textContent && b.textContent.includes('Analyze with Defensive AI'));
      if (target) target.click();
    });

    console.log('Waiting for Defensive AI classification to execute...');
    for (let i = 0; i < 20; i++) {
      await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));
      const hasDef = await page.evaluate(() => document.body.innerText.includes('Defensive AI Classification'));
      if (hasDef) {
        console.log('Defensive AI classification ready on page!');
        break;
      }
    }
    await page.evaluate(() => new Promise(r => setTimeout(r, 1500)));

    console.log('Capturing fig10_defensive_portal.png...');
    await page.screenshot({
      path: path.join(OUTPUT_DIR, 'fig10_defensive_portal.png'),
      fullPage: false
    });
  } catch (e) {
    console.error('Error capturing fig10:', e);
  }

  // 5. fig11_incidents.png - Incidents Dashboard Full Width
  try {
    console.log('Capturing fig11_incidents.png...');
    await page.goto('http://localhost:5173/admin/incidents', { waitUntil: 'networkidle2' });
    await page.evaluate(() => new Promise(r => setTimeout(r, 2000)));

    await page.screenshot({
      path: path.join(OUTPUT_DIR, 'fig11_incidents.png'),
      fullPage: false
    });
  } catch (e) {
    console.error('Error capturing fig11:', e);
  }

  // 6. fig12_analytics_persisted.png - Analytics Page Full Width
  try {
    console.log('Capturing fig12_analytics_persisted.png...');
    await page.goto('http://localhost:5173/admin/analytics', { waitUntil: 'networkidle2' });
    await page.evaluate(() => new Promise(r => setTimeout(r, 2000)));

    await page.screenshot({
      path: path.join(OUTPUT_DIR, 'fig12_analytics_persisted.png'),
      fullPage: false
    });
  } catch (e) {
    console.error('Error capturing fig12:', e);
  }

  await browser.close();
  console.log('Part 2 capture completed!');
})();

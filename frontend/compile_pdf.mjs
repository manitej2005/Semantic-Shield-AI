import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const HTML_PATH = 'file:///C:/Users/home/.gemini/antigravity-ide/brain/f4ed86f4-2997-4b48-8250-cd4f069efbe0/paper/SemanticShield_AI_Research_Paper.html';
const PDF_PATH_1 = 'C:/Users/home/.gemini/antigravity-ide/brain/f4ed86f4-2997-4b48-8250-cd4f069efbe0/paper/SemanticShield_AI_Research_Paper.pdf';
const PDF_PATH_ROOT = 'c:/Users/home/OneDrive/Desktop/Semantic_Sheild_AI/SemanticShield_AI_Research_Paper.pdf';

(async () => {
  console.log('Launching Edge browser for PDF compilation...');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.goto(HTML_PATH, { waitUntil: 'networkidle0' });
  await page.evaluate(() => new Promise(r => setTimeout(r, 1000)));

  console.log('Rendering PDF...');
  await page.pdf({
    path: PDF_PATH_1,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: `
      <div style="font-family: 'Times New Roman', Times, serif; font-size: 8pt; font-style: italic; width: 100%; text-align: right; margin-right: 15mm; margin-top: 5mm; border-bottom: 0.5pt solid #666; padding-bottom: 2px;">
        SemanticShield AI - Phishing Simulation and Behavioral Threat Analysis
      </div>
    `,
    footerTemplate: `
      <div style="font-family: 'Times New Roman', Times, serif; font-size: 9pt; width: 100%; text-align: center; margin-bottom: 5mm;">
        <span class="pageNumber"></span>
      </div>
    `,
    margin: {
      top: '18mm',
      bottom: '18mm',
      left: '15mm',
      right: '15mm'
    }
  });

  // Copy to workspace root as requested
  fs.copyFileSync(PDF_PATH_1, PDF_PATH_ROOT);
  console.log(`Successfully compiled PDF to:\n1. ${PDF_PATH_1}\n2. ${PDF_PATH_ROOT}`);

  await browser.close();
})();

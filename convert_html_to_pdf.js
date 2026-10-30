import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';

(async () => {
  const htmlPath = path.resolve('paper/source/paper.html');
  const pdfPath = path.resolve('paper/SemanticShield_AI_Research_Paper.pdf');

  if (!fs.existsSync(htmlPath)) {
    console.error(`HTML file missing: ${htmlPath}`);
    process.exit(1);
  }

  console.log(`Rendering PDF from ${htmlPath}...`);

  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.goto(`file:///${htmlPath.replace(/\\/g, '/')}`, { waitUntil: 'networkidle0' });

  // Generate PDF with exact IEEE layout settings
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    margin: {
      top: '22mm',
      bottom: '20mm',
      left: '15mm',
      right: '15mm'
    },
    headerTemplate: `
      <div style="font-family: 'Times New Roman', Times, serif; font-size: 8.5pt; font-style: italic; color: #333333; text-align: center; width: 100%; margin: 0 15mm; padding-bottom: 3px; border-bottom: 0.5pt solid #444444;">
        SemanticShield AI — An Intelligent Agent for Phishing Simulation and Behavioral Threat Analysis
      </div>
    `,
    footerTemplate: `
      <div style="font-family: 'Times New Roman', Times, serif; font-size: 9.5pt; color: #111111; text-align: center; width: 100%;">
        <span class="pageNumber"></span>
      </div>
    `
  });

  await browser.close();
  console.log(`PDF rendered successfully at: ${pdfPath}`);
})();

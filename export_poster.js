import puppeteer from 'puppeteer';
import path from 'path';
import fs from 'fs';

(async () => {
  const htmlPath = path.resolve('poster.html');
  const pdfPath = path.resolve('SemanticShield_Poster_Redesign.pdf');
  const pngPath = path.resolve('SemanticShield_Poster_Redesign.png');
  const previewPath = path.resolve('SemanticShield_Poster_preview.png');

  if (!fs.existsSync(htmlPath)) {
    console.error(`HTML file missing: ${htmlPath}`);
    process.exit(1);
  }

  console.log(`Launching Edge browser via Puppeteer...`);
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });

  const page = await browser.newPage();
  
  // 594mm x 841mm in standard 96 DPI CSS pixels is 2245 x 3179
  // For 300 DPI equivalent, deviceScaleFactor = 300 / 96 = 3.125 (7016 x 9934 px)
  await page.setViewport({
    width: 2245,
    height: 3179,
    deviceScaleFactor: 2 // 4490 x 6358 px (ultra sharp, fast to encode)
  });

  console.log(`Loading ${htmlPath}...`);
  await page.goto(`file:///${htmlPath.replace(/\\/g, '/')}`, { 
    waitUntil: ['load', 'networkidle0'] 
  });

  // Ensure fonts are loaded
  await page.evaluateHandle('document.fonts.ready');
  // Small wait for layout stability
  await new Promise(r => setTimeout(r, 1000));

  console.log(`Generating Print-Ready A1 PDF...`);
  await page.pdf({
    path: pdfPath,
    width: '594mm',
    height: '841mm',
    printBackground: true,
    margin: {
      top: 0,
      right: 0,
      bottom: 0,
      left: 0
    }
  });
  console.log(`PDF saved to: ${pdfPath}`);

  console.log(`Capturing High-Resolution PNG (4490x6358 px)...`);
  const posterElement = await page.$('.poster-canvas');
  if (posterElement) {
    await posterElement.screenshot({
      path: pngPath,
      type: 'png'
    });
    // Also save copy to previewPath
    fs.copyFileSync(pngPath, previewPath);
    console.log(`High-res PNG saved to: ${pngPath}`);
  } else {
    await page.screenshot({
      path: pngPath,
      type: 'png',
      fullPage: true
    });
    fs.copyFileSync(pngPath, previewPath);
    console.log(`Fullpage PNG saved to: ${pngPath}`);
  }

  await browser.close();
  console.log('All exports completed successfully!');
})();

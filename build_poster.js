import fs from 'fs';
import path from 'path';
import puppeteer from 'puppeteer';

function getBase64Image(filePath) {
  if (fs.existsSync(filePath)) {
    const fileData = fs.readFileSync(filePath);
    return `data:image/png;base64,${fileData.toString('base64')}`;
  }
  return '';
}

const imgSetup = getBase64Image(path.resolve('paper_screenshots/fig7_simulator_setup.png'));
const imgAnalysis = getBase64Image(path.resolve('paper_screenshots/fig8_vulnerable_result.png'));
const imgIncidents = getBase64Image(path.resolve('paper_screenshots/fig11_incidents.png'));

const htmlContent = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SemanticShield AI - Scientific Poster</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,400;1,600&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --navy: #1B2466;
    --orange: #E8731A;
    --cream: #FAF8F3;
    --gold: #C9A24A;
    --beige: #F0E9DC;
    --border-dark: #1B2466;
    --text-dark: #111827;
    --card-bg: #FFFFFF;
  }

  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  @page {
    size: 420mm 594mm;
    margin: 0;
  }

  body {
    width: 420mm;
    height: 594mm;
    background-color: var(--cream);
    font-family: 'Inter', sans-serif;
    color: var(--text-dark);
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    overflow: hidden;
  }

  /* Outer Double Border Frame */
  .outer-frame {
    width: 420mm;
    height: 594mm;
    padding: 10mm;
    background-color: var(--cream);
  }

  .navy-outer-border {
    width: 100%;
    height: 100%;
    border: 2.5mm solid var(--navy);
    padding: 2mm;
    background-color: var(--cream);
  }

  .gold-inner-border {
    width: 100%;
    height: 100%;
    border: 1.2mm solid var(--gold);
    padding: 6mm 8mm;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    background-color: var(--cream);
  }

  /* Section Titles */
  .section-title-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2mm;
    border-bottom: 1.5px solid var(--gold);
    padding-bottom: 1mm;
  }

  .section-title {
    font-family: 'Playfair Display', serif;
    font-size: 14pt;
    font-weight: 700;
    color: var(--navy);
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }

  .section-subtitle-note {
    font-size: 9pt;
    color: #666;
    font-weight: 500;
  }

  /* 1. HEADER */
  .header-section {
    display: flex;
    align-items: center;
    gap: 6mm;
    padding-bottom: 3mm;
    border-bottom: 1.5px solid var(--gold);
  }

  .logo-container {
    width: 24mm;
    height: 24mm;
    flex-shrink: 0;
  }

  .header-text {
    display: flex;
    flex-direction: column;
    gap: 1mm;
  }

  .university-name {
    font-family: 'Playfair Display', serif;
    font-size: 24pt;
    font-weight: 800;
    color: var(--navy);
    letter-spacing: 2px;
    line-height: 1.1;
  }

  .dept-name {
    font-size: 12.5pt;
    font-weight: 700;
    color: var(--navy);
    letter-spacing: 0.5px;
  }

  .city-name {
    font-size: 10pt;
    color: #555;
    font-weight: 500;
  }

  /* 2. HERO */
  .hero-container {
    display: flex;
    flex-direction: column;
    gap: 0;
    border: 1px solid var(--navy);
    background-color: var(--navy);
    border-radius: 2px;
    overflow: hidden;
  }

  .meander-strip {
    height: 5.5mm;
    width: 100%;
    background-color: var(--navy);
    display: block;
  }

  .hero-main {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 4mm 8mm;
    background-color: var(--navy);
    color: white;
  }

  .hero-left {
    flex: 1;
    padding-right: 6mm;
  }

  .hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 25pt;
    font-weight: 700;
    color: #FFFFFF;
    line-height: 1.2;
    margin-bottom: 2mm;
  }

  .hero-title .highlight {
    color: var(--orange);
  }

  .hero-subtitle {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 12.5pt;
    color: var(--beige);
    letter-spacing: 0.3px;
  }

  .hero-right-illustration {
    width: 32mm;
    height: 32mm;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .stat-tiles-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    background-color: var(--navy);
    border-top: 1px solid rgba(201, 162, 74, 0.4);
    padding: 2.5mm 0;
  }

  .stat-tile {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 3mm;
    padding: 1mm 4mm;
    border-right: 1px solid rgba(201, 162, 74, 0.35);
  }

  .stat-tile:last-child {
    border-right: none;
  }

  .stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 24pt;
    font-weight: 800;
    color: var(--orange);
    line-height: 1;
  }

  .stat-label {
    font-size: 9pt;
    font-weight: 600;
    color: #FFFFFF;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    line-height: 1.25;
  }

  /* 3. PROJECT TEAM */
  .team-section {
    display: flex;
    gap: 3mm;
    align-items: stretch;
  }

  .team-label-box {
    width: 38mm;
    background-color: var(--navy);
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Playfair Display', serif;
    font-size: 11pt;
    font-weight: 700;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    text-align: center;
    padding: 2mm 3mm;
    border-radius: 2px;
    flex-shrink: 0;
  }

  .team-cards-grid {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 3mm;
  }

  .member-card {
    background-color: var(--card-bg);
    border: 1px solid var(--gold);
    border-radius: 2px;
    padding: 2.5mm 4mm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.03);
  }

  .member-name {
    font-family: 'Playfair Display', serif;
    font-size: 11.5pt;
    font-weight: 700;
    color: var(--navy);
  }

  .member-roll {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10pt;
    font-weight: 600;
    color: var(--orange);
    margin: 0.5mm 0;
  }

  .member-fullname {
    font-size: 8pt;
    color: #6B7280;
    font-weight: 500;
  }

  /* 4. ABSTRACT & RESEARCH GAPS */
  .grid-abstract-gaps {
    display: grid;
    grid-template-columns: 1.4fr 1fr;
    gap: 5mm;
  }

  .abstract-box {
    background-color: var(--card-bg);
    border: 1px solid var(--gold);
    padding: 3.5mm 4.5mm;
    border-radius: 2px;
    font-size: 9.5pt;
    line-height: 1.45;
    color: #1F2937;
    text-align: justify;
  }

  .gaps-box {
    background-color: var(--card-bg);
    border: 1px solid var(--gold);
    padding: 3.5mm 4.5mm;
    border-radius: 2px;
    display: flex;
    flex-direction: column;
    justify-content: space-around;
  }

  .gap-item {
    display: flex;
    align-items: flex-start;
    gap: 2.5mm;
    font-size: 9pt;
    line-height: 1.35;
    color: #1F2937;
    margin-bottom: 1.5mm;
  }
  .gap-item:last-child {
    margin-bottom: 0;
  }

  .diamond-bullet {
    color: var(--orange);
    font-size: 9pt;
    line-height: 1;
    margin-top: 0.5mm;
  }

  /* 5. METHODOLOGY PIPELINE */
  .pipeline-container {
    background-color: var(--card-bg);
    border: 1px solid var(--gold);
    border-radius: 2px;
    padding: 3.5mm 4mm;
    display: flex;
    align-items: center;
    gap: 3mm;
  }

  .pipe-input-box {
    width: 48mm;
    border: 1.5px solid var(--navy);
    border-radius: 2px;
    padding: 2.5mm 3mm;
    background-color: #FAFAFC;
    flex-shrink: 0;
  }

  .pipe-box-title {
    font-family: 'Playfair Display', serif;
    font-size: 10pt;
    font-weight: 700;
    color: var(--navy);
    margin-bottom: 1mm;
    border-bottom: 1px solid #E5E7EB;
    padding-bottom: 0.5mm;
  }

  .pipe-box-content {
    font-size: 8.2pt;
    color: #4B5563;
    line-height: 1.35;
  }

  .pipe-arrow {
    font-size: 16pt;
    color: var(--orange);
    font-weight: bold;
    flex-shrink: 0;
  }

  .pipe-center-navy {
    width: 44mm;
    background-color: var(--navy);
    color: white;
    border-radius: 2px;
    padding: 3mm 3mm;
    text-align: center;
    flex-shrink: 0;
  }

  .pipe-center-title {
    font-family: 'Playfair Display', serif;
    font-size: 10.5pt;
    font-weight: 700;
    margin-bottom: 1mm;
    color: #FFFFFF;
  }

  .pipe-center-sub {
    font-size: 7.8pt;
    color: var(--beige);
    line-height: 1.25;
  }

  .pipe-steps-grid {
    flex: 1;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2mm;
  }

  .step-card {
    border: 1px solid #D1D5DB;
    background-color: #FFFFFF;
    border-radius: 2px;
    padding: 2mm 2.5mm;
    display: flex;
    align-items: center;
    gap: 2mm;
  }

  .roman-badge {
    width: 6mm;
    height: 6mm;
    background-color: var(--orange);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Playfair Display', serif;
    font-size: 8pt;
    font-weight: 700;
    flex-shrink: 0;
  }

  .step-text {
    font-size: 8pt;
    font-weight: 600;
    color: var(--navy);
    line-height: 1.2;
  }

  .pipe-output-box {
    width: 52mm;
    border: 1.5px solid var(--orange);
    border-radius: 2px;
    padding: 2.5mm 3mm;
    background-color: #FFFDF9;
    flex-shrink: 0;
  }

  /* 6. ARCHITECTURE & WORKFLOW */
  .grid-arch-workflow {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5mm;
  }

  .arch-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
  }

  .arch-table tr {
    margin-bottom: 1mm;
  }

  .arch-label-cell {
    width: 32%;
    background-color: var(--navy);
    color: white;
    font-weight: 700;
    padding: 2.2mm 3mm;
    font-size: 8.5pt;
    border-bottom: 1.5mm solid var(--cream);
  }

  .arch-label-cell.ai-highlight {
    background-color: var(--orange);
  }

  .arch-value-cell {
    background-color: var(--beige);
    color: #1F2937;
    padding: 2.2mm 3mm;
    font-size: 8.2pt;
    border-bottom: 1.5mm solid var(--cream);
    line-height: 1.3;
  }

  .workflow-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2.5mm;
  }

  .wf-card {
    background-color: var(--card-bg);
    border: 1px solid var(--gold);
    border-radius: 2px;
    padding: 2.5mm 2mm;
    display: flex;
    align-items: center;
    gap: 2mm;
  }

  .wf-card.ai-highlight {
    border: 1.5px solid var(--orange);
    background-color: #FFFBF7;
  }

  .wf-badge {
    width: 5.5mm;
    height: 5.5mm;
    background-color: var(--navy);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 8pt;
    font-weight: 700;
    flex-shrink: 0;
  }

  .wf-card.ai-highlight .wf-badge {
    background-color: var(--orange);
  }

  .wf-text {
    font-size: 8pt;
    font-weight: 600;
    color: var(--navy);
    line-height: 1.25;
  }

  /* 7. IMPLEMENTATION PROTOTYPE */
  .proto-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 4mm;
  }

  .proto-frame {
    background-color: var(--card-bg);
    border: 1px solid var(--navy);
    border-radius: 2px;
    padding: 2mm;
    display: flex;
    flex-direction: column;
    gap: 1.5mm;
  }

  .proto-img {
    width: 100%;
    height: 44mm;
    object-fit: cover;
    object-position: top left;
    border: 1px solid #E5E7EB;
  }

  .proto-caption {
    font-size: 8pt;
    font-weight: 600;
    color: var(--navy);
    text-align: center;
    padding: 0.5mm 1mm;
  }

  /* 8. EVALUATION, TESTS, STACK */
  .grid-eval-tests-stack {
    display: grid;
    grid-template-columns: 1.15fr 1fr 1fr;
    gap: 4mm;
  }

  .eval-chips-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1.8mm;
  }

  .tick-chip {
    background-color: var(--card-bg);
    border: 1px solid var(--gold);
    border-radius: 2px;
    padding: 1.8mm 2mm;
    display: flex;
    align-items: center;
    gap: 1.5mm;
    font-size: 7.5pt;
    font-weight: 600;
    color: var(--navy);
    line-height: 1.2;
  }

  .tick-icon {
    color: var(--orange);
    font-weight: bold;
    font-size: 8.5pt;
    flex-shrink: 0;
  }

  .tests-list-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2mm 3mm;
    background-color: var(--card-bg);
    border: 1px solid var(--gold);
    padding: 3mm;
    border-radius: 2px;
    height: 100%;
    align-content: center;
  }

  .test-item {
    display: flex;
    align-items: center;
    gap: 1.5mm;
    font-size: 8pt;
    font-weight: 600;
    color: #1F2937;
  }

  .stack-chips-wrap {
    display: flex;
    flex-wrap: wrap;
    gap: 1.8mm;
    background-color: var(--card-bg);
    border: 1px solid var(--gold);
    padding: 3mm;
    border-radius: 2px;
    height: 100%;
    align-content: center;
  }

  .tech-chip {
    border: 1px solid var(--navy);
    background-color: #FFFFFF;
    color: var(--navy);
    font-size: 8pt;
    font-weight: 600;
    padding: 1.2mm 2.8mm;
    border-radius: 2px;
  }

  .tech-chip.gemini-highlight {
    background-color: var(--orange);
    border-color: var(--orange);
    color: #FFFFFF;
  }

  /* 9. CONCLUSION & LIMITATIONS */
  .grid-conclusion-limits {
    display: grid;
    grid-template-columns: 0.95fr 1fr;
    gap: 5mm;
  }

  .conclusion-card {
    background-color: var(--navy);
    color: white;
    border-radius: 2px;
    padding: 3.5mm 4.5mm;
    font-size: 9pt;
    line-height: 1.45;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .limits-card {
    background-color: var(--card-bg);
    border: 1px solid var(--gold);
    border-radius: 2px;
    padding: 3mm 4mm;
    font-size: 8.2pt;
    line-height: 1.35;
    color: #1F2937;
    display: flex;
    flex-direction: column;
    gap: 1.5mm;
  }

  .limits-card strong {
    color: var(--navy);
  }

  /* 10. FOOTER */
  .footer-rule {
    width: 100%;
    height: 1px;
    background-color: var(--gold);
    margin-top: 1mm;
  }
</style>
</head>
<body>

<div class="outer-frame">
  <div class="navy-outer-border">
    <div class="gold-inner-border">

      <!-- 1. HEADER -->
      <div class="header-section">
        <div class="logo-container">
          <svg viewBox="0 0 100 100" width="100%" height="100%">
            <!-- Outer Gold Ring -->
            <circle cx="50" cy="50" r="46" fill="none" stroke="#1B2466" stroke-width="4"/>
            <circle cx="50" cy="50" r="42" fill="none" stroke="#C9A24A" stroke-width="2"/>
            <circle cx="50" cy="50" r="39" fill="#1B2466"/>
            <!-- Stars -->
            <polygon points="50,16 52,21 57,21 53,24 55,29 50,26 45,29 47,24 43,21 48,21" fill="#E8731A"/>
            <polygon points="30,22 31,25 35,25 32,27 33,31 30,29 27,31 28,27 25,25 29,25" fill="#C9A24A"/>
            <polygon points="70,22 71,25 75,25 72,27 73,31 70,29 67,31 68,27 65,25 69,25" fill="#C9A24A"/>
            <!-- Inner Shield with MR Emblem -->
            <path d="M 30 38 L 70 38 L 70 65 Q 50 82 30 65 Z" fill="#FAF8F3" stroke="#C9A24A" stroke-width="2"/>
            <!-- M Pillar Symbol -->
            <path d="M 38 62 V 44 L 50 54 L 62 44 V 62" fill="none" stroke="#1B2466" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- Graduation Cap Top -->
            <polygon points="50,30 25,40 50,50 75,40" fill="#E8731A"/>
            <polygon points="50,30 25,40 50,43" fill="#C9A24A"/>
            <path d="M 70 42 V 55" stroke="#E8731A" stroke-width="2"/>
            <circle cx="70" cy="56" r="2" fill="#E8731A"/>
          </svg>
        </div>
        <div class="header-text">
          <div class="university-name">MALLA REDDY UNIVERSITY</div>
          <div class="dept-name">Department of Cyber Security, ECE &amp; IoT</div>
          <div class="city-name">Hyderabad, Telangana</div>
        </div>
      </div>

      <!-- 2. HERO -->
      <div class="hero-container">
        <!-- Top Greek Key -->
        <svg class="meander-strip" preserveAspectRatio="none" viewBox="0 0 600 12">
          <pattern id="greek-top" width="24" height="12" patternUnits="userSpaceOnUse">
            <path d="M 0 12 V 2 H 10 V 10 H 4 V 6 H 7 V 8 H 6 V 12 M 12 0 V 10 H 22 V 2 H 16 V 6 H 19 V 4 H 18 V 0" fill="none" stroke="#C9A24A" stroke-width="1.5"/>
          </pattern>
          <rect width="100%" height="12" fill="url(#greek-top)"/>
        </svg>

        <div class="hero-main">
          <div class="hero-left">
            <div class="hero-title">An <span class="highlight">Intelligent Agent</span> for Phishing Simulation and Behavioral Threat Analysis</div>
            <div class="hero-subtitle">SemanticShield AI: A Behavior-Driven Framework for Realistic Phishing Simulation</div>
          </div>
          <div class="hero-right-illustration">
            <svg viewBox="0 0 100 100" width="100%" height="100%">
              <!-- Outer Shield Line -->
              <path d="M 50 10 L 85 22 V 50 Q 85 78 50 92 Q 15 78 15 50 V 22 Z" fill="none" stroke="#C9A24A" stroke-width="2.5"/>
              <path d="M 50 15 L 80 25 V 48 Q 80 73 50 86 Q 20 73 20 48 V 25 Z" fill="none" stroke="#C9A24A" stroke-width="1" stroke-dasharray="3,2"/>
              <!-- Envelope -->
              <rect x="34" y="36" width="32" height="20" fill="none" stroke="#C9A24A" stroke-width="2" rx="1"/>
              <path d="M 34 36 L 50 48 L 66 36" fill="none" stroke="#C9A24A" stroke-width="2"/>
              <!-- Fish Hook -->
              <path d="M 50 56 V 68 Q 50 75 42 75 Q 35 75 35 68 Q 35 64 39 64" fill="none" stroke="#E8731A" stroke-width="2.5" stroke-linecap="round"/>
              <polygon points="39,61 43,65 37,67" fill="#E8731A"/>
              <!-- Orange Nodes and Dashed Lines -->
              <circle cx="24" cy="30" r="3" fill="#E8731A"/>
              <circle cx="76" cy="30" r="3" fill="#E8731A"/>
              <circle cx="82" cy="60" r="3" fill="#E8731A"/>
              <circle cx="18" cy="60" r="3" fill="#E8731A"/>
              <line x1="24" y1="30" x2="34" y2="36" stroke="#E8731A" stroke-width="1.2" stroke-dasharray="2,2"/>
              <line x1="76" y1="30" x2="66" y2="36" stroke="#E8731A" stroke-width="1.2" stroke-dasharray="2,2"/>
              <line x1="82" y1="60" x2="66" y2="56" stroke="#E8731A" stroke-width="1.2" stroke-dasharray="2,2"/>
              <line x1="18" y1="60" x2="34" y2="56" stroke="#E8731A" stroke-width="1.2" stroke-dasharray="2,2"/>
            </svg>
          </div>
        </div>

        <div class="stat-tiles-strip">
          <div class="stat-tile">
            <div class="stat-number">4</div>
            <div class="stat-label">Behavioral employee<br>profiles</div>
          </div>
          <div class="stat-tile">
            <div class="stat-number">3</div>
            <div class="stat-label">Weighted analysis<br>agents</div>
          </div>
          <div class="stat-tile">
            <div class="stat-number">4</div>
            <div class="stat-label">Phishing attack<br>scenarios</div>
          </div>
          <div class="stat-tile">
            <div class="stat-number">5</div>
            <div class="stat-label">Architecture<br>layers</div>
          </div>
        </div>

        <!-- Bottom Greek Key -->
        <svg class="meander-strip" preserveAspectRatio="none" viewBox="0 0 600 12">
          <pattern id="greek-bottom" width="24" height="12" patternUnits="userSpaceOnUse">
            <path d="M 0 12 V 2 H 10 V 10 H 4 V 6 H 7 V 8 H 6 V 12 M 12 0 V 10 H 22 V 2 H 16 V 6 H 19 V 4 H 18 V 0" fill="none" stroke="#C9A24A" stroke-width="1.5"/>
          </pattern>
          <rect width="100%" height="12" fill="url(#greek-bottom)"/>
        </svg>
      </div>

      <!-- 3. PROJECT TEAM -->
      <div class="team-section">
        <div class="team-label-box">PROJECT TEAM</div>
        <div class="team-cards-grid">
          <div class="member-card">
            <div class="member-name">Ch. Avinash</div>
            <div class="member-roll">2311CS040035</div>
            <div class="member-fullname">[CONFIRM full name]</div>
          </div>
          <div class="member-card">
            <div class="member-name">K. Mani Tej Kumar</div>
            <div class="member-roll">2311CS040070</div>
            <div class="member-fullname">[CONFIRM full name]</div>
          </div>
          <div class="member-card">
            <div class="member-name">K. Kowshik</div>
            <div class="member-roll">2311CS040074</div>
            <div class="member-fullname">[CONFIRM full name]</div>
          </div>
        </div>
      </div>

      <!-- 4. ABSTRACT & RESEARCH GAPS ADDRESSED -->
      <div class="grid-abstract-gaps">
        <div>
          <div class="section-title-container">
            <div class="section-title">ABSTRACT</div>
          </div>
          <div class="abstract-box">
            Phishing remains the most common entry point for breaches, yet most awareness programs rely on static, one-size-fits-all test emails that ignore how differently people actually react. This work presents SemanticShield AI, an intelligent agent that simulates phishing attacks against AI-driven employee personas, each with its own behavioral profile, and analyzes the resulting decisions. A Gemini-powered agent reasons through a phishing email as a trusting, security-conscious, overwhelmed or executive employee, streams its reasoning live, and commits to a verdict. The verdict is passed through a weighted multi-agent risk engine to produce a threat category, severity and confidence score, which are logged as incidents on a dashboard.
          </div>
        </div>

        <div>
          <div class="section-title-container">
            <div class="section-title">RESEARCH GAPS ADDRESSED</div>
          </div>
          <div class="gaps-box">
            <div class="gap-item"><span class="diamond-bullet">◆</span> Static phishing tests that ignore individual behavior</div>
            <div class="gap-item"><span class="diamond-bullet">◆</span> Simulation and threat analysis handled as separate tools</div>
            <div class="gap-item"><span class="diamond-bullet">◆</span> No visible reasoning behind why a user falls for or spots an attack</div>
            <div class="gap-item"><span class="diamond-bullet">◆</span> Generic risk scores that are not tied to employee role or profile</div>
            <div class="gap-item"><span class="diamond-bullet">◆</span> Costly commercial platforms that are hard to adapt for research</div>
          </div>
        </div>
      </div>

      <!-- 5. PHISHING SIMULATION PIPELINE: METHODOLOGY -->
      <div>
        <div class="section-title-container">
          <div class="section-title">PHISHING SIMULATION PIPELINE: METHODOLOGY</div>
        </div>
        <div class="pipeline-container">
          <div class="pipe-input-box">
            <div class="pipe-box-title">Scenario Input</div>
            <div class="pipe-box-content">Scenario, employee role, behavior profile, email subject and body</div>
          </div>

          <div class="pipe-arrow">&#10142;</div>

          <div class="pipe-center-navy">
            <div class="pipe-center-title">Simulation Engine</div>
            <div class="pipe-center-sub">Central orchestrator &middot;<br>Google Gemini API</div>
          </div>

          <div class="pipe-arrow">&#10142;</div>

          <div class="pipe-steps-grid">
            <div class="step-card">
              <div class="roman-badge">I</div>
              <div class="step-text">Trusting Persona<br><span style="font-weight:400; color:#555;">(HR Manager)</span></div>
            </div>
            <div class="step-card">
              <div class="roman-badge">II</div>
              <div class="step-text">Security-Conscious<br><span style="font-weight:400; color:#555;">(Developer)</span></div>
            </div>
            <div class="step-card">
              <div class="roman-badge">III</div>
              <div class="step-text">Overwhelmed<br><span style="font-weight:400; color:#555;">(Finance Manager)</span></div>
            </div>
            <div class="step-card">
              <div class="roman-badge">IV</div>
              <div class="step-text">Executive Persona<br><span style="font-weight:400; color:#555;">(VP)</span></div>
            </div>
            <div class="step-card">
              <div class="roman-badge">V</div>
              <div class="step-text">Decision Extraction<br><span style="font-size:7pt; color:#E8731A;">[VULNERABLE / SAFE]</span></div>
            </div>
            <div class="step-card">
              <div class="roman-badge">VI</div>
              <div class="step-text">Risk Scoring<br><span style="font-size:7pt; color:#555;">Sem 40% &middot; Beh 25% &middot; URL 35%</span></div>
            </div>
          </div>

          <div class="pipe-arrow">&#10142;</div>

          <div class="pipe-output-box">
            <div class="pipe-box-title" style="color: var(--orange);">Threat Analysis Result</div>
            <div class="pipe-box-content">Category, severity and confidence; logged as an incident and streamed live</div>
          </div>
        </div>
      </div>

      <!-- 6. ARCHITECTURE & WORKFLOW -->
      <div class="grid-arch-workflow">
        <div>
          <div class="section-title-container">
            <div class="section-title">LAYERED SYSTEM ARCHITECTURE</div>
          </div>
          <table class="arch-table">
            <tr>
              <td class="arch-label-cell">Presentation</td>
              <td class="arch-value-cell">React two-panel interface &middot; live reasoning stream</td>
            </tr>
            <tr>
              <td class="arch-label-cell">Application</td>
              <td class="arch-value-cell">FastAPI REST and WebSocket endpoints &middot; Pydantic validation</td>
            </tr>
            <tr>
              <td class="arch-label-cell">Business Logic</td>
              <td class="arch-value-cell">Simulation engine, supervisor agent, risk engine, incident and activity managers</td>
            </tr>
            <tr>
              <td class="arch-label-cell ai-highlight">AI Integration</td>
              <td class="arch-value-cell" style="background-color: #FFF8F0;">Google Gemini API &middot; behavioral system prompts &middot; streaming</td>
            </tr>
            <tr>
              <td class="arch-label-cell">Data Persistence</td>
              <td class="arch-value-cell">SQLite &middot; SQLAlchemy &middot; Alembic migrations</td>
            </tr>
          </table>
        </div>

        <div>
          <div class="section-title-container">
            <div class="section-title">END-TO-END WORKFLOW</div>
          </div>
          <div class="workflow-grid">
            <div class="wf-card"><div class="wf-badge">1</div><div class="wf-text">Select Scenario</div></div>
            <div class="wf-card"><div class="wf-badge">2</div><div class="wf-text">Choose Role &amp; Profile</div></div>
            <div class="wf-card"><div class="wf-badge">3</div><div class="wf-text">Load Phishing Email</div></div>
            <div class="wf-card"><div class="wf-badge">4</div><div class="wf-text">Run Simulation</div></div>
            <div class="wf-card ai-highlight"><div class="wf-badge">5</div><div class="wf-text" style="color:var(--orange);">Gemini Streams Reasoning</div></div>
            <div class="wf-card"><div class="wf-badge">6</div><div class="wf-text">Extract Decision</div></div>
            <div class="wf-card"><div class="wf-badge">7</div><div class="wf-text">Score Risk</div></div>
            <div class="wf-card"><div class="wf-badge">8</div><div class="wf-text">Log Incident &amp; Activity</div></div>
            <div class="wf-card"><div class="wf-badge">9</div><div class="wf-text">View Live Results</div></div>
          </div>
        </div>
      </div>

      <!-- 7. IMPLEMENTATION: WORKING PROTOTYPE -->
      <div>
        <div class="section-title-container">
          <div class="section-title">IMPLEMENTATION: WORKING PROTOTYPE</div>
        </div>
        <div class="proto-grid">
          <div class="proto-frame">
            <img class="proto-img" src="${imgSetup}" alt="Simulation Setup">
            <div class="proto-caption">Simulation Setup: scenario, role and profile selection</div>
          </div>
          <div class="proto-frame">
            <img class="proto-img" src="${imgAnalysis}" alt="Live Analysis">
            <div class="proto-caption">Live Analysis: streaming agent reasoning</div>
          </div>
          <div class="proto-frame">
            <img class="proto-img" src="${imgIncidents}" alt="Result Card">
            <div class="proto-caption">Result Card: decision, category, severity, confidence</div>
          </div>
        </div>
      </div>

      <!-- 8. PROFILES, TESTS, TECH STACK -->
      <div class="grid-eval-tests-stack">
        <div>
          <div class="section-title-container">
            <div class="section-title">PROFILES &amp; SCENARIOS EVALUATED</div>
            <div class="section-subtitle-note">4 profiles &times; 4 scenarios</div>
          </div>
          <div class="eval-chips-grid">
            <div class="tick-chip"><span class="tick-icon">&#10003;</span> Trusting HR Manager</div>
            <div class="tick-chip"><span class="tick-icon">&#10003;</span> Security-Conscious Developer</div>
            <div class="tick-chip"><span class="tick-icon">&#10003;</span> Overwhelmed Finance Manager</div>
            <div class="tick-chip"><span class="tick-icon">&#10003;</span> Executive VP</div>
            <div class="tick-chip"><span class="tick-icon">&#10003;</span> Microsoft 365 Credential Harvest</div>
            <div class="tick-chip"><span class="tick-icon">&#10003;</span> Wire Transfer Fraud</div>
            <div class="tick-chip"><span class="tick-icon">&#10003;</span> Executive Impersonation</div>
            <div class="tick-chip"><span class="tick-icon">&#10003;</span> QR Code Phishing</div>
          </div>
        </div>

        <div>
          <div class="section-title-container">
            <div class="section-title">FUNCTIONAL TESTS PASSED</div>
          </div>
          <div class="tests-list-grid">
            <div class="test-item"><span class="tick-icon">&#10003;</span> Simulation API <span style="font-size:7pt; color:#888;">[CONFIRM]</span></div>
            <div class="test-item"><span class="tick-icon">&#10003;</span> Incident Creation <span style="font-size:7pt; color:#888;">[CONFIRM]</span></div>
            <div class="test-item"><span class="tick-icon">&#10003;</span> Streaming Response <span style="font-size:7pt; color:#888;">[CONFIRM]</span></div>
            <div class="test-item"><span class="tick-icon">&#10003;</span> Activity Logging <span style="font-size:7pt; color:#888;">[CONFIRM]</span></div>
            <div class="test-item"><span class="tick-icon">&#10003;</span> Decision Extraction <span style="font-size:7pt; color:#888;">[CONFIRM]</span></div>
            <div class="test-item"><span class="tick-icon">&#10003;</span> WebSocket Updates <span style="font-size:7pt; color:#888;">[CONFIRM]</span></div>
            <div class="test-item"><span class="tick-icon">&#10003;</span> Risk Scoring <span style="font-size:7pt; color:#888;">[CONFIRM]</span></div>
            <div class="test-item"><span class="tick-icon">&#10003;</span> Database Persistence <span style="font-size:7pt; color:#888;">[CONFIRM]</span></div>
          </div>
        </div>

        <div>
          <div class="section-title-container">
            <div class="section-title">TECHNOLOGY STACK</div>
          </div>
          <div class="stack-chips-wrap">
            <div class="tech-chip">React.js</div>
            <div class="tech-chip">FastAPI</div>
            <div class="tech-chip">Python 3.10</div>
            <div class="tech-chip gemini-highlight">Gemini API</div>
            <div class="tech-chip">SQLite</div>
            <div class="tech-chip">SQLAlchemy</div>
            <div class="tech-chip">Alembic</div>
            <div class="tech-chip">WebSocket</div>
            <div class="tech-chip">Pydantic</div>
          </div>
        </div>
      </div>

      <!-- 9. CONCLUSION & LIMITATIONS -->
      <div class="grid-conclusion-limits">
        <div>
          <div class="section-title-container">
            <div class="section-title">CONCLUSION</div>
          </div>
          <div class="conclusion-card">
            SemanticShield AI shows that the same phishing email carries very different risk depending on who receives it. By pairing behavior-driven simulation with a weighted multi-agent risk engine, it gives security teams a transparent, explainable view of human vulnerability and a practical basis for targeted awareness training.
          </div>
        </div>

        <div>
          <div class="section-title-container">
            <div class="section-title">LIMITATIONS &amp; FUTURE WORK</div>
          </div>
          <div class="limits-card">
            <div><strong>Limits:</strong> persona behavior depends on prompt design and the underlying language model; simulated personas are not real human responses; free-tier API rate limits; no large-scale user validation yet.</div>
            <div><strong>Next:</strong> calibrate personas with real employee response data, add SMS and voice phishing scenarios, adaptive training recommendations, attacker-versus-defender multi-agent loops, and migration to a cloud database.</div>
          </div>
        </div>
      </div>

      <!-- 10. FOOTER -->
      <div class="footer-rule"></div>

    </div>
  </div>
</div>

</body>
</html>
`;

const htmlPath = path.resolve('SemanticShield_Poster.html');
const pdfPath = path.resolve('SemanticShield_Poster.pdf');

fs.writeFileSync(htmlPath, htmlContent, 'utf-8');
console.log('Saved SemanticShield_Poster.html');

(async () => {
  console.log('Launching Edge Puppeteer to export PDF...');
  const browser = await puppeteer.launch({
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0' });

  // Render vector PDF at exact 420mm x 594mm size
  await page.pdf({
    path: pdfPath,
    width: '420mm',
    height: '594mm',
    printBackground: true,
    margin: { top: '0mm', right: '0mm', bottom: '0mm', left: '0mm' }
  });

  console.log('Saved SemanticShield_Poster.pdf successfully!');

  // Rasterize page to high-res PNG for visual audit inspection
  await page.setViewport({ width: 1587, height: 2245, deviceScaleFactor: 2 });
  const pngPath = path.resolve('SemanticShield_Poster_preview.png');
  await page.screenshot({ path: pngPath, fullPage: true });
  console.log('Saved preview screenshot SemanticShield_Poster_preview.png');

  await browser.close();
})();

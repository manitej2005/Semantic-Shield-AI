# 🛠️ SemanticShield AI Developer Setup & Installation Guide

> **Step-by-step guide to installing, configuring, and running SemanticShield AI locally.**

---

## 📋 Prerequisites

Before starting, ensure your system has:
* **Node.js**: `v18.0.0` or higher
* **npm**: `v9.0.0` or higher
* **Python**: `v3.10` to `v3.13`
* **Google Chrome / Chromium Browser**: Modern version supporting Manifest V3

---

## 1. Backend Setup (FastAPI Python Application)

1. Open your terminal and navigate to the `backend/` directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   * **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   * **Linux / macOS**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure Environment Variables:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Google Gemini API key if available:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```
   *(Note: If no API key is provided, the backend seamlessly activates local heuristic mock mode).*

5. Start the FastAPI backend server:
   ```bash
   python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
   ```
   The backend API will be available at `http://127.0.0.1:8000`.  
   Interactive API docs (Swagger UI) will be available at `http://127.0.0.1:8000/docs`.

---

## 2. Frontend Setup (React SPA)

1. Open a new terminal window and navigate to `frontend/`:
   ```bash
   cd frontend
   ```

2. Install Node dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

4. Open your browser and navigate to the local URL (typically `http://localhost:5173`).

---

## 3. Browser Extension Setup (Sentinel Web Guard)

To install and run the browser extension in Chrome or any Chromium-based browser (Brave, Edge):

1. Open Chrome and navigate to:
   ```
   chrome://extensions
   ```

2. Enable **Developer mode** using the toggle switch in the top-right corner.

3. Click the **Load unpacked** button in the top-left corner.

4. Select the `extension/` folder from this repository.

5. The **Sentinel Web Guard** extension icon will appear in your extensions toolbar. Click the extension pin icon to pin it to your browser toolbar.

6. Navigating to any website will trigger background analysis via `http://127.0.0.1:8000/analyze`.

---

## 🧪 Running Integration Tests

To run the backend integration tests:

```bash
cd backend
python -m unittest discover -s tests
python tests/test_soc_integration.py
python tests/test_threat_engine.py
```

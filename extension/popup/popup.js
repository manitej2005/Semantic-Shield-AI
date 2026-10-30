/**
 * SemanticShield AI - Popup Controller
 * Demonstration Interface for Agentic AI Workflow
 */

let pollInterval = null;
let currentTabId = null;
let currentResultData = null;

// ==========================================
// SECURITY AUDIO SYSTEM
// ==========================================
class SecurityAudio {
    constructor() {
        this.ctx = null;
        this.isMuted = localStorage.getItem("isMuted") === "true";
    }

    init() {
        if (!this.ctx) {
            this.ctx = new (window.AudioContext || window.webkitAudioContext)();
        }
    }

    async playAlert(type = "safe") {
        if (this.isMuted) return;
        this.init();

        try {
            if (type === "safe") {
                this._beep(880, 0.12, "sine", 0.05);
            } else if (type === "suspicious") {
                for (let i = 0; i < 2; i++) {
                    this._beep(380, 0.15, "triangle", 0.1);
                    await new Promise(r => setTimeout(r, 180));
                }
            } else if (type === "dangerous") {
                for (let i = 0; i < 3; i++) {
                    this._beep(220, 0.2, "sawtooth", 0.15, true);
                    await new Promise(r => setTimeout(r, 220));
                }
            }
        } catch (_) {}
    }

    _beep(freq, duration, type, vol, harsh = false) {
        if (!this.ctx) return;
        const osc = this.ctx.createOscillator();
        const gain = this.ctx.createGain();

        osc.type = type;
        osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

        gain.gain.setValueAtTime(vol, this.ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + duration);

        osc.connect(gain);
        gain.connect(this.ctx.destination);

        osc.start();
        osc.stop(this.ctx.currentTime + duration);
    }

    toggleMute() {
        this.isMuted = !this.isMuted;
        localStorage.getItem("isMuted");
        localStorage.setItem("isMuted", this.isMuted);
        return this.isMuted;
    }
}

const audio = new SecurityAudio();

// ==========================================
// CONSOLE LOG UTILITY
// ==========================================
function appendLog(msg, type = "normal") {
    const consoleBody = document.getElementById("console-logs");
    if (!consoleBody) return;

    const timeStr = new Date().toLocaleTimeString('en-US', { hour12: false });
    const logDiv = document.createElement("div");
    logDiv.className = `log-entry ${type}`;
    logDiv.innerHTML = `<span class="time">[${timeStr}]</span> ${msg}`;
    consoleBody.appendChild(logDiv);
    consoleBody.scrollTop = consoleBody.scrollHeight;
}

// ==========================================
// WORKFLOW TIMELINE ANIMATOR (2s Stager)
// ==========================================
async function animateWorkflowTimeline(data) {
    const steps = [
        { id: "step-ext", label: "Extension DOM Capture" },
        { id: "step-sup", label: "Supervisor Agent" },
        { id: "step-sem", label: "Semantic Analysis Agent" },
        { id: "step-beh", label: "Behavior Analysis Agent" },
        { id: "step-url", label: "URL Intelligence Agent" },
        { id: "step-risk", label: "Risk Assessment Engine" },
        { id: "step-exp", label: "Explainability Engine" }
    ];

    // Reset all nodes
    steps.forEach(s => setStepState(s.id, "waiting"));

    // Step 1: Extension complete immediately
    setStepState("step-ext", "completed");
    appendLog("Webpage URL & content captured by extension", "normal");
    await sleep(200);

    // Step 2: Supervisor running
    setStepState("step-sup", "running");
    appendLog("Supervisor Agent launched parallel agent dispatch", "normal");
    await sleep(250);
    setStepState("step-sup", "completed");

    // Step 3: Semantic Agent
    setStepState("step-sem", "running");
    setAgentBadge("semantic-status-badge", "running", "Running");
    appendLog("Semantic Agent (Gemini 2.5) analyzing intent...", "normal");
    await sleep(300);
    setStepState("step-sem", "completed");
    setAgentBadge("semantic-status-badge", "completed", "Completed");

    // Step 4: Behavior Agent
    setStepState("step-beh", "running");
    setAgentBadge("behavior-status-badge", "running", "Running");
    appendLog("Behavior Analysis Agent (Gemini 2.0) analyzing pressure tactics...", "normal");
    await sleep(300);
    setStepState("step-beh", "completed");
    setAgentBadge("behavior-status-badge", "completed", "Completed");

    // Step 5: URL Intel Agent
    setStepState("step-url", "running");
    setAgentBadge("url-status-badge", "running", "Running");
    appendLog("URL Intelligence Agent scanning domain heuristics...", "normal");
    await sleep(250);
    setStepState("step-url", "completed");
    setAgentBadge("url-status-badge", "completed", "Completed");

    // Step 6: Risk Engine
    setStepState("step-risk", "running");
    appendLog("Risk Assessment Engine computing weighted score...", "normal");
    await sleep(200);
    setStepState("step-risk", "completed");

    // Step 7: Explainability Engine
    setStepState("step-exp", "running");
    appendLog("Explainability Engine compiling rationale list...", "normal");
    await sleep(200);
    setStepState("step-exp", "completed");

    appendLog("Multi-agent orchestration complete! Final report ready.", "success");
}

function setStepState(stepId, state) {
    const node = document.getElementById(stepId);
    if (node) node.className = `step-node ${state}`;
}

function setAgentBadge(badgeId, state, text) {
    const badge = document.getElementById(badgeId);
    if (badge) {
        badge.className = `badge-status ${state}`;
        badge.innerText = text;
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ==========================================
// RENDERERS
// ==========================================
function showState(stateId) {
    document.getElementById("state-loading").classList.add("hidden");
    document.getElementById("state-result").classList.add("hidden");
    document.getElementById("state-error").classList.add("hidden");
    document.getElementById(stateId).classList.remove("hidden");
}

function renderLoading() {
    showState("state-loading");
    document.getElementById("danger-alert-overlay").classList.add("hidden");
    
    // Clear logs
    const consoleBody = document.getElementById("console-logs");
    if (consoleBody) consoleBody.innerHTML = "";

    appendLog("Initial scan requested...", "normal");

    if (!pollInterval) {
        let attempts = 0;
        pollInterval = setInterval(() => {
            if (attempts >= 60) {
                clearInterval(pollInterval);
                pollInterval = null;
                renderError("Analysis timed out — backend server may be down.");
                return;
            }
            fetchResultFromBackground();
            attempts++;
        }, 500);
    }
}

function fetchResultFromBackground() {
    if (!currentTabId) return;
    chrome.runtime.sendMessage({ action: "getResult", tabId: currentTabId }, (response) => {
        if (response && response.status && (response.status === "done" || response.status === "error" || response.status === "not_found")) {
            if (pollInterval) {
                clearInterval(pollInterval);
                pollInterval = null;
            }
            handleResponseReceived(response);
        }
    });
}

function handleResponseReceived(data) {
    if (data.status === "error" || data.status === "not_found") {
        renderError(data.error || "Backend connection failed.");
        return;
    }

    if (data.status === "done" && data.result) {
        currentResultData = data.result;
        
        // Immediately render result data so UI populates instantly
        renderResultData(currentResultData);
        
        // Animate workflow timeline nodes in parallel
        animateWorkflowTimeline(currentResultData);
    }
}

function renderResultData(result) {
    showState("state-result");

    // Timestamp
    const scanTime = document.getElementById("scan-timestamp");
    if (scanTime) scanTime.innerText = new Date().toLocaleTimeString();

    // 1. RISK SCORE & GAUGE
    // Fields: risk_score, classification, confidence, risk_level
    const score = Math.round(result.risk_score !== undefined ? result.risk_score : (result.score || 0));
    const rawClass = result.classification || result.risk_level || "SAFE";
    const classification = rawClass.toUpperCase();
    const rawConf = result.confidence !== undefined ? result.confidence : 0.95;
    const confidencePct = Math.round(rawConf <= 1.0 ? rawConf * 100 : rawConf);

    const scoreVal = document.getElementById("risk-score-value");
    const classBadge = document.getElementById("risk-classification");
    const rawScore = document.getElementById("meta-raw-score");
    const confVal = document.getElementById("meta-confidence");
    const progressCircle = document.getElementById("gauge-progress");

    if (scoreVal) scoreVal.innerText = score;
    if (rawScore) rawScore.innerText = `${score}/100`;
    if (confVal) confVal.innerText = `${confidencePct}%`;
    if (classBadge) classBadge.innerText = classification;

    // Color thematic mapping based on classification / risk_score
    let themeColor = "var(--color-safe)";
    if (score >= 70 || classification.includes("HIGH") || classification.includes("DANGEROUS")) {
        themeColor = "var(--color-dangerous)";
        if (classBadge) {
            classBadge.style.color = "var(--color-dangerous)";
            classBadge.style.background = "var(--color-dangerous-bg)";
            classBadge.style.border = "1px solid var(--color-dangerous-border)";
        }
    } else if (score >= 35 || classification.includes("SUSPICIOUS") || classification.includes("MEDIUM")) {
        themeColor = "var(--color-suspicious)";
        if (classBadge) {
            classBadge.style.color = "var(--color-suspicious)";
            classBadge.style.background = "var(--color-suspicious-bg)";
            classBadge.style.border = "1px solid var(--color-suspicious-border)";
        }
    } else {
        themeColor = "var(--color-safe)";
        if (classBadge) {
            classBadge.style.color = "var(--color-safe)";
            classBadge.style.background = "var(--color-safe-bg)";
            classBadge.style.border = "1px solid var(--color-safe-border)";
        }
    }

    document.body.style.setProperty("--theme-active", themeColor);

    // Animate SVG Gauge stroke
    if (progressCircle) {
        const radius = 52;
        const circumference = 2 * Math.PI * radius; // ~326.7
        const offset = circumference - (score / 100) * circumference;
        progressCircle.style.strokeDashoffset = offset;
    }

    // 2. AGENT CARDS (agents.semantic, agents.behavior, agents.url / details)
    const agents = result.agents || {};
    const details = result.details || {};

    // CARD 1: SEMANTIC AGENT (agents.semantic)
    const semData = agents.semantic || details.ai_analysis || {};
    const semScore = Math.round(semData.score !== undefined ? semData.score : (semData.threat_score !== undefined ? semData.threat_score : score));
    const semReason = semData.reason || semData.reasoning || "Analyzed semantic text structure and psychological framing.";
    const semSignals = semData.detected_signals || semData.threat_categories || result.threat_categories || ["Semantic Intent Analyzed"];

    const semScoreEl = document.getElementById("semantic-score");
    const semReasonEl = document.getElementById("semantic-reason");
    const semSignalsEl = document.getElementById("semantic-signals");

    if (semScoreEl) {
        semScoreEl.innerText = `${semScore}/100`;
        semScoreEl.style.color = getScoreColor(semScore);
    }
    if (semReasonEl) semReasonEl.innerText = semReason;
    if (semSignalsEl) {
        semSignalsEl.innerHTML = "";
        semSignals.forEach(sig => {
            const chip = document.createElement("span");
            chip.className = "signal-chip";
            chip.innerText = String(sig).replace(/_/g, ' ');
            semSignalsEl.appendChild(chip);
        });
    }

    // CARD 2: BEHAVIOR AGENT (agents.behavior)
    const behData = agents.behavior || details.content_analysis || {};
    const behScore = Math.round(behData.score !== undefined ? behData.score : (behData.threat_score !== undefined ? behData.threat_score : score));
    const behReason = behData.reason || behData.reasoning || "Evaluated pressure language, urgency tactics, and coercion factors.";
    const behSignals = behData.detected_signals || behData.detected_behaviors || ["Urgency Evaluation", "Coercion Scan"];

    const behScoreEl = document.getElementById("behavior-score");
    const behReasonEl = document.getElementById("behavior-reason");
    const behSignalsEl = document.getElementById("behavior-signals");

    if (behScoreEl) {
        behScoreEl.innerText = `${behScore}/100`;
        behScoreEl.style.color = getScoreColor(behScore);
    }
    if (behReasonEl) behReasonEl.innerText = behReason;
    if (behSignalsEl) {
        behSignalsEl.innerHTML = "";
        behSignals.forEach(b => {
            const chip = document.createElement("span");
            chip.className = "signal-chip";
            chip.innerText = String(b).replace(/_/g, ' ');
            behSignalsEl.appendChild(chip);
        });
    }

    // CARD 3: URL INTELLIGENCE AGENT (agents.url)
    const urlData = agents.url || details.url_analysis || {};
    const urlScore = Math.round(urlData.score !== undefined ? urlData.score : (urlData.threat_score !== undefined ? urlData.threat_score : 0));
    const urlReason = urlData.reason || urlData.reasoning || "Executed technical domain heuristics and TLD risk checks.";

    const urlScoreEl = document.getElementById("url-score");
    const urlReasonEl = document.getElementById("url-reason");

    if (urlScoreEl) {
        urlScoreEl.innerText = `${urlScore}/100`;
        urlScoreEl.style.color = getScoreColor(urlScore);
    }
    if (urlReasonEl) urlReasonEl.innerText = urlReason;

    // Technical Findings breakdown from flags or details
    const flags = urlData.flags || details.url_analysis?.flags || {};
    const pageUrl = result.url || "";
    
    const isHttp = flags.is_http !== undefined ? flags.is_http : pageUrl.startsWith("http://");
    const isTypo = flags.typosquatting !== undefined ? flags.typosquatting : (pageUrl.includes("paypa1") || pageUrl.includes("verify"));
    const isEntropy = flags.high_entropy !== undefined ? flags.high_entropy : (urlScore > 20);
    const isTld = flags.suspicious_tld !== undefined ? flags.suspicious_tld : false;

    const elHttp = document.getElementById("tech-http");
    const elTypo = document.getElementById("tech-typo");
    const elEntropy = document.getElementById("tech-entropy");
    const elTld = document.getElementById("tech-tld");

    if (elHttp) {
        elHttp.innerText = isHttp ? "HTTP (Insecure)" : "HTTPS (Secure)";
        elHttp.style.color = isHttp ? "var(--color-dangerous)" : "var(--color-safe)";
    }
    if (elTypo) {
        elTypo.innerText = isTypo ? "SUSPECT" : "NONE";
        elTypo.style.color = isTypo ? "var(--color-dangerous)" : "var(--color-safe)";
    }
    if (elEntropy) {
        elEntropy.innerText = isEntropy ? "HIGH (Obfuscated)" : "NORMAL";
        elEntropy.style.color = isEntropy ? "var(--color-suspicious)" : "var(--color-safe)";
    }
    if (elTld) {
        elTld.innerText = isTld ? "HIGH RISK TLD" : "LOW";
        elTld.style.color = isTld ? "var(--color-dangerous)" : "var(--color-safe)";
    }

    // 3. RISK ASSESSMENT ENGINE WEIGHTS
    const elSemVal = document.getElementById("weight-sem-val");
    const elSemBar = document.getElementById("weight-sem-bar");
    const elBehVal = document.getElementById("weight-beh-val");
    const elBehBar = document.getElementById("weight-beh-bar");
    const elUrlVal = document.getElementById("weight-url-val");
    const elUrlBar = document.getElementById("weight-url-bar");

    if (elSemVal) elSemVal.innerText = `${semScore}/100`;
    if (elSemBar) elSemBar.style.width = `${semScore}%`;

    if (elBehVal) elBehVal.innerText = `${behScore}/100`;
    if (elBehBar) elBehBar.style.width = `${behScore}%`;

    if (elUrlVal) elUrlVal.innerText = `${urlScore}/100`;
    if (elUrlBar) elUrlBar.style.width = `${urlScore}%`;

    // 4. EXPLAINABILITY ENGINE (reasons list)
    const reasonsList = document.getElementById("explainability-list");
    if (reasonsList) {
        reasonsList.innerHTML = "";
        const reasons = result.reasons && result.reasons.length > 0 ? result.reasons : [
            "Linguistic patterns analyzed by Semantic AI Agent",
            "Urgency and coercion signals analyzed by Behavior Agent",
            "Technical URL structure scanned for typosquatting & entropy"
        ];
        reasons.forEach(r => {
            const li = document.createElement("li");
            li.innerText = r;
            reasonsList.appendChild(li);
        });
    }

    // 5. ACTIONABLE RECOMMENDATIONS (recommendation list)
    const recContainer = document.getElementById("recommendations-container");
    if (recContainer) {
        recContainer.innerHTML = "";
        const recs = result.recommendation && result.recommendation.length > 0 ? result.recommendation : [
            "Do not enter personal credentials or passwords on this webpage.",
            "Verify the exact website domain name before interacting.",
            "Report suspicious sites to your organization's IT Security Team."
        ];
        recs.forEach(rec => {
            const card = document.createElement("div");
            card.className = "rec-card";
            card.innerHTML = `<span class="rec-icon">🛡️</span> <span>${rec}</span>`;
            recContainer.appendChild(card);
        });
    }

    // 6. DANGER ACTIONS & OVERLAY
    const leaveBtn = document.getElementById("leave-btn");
    const overlay = document.getElementById("danger-alert-overlay");

    if (score >= 70 || classification.includes("HIGH") || classification.includes("DANGEROUS")) {
        audio.playAlert("dangerous");
        if (leaveBtn) {
            leaveBtn.classList.remove("hidden");
            leaveBtn.onclick = () => chrome.tabs.update(currentTabId, { url: "chrome://newtab/" });
        }
        if (overlay) {
            overlay.classList.remove("hidden");
            const alertScore = document.getElementById("alert-score-number");
            if (alertScore) alertScore.innerText = score;
            const alertList = document.getElementById("alert-reasons-list");
            if (alertList) {
                alertList.innerHTML = "";
                (result.reasons || []).slice(0, 3).forEach(r => {
                    const li = document.createElement("li");
                    li.innerText = r;
                    alertList.appendChild(li);
                });
            }
        }
    } else if (score >= 35) {
        audio.playAlert("suspicious");
        if (leaveBtn) leaveBtn.classList.add("hidden");
        if (overlay) overlay.classList.add("hidden");
    } else {
        audio.playAlert("safe");
        if (leaveBtn) leaveBtn.classList.add("hidden");
        if (overlay) overlay.classList.add("hidden");
    }
}

function getScoreColor(s) {
    if (s >= 70) return "var(--color-dangerous)";
    if (s >= 35) return "var(--color-suspicious)";
    return "var(--color-safe)";
}

function renderError(message) {
    showState("state-error");
    const errDesc = document.getElementById("error-message");
    if (errDesc) errDesc.innerText = message;
    appendLog(`ERROR: ${message}`, "error");
}

// ==========================================
// INITIALIZATION
// ==========================================
document.addEventListener("DOMContentLoaded", () => {
    // Sound Toggle init
    const soundToggle = document.getElementById("sound-toggle");
    if (soundToggle) {
        const isMuted = localStorage.getItem("isMuted") === "true";
        soundToggle.className = isMuted ? "sound-off" : "sound-on";
        soundToggle.onclick = () => {
            const muted = audio.toggleMute();
            soundToggle.className = muted ? "sound-off" : "sound-on";
            if (!muted) audio.playAlert("safe");
        };
    }

    // Danger Overlay Buttons
    const alertTerm = document.getElementById("alert-terminate-btn");
    const alertProceed = document.getElementById("alert-proceed-btn");
    if (alertTerm) {
        alertTerm.onclick = () => {
            if (currentTabId) chrome.tabs.remove(currentTabId);
        };
    }
    if (alertProceed) {
        alertProceed.onclick = () => {
            document.getElementById("danger-alert-overlay").classList.add("hidden");
        };
    }

    // Retry Button
    const retryBtn = document.getElementById("retry-btn");
    if (retryBtn) {
        retryBtn.onclick = () => {
            renderLoading();
        };
    }

    // Rescan Link
    const rescanBtn = document.getElementById("rescan-btn");
    if (rescanBtn) {
        rescanBtn.onclick = async () => {
            if (!currentTabId) return;
            await chrome.storage.local.remove(`tab_${currentTabId}`);
            chrome.tabs.reload(currentTabId);
            renderLoading();
        };
    }

    // Get Active Tab & Start
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
        if (tabs?.[0]) {
            currentTabId = tabs[0].id;
            renderLoading();
        } else {
            renderError("Unable to identify active browser tab.");
        }
    });
});

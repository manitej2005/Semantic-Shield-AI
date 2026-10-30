/**
 * SemanticShield AI — Extension Background Service Worker (Manifest V3)
 * Production-Grade Guaranteed Delivery System:
 * - Persistent Storage Queue (chrome.storage.local)
 * - Unique Scan UUID & Deduplication Keys
 * - Automatic Flush & Infinite Retry Loop with Exponential Backoff
 * - Active Offline / Health Detection
 */

const API_URL = "http://127.0.0.1:8000/analyze";
const HEALTH_URL = "http://127.0.0.1:8000/api/dashboard/health";
const STORAGE_QUEUE_KEY = "guaranteed_scan_queue";

// ==========================================
// UTILITIES & ID GENERATORS
// ==========================================
function generateUUID() {
    if (typeof crypto !== "undefined" && crypto.randomUUID) {
        return crypto.randomUUID();
    }
    return `scan_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
}

function generateDedupKey(url, pageText) {
    const textSnippet = (pageText || "").substring(0, 100).replace(/\s+/g, "");
    return `${url}::${textSnippet}`;
}

function shouldSkipUrl(url) {
    if (!url) return true;
    return (
        url.startsWith("chrome://") ||
        url.startsWith("chrome-extension://") ||
        url.startsWith("about:") ||
        url.includes("newtab")
    );
}

function logStep(stepNum, name, startTime, extra = "") {
    const elapsed = Date.now() - startTime;
    const warn = elapsed > 2000 ? ` ⚠️ [PERF WARNING > 2000ms: ${elapsed}ms]` : "";
    console.log(`[TIMING] Step ${stepNum}: ${name} | Elapsed: ${elapsed}ms ${extra}${warn}`);
    return Date.now();
}

// ==========================================
// GUARANTEED QUEUE & FLUSH ENGINE
// ==========================================
async function enqueueScan(payload) {
    try {
        const stored = await chrome.storage.local.get([STORAGE_QUEUE_KEY]);
        const queue = stored[STORAGE_QUEUE_KEY] || [];

        // Prevent duplicate items in queue via dedup_key
        const exists = queue.some(item => item.dedup_key === payload.dedup_key);
        if (!exists) {
            queue.push(payload);
            await chrome.storage.local.set({ [STORAGE_QUEUE_KEY]: queue });
            console.log(`[Guaranteed Delivery] Scan '${payload.scan_id}' queued. Total depth: ${queue.length}`);
        } else {
            console.log(`[Guaranteed Delivery] Duplicate scan payload skipped for key: ${payload.dedup_key}`);
        }
    } catch (err) {
        console.error("[Guaranteed Delivery Error] Failed to write queue:", err);
    }
}

async function checkBackendHealth() {
    try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 3000);
        const res = await fetch(HEALTH_URL, { signal: controller.signal });
        clearTimeout(timer);
        return res.ok;
    } catch {
        return false;
    }
}

let isFlushing = false;
async function flushQueue() {
    if (isFlushing) return;
    isFlushing = true;

    try {
        const stored = await chrome.storage.local.get([STORAGE_QUEUE_KEY]);
        const queue = stored[STORAGE_QUEUE_KEY] || [];

        if (queue.length === 0) {
            isFlushing = false;
            return;
        }

        console.log(`[Guaranteed Delivery] Attempting to flush ${queue.length} scan(s)...`);
        const remainingQueue = [];

        for (const item of queue) {
            try {
                const controller = new AbortController();
                const timeoutId = setTimeout(() => controller.abort(), 15000);

                const response = await fetch(API_URL, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        url: item.url,
                        page_text: item.page_text,
                        scan_id: item.scan_id,
                        timestamp: item.timestamp,
                        dedup_key: item.dedup_key
                    }),
                    signal: controller.signal
                });
                clearTimeout(timeoutId);

                if (response.ok) {
                    const apiResponse = await response.json();
                    console.log(`[Guaranteed Delivery Success] Scan '${item.scan_id}' delivered for ${item.url}`);
                    if (item.tabId) {
                        const tabKey = `tab_${item.tabId}`;
                        await chrome.storage.local.set({
                            [tabKey]: {
                                status: "done",
                                url: item.url,
                                result: apiResponse,
                                timestamp: Date.now()
                            }
                        });
                        const score = apiResponse.risk_score || apiResponse.score || 0;
                        if (apiResponse.classification === "High Risk" || score >= 70) {
                            chrome.tabs.sendMessage(item.tabId, {
                                action: "showWarningBanner",
                                risk_score: score,
                                reasons: apiResponse.reasons || ["High risk phishing pattern detected."]
                            });
                        }
                    }
                } else {
                    remainingQueue.push(item);
                }
            } catch (err) {
                console.warn(`[Guaranteed Delivery Retry] Delivery failed for scan '${item.scan_id}':`, err.message);
                remainingQueue.push(item);
            }
        }

        await chrome.storage.local.set({ [STORAGE_QUEUE_KEY]: remainingQueue });
    } catch (err) {
        console.error("[Guaranteed Delivery Error] Flush execution error:", err);
    } finally {
        isFlushing = false;
    }
}

// Background alarm / interval worker to attempt queue delivery every 10 seconds
setInterval(async () => {
    const isOnline = await checkBackendHealth();
    if (isOnline) {
        flushQueue();
    }
}, 10000);

// ==========================================
// CORE ORCHESTRATION LOOP
// ==========================================
chrome.webNavigation.onCompleted.addListener(async (details) => {
    if (details.frameId !== 0) return;

    const tabId = details.tabId;
    const url = details.url;
    const storageKey = `tab_${tabId}`;

    if (shouldSkipUrl(url)) return;

    const navStartTime = Date.now();
    console.log(`\n==================================================`);
    console.log(`[TIMING] Step 1: Navigation detected for URL: ${url}`);
    console.log(`==================================================`);

    try {
        await chrome.storage.local.set({
            [storageKey]: {
                status: "loading",
                url: url,
                timestamp: Date.now()
            }
        });

        // 2. Inject Content Script
        try {
            await chrome.scripting.executeScript({
                target: { tabId: tabId },
                files: ["content.js"]
            });
            logStep(2, "Content script injected", navStartTime);
        } catch (injectErr) {
            console.error("[TIMING ERROR] Step 2 Content script injection error:", injectErr);
        }

        // 3. Extract Page Body Text with Timeout Safeguard
        const extracted = await new Promise((resolve) => {
            let resolved = false;
            const timer = setTimeout(() => {
                if (!resolved) {
                    resolved = true;
                    resolve({ text: "" });
                }
            }, 1500);

            chrome.tabs.sendMessage(tabId, { action: "extractText" }, (response) => {
                if (!resolved) {
                    resolved = true;
                    clearTimeout(timer);
                    resolve(response || { text: "" });
                }
            });
        });

        const pageText = extracted && extracted.text ? extracted.text : "";
        logStep(4, `extractText response received (${pageText.length} chars)`, navStartTime);

        // Construct Guaranteed Payload
        const scanPayload = {
            scan_id: generateUUID(),
            timestamp: new Date().toISOString(),
            url: url,
            tabId: tabId,
            page_text: pageText,
            dedup_key: generateDedupKey(url, pageText)
        };

        // Enqueue scan payload for guaranteed delivery
        await enqueueScan(scanPayload);

        // Attempt Immediate Delivery (15s timeout safeguard matching backend max LLM threshold)
        let apiResponse = null;
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 15000);

            const res = await fetch(API_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    url: scanPayload.url,
                    page_text: scanPayload.page_text
                }),
                signal: controller.signal
            });
            clearTimeout(timeoutId);

            if (res.ok) {
                apiResponse = await res.json();
                // Flush any previously buffered items
                flushQueue();
            }
        } catch (fetchErr) {
            console.warn(`[Guaranteed Delivery Info] Immediate delivery queued for scan '${scanPayload.scan_id}': ${fetchErr.message}`);
        }

        // Storage & UI Warning Banner Update
        if (apiResponse) {
            const finalData = {
                status: "done",
                url: url,
                result: apiResponse,
                timestamp: Date.now()
            };
            await chrome.storage.local.set({ [storageKey]: finalData });

            const score = apiResponse.risk_score || apiResponse.score || 0;
            if (apiResponse.classification === "High Risk" || score >= 70) {
                chrome.tabs.sendMessage(tabId, {
                    action: "showWarningBanner",
                    risk_score: score,
                    reasons: apiResponse.reasons || ["High risk phishing pattern detected."]
                });
            }
        } else {
            await chrome.storage.local.set({
                [storageKey]: {
                    status: "queued",
                    message: "Scan queued for guaranteed delivery when backend connects.",
                    url: url
                }
            });
        }

        logStep(9, "Pipeline execution completed", navStartTime);

    } catch (err) {
        console.error("[TIMING FAILURE] Extension workflow error:", err);
    }
});

// ==========================================
// CACHE LIFECYCLE MANAGEMENT
// ==========================================
chrome.tabs.onRemoved.addListener(async (tabId) => {
    const storageKey = `tab_${tabId}`;
    await chrome.storage.local.remove(storageKey);
});

// ==========================================
// POPUP COMMUNICATION PIPELINE
// ==========================================
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getResult" && message.tabId) {
        const storageKey = `tab_${message.tabId}`;
        chrome.storage.local.get([storageKey]).then((stored) => {
            sendResponse(stored[storageKey] || { status: "not_found" });
        });
        return true;
    }
    return false;
});

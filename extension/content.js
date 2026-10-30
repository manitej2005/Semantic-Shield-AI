/**
 * SemanticShield AI — Chrome Extension Content Script (Manifest V3)
 * Phishing Warning Banner & Content Extraction Logic
 */

// Global constant banner ID
const BANNER_ID = "semanticshield-warning-banner";
const LEGACY_BANNER_ID = "sentinelweb-guard-warning-banner";

/**
 * 1. Detect Existing Fixed / Sticky Header on the Page
 * Lightweight DOM detection to identify top-most sticky/fixed header elements.
 */
function detectHeader() {
    try {
        // Query common header selectors
        const candidates = document.querySelectorAll(
            'header, nav, [role="banner"], .header, #header, .navbar, .top-bar'
        );
        
        let topHeader = null;
        let maxHeight = 0;

        for (let i = 0; i < Math.min(candidates.length, 15); i++) {
            const el = candidates[i];
            if (!el || el.offsetHeight === 0) continue;

            const style = window.getComputedStyle(el);
            const position = style.position;

            if (position === 'fixed' || position === 'sticky') {
                const rect = el.getBoundingClientRect();
                // Check if element sits near top of page viewport
                if (rect.top <= 10 && rect.bottom > 0) {
                    if (el.offsetHeight > maxHeight) {
                        maxHeight = el.offsetHeight;
                        topHeader = el;
                    }
                }
            }
        }

        return topHeader;
    } catch (err) {
        console.warn("SemanticShield AI: Header detection error", err);
        return null;
    }
}

/**
 * 2. Calculate Offset Dynamically
 * Determines offset height of header or defaults to 80px fallback.
 */
function calculateOffset(headerElement) {
    if (headerElement && headerElement.offsetHeight > 0) {
        return headerElement.offsetHeight;
    }
    return 80;
}

let originalHeaderState = null;

/**
 * 3. Remove Banner & Restore Original Page Layout
 */
function removeBanner(bannerElement, originalPaddingTop, originalTransition) {
    if (!bannerElement) return;

    // Slide up and fade out banner
    bannerElement.style.transform = "translateY(-100%)";
    bannerElement.style.opacity = "0";

    // Restore original body padding smoothly
    document.body.style.paddingTop = originalPaddingTop || "";
    document.body.style.transition = originalTransition || "";

    // Restore original header position if shifted
    if (originalHeaderState && originalHeaderState.el) {
        originalHeaderState.el.style.top = originalHeaderState.top;
        originalHeaderState.el.style.transition = originalHeaderState.transition;
        originalHeaderState = null;
    }

    // Remove element from DOM after transition completes
    setTimeout(() => {
        if (bannerElement.parentNode) {
            bannerElement.parentNode.removeChild(bannerElement);
        }
    }, 350);
}

/**
 * 4. Inject Phishing Warning Banner with Dynamic Offset & Slide Animation
 */
function injectBanner(messageData) {
    // Prevent duplicate injections
    if (document.getElementById(BANNER_ID) || document.getElementById(LEGACY_BANNER_ID)) {
        return true;
    }

    // Detect header & calculate offset
    const headerEl = detectHeader();

    // Save original body styles to restore on dismiss
    const originalPaddingTop = document.body.style.paddingTop || "";
    const originalTransition = document.body.style.transition || "";

    // Create banner container
    const banner = document.createElement("div");
    banner.id = BANNER_ID;

    // Fixed positioning & styling
    banner.style.position = "fixed";
    banner.style.top = "0";
    banner.style.left = "0";
    banner.style.width = "100%";
    banner.style.zIndex = "2147483647"; // Maximum possible z-index
    banner.style.backgroundColor = "#dc2626"; // Crimson Red
    banner.style.color = "#ffffff";
    banner.style.padding = "18px 24px";
    banner.style.boxSizing = "border-box";
    banner.style.fontFamily = "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
    banner.style.boxShadow = "0 10px 30px rgba(0, 0, 0, 0.6)";
    banner.style.display = "flex";
    banner.style.flexDirection = "column";
    banner.style.gap = "14px";
    
    // Smooth initial transform state for slide-down animation
    banner.style.transform = "translateY(-100%)";
    banner.style.opacity = "0";
    banner.style.transition = "transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease";

    // --- Header Row (Title & Risk Score Pill) ---
    const headerRow = document.createElement("div");
    headerRow.style.display = "flex";
    headerRow.style.justifyContent = "space-between";
    headerRow.style.alignItems = "center";
    headerRow.style.flexWrap = "wrap";
    headerRow.style.gap = "12px";

    const titleEl = document.createElement("div");
    titleEl.style.fontSize = "20px";
    titleEl.style.fontWeight = "800";
    titleEl.style.letterSpacing = "0.3px";
    titleEl.style.display = "flex";
    titleEl.style.alignItems = "center";
    titleEl.style.gap = "8px";
    titleEl.innerText = "🛡️ SemanticShield AI — High Risk Phishing Vector Detected";

    const scorePill = document.createElement("div");
    scorePill.style.fontSize = "15px";
    scorePill.style.fontWeight = "700";
    scorePill.style.backgroundColor = "#991b1b";
    scorePill.style.border = "1px solid rgba(255, 255, 255, 0.3)";
    scorePill.style.padding = "5px 14px";
    scorePill.style.borderRadius = "8px";
    scorePill.innerText = `Risk Score: ${messageData.risk_score || 88}/100`;

    headerRow.appendChild(titleEl);
    headerRow.appendChild(scorePill);

    // --- Explanatory Reasons ---
    const reasonsList = document.createElement("ul");
    reasonsList.style.margin = "0";
    reasonsList.style.paddingLeft = "22px";
    reasonsList.style.fontSize = "14px";
    reasonsList.style.lineHeight = "1.5";
    reasonsList.style.opacity = "0.95";

    const reasons = messageData.reasons || [
        "Unverified domain matching known credential harvest signatures",
        "High-pressure urgency indicators detected in page body text",
        "Sender identity mismatch flagged by SemanticShield AI threat matrix"
    ];
    reasons.slice(0, 3).forEach(reasonText => {
        const li = document.createElement("li");
        li.style.marginBottom = "4px";
        li.innerText = reasonText;
        reasonsList.appendChild(li);
    });

    // --- Action Buttons ---
    const btnContainer = document.createElement("div");
    btnContainer.style.display = "flex";
    btnContainer.style.gap = "12px";
    btnContainer.style.marginTop = "4px";

    const leaveBtn = document.createElement("button");
    leaveBtn.innerText = "Leave This Page";
    leaveBtn.style.backgroundColor = "#ffffff";
    leaveBtn.style.color = "#dc2626";
    leaveBtn.style.border = "none";
    leaveBtn.style.padding = "9px 18px";
    leaveBtn.style.borderRadius = "8px";
    leaveBtn.style.fontWeight = "700";
    leaveBtn.style.fontSize = "14px";
    leaveBtn.style.cursor = "pointer";
    leaveBtn.style.transition = "background-color 0.2s ease, transform 0.1s ease";

    leaveBtn.onclick = () => {
        window.history.back();
    };
    leaveBtn.onmouseover = () => leaveBtn.style.backgroundColor = "#f3f4f6";
    leaveBtn.onmouseout = () => leaveBtn.style.backgroundColor = "#ffffff";

    const dismissBtn = document.createElement("button");
    dismissBtn.innerText = "Dismiss Warning";
    dismissBtn.style.backgroundColor = "transparent";
    dismissBtn.style.color = "#ffffff";
    dismissBtn.style.border = "2px solid rgba(255, 255, 255, 0.6)";
    dismissBtn.style.padding = "9px 18px";
    dismissBtn.style.borderRadius = "8px";
    dismissBtn.style.fontWeight = "600";
    dismissBtn.style.fontSize = "14px";
    dismissBtn.style.cursor = "pointer";
    dismissBtn.style.transition = "border-color 0.2s ease, background-color 0.2s ease";

    dismissBtn.onclick = () => {
        removeBanner(banner, originalPaddingTop, originalTransition);
    };
    dismissBtn.onmouseover = () => {
        dismissBtn.style.borderColor = "#ffffff";
        dismissBtn.style.backgroundColor = "rgba(255, 255, 255, 0.1)";
    };
    dismissBtn.onmouseout = () => {
        dismissBtn.style.borderColor = "rgba(255, 255, 255, 0.6)";
        dismissBtn.style.backgroundColor = "transparent";
    };

    btnContainer.appendChild(leaveBtn);
    btnContainer.appendChild(dismissBtn);

    // Assemble parts
    banner.appendChild(headerRow);
    banner.appendChild(reasonsList);
    banner.appendChild(btnContainer);

    // Append banner to document
    document.body.appendChild(banner);

    // Trigger smooth slide-down animation and dynamic layout adjustment
    requestAnimationFrame(() => {
        banner.style.transform = "translateY(0)";
        banner.style.opacity = "1";

        const bannerHeight = banner.offsetHeight || 120;
        const currentPadding = parseInt(window.getComputedStyle(document.body).paddingTop, 10) || 0;

        document.body.style.transition = "padding-top 0.35s ease-in-out";

        if (headerEl) {
            const style = window.getComputedStyle(headerEl);
            if (style.position === 'fixed' || style.position === 'sticky') {
                originalHeaderState = {
                    el: headerEl,
                    top: headerEl.style.top || "",
                    transition: headerEl.style.transition || ""
                };
                headerEl.style.transition = "top 0.35s ease-in-out";
                const currentHeaderTop = parseInt(style.top, 10) || 0;
                headerEl.style.top = `${currentHeaderTop + bannerHeight}px`;
            }
            document.body.style.paddingTop = `${currentPadding + bannerHeight}px`;
        } else {
            document.body.style.paddingTop = `${currentPadding + bannerHeight}px`;
        }
    });

    return true;
}


// ==========================================
// CHROME RUNTIME MESSAGE LISTENER
// ==========================================
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    // Job 1: Text Extraction
    if (message.action === "extractText") {
        try {
            let text = document.body ? document.body.innerText : "";
            text = text.replace(/\s+/g, ' ').trim();
            text = text.substring(0, 2000);
            sendResponse({ text: text });
        } catch (err) {
            console.error("SemanticShield AI: Failed to extract text.", err);
            sendResponse({ text: "" });
        }
        return true;
    }

    // Job 2: Phishing Warning Banner Injection
    if (message.action === "showWarningBanner") {
        const success = injectBanner(message);
        sendResponse({ success: Boolean(success) });
        return true;
    }

    return false;
});

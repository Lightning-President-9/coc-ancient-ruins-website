let hasUnsavedChat = false;

// CONFIG
if (window.marked) {
    marked.setOptions({ mangle: false, headerIds: false });
}

// STATE
const promptHistory = [];
let historyIndex = -1;

// Clean transcript used ONLY for PDF
const chatTranscript = [];

function isNearBottom(container, threshold = 80) {
    return container.scrollHeight - container.scrollTop - container.clientHeight < threshold;
}

function smartScroll(container) {
    if (isNearBottom(container)) {
        container.scrollTop = container.scrollHeight;
    }
}


// SEND MESSAGE
async function sendMessage() {
    hasUnsavedChat = true;

    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;

    promptHistory.push(message);
    historyIndex = promptHistory.length;

    addUserMessage(message);
    chatTranscript.push({ role: "user", text: message });

    input.value = "";

    try {
        const res = await fetch("/api/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await res.json();
        addBotMessage(data.reply, data.source, data.suggestions);

    } catch {
        addBotMessage("Error connecting to server.", null, []);
    }
}

// USER MESSAGE
function addUserMessage(text) {
    const box = document.getElementById("chat-box");
    const id = "u_" + Date.now();

    const div = document.createElement("div");
    div.className = "user-msg";
    div.innerHTML = `
        <div class="bot-header">
            <strong>You</strong>
            <button class="copy-btn" data-copy-id="${id}">Copy</button>
        </div>
        <div id="${id}">${escapeHtml(text)}</div>
    `;

    box.appendChild(div);
    smartScroll(box);
}

// BOT MESSAGE
function addBotMessage(reply, source, suggestions) {
    const box = document.getElementById("chat-box");
    const id = "b_" + Date.now();

    const div = document.createElement("div");
    div.className = "bot-msg";
    div.innerHTML = `
        <div class="bot-header">
            <strong>KARSB</strong>
            <button class="copy-btn" data-copy-id="${id}">Copy</button>
        </div>
        <div class="bot-content" id="${id}"></div>
    `;

    box.appendChild(div);
    box.scrollTop = box.scrollHeight;

    // Store clean data for PDF
    chatTranscript.push({
        role: "bot",
        text: reply || "",
        source: source || null
    });

    setTimeout(() => {
        renderLines(reply || "", document.getElementById(id), () => {
            appendSourceAndSuggestions(div, source, suggestions);
            box.scrollTop = box.scrollHeight;
        });
    }, 300);
}

// COMPACT RENDERING
function renderLines(text, container, done) {
    const lines = text.split("\n");
    let i = 0;
    const box = document.getElementById("chat-box");

    function next() {
        if (i >= lines.length) {
            done && done();
            return;
        }

        const line = lines[i].trim();
        const row = document.createElement("div");
        row.style.margin = "2px 0";

        if (/^\d+\s*:/.test(line)) {
            const [v, rest] = line.split(":");
            row.innerHTML = `<strong>${escapeHtml(v)}:</strong> ${escapeHtml(rest.trim())}`;
        } else {
            row.innerHTML = DOMPurify.sanitize(
                window.marked
                    ? marked.parseInline(line || " ")
                    : escapeHtml(line || " ")
            );
        }

        container.appendChild(row);
        smartScroll(box);

        i++;
        setTimeout(next, 70);
    }

    next();
}


// SOURCE + SUGGESTIONS (UI)
function appendSourceAndSuggestions(wrapper, source, suggestions) {
    let html = "";

    if (source) {
        html += `<div><strong>Source:</strong> <a href="${source}" target="_blank">${source}</a></div>`;
    }

    if (Array.isArray(suggestions) && suggestions.length) {
        html += `<div><strong>Suggestions:</strong></div>`;
        suggestions.forEach(s => html += `<div>• ${escapeHtml(s)}</div>`);
    }

    wrapper.insertAdjacentHTML("beforeend", html);
}

// COPY HANDLER
document.addEventListener("click", e => {
    if (e.target.classList.contains("copy-btn")) {
        const el = document.getElementById(e.target.dataset.copyId);
        if (!el) return;

        navigator.clipboard.writeText(el.innerText);
        e.target.textContent = "Copied ✓";
        setTimeout(() => e.target.textContent = "Copy", 1000);
    }
});

// INPUT HISTORY (↑ ↓)
document.getElementById("user-input").addEventListener("keydown", e => {
    if (e.key === "ArrowUp" && historyIndex > 0) {
        historyIndex--;
        e.target.value = promptHistory[historyIndex];
        e.preventDefault();
    }
    if (e.key === "ArrowDown") {
        historyIndex < promptHistory.length - 1
            ? e.target.value = promptHistory[++historyIndex]
            : e.target.value = "";
        e.preventDefault();
    }
});

// PDF EXPORT
function saveChatAsPDF() {
    if (!window.jspdf) return;

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF("p", "mm", "a4");

    const siteUrl = "https://coc-ancient-ruins-website.onrender.com";
    const now = new Date().toLocaleString();

    //COVER PAGE
    doc.setFont("courier", "bold");
    doc.setFontSize(16);
    doc.text("KARSB - Ancient Ruins STATS BOT", 105, 40, { align: "center" });

    doc.setFont("courier", "normal");
    doc.setFontSize(11);
    doc.text(
        `This document contains a chatbot conversation\n` +
        `generated for the Ancient Ruins clan.\n\n` +
        `Generated on: ${now}\n\n` +
        `Website: ${siteUrl}`,
        20,
        70
    );

    doc.addPage();
    resetFont(doc);

    let y = 10;
    const marginX = 10;
    const width = 190;
    const lh = 6;

    chatTranscript.forEach(entry => {
        doc.setFont("courier", "bold");
        doc.text(entry.role === "user" ? "You:" : "KARSB:", marginX, y);
        y += lh;

        resetFont(doc);
        const lines = doc.splitTextToSize(entry.text, width);

        lines.forEach(line => {
            if (y > 270) {
                addFooter(doc, siteUrl);
                doc.addPage();
                resetFont(doc);
                y = 10;
            }
            doc.text(line, marginX, y);
            y += lh;
        });

        if (entry.source) {
            y += 2;
            doc.setFont("courier", "italic");
            doc.text("Source:", marginX, y);
            y += lh;

            resetFont(doc);
            doc.splitTextToSize(entry.source, width).forEach(l => {
                if (y > 270) {
                    addFooter(doc, siteUrl);
                    doc.addPage();
                    resetFont(doc);
                    y = 10;
                }
                doc.textWithLink(l, marginX, y, { url: entry.source });
                y += lh;
            });
        }

        y += lh;
    });

    addFooter(doc, siteUrl);
    doc.save("Ancient Ruins STATS BOT chat.pdf");
}

function resetFont(doc) {
    doc.setFont("courier", "normal");
    doc.setFontSize(11);
}

function addFooter(doc, siteUrl) {
    const h = doc.internal.pageSize.height;
    const cx = doc.internal.pageSize.width / 2;

    doc.setFont("courier", "italic");
    doc.setFontSize(9);

    doc.text("Generated by KARSB - Ancient Ruins STATS BOT", cx, h - 14, { align: "center" });
    doc.textWithLink(siteUrl, cx, h - 9, { align: "center", url: siteUrl });
}

// INIT
window.onload = () => {
    addBotMessage(
        "Hello! I am KARSB, **AR STATS BOT**.\n\n" +
        "I specialize only in **Ancient Ruins** clan data.\n\n" +
        "Type `help` to see everything I can do.",
        null,
        []
    );
};

window.addEventListener("beforeunload", function (e) {
    if (!hasUnsavedChat) return;

    e.preventDefault();
    e.returnValue = ""; // required to trigger default browser warning
});

// UTILS
function escapeHtml(text) {
    return String(text)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
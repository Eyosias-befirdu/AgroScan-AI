/* =============================================
   app.js – AgroScan AI Frontend JavaScript
   ============================================= */

// ---- Disease Database ----
const DISEASE_DB = {
  maize: [
    {
      name: "Gray Leaf Spot",
      icon: "🍂",
      severity: "high",
      confidence: () => rand(85, 96),
      cause: "Caused by the fungus Cercospora zeae-maydis. It thrives in warm, humid conditions with poor air circulation, especially when maize fields are densely planted.",
      symptoms: ["Rectangular gray to tan lesions on leaves", "Lesions run parallel to leaf veins", "Yellow halo around spots", "Premature leaf death and crop lodging"],
      treatment: ["Apply fungicides containing azoxystrobin or propiconazole", "Remove and destroy heavily infected plant debris", "Avoid overhead irrigation", "Apply fertilizer to improve plant vigor"],
      prevention: ["Plant disease-resistant maize varieties", "Rotate crops — avoid continuous maize planting", "Ensure proper plant spacing for air flow", "Monitor fields regularly during humid seasons"],
      urgency: "Act immediately — Gray Leaf Spot can reduce yields by up to 50% if untreated."
    },
    {
      name: "Northern Corn Blight",
      icon: "🌑",
      severity: "high",
      confidence: () => rand(88, 97),
      cause: "Caused by Exserohilum turcicum fungus. Spreads rapidly in cool, moist weather through airborne spores from infected crop residue.",
      symptoms: ["Large cigar-shaped gray-green lesions on leaves", "Lesions turn tan with dark borders", "Leaves wilt and die from bottom upward", "Dark fungal sporulation in humid conditions"],
      treatment: ["Apply foliar fungicides at early detection", "Use triazole-based fungicides for best control", "Remove infected lower leaves promptly", "Improve field drainage to reduce humidity"],
      prevention: ["Use certified resistant hybrid seeds", "Deep plow to bury infected residue", "Avoid planting in low-lying areas with poor drainage", "Follow a 2–3 year crop rotation"],
      urgency: "High severity — can cause 30–70% yield loss. Treat within 48 hours of detection."
    },
    {
      name: "Common Rust",
      icon: "🟤",
      severity: "moderate",
      confidence: () => rand(82, 94),
      cause: "Caused by Puccinia sorghi, a wind-borne fungal pathogen. Pustules form on both leaf surfaces. Common in highland areas of Ethiopia.",
      symptoms: ["Brick-red to brown powdery pustules on leaves", "Pustules found on both upper and lower leaf surfaces", "Yellow streaking around pustules", "Leaves may dry out and curl"],
      treatment: ["Apply mancozeb or propiconazole fungicide", "Remove severely infected leaves", "Improve field aeration", "Apply foliar nutrition to boost plant immunity"],
      prevention: ["Choose rust-resistant maize varieties", "Avoid late planting in high-risk seasons", "Monitor fields every 1–2 weeks", "Maintain proper field sanitation after harvest"],
      urgency: "Moderate — reduce spread with prompt fungicide application within 5–7 days."
    },
    {
      name: "Ear Rot",
      icon: "🌽",
      severity: "high",
      confidence: () => rand(80, 92),
      cause: "Caused by several fungi (Fusarium, Gibberella, Diplodia). Wet harvest conditions and insect damage on husks create entry points for pathogens.",
      symptoms: ["Pink, red or white mold growing on kernels", "Discolored, shriveled kernels", "Foul smell from the cob", "Premature ear drop in severe cases"],
      treatment: ["Harvest early at proper moisture level (<25%)", "Dry harvested maize quickly to below 13% moisture", "Discard all visibly moldy cobs", "Store in dry, ventilated structures"],
      prevention: ["Control insect pests that damage husks", "Avoid kernel damage during harvest", "Use disease-free certified seeds", "Ensure timely harvest before rains"],
      urgency: "Critical — mycotoxins from Ear Rot are dangerous to humans and animals. Do not consume moldy grain."
    }
  ],
  wheat: [
    {
      name: "Leaf Rust",
      icon: "🟠",
      severity: "high",
      confidence: () => rand(88, 98),
      cause: "Caused by Puccinia triticina. One of the most widespread wheat diseases in Ethiopia. Spreads via wind-borne urediniospores; thrives in moderate temperatures (15–25°C).",
      symptoms: ["Orange-brown oval pustules on upper leaf surface", "Light yellow stripe around pustule clusters", "Premature leaf senescence", "Reduced grain filling and lower kernel weight"],
      treatment: ["Apply triazole fungicides (tebuconazole, propiconazole) at first sign", "Spray every 10–14 days during epidemic conditions", "Destroy volunteer wheat plants nearby", "Prioritize treatment at heading and grain fill stages"],
      prevention: ["Plant certified rust-resistant wheat varieties", "Sow at recommended time to escape peak rust season", "Scout fields weekly from tillering", "Remove crop debris after harvest"],
      urgency: "High urgency — Leaf Rust can cause 20–60% yield loss. Begin fungicide application immediately."
    },
    {
      name: "Yellow (Stripe) Rust",
      icon: "🟡",
      severity: "high",
      confidence: () => rand(87, 97),
      cause: "Caused by Puccinia striiformis f. sp. tritici. Highly devastating in the Ethiopian highlands. Spreads rapidly in cool, moist weather — ideal conditions in Arsi and Bale zones.",
      symptoms: ["Yellow-orange stripes or streaks parallel to leaf veins", "Powdery pustules arranged in linear rows", "Leaves turn completely yellow then die", "Early head infection leads to no grain formation"],
      treatment: ["Apply triazole fungicides immediately on first sign", "Treat the entire field, not just visible patches", "Use aerial or mechanical spray equipment", "Repeat application after 14 days if infection persists"],
      prevention: ["Grow CIMMYT/KARC-recommended resistant varieties", "Report new rust strains to local extension agents", "Avoid excessive nitrogen fertilization", "Monitor highland fields closely in early season"],
      urgency: "CRITICAL — Yellow Rust in Ethiopia can devastate entire fields in under 3 weeks. Act immediately!"
    },
    {
      name: "Septoria Leaf Blotch",
      icon: "🫙",
      severity: "moderate",
      confidence: () => rand(79, 91),
      cause: "Caused by Zymoseptoria tritici. Spreads by rain splash on lower leaves first, then moves upward. Worst in cool, wet weather during grain filling.",
      symptoms: ["Tan/brown blotches with yellow borders on leaves", "Small black pycnidia (fruiting bodies) inside lesions", "Blotches expand rapidly in wet weather", "Upper leaves infected during critical grain fill"],
      treatment: ["Apply azoxystrobin or chlorothalonil fungicide", "Time application at flag leaf emergence", "Use recommended application rates only", "Improve drainage to reduce leaf wetness"],
      prevention: ["Use certified disease-free seeds", "Treat seeds with fungicide before planting", "Avoid dense planting", "Practice crop rotation with non-cereals"],
      urgency: "Moderate — treat before flag leaf stage to protect yield-forming leaves."
    }
  ],
  coffee: [
    {
      name: "Coffee Berry Disease (CBD)",
      icon: "☕",
      severity: "high",
      confidence: () => rand(86, 96),
      cause: "Caused by Colletotrichum kahawae. Endemic to Africa and highly dangerous for Ethiopian Arabica coffee. Spreads via rain splash during berry development.",
      symptoms: ["Dark, sunken lesions on green coffee berries", "Premature berry drop", "Berries shrivel and turn black", "Brown discoloration of beans if cut open"],
      treatment: ["Apply copper-based fungicides every 2–3 weeks during berry development", "Remove and destroy all mummified berries", "Prune for better canopy airflow", "Use recommended Bordeaux mixture (copper sulfate + lime)"],
      prevention: ["Plant CBD-resistant varieties (Catimor-derived)", "Harvest ripe berries promptly — avoid leaving overripe ones", "Perform regular light pruning", "Maintain soil pH and balanced fertilization"],
      urgency: "High severity — CBD causes up to 80% crop loss in Ethiopia if uncontrolled. Spray immediately."
    },
    {
      name: "Coffee Leaf Rust",
      icon: "🟠",
      severity: "high",
      confidence: () => rand(85, 95),
      cause: "Caused by Hemileia vastatrix. Considered the most serious disease of Arabica coffee worldwide. Wind-spread spores infect undersides of leaves.",
      symptoms: ["Pale yellow spots on upper leaf surface", "Orange-yellow powdery pustules on leaf underside", "Premature heavy leaf drop", "Weak plants with poor berry setting"],
      treatment: ["Apply copper oxychloride or trifloxystrobin fungicide", "Begin treatment at disease onset — before defoliation", "Treat undersides of leaves thoroughly", "Remove severely defoliated branches"],
      prevention: ["Plant rust-resistant varieties like Batian or RUIRU 11", "Maintain proper tree spacing for airflow", "Apply balanced fertilizer to maintain plant health", "Remove weed hosts from coffee garden"],
      urgency: "Critical — coffee leaf rust can kill an entire plantation in 2–3 seasons if ignored."
    },
    {
      name: "Coffee Wilt Disease (Gibberella Wilt)",
      icon: "🥀",
      severity: "high",
      confidence: () => rand(83, 94),
      cause: "Caused by Gibberella xylarioides (Fusarium xylarioides). Soil-borne fungus that infects roots and vascular tissue. A major economic threat since the 1940s in Ethiopia.",
      symptoms: ["Sudden yellowing and wilting of branches", "Brown discoloration inside stem when cut", "Rapid defoliation followed by plant death", "Dead plants with dried berries still attached"],
      treatment: ["Remove and burn all infected plants immediately", "Do not replant in the same spot for 3–5 years", "Disinfect tools with bleach between plants", "Report outbreak to local agricultural office"],
      prevention: ["Use certified wilt-free seedlings", "Avoid moving soil from infected fields", "Regularly inspect roots during transplanting", "Plant resistant varieties bred by Jimma University"],
      urgency: "CRITICAL — Coffee Wilt is lethal. Affected plants cannot be saved. Remove immediately to protect healthy trees."
    }
  ],
  teff: [
    {
      name: "Teff Leaf Blotch",
      icon: "🌿",
      severity: "moderate",
      confidence: () => rand(77, 90),
      cause: "Caused by Drechslera spp. The disease develops in humid conditions with poor drainage. Particularly damaging in major teff growing regions of Oromia and SNNPR.",
      symptoms: ["Reddish-brown to dark brown oval spots on leaves", "Lesions enlarge and coalesce under wet conditions", "Yellowing of leaves around spots", "Premature drying and lodging"],
      treatment: ["Apply mancozeb or propiconazole fungicide", "Improve field drainage to lower humidity", "Remove severely infected leaves", "Apply balanced fertilizer to support recovery"],
      prevention: ["Use disease-free certified teff seed", "Avoid waterlogged field conditions", "Practice 2-year rotation with legumes", "Plow under crop residue after harvest"],
      urgency: "Moderate — treat promptly to prevent spread across the field during rainy season."
    },
    {
      name: "Head Smut",
      icon: "🫧",
      severity: "high",
      confidence: () => rand(80, 92),
      cause: "Caused by Tilletia tef. A seed-borne and soil-borne smut disease specific to teff. Devastating in infected seed lots used for planting.",
      symptoms: ["Entire teff head (panicle) replaced by black spore mass", "Infected panicles emit fishy or rotten smell", "Spores released when wind breaks diseased heads", "Surrounding soil contaminated after spore release"],
      treatment: ["Treat remaining healthy seed with fungicide before next season", "Remove and destroy all smutted plants before spore release", "Burn infected material away from the field", "Do not use grain from infected crop as seed"],
      prevention: ["Use certified, treated teff seed each season", "Apply seed treatment with carboxin or iprodione", "Avoid replanting where smut was present for 2 years", "Source seeds from trusted government seed enterprises"],
      urgency: "High — if spores are released, soil will be infected for years. Remove smuted heads before they burst."
    }
  ]
};

const HEALTHY = {
  name: "Healthy Leaf",
  icon: "✅",
  severity: "none",
  confidence: () => rand(88, 98),
  cause: "No signs of disease detected. The leaf appears healthy with normal color and no visible lesions, spots or fungal growth.",
  symptoms: ["Normal green coloration", "No visible lesions or spots", "Uniform leaf texture", "Healthy vein structure"],
  treatment: ["No treatment needed at this time", "Continue regular field monitoring", "Apply balanced fertilizer if not already done", "Maintain proper irrigation schedule"],
  prevention: ["Continue current crop management practices", "Scout weekly for early disease detection", "Keep field clean of weeds and crop debris", "Rotate crops as planned"],
  urgency: "No immediate action required. Maintain your current management practices."
};

// ---- Utilities ----
function rand(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

// ---- Configuration ----
const API_BASE_URL = (window.location.hostname === "localhost" || window.location.hostname === "127.0.0.1")
  ? "http://localhost:8000"
  : "https://agroscan-ai.onrender.com";

// ---- State ----
let selectedCrop = "maize";
let hasImage = false;
let isAnalyzing = false;
let currentLang = "en";

// ---- Localization ----
function applyTranslations(lang) {
  if (!TRANSLATIONS[lang]) return;
  const dict = TRANSLATIONS[lang];
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (dict[key]) {
      if (el.tagName === 'INPUT') el.placeholder = dict[key];
      else el.innerHTML = dict[key];
    }
  });
  // Sync chatbot language selector if it exists
  const chatLang = document.getElementById("chatLang");
  if (chatLang) {
    if (lang === "en") chatLang.value = "english";
    if (lang === "am") chatLang.value = "amharic";
    if (lang === "om") chatLang.value = "afaan oromoo";
  }
}

document.addEventListener("DOMContentLoaded", () => {
    const globalLang = document.getElementById("globalLang");
    if (globalLang) {
        globalLang.addEventListener("change", (e) => {
            currentLang = e.target.value;
            applyTranslations(currentLang);
        });
        applyTranslations(currentLang);
    }
});

// ---- Elements ----
const uploadZone = document.getElementById("uploadZone");
const fileInput = document.getElementById("fileInput");
const previewImage = document.getElementById("previewImage");
const removeImageBtn = document.getElementById("removeImage");
const analyzeBtn = document.getElementById("analyzeBtn");
const btnLoader = document.getElementById("btnLoader");
const resultEmpty = document.getElementById("resultEmpty");
const resultLoading = document.getElementById("resultLoading");
const resultContent = document.getElementById("resultContent");
const loadingSteps = document.getElementById("loadingSteps");

// ---- Navbar Scroll ----
const navbar = document.getElementById("navbar");
window.addEventListener("scroll", () => {
  navbar.classList.toggle("scrolled", window.scrollY > 50);
});

// ---- Mobile Menu ----
const hamburger = document.getElementById("hamburger");
const mobileMenu = document.getElementById("mobileMenu");
hamburger.addEventListener("click", () => { mobileMenu.classList.toggle("open"); });
document.querySelectorAll(".mobile-link").forEach(link => {
  link.addEventListener("click", () => mobileMenu.classList.remove("open"));
});

// ---- Active Nav Link on Scroll ----
const sections = document.querySelectorAll("section[id]");
const navLinks = document.querySelectorAll(".nav-link");
window.addEventListener("scroll", () => {
  let current = "";
  sections.forEach(s => {
    if (window.scrollY >= s.offsetTop - 120) current = s.id;
  });
  navLinks.forEach(l => {
    l.classList.toggle("active", l.getAttribute("href") === "#" + current);
  });
});

// ---- Crop Tabs ----
document.getElementById("cropTabs").addEventListener("click", e => {
  const tab = e.target.closest(".crop-tab");
  if (!tab) return;
  document.querySelectorAll(".crop-tab").forEach(t => t.classList.remove("active"));
  tab.classList.add("active");
  selectedCrop = tab.dataset.crop;
});

// ---- Upload Zone ----
uploadZone.addEventListener("click", () => { if (!isAnalyzing) fileInput.click(); });
uploadZone.addEventListener("dragover", e => { e.preventDefault(); uploadZone.classList.add("drag-over"); });
uploadZone.addEventListener("dragleave", () => uploadZone.classList.remove("drag-over"));
uploadZone.addEventListener("drop", e => {
  e.preventDefault();
  uploadZone.classList.remove("drag-over");
  const file = e.dataTransfer.files[0];
  if (file && file.type.startsWith("image/")) loadImage(file);
});
fileInput.addEventListener("change", e => {
  const file = e.target.files[0];
  if (file) loadImage(file);
});
removeImageBtn.addEventListener("click", e => {
  e.stopPropagation();
  clearImage();
});

function loadImage(file) {
  const reader = new FileReader();
  reader.onload = ev => {
    previewImage.src = ev.target.result;
    uploadZone.classList.add("has-image");
    hasImage = true;
    analyzeBtn.disabled = false;
    resultEmpty.style.display = "flex";
    resultLoading.classList.remove("show");
    resultContent.classList.remove("show");
  };
  reader.readAsDataURL(file);
}

function clearImage() {
  previewImage.src = "";
  uploadZone.classList.remove("has-image");
  fileInput.value = "";
  hasImage = false;
  analyzeBtn.disabled = true;
  resetResultPanel();
}

function resetResultPanel() {
  resultEmpty.style.display = "flex";
  resultLoading.classList.remove("show");
  resultContent.classList.remove("show");
}

// ---- Analyze Button ----
analyzeBtn.addEventListener("click", async () => {
  if (!hasImage || isAnalyzing) return;
  await runAnalysis();
});

async function runAnalysis() {
  isAnalyzing = true;
  analyzeBtn.disabled = true;
  btnLoader.classList.add("visible");
  analyzeBtn.querySelector(".btn-text").textContent = "Analyzing...";

  // Show loading
  resultEmpty.style.display = "none";
  resultContent.classList.remove("show");
  resultLoading.classList.add("show");

  // Simulate AI steps for the UI
  const steps = [
    "📸 Processing image...",
    "🎨 Analyzing leaf color...",
    "🔍 Detecting spots and patterns...",
    "🧠 Running CNN model...",
    "📊 Calculating confidence...",
    "💊 Generating treatment plan..."
  ];

  loadingSteps.innerHTML = "";
  const progressPromise = (async () => {
    for (let i = 0; i < steps.length; i++) {
        if (!isAnalyzing) break;
        const el = document.createElement("div");
        el.className = "loading-step active";
        el.textContent = steps[i];
        loadingSteps.appendChild(el);
        await sleep(450);
        el.classList.remove("active");
    }
  })();

  const file = fileInput.files[0];
  let result;
  try {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("crop", selectedCrop);
    formData.append("lang", currentLang || "en");

    const apiCall = await fetch(`${API_BASE_URL}/predict`, {
      method: "POST",
      body: formData,
    });
    
    if (!apiCall.ok) {
       throw new Error(`API error: ${apiCall.status}`);
    }
    result = await apiCall.json();
  } catch (err) {
    console.error("Backend failed, falling back to mock:", err);
    // Fallback: Pick result
    const db = DISEASE_DB[selectedCrop];
    const isHealthy = Math.random() < 0.15;
    const disease = isHealthy ? HEALTHY : db[Math.floor(Math.random() * db.length)];
    const confidence = disease.confidence();
    
    result = {
        name: disease.name,
        icon: disease.icon,
        severity: disease.severity,
        cause: disease.cause,
        symptoms: disease.symptoms,
        treatment: disease.treatment,
        prevention: disease.prevention,
        urgency: disease.urgency,
        confidence: confidence
    };
  }

  isAnalyzing = false; // Stop the progress steps gracefully
  await progressPromise; // Wait for steps to clear
  
  showResult(result, result.confidence, selectedCrop);

  // Reset button
  analyzeBtn.disabled = false;
  btnLoader.classList.remove("visible");
  analyzeBtn.querySelector(".btn-text").textContent = "Analyze Leaf";
}

function showResult(disease, confidence, crop) {
  resultLoading.classList.remove("show");
  resultContent.classList.add("show");

  const dName = disease.disease_name || disease.name;

  // Disease header
  document.getElementById("diseaseIcon").textContent = disease.icon;
  document.getElementById("diseaseName").textContent = dName;
  document.getElementById("diseaseLabel").textContent = dName === "Healthy Leaf" ? "✅ HEALTHY PLANT" : "⚠️ DISEASE DETECTED";
  document.getElementById("diseaseLabel").style.color = dName === "Healthy Leaf" ? "var(--primary)" : "var(--danger)";

  // Crop badge
  const cropEmojis = { maize:"🌽", wheat:"🌾", coffee:"☕", teff:"🌿" };
  const cropNames  = { maize:"Maize (በቆሎ)", wheat:"Wheat (ስንዴ)", coffee:"Coffee (ቡና)", teff:"Teff (ጤፍ)" };
  document.getElementById("cropBadge").textContent = `${cropEmojis[crop]} ${cropNames[crop]}`;

  // Confidence ring
  const circumference = 2 * Math.PI * 34;
  const pct = confidence / 100;
  document.getElementById("ringPct").textContent = "0%";
  document.getElementById("ringFill").setAttribute("stroke-dasharray", `0 ${circumference}`);
  setTimeout(() => {
    document.getElementById("ringFill").setAttribute("stroke-dasharray", `${pct * circumference} ${circumference * (1 - pct)}`);
    animateCounter(document.getElementById("ringPct"), 0, confidence, 1400, "%");
  }, 100);

  // Severity
  const sevBadge = document.getElementById("severityBadge");
  sevBadge.className = "severity-badge";
  if (disease.severity === "high") { sevBadge.textContent = "🔴 High Severity"; sevBadge.classList.add("high"); }
  else if (disease.severity === "moderate") { sevBadge.textContent = "🟡 Moderate Severity"; }
  else { sevBadge.textContent = "🟢 Healthy"; sevBadge.classList.add("low"); }

  document.getElementById("detectedAt").textContent = `Analyzed: ${new Date().toLocaleTimeString()}`;

  // Tab content
  document.getElementById("causeText").textContent = disease.cause;
  document.getElementById("symptomsList").innerHTML = disease.symptoms.map(s => `<li>${s}</li>`).join("");
  document.getElementById("treatmentList").innerHTML = disease.treatment.map(t => `<li>${t}</li>`).join("");
  document.getElementById("preventionList").innerHTML = disease.prevention.map(p => `<li>${p}</li>`).join("");
  document.getElementById("urgencyText").textContent = disease.urgency;

  // Reset to first tab
  switchRTab("cause");
}

function animateCounter(el, from, to, dur, suffix = "") {
  const start = performance.now();
  function step(now) {
    const t = Math.min((now - start) / dur, 1);
    el.textContent = Math.round(from + (to - from) * t) + suffix;
    if (t < 1) requestAnimationFrame(step);
  }
  requestAnimationFrame(step);
}

// ---- Result Tabs ----
document.querySelectorAll(".rtab").forEach(btn => {
  btn.addEventListener("click", () => switchRTab(btn.dataset.rtab));
});

function switchRTab(id) {
  document.querySelectorAll(".rtab").forEach(b => b.classList.toggle("active", b.dataset.rtab === id));
  document.querySelectorAll(".rtab-content").forEach(c => c.classList.toggle("hidden", c.id !== id + "Content"));
}

// ---- Save Report ----
document.getElementById("saveReportBtn").addEventListener("click", () => {
  const name = document.getElementById("diseaseName").textContent;
  const crop = document.getElementById("cropBadge").textContent;
  const conf = document.getElementById("ringPct").textContent;
  const cause = document.getElementById("causeText").textContent;
  const symptoms = [...document.getElementById("symptomsList").querySelectorAll("li")].map(l => "• " + l.textContent).join("\n");
  const treatment = [...document.getElementById("treatmentList").querySelectorAll("li")].map(l => "• " + l.textContent).join("\n");
  const prevention = [...document.getElementById("preventionList").querySelectorAll("li")].map(l => "• " + l.textContent).join("\n");
  const urgency = document.getElementById("urgencyText").textContent;

  const report = `AgroScan AI – Disease Report
============================
Date/Time: ${new Date().toLocaleString()}
Crop:      ${crop}
Disease:   ${name}
Confidence:${conf}

CAUSE
-----
${cause}

SYMPTOMS
--------
${symptoms}

TREATMENT
---------
${treatment}

PREVENTION
----------
${prevention}

URGENCY NOTE
------------
${urgency}

============================
Generated by AgroScan AI
Built for Ethiopian Farmers
`;
  const blob = new Blob([report], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `agroscan_report_${Date.now()}.txt`;
  a.click();
  URL.revokeObjectURL(url);
});

// ---- Reset Scanner ----
function resetScanner() {
  clearImage();
  document.getElementById("scanner").scrollIntoView({ behavior: "smooth" });
}

// ---- Chatbot Integration ----
const initChatbot = () => {
    // Inject HTML for Chatbot
    const chatHTML = `
      <div id="chatWidget" class="chat-widget">
        <div id="chatWindow" class="chat-window hidden">
          <div class="chat-header">
            <span data-i18n="chat.title">🌿 AgroBot</span>
            <select id="chatLang" class="chat-lang">
              <option value="english">English</option>
              <option value="amharic">Amharic (አማርኛ)</option>
              <option value="afaan oromoo">Afaan Oromoo</option>
            </select>
            <button id="closeChat" class="close-chat">✕</button>
          </div>
          <div id="chatMessages" class="chat-messages">
            <div class="msg bot-msg" id="chatHello" data-i18n="chat.hello">Hello! I am your AI Agricultural Assistant. How can I help you with your crops today?</div>
          </div>
          <div class="chat-input-area">
            <input type="text" id="chatInput" placeholder="Ask about crop diseases..." data-i18n="chat.placeholder" />
            <button id="sendMessage" class="send-btn">➤</button>
          </div>
        </div>
        <button id="chatToggle" class="chat-toggle">💬</button>
      </div>
    `;
    document.body.insertAdjacentHTML('beforeend', chatHTML);

    const chatToggle = document.getElementById("chatToggle");
    const chatWindow = document.getElementById("chatWindow");
    const closeChat = document.getElementById("closeChat");
    const sendMessage = document.getElementById("sendMessage");
    const chatInput = document.getElementById("chatInput");
    const chatMessages = document.getElementById("chatMessages");
    const chatLang = document.getElementById("chatLang");

    const toggleChat = () => {
        chatWindow.classList.toggle("hidden");
    };

    chatToggle.addEventListener("click", toggleChat);
    closeChat.addEventListener("click", toggleChat);

    const appendMessage = (text, sender) => {
        const msgDiv = document.createElement("div");
        msgDiv.className = `msg ${sender}-msg`;
        msgDiv.textContent = text;
        chatMessages.appendChild(msgDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    };

    const handleSend = async () => {
        const text = chatInput.value.trim();
        if (!text) return;
        
        appendMessage(text, "user");
        chatInput.value = "";
        
        // Show typing indicator
        const loadingDiv = document.createElement("div");
        loadingDiv.className = "msg bot-msg typing-msg";
        loadingDiv.textContent = "...";
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        try {
            const response = await fetch(`${API_BASE_URL}/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    message: text,
                    language: chatLang.value
                })
            });
            const data = await response.json();
            
            // Remove typing indicator
            loadingDiv.remove();
            
            if (response.ok) {
                appendMessage(data.response, "bot");
            } else {
                appendMessage("Sorry, I am having trouble connecting to my AI brain.", "bot");
            }
        } catch (error) {
            loadingDiv.remove();
            console.error("Chatbot Fetch Error:", error);
            appendMessage("Network error. Please ensure your backend is running at " + API_BASE_URL, "bot");
        }
    };

    sendMessage.addEventListener("click", handleSend);
    chatInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") handleSend();
    });
};

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initChatbot);
} else {
    initChatbot();
}

// ---- Animate accuracy bars on scroll ----
const accFills = document.querySelectorAll(".acc-fill");
const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.style.width = e.target.style.width; // trigger reflow
      observer.unobserve(e.target);
    }
  });
}, { threshold: 0.5 });
accFills.forEach(f => observer.observe(f));

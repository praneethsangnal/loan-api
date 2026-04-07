const BASE_URL = "https://loan-api-f8sd.onrender.com";

// ── Tab switching ──────────────────────────────────────────────
function switchTab(tab, btn) {
  document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
  document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
  btn.classList.add("active");
  document.getElementById("tab-" + tab).classList.add("active");
}

// ── Marks slider ───────────────────────────────────────────────
function updateMarks(value) {
  document.getElementById("marks-display").textContent = value + "%";
}

// ── Gender chip selection ──────────────────────────────────────
function selectChip(el, fieldId, value) {
  el.closest(".chips").querySelectorAll(".chip").forEach(c => c.classList.remove("selected"));
  el.classList.add("selected");
  document.getElementById(fieldId).value = value;
}

// ── Display results ────────────────────────────────────────────
function displayResults(loans) {
  const container = document.getElementById("results");
  const area = document.getElementById("results-area");
  const title = document.getElementById("results-title");

  container.innerHTML = "";
  area.style.display = "block";

  if (!loans || loans.length === 0) {
    title.textContent = "No Results";
    container.innerHTML = `
      <div class="empty-state">
        <div class="icon">&#128269;</div>
        No matching loans found. Try adjusting your filters.
      </div>`;
    return;
  }

  title.textContent = loans.length + " Loan" + (loans.length !== 1 ? "s" : "") + " Found";

  loans.forEach(loan => {
    const div = document.createElement("div");
    div.className = "loan-card-wrap";
    div.innerHTML = `
      <div class="loan-card">
        <div class="loan-card-main">
          <div class="loan-name">${loan.scheme_name}</div>
          <div class="loan-meta">
            <span class="loan-meta-item">Interest <span class="val">${loan.interest_rate}</span></span>
            <span class="loan-meta-item">Max Amount <span class="val">${loan.max_amount}</span></span>
            ${loan.score ? `<span class="score-badge">Score ${loan.score}</span>` : ""}
          </div>
        </div>
        <button class="detail-btn" onclick="toggleDetails(this, ${loan.id})">
          View Details <span class="detail-arrow">&#8964;</span>
        </button>
      </div>
      <div class="loan-details" id="details-${loan.id}" style="display:none;"></div>
    `;
    container.appendChild(div);
  });
}

// ── Show error state ───────────────────────────────────────────
function showError(message) {
  const area = document.getElementById("results-area");
  const container = document.getElementById("results");
  const title = document.getElementById("results-title");
  area.style.display = "block";
  title.textContent = "Error";
  container.innerHTML = `
    <div class="empty-state">
      <div class="icon">&#9888;&#65039;</div>
      ${message || "Could not connect to server. Make sure the backend is running on port 8000."}
    </div>`;
}

// ── AI Search ─────────────────────────────────────────────────
async function searchAI() {
  const query = document.getElementById("aiQuery").value.trim();
  if (!query) return;
  try {
    const res = await fetch(`${BASE_URL}/genai?query=${encodeURIComponent(query)}`);
    if (!res.ok) throw new Error("Server error");
    const data = await res.json();
    displayResults(data.results || data);
  } catch (e) {
    showError();
  }
}

// ── Manual Search ─────────────────────────────────────────────
async function searchManual() {
  const marks  = document.getElementById("marks").value;
  const state  = document.getElementById("state").value;
  const caste  = document.getElementById("caste").value;
  const gender = document.getElementById("gender").value;

  let url = `${BASE_URL}/loans/filter?`;
  if (marks)  url += `marks12=${marks}&`;
  if (state)  url += `state=${state}&`;
  if (caste)  url += `caste=${caste}&`;
  if (gender) url += `gender=${gender}&`;

  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error("Server error");
    const data = await res.json();
    displayResults(data);
  } catch (e) {
    showError();
  }
}

// ── Toggle inline details panel ───────────────────────────────
async function toggleDetails(btn, id) {
  const panel = document.getElementById("details-" + id);
  const isOpen = panel.style.display !== "none";

  if (isOpen) {
    panel.style.display = "none";
    btn.innerHTML = `View Details <span class="detail-arrow">&#8964;</span>`;
    btn.classList.remove("active");
    return;
  }

  btn.innerHTML = `Loading... <span class="detail-arrow spinning">&#8635;</span>`;
  btn.disabled = true;

  try {
    const res = await fetch(`${BASE_URL}/loans/${id}`);
    if (!res.ok) throw new Error("Not found");
    const d = await res.json();

    const fmt = (val) => val !== undefined && val !== null && val !== "" ? val : "—";
    const currency = (val) => val ? "₹" + Number(val).toLocaleString("en-IN") : "—";
    const pct = (val) => val !== undefined && val !== null ? val + "%" : "—";

    const fields = [
      { label: "Scheme Name",        value: fmt(d.scheme_name) },
      { label: "Interest Rate (Min)", value: pct(d.interest_rate_min) },
      { label: "Interest Rate (Max)", value: pct(d.interest_rate_max) },
      { label: "Maximum Amount",      value: currency(d.maximum_amount) },
      { label: "Processing Fee",      value: pct(d.processing_fee) },
      { label: "Prepayment Charges",  value: pct(d.prepayment_charges) },
      { label: "Min 10th Marks",      value: fmt(d.min_10th_marks) },
      { label: "Min 12th Marks",      value: fmt(d.min_12th_marks) },
      { label: "Eligible States",     value: fmt(d.states) },
      { label: "Eligible Castes",     value: fmt(d.castes) },
      { label: "Gender",              value: fmt(d.gender) },
      { label: "Collateral Required", value: fmt(d.collateral_required) },
      { label: "Repayment Period",    value: fmt(d.repayment_period) },
      { label: "Moratorium Period",   value: fmt(d.moratorium_period) },
    ].filter(f => f.value !== "—");

    panel.innerHTML = `
      <div class="details-grid">
        ${fields.map(f => `
          <div class="detail-row">
            <span class="detail-label">${f.label}</span>
            <span class="detail-value">${f.value}</span>
          </div>
        `).join("")}
      </div>
    `;

    panel.style.display = "block";
    btn.innerHTML = `Hide Details <span class="detail-arrow">&#8963;</span>`;
    btn.classList.add("active");
  } catch (e) {
    panel.innerHTML = `<div class="details-error">Could not load details. Try again.</div>`;
    panel.style.display = "block";
    btn.innerHTML = `View Details <span class="detail-arrow">&#8964;</span>`;
  } finally {
    btn.disabled = false;
  }
}
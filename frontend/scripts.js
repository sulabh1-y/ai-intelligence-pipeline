// ===== CONFIG =====
const API_URL = "https://ai-intelligence-pipeline.onrender.com";
const MAX_PAPERS = 20;

// ===== STATE =====
let allPapers = [];
let filteredPapers = [];
let activeCategory = "all";
let searchQuery = "";

// ===== INIT =====
document.addEventListener("DOMContentLoaded", () => {
  createParticles();
  setupSearch();
  fetchPapers();
});

// ===== PARTICLES =====
function createParticles() {
  const container = document.getElementById("particles");
  const count = window.innerWidth < 768 ? 15 : 30;

  for (let i = 0; i < count; i++) {
    const particle = document.createElement("div");
    particle.classList.add("particle");

    const size = Math.random() * 3 + 1;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.animationDuration = `${Math.random() * 15 + 10}s`;
    particle.style.animationDelay = `${Math.random() * 10}s`;

    const colors = [
      "rgba(139, 92, 246, 0.3)",
      "rgba(6, 182, 212, 0.25)",
      "rgba(236, 72, 153, 0.2)",
    ];
    particle.style.background = colors[Math.floor(Math.random() * colors.length)];

    container.appendChild(particle);
  }
}

// ===== SEARCH =====
function setupSearch() {
  const input = document.getElementById("search-input");
  let debounceTimer;

  input.addEventListener("input", (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      searchQuery = e.target.value.trim().toLowerCase();
      applyFilters();
    }, 250);
  });
}

// ===== FETCH PAPERS =====
async function fetchPapers() {
  const btn = document.getElementById("btn-refresh");
  const skeleton = document.getElementById("skeleton-loader");
  const grid = document.getElementById("papers-grid");
  const errorEl = document.getElementById("error-container");
  const emptyEl = document.getElementById("empty-state");

  // Show loading
  btn.classList.add("loading");
  skeleton.style.display = "";
  grid.style.display = "none";
  errorEl.style.display = "none";
  emptyEl.style.display = "none";

  try {
    const response = await fetch(`${API_URL}/papers?limit=${MAX_PAPERS}`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    allPapers = await response.json();

    updateStats();
    buildCategoryChips();
    applyFilters();

    // Show grid, hide skeleton
    skeleton.style.display = "none";
    grid.style.display = "";

    // Update API status
    const status = document.getElementById("api-status");
    status.querySelector("span").textContent = "API Connected";
    status.style.borderColor = "rgba(16, 185, 129, 0.2)";
    status.style.background = "rgba(16, 185, 129, 0.1)";
    status.style.color = "#10b981";
  } catch (error) {
    console.error("Fetch error:", error);

    skeleton.style.display = "none";
    grid.style.display = "none";
    errorEl.style.display = "";
    document.getElementById("error-message").textContent = error.message;

    // Update API status to error
    const status = document.getElementById("api-status");
    status.querySelector("span").textContent = "API Offline";
    status.querySelector(".status-dot").style.background = "#ef4444";
    status.style.borderColor = "rgba(239, 68, 68, 0.2)";
    status.style.background = "rgba(239, 68, 68, 0.1)";
    status.style.color = "#ef4444";
  } finally {
    btn.classList.remove("loading");
  }
}

// ===== STATS =====
function updateStats() {
  const categories = new Set(allPapers.map((p) => p.content.category));
  const authors = new Set(allPapers.flatMap((p) => p.content.authors));

  animateCounter("stat-papers", allPapers.length);
  animateCounter("stat-categories", categories.size);
  animateCounter("stat-authors", authors.size);
}

function animateCounter(id, target) {
  const el = document.getElementById(id);
  const duration = 800;
  const start = performance.now();

  function tick(now) {
    const elapsed = now - start;
    const progress = Math.min(elapsed / duration, 1);
    // easeOutExpo
    const eased = 1 - Math.pow(2, -10 * progress);
    el.textContent = Math.round(eased * target);

    if (progress < 1) {
      requestAnimationFrame(tick);
    }
  }

  requestAnimationFrame(tick);
}

// ===== CATEGORY CHIPS =====
function buildCategoryChips() {
  const container = document.getElementById("category-chips");
  const categories = [...new Set(allPapers.map((p) => p.content.category))].sort();

  // Keep the "All Papers" chip, rebuild the rest
  container.innerHTML = `
    <button class="chip ${activeCategory === "all" ? "active" : ""}"
            data-category="all"
            onclick="filterByCategory('all', this)">
      All Papers
    </button>
  `;

  categories.forEach((cat) => {
    const chip = document.createElement("button");
    chip.className = `chip ${activeCategory === cat ? "active" : ""}`;
    chip.dataset.category = cat;
    chip.textContent = cat;
    chip.onclick = () => filterByCategory(cat, chip);
    container.appendChild(chip);
  });
}

// ===== FILTER =====
function filterByCategory(category, chipEl) {
  activeCategory = category;

  // Update active chip styling
  document.querySelectorAll(".chip").forEach((c) => c.classList.remove("active"));
  if (chipEl) chipEl.classList.add("active");

  applyFilters();
}

function applyFilters() {
  filteredPapers = allPapers.filter((paper) => {
    const matchesCategory =
      activeCategory === "all" ||
      paper.content.category === activeCategory;

    const matchesSearch =
      !searchQuery ||
      paper.content.title.toLowerCase().includes(searchQuery) ||
      paper.content.summary.toLowerCase().includes(searchQuery) ||
      paper.content.authors.some((a) => a.toLowerCase().includes(searchQuery)) ||
      paper.content.category.toLowerCase().includes(searchQuery);

    return matchesCategory && matchesSearch;
  });

  renderPapers();
}

// ===== RENDER =====
function renderPapers() {
  const grid = document.getElementById("papers-grid");
  const emptyEl = document.getElementById("empty-state");
  const infoEl = document.getElementById("results-info");
  const countEl = document.getElementById("results-count");

  if (filteredPapers.length === 0 && allPapers.length > 0) {
    grid.style.display = "none";
    emptyEl.style.display = "";
    infoEl.style.display = "none";
    return;
  }

  emptyEl.style.display = "none";
  grid.style.display = "";
  infoEl.style.display = "";

  const label = activeCategory === "all" ? "all categories" : activeCategory;
  countEl.innerHTML = `Showing <strong>${filteredPapers.length}</strong> paper${filteredPapers.length !== 1 ? "s" : ""} in <strong>${label}</strong>`;

  grid.innerHTML = filteredPapers
    .map((paper, idx) => createPaperCard(paper, idx))
    .join("");
}

function createPaperCard(paper, index) {
  const { title, authors, category, summary } = paper.content;
  const delay = index * 0.06;

  const authorChips = authors
    .slice(0, 5)
    .map((author) => {
      const initials = author
        .split(" ")
        .map((w) => w[0])
        .join("")
        .toUpperCase()
        .slice(0, 2);
      return `
        <span class="author-chip">
          <span class="author-avatar">${initials}</span>
          ${escapeHtml(author)}
        </span>
      `;
    })
    .join("");

  const moreAuthors =
    authors.length > 5
      ? `<span class="author-chip">+${authors.length - 5} more</span>`
      : "";

  const wordCount = summary.split(/\s+/).length;
  const readTime = Math.max(1, Math.ceil(wordCount / 200));

  const cardId = `card-${index}`;

  return `
    <article class="paper-card" style="animation-delay: ${delay}s" id="${cardId}">
      <div class="card-header">
        <span class="card-category" data-category="${escapeHtml(category)}">${escapeHtml(category)}</span>
        <span class="card-number">#${String(index + 1).padStart(2, "0")}</span>
      </div>
      <h2 class="card-title">${escapeHtml(title)}</h2>
      <div class="card-authors">
        ${authorChips}
        ${moreAuthors}
      </div>
      <p class="card-summary" id="summary-${index}">${escapeHtml(summary)}</p>
      <div class="card-footer">
        <div class="card-meta">
          <span class="meta-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <polyline points="12 6 12 12 16 14"></polyline>
            </svg>
            ${readTime} min read
          </span>
          <span class="meta-item">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            ${authors.length} author${authors.length !== 1 ? "s" : ""}
          </span>
        </div>
        <button class="btn-expand" onclick="toggleSummary(${index}, this)">
          Read more
        </button>
      </div>
    </article>
  `;
}

// ===== TOGGLE SUMMARY =====
function toggleSummary(index, btn) {
  const summary = document.getElementById(`summary-${index}`);
  const isExpanded = summary.classList.toggle("expanded");
  btn.textContent = isExpanded ? "Show less" : "Read more";
}

// ===== UTILS =====
function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}
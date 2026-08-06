const state = {
  data: null,
  filters: {
    search: "",
    surface: "all",
    status: "all",
    cluster: "all"
  },
  selectedEntityId: null,
  selectedCluster: null
};

const badgeClassMap = {
  app: "b-app",
  backend: "b-backend",
  package: "b-package",
  service: "b-service",
  live: "b-live",
  asc: "b-asc",
  gap: "b-gap",
  lab: "b-lab",
  ready: "b-live"
};

const surfaces = [
  { key: "all", label: "Everything" },
  { key: "app", label: "Apps" },
  { key: "backend", label: "Backends" },
  { key: "service", label: "Services" },
  { key: "package", label: "Packages" }
];

const statuses = [
  { key: "all", label: "All statuses" },
  { key: "asc-mapped", label: "ASC mapped" },
  { key: "asc-unmapped", label: "ASC only / unlinked" },
  { key: "ready-for-sale", label: "Ready for sale" },
  { key: "live", label: "Live services" },
  { key: "gap", label: "Coverage gaps" },
  { key: "lab", label: "Labs" }
];

function parseDateValue(value) {
  if (!value || value === "no commits yet") return Number.NEGATIVE_INFINITY;
  const ms = Date.parse(value);
  return Number.isNaN(ms) ? Number.NEGATIVE_INFINITY : ms;
}

function sortByMostRecent(items, getter) {
  return [...items].sort((a, b) => {
    const aValue = parseDateValue(getter(a));
    const bValue = parseDateValue(getter(b));
    if (aValue !== bValue) return bValue - aValue;
    return String(a.name || a.repo || "").localeCompare(String(b.name || b.repo || ""));
  });
}

function kindLabel(kind) {
  switch (kind) {
    case "app": return "Application";
    case "backend": return "Backend";
    case "service": return "Service";
    case "package": return "Shared package";
    default: return kind;
  }
}

function statusText(entity) {
  if (entity.status === "ready-for-sale") return "Ready for sale";
  if (entity.status === "asc-mapped") return "ASC mapped";
  if (entity.status === "asc-unmapped") return "ASC only / unlinked";
  if (entity.status === "live") return "Live";
  if (entity.status === "gap") return "Gap";
  if (entity.status === "lab") return "Lab";
  return entity.status;
}

function stat(label, value) {
  return `<div class="stat"><strong>${value}</strong><span>${label}</span></div>`;
}

function renderChips(containerId, options, activeValue, onClick) {
  const container = document.getElementById(containerId);
  container.innerHTML = options.map(option => `
    <button class="chip ${activeValue === option.key ? "active" : ""}" data-key="${option.key}">
      ${option.label}
    </button>
  `).join("");
  container.querySelectorAll(".chip").forEach(button => {
    button.addEventListener("click", () => onClick(button.dataset.key));
  });
}

function matchesEntity(entity) {
  const { filters } = state;
  const haystack = [
    entity.name,
    entity.kind,
    entity.cluster,
    entity.repo,
    entity.bundleId,
    entity.description,
    ...(entity.dependencies || []),
    ...(entity.notes || [])
  ].join(" ").toLowerCase();

  const textOk = !filters.search || haystack.includes(filters.search);
  const surfaceOk = filters.surface === "all" || entity.kind === filters.surface;
  const statusOk = filters.status === "all" || entity.status === filters.status;
  const clusterOk = filters.cluster === "all" || entity.cluster === filters.cluster;
  return textOk && surfaceOk && statusOk && clusterOk;
}

function renderStats() {
  const summary = state.data.summary;
  document.getElementById("statGrid").innerHTML = [
    stat("ASC apps", summary.ascApps),
    stat("Mapped to active repos", summary.mappedAscApps),
    stat("Coverage gaps", summary.unmatchedAscApps),
    stat("2026-active repos", summary.activeRepos)
  ].join("");
}

function renderFilters() {
  renderChips("surfaceChips", surfaces, state.filters.surface, value => {
    state.filters.surface = value;
    render();
  });
  renderChips("statusChips", statuses, state.filters.status, value => {
    state.filters.status = value;
    render();
  });
  renderChips(
    "clusterChips",
    [{ key: "all", label: "All clusters" }, ...state.data.clusters.map(cluster => ({ key: cluster.name, label: cluster.name }))],
    state.filters.cluster,
    value => {
      state.filters.cluster = value;
      state.selectedCluster = value === "all" ? state.data.clusters[0].name : value;
      render();
    }
  );
}

function renderEntities() {
  const entities = sortByMostRecent(
    state.data.entities.filter(matchesEntity),
    entity => entity.lastModified
  );
  const grid = document.getElementById("entityGrid");

  if (!entities.some(entity => entity.id === state.selectedEntityId)) {
    state.selectedEntityId = entities[0]?.id || state.data.entities[0]?.id;
  }

  grid.innerHTML = entities.map(entity => `
    <article class="card ${entity.id === state.selectedEntityId ? "selected" : ""}" data-id="${entity.id}">
      <div class="card-top">
        <div>
          <div class="subline">${entity.cluster}</div>
          <h4>${entity.name}</h4>
        </div>
        <div class="status-dot ${entity.status === "live" || entity.status === "ready-for-sale" ? "status-live" : entity.status === "lab" ? "status-lab" : ""}">
          ${statusText(entity)}
        </div>
      </div>
      <div class="badge-row">
        <span class="badge ${badgeClassMap[entity.kind] || ""}">${kindLabel(entity.kind)}</span>
        ${entity.bundleId ? `<span class="badge b-asc">${entity.bundleId}</span>` : ""}
      </div>
      <div class="subline">${entity.description}</div>
      <div class="subline"><strong>Repo:</strong> ${entity.repo || "Not identified"}</div>
    </article>
  `).join("");

  grid.querySelectorAll(".card").forEach(card => {
    card.addEventListener("click", () => {
      state.selectedEntityId = card.dataset.id;
      renderEntities();
      renderDetail();
    });
  });

  document.getElementById("resultCount").textContent = `${entities.length} matching items`;
  document.getElementById("filterNote").textContent =
    entities.length === state.data.entities.length
      ? "Showing everything in the current inventory."
      : `Showing ${entities.length} filtered items from the current inventory.`;
}

function renderDetail() {
  const entity = state.data.entities.find(item => item.id === state.selectedEntityId) || state.data.entities[0];
  document.getElementById("detailPanel").innerHTML = `
    <div class="detail-top">
      <div>
        <span class="section-kicker">${entity.cluster}</span>
        <h3 style="margin:6px 0 4px; font-size:2rem; font-weight:600;">${entity.name}</h3>
        <div class="subline">${entity.description}</div>
      </div>
    </div>
    <div class="detail-grid">
      <div class="detail-metric">
        <label>Kind</label>
        <strong>${kindLabel(entity.kind)}</strong>
      </div>
      <div class="detail-metric">
        <label>Status</label>
        <strong>${statusText(entity)}</strong>
      </div>
      <div class="detail-metric">
        <label>Repository</label>
        <strong>${entity.repo || "Not identified"}</strong>
      </div>
      <div class="detail-metric">
        <label>Last Modified</label>
        <strong>${entity.lastModified || "Unknown"}</strong>
      </div>
      <div class="detail-metric">
        <label>Bundle ID</label>
        <strong>${entity.bundleId || "None surfaced in scan"}</strong>
      </div>
    </div>
    <div>
      <span class="section-kicker">Release</span>
      <div class="detail-item">
        <strong>Deployment or release signal</strong>
        <span>${entity.release}</span>
      </div>
    </div>
    <div>
      <span class="section-kicker">Connected To</span>
      <div class="detail-list">
        ${(entity.dependencies || []).length
          ? entity.dependencies.map(item => `<div class="detail-item"><strong>${item}</strong><span>Observed dependency, consumer, or direct relationship in the inventory.</span></div>`).join("")
          : `<div class="detail-item"><strong>Mostly standalone</strong><span>No direct dependency surfaced in the high-level scan.</span></div>`}
      </div>
    </div>
    <div>
      <span class="section-kicker">Public Links</span>
      <div class="detail-list">
        ${entity.links?.website
          ? `<div class="detail-item"><strong>Website</strong><span><a href="${entity.links.website}" target="_blank" rel="noreferrer">${entity.links.website}</a>${entity.links.websiteSource ? ` (${entity.links.websiteSource})` : ""}</span></div>`
          : ""}
        ${entity.links?.appStore
          ? `<div class="detail-item"><strong>App Store</strong><span><a href="${entity.links.appStore}" target="_blank" rel="noreferrer">${entity.links.appStore}</a>${entity.links.appStoreSource ? ` (${entity.links.appStoreSource})` : ""}</span></div>`
          : ""}
        ${!entity.links?.website && !entity.links?.appStore
          ? `<div class="detail-item"><strong>No public link recorded yet</strong><span>This entry does not yet have a verified website or public App Store page in the shared index.</span></div>`
          : ""}
      </div>
    </div>
    <div>
      <span class="section-kicker">Notes</span>
      <div class="detail-list">
        ${(entity.notes || []).map(note => `<div class="detail-item"><span>${note}</span></div>`).join("")}
      </div>
    </div>
  `;
}

function renderClusters() {
  const list = document.getElementById("clusterList");
  list.innerHTML = state.data.clusters.map(cluster => `
    <div class="cluster-row ${cluster.name === state.selectedCluster ? "active" : ""}" data-cluster="${cluster.name}">
      <strong>${cluster.name}</strong>
      <span>${cluster.summary}</span>
    </div>
  `).join("");

  list.querySelectorAll(".cluster-row").forEach(row => {
    row.addEventListener("click", () => {
      state.selectedCluster = row.dataset.cluster;
      state.filters.cluster = row.dataset.cluster;
      render();
    });
  });

  const activeCluster = state.data.clusters.find(cluster => cluster.name === state.selectedCluster) || state.data.clusters[0];
  document.getElementById("serviceList").innerHTML = `
    <div class="mini-item" style="background: rgba(255,255,255,0.85);">
      <strong>${activeCluster.name}</strong>
      <span>${activeCluster.maturity}. ${activeCluster.summary}</span>
    </div>
    ${activeCluster.highlights.map(item => `
      <div class="mini-item">
        <strong>${item}</strong>
        <span>Key component in this cluster.</span>
      </div>
    `).join("")}
    ${activeCluster.watchpoints.map(item => `
      <div class="mini-item">
        <strong>Watchpoint</strong>
        <span>${item}</span>
      </div>
    `).join("")}
  `;
}

function renderRepoTable() {
  const repos = sortByMostRecent(state.data.repos, repo => repo.last2026Commit);
  document.getElementById("repoTableBody").innerHTML = repos.map(repo => `
    <tr>
      <td>${repo.repo}</td>
      <td>${repo.branch}</td>
      <td>${repo.last2026Commit}</td>
      <td>${repo.kind}</td>
      <td>${repo.role}</td>
    </tr>
  `).join("");
}

function renderFlyOperations() {
  const operations = state.data.flyOperations;
  const table = document.getElementById("flyTableBody");
  if (!operations) {
    table.innerHTML = `<tr><td colspan="5">No Fly.io operations data has been recorded.</td></tr>`;
    return;
  }
  document.getElementById("flyObservedAt").textContent = `Observed: ${operations.observedAt || "unknown"}`;
  document.getElementById("flyCostNote").textContent =
    `Cost status: ${operations.costStatus || "unknown"}. ${operations.costNote || ""}`;
  table.innerHTML = operations.services.map(service => `
    <tr>
      <td>${service.app}</td>
      <td><span class="status-dot ${service.status === "deployed" ? "status-live" : ""}">${service.status}</span></td>
      <td>${service.latestDeploy || "Not observed"}</td>
      <td>${service.cost == null ? "Not observed" : `${operations.costCurrency || "USD"} ${service.cost}`}</td>
      <td>${service.note || "—"}</td>
    </tr>
  `).join("");
}

function bindSearch() {
  const input = document.getElementById("searchInput");
  input.addEventListener("input", event => {
    state.filters.search = event.target.value.trim().toLowerCase();
    render();
  });
}

function render() {
  renderFilters();
  renderEntities();
  renderDetail();
  renderClusters();
  renderFlyOperations();
  renderRepoTable();
}

async function init() {
  const response = await fetch("../current/index.json");
  state.data = await response.json();
  state.selectedEntityId = state.data.entities[0]?.id || null;
  state.selectedCluster = state.data.clusters[0]?.name || null;
  document.getElementById("heroScope").textContent =
    `Current shared inventory built from ${state.data.scope.roots.join(" and ")}. Last baseline snapshot: ${state.data.scope.dateLabel}.`;
  document.getElementById("footerNote").textContent =
    `Generated baseline: ${state.data.scope.dateLabel}. App Store Connect access during the baseline scan: ${state.data.scope.appStoreConnectAccess}.`;
  renderStats();
  bindSearch();
  render();
}

init().catch(error => {
  document.getElementById("filterNote").textContent = "Unable to load the inventory JSON.";
  document.getElementById("heroScope").textContent = `Load error: ${error.message}`;
});

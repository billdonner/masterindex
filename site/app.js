const state = {
  data: null,
  tasks: null,
  filters: { search: "", surface: "all", status: "all", review: "all", cluster: "all" },
  selectedEntityId: null,
  selectedCluster: null
};

const badgeClassMap = { app: "b-app", backend: "b-backend", package: "b-package", service: "b-service", website: "b-service" };
const surfaces = [
  { key: "all", label: "Everything" }, { key: "app", label: "Apps" },
  { key: "backend", label: "Backends" }, { key: "service", label: "Services" },
  { key: "package", label: "Packages" }, { key: "website", label: "Websites" }
];
const statuses = [
  { key: "all", label: "All statuses" }, { key: "asc-mapped", label: "ASC mapped" },
  { key: "ready-for-sale", label: "Ready for sale" }, { key: "live", label: "Live services" },
  { key: "asc-unmapped", label: "ASC only / unlinked" }, { key: "deferred", label: "Deferred" }, { key: "retired", label: "Retired" }, { key: "parked", label: "Parked" },
  { key: "unreachable", label: "Unreachable" }, { key: "misconfigured", label: "Misconfigured" },
  { key: "stale", label: "Stale" }, { key: "gap", label: "Coverage gaps" }, { key: "lab", label: "Labs" }
];
const reviewFilters = [
  { key: "all", label: "All records" }, { key: "missing-links", label: "Missing public links" },
  { key: "website", label: "Has website" }, { key: "app-store", label: "Has App Store page" },
  { key: "tasks", label: "Has active task" }
];

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[char]);
}
function parseDateValue(value) { const ms = Date.parse(value); return Number.isNaN(ms) ? Number.NEGATIVE_INFINITY : ms; }
function sortByMostRecent(items, getter) {
  return [...items].sort((a, b) => parseDateValue(getter(b)) - parseDateValue(getter(a)) || String(a.name || a.repo).localeCompare(String(b.name || b.repo)));
}
function kindLabel(kind) { return ({ app: "Application", backend: "Backend", service: "Service", package: "Shared package", website: "Website" })[kind] || kind; }
function statusText(entity) { return ({ "ready-for-sale": "Ready for sale", "asc-mapped": "ASC mapped", live: "Live", "live-degraded-probes": "Live, probes degraded", "asc-unmapped": "ASC only / unlinked", deferred: "Deferred", retired: "Retired", parked: "Parked", unreachable: "Unreachable", misconfigured: "Misconfigured", stale: "Stale", "active-alternate": "Active alternate", gap: "Gap", lab: "Lab", "local-only": "Local only", active: "Active" })[entity.status] || entity.status; }
function stat(label, value) { return `<div class="stat"><strong>${escapeHtml(value)}</strong><span>${escapeHtml(label)}</span></div>`; }
function entityTasks(entityId) { return (state.tasks?.entryTasks?.[entityId] || []).filter(task => task.status === "active"); }
function hasPublicLink(entity) { return Object.values(entity.links || {}).some(value => typeof value === "string" && /^https?:\/\//.test(value)); }
function formatCadence(task) {
  const value = task.cadence?.value || "";
  if (value.includes("HOURLY;INTERVAL=6")) return "Every six hours";
  if (value.includes("DAILY")) return "Daily";
  if (value.includes("WEEKLY")) return "Weekly";
  return value || "Scheduled";
}

function syncUrl() {
  const params = new URLSearchParams();
  if (state.selectedEntityId) params.set("entity", state.selectedEntityId);
  if (state.selectedCluster && state.filters.cluster !== "all") params.set("cluster", state.selectedCluster);
  if (state.filters.review !== "all") params.set("filter", state.filters.review);
  history.replaceState(null, "", `${location.pathname}${params.toString() ? `?${params}` : ""}`);
}
function renderChips(containerId, options, activeValue, onClick) {
  const container = document.getElementById(containerId);
  container.innerHTML = options.map(option => `<button class="chip ${activeValue === option.key ? "active" : ""}" data-key="${escapeHtml(option.key)}">${escapeHtml(option.label)}</button>`).join("");
  container.querySelectorAll(".chip").forEach(button => button.addEventListener("click", () => onClick(button.dataset.key)));
}
function matchesEntity(entity) {
  const { filters } = state;
  const haystack = [entity.name, entity.kind, entity.cluster, entity.repo, entity.bundleId, entity.description, entity.release, ...Object.values(entity.links || {}), ...(entity.dependencies || []), ...(entity.notes || [])].join(" ").toLowerCase();
  const reviewMatches = {
    all: true,
    "missing-links": !hasPublicLink(entity),
    website: Boolean(entity.links?.website),
    "app-store": Boolean(entity.links?.appStore),
    tasks: entityTasks(entity.id).length > 0
  };
  return (!filters.search || haystack.includes(filters.search)) &&
    (filters.surface === "all" || entity.kind === filters.surface) &&
    (filters.status === "all" || entity.status === filters.status) &&
    (filters.cluster === "all" || entity.cluster === filters.cluster) && reviewMatches[filters.review];
}
function renderStats() {
  const summary = state.data.summary;
  document.getElementById("statGrid").innerHTML = [stat("ASC apps", summary.ascApps), stat("Mapped ASC records", summary.mappedAscApps), stat("Coverage gaps", summary.unmatchedAscApps), stat("2026-active repos", summary.activeRepos)].join("");
}
function renderAttention() {
  const missingLinks = state.data.entities.filter(entity => !hasPublicLink(entity)).length;
  const activeTasks = Object.values(state.tasks?.entryTasks || {}).flat().filter(task => task.status === "active").length;
  const cards = [
    { label: "Public-link coverage", detail: `${missingLinks} of ${state.data.entities.length} entities have no verified website or App Store page recorded.`, filter: "missing-links" },
    { label: "Recorded inventory gaps", detail: `${state.data.summary.unmatchedAscApps} unmatched ASC apps; ${state.data.gaps.length} gap records are retained in the current index.`, filter: "all" },
    { label: "Active entity tasks", detail: `${activeTasks} targeted checks are registered; all entities also inherit the shared verification cadence.`, filter: "tasks" }
  ];
  document.getElementById("attentionList").innerHTML = cards.map(card => `<button class="attention-card" data-filter="${card.filter}"><strong>${escapeHtml(card.label)}</strong><span>${escapeHtml(card.detail)}</span><em>Review</em></button>`).join("");
  document.querySelectorAll(".attention-card").forEach(card => card.addEventListener("click", () => { state.filters.review = card.dataset.filter; render(); }));
}
function renderFilters() {
  renderChips("surfaceChips", surfaces, state.filters.surface, value => { state.filters.surface = value; render(); });
  renderChips("statusChips", statuses, state.filters.status, value => { state.filters.status = value; render(); });
  renderChips("reviewChips", reviewFilters, state.filters.review, value => { state.filters.review = value; render(); });
  renderChips("clusterChips", [{ key: "all", label: "All clusters" }, ...state.data.clusters.map(cluster => ({ key: cluster.name, label: cluster.name }))], state.filters.cluster, value => {
    state.filters.cluster = value;
    state.selectedCluster = value === "all" ? state.data.clusters[0]?.name : value;
    render();
  });
}
function renderEntities() {
  const entities = sortByMostRecent(state.data.entities.filter(matchesEntity), entity => entity.lastModified);
  if (!entities.some(entity => entity.id === state.selectedEntityId)) state.selectedEntityId = entities[0]?.id || state.data.entities[0]?.id;
  document.getElementById("entityGrid").innerHTML = entities.length ? entities.map(entity => `<article class="card ${entity.id === state.selectedEntityId ? "selected" : ""}" data-id="${escapeHtml(entity.id)}" tabindex="0" role="button" aria-label="View ${escapeHtml(entity.name)} details">
    <div class="card-top"><div><div class="subline">${escapeHtml(entity.cluster)}</div><h4>${escapeHtml(entity.name)}</h4></div><div class="status-dot ${entity.status.startsWith("live") || entity.status === "ready-for-sale" ? "status-live" : entity.status === "lab" ? "status-lab" : ""}">${escapeHtml(statusText(entity))}</div></div>
    <div class="badge-row"><span class="badge ${badgeClassMap[entity.kind] || ""}">${escapeHtml(kindLabel(entity.kind))}</span>${entity.bundleId ? `<span class="badge b-asc">${escapeHtml(entity.bundleId)}</span>` : ""}${entityTasks(entity.id).length ? `<span class="badge b-task">${entityTasks(entity.id).length} active task${entityTasks(entity.id).length === 1 ? "" : "s"}</span>` : ""}</div>
    <div class="subline">${escapeHtml(entity.description)}</div><div class="subline"><strong>Repo:</strong> ${escapeHtml(entity.repo || "Not identified")}</div></article>`).join("") : `<p class="empty-state">No entries match the current filters.</p>`;
  document.querySelectorAll(".card").forEach(card => {
    const select = () => { state.selectedEntityId = card.dataset.id; renderEntities(); renderDetail(); syncUrl(); };
    card.addEventListener("click", select);
    card.addEventListener("keydown", event => { if (event.key === "Enter" || event.key === " ") { event.preventDefault(); select(); } });
  });
  document.getElementById("resultCount").textContent = `${entities.length} matching ${entities.length === 1 ? "item" : "items"}`;
  document.getElementById("filterNote").textContent = entities.length === state.data.entities.length ? "Showing everything in the current inventory." : `Showing ${entities.length} filtered items from the current inventory.`;
}
function linkItem(label, url, source) { return `<div class="detail-item"><strong>${escapeHtml(label)}</strong><span><a href="${escapeHtml(url)}" target="_blank" rel="noreferrer">${escapeHtml(url)}</a>${source ? ` <small>(${escapeHtml(source)})</small>` : ""}</span></div>`; }
function renderDetail() {
  const entity = state.data.entities.find(item => item.id === state.selectedEntityId) || state.data.entities[0];
  if (!entity) return;
  const links = entity.links || {};
  const knownLinks = [
    ["Website", links.website, links.websiteSource], ["Product site", links.productSite],
    ["Portfolio page", links.portfolioPage], ["App Store", links.appStore, links.appStoreSource],
    ["TestFlight", links.testFlight], ["GitHub", links.github],
    ["Privacy policy", links.privacyPolicy], ["Support", links.support],
    ["Backend", links.backend], ["Health", links.health], ["OpenAPI", links.openapi]
  ].filter(([, url]) => url);
  const tasks = entityTasks(entity.id);
  document.getElementById("detailPanel").innerHTML = `<div class="detail-top"><div><span class="section-kicker">${escapeHtml(entity.cluster)}</span><h3 class="detail-title">${escapeHtml(entity.name)}</h3><div class="subline">${escapeHtml(entity.description)}</div></div></div>
    <div class="detail-grid"><div class="detail-metric"><label>Kind</label><strong>${escapeHtml(kindLabel(entity.kind))}</strong></div><div class="detail-metric"><label>Status</label><strong>${escapeHtml(statusText(entity))}</strong></div><div class="detail-metric"><label>Repository</label><strong>${escapeHtml(entity.repo || "Not identified")}</strong></div><div class="detail-metric"><label>Last modified</label><strong>${escapeHtml(entity.lastModified || "Unknown")}</strong></div><div class="detail-metric"><label>Bundle ID</label><strong>${escapeHtml(entity.bundleId || "None surfaced in scan")}</strong></div></div>
    <div><span class="section-kicker">Release</span><div class="detail-item"><strong>Deployment or release signal</strong><span>${escapeHtml(entity.release || "No release signal recorded.")}</span></div></div>
    <div><span class="section-kicker">Connected to</span><div class="detail-list">${(entity.dependencies || []).length ? entity.dependencies.map(item => `<div class="detail-item"><strong>${escapeHtml(item)}</strong><span>Observed dependency, consumer, or direct relationship in the inventory.</span></div>`).join("") : `<div class="detail-item"><strong>Mostly standalone</strong><span>No direct dependency surfaced in the high-level scan.</span></div>`}</div></div>
    <div><span class="section-kicker">Public links</span><div class="detail-list">${knownLinks.length ? knownLinks.map(([label, url, source]) => linkItem(label, url, source)).join("") : `<div class="detail-item"><strong>No public link recorded yet</strong><span>This entry does not yet have a verified website or public App Store page in the shared index.</span></div>`}</div></div>
    <div><span class="section-kicker">Active tasks</span><div class="detail-list">${tasks.length ? tasks.map(task => `<div class="detail-item"><strong>${escapeHtml(task.name)}</strong><span>${escapeHtml(formatCadence(task))} · ${escapeHtml(task.purpose)}</span></div>`).join("") : `<div class="detail-item"><strong>Covered by the shared cadence</strong><span>No entry-specific task is registered; the default six-hour verification and daily refresh policy still applies.</span></div>`}</div></div>
    <div><span class="section-kicker">Notes</span><div class="detail-list">${(entity.notes || []).map(note => `<div class="detail-item"><span>${escapeHtml(note)}</span></div>`).join("") || `<div class="detail-item"><span>No additional notes recorded.</span></div>`}</div></div>`;
}
function renderClusters() {
  const clusters = state.data.clusters;
  document.getElementById("clusterList").innerHTML = clusters.map(cluster => `<button class="cluster-row ${cluster.name === state.selectedCluster ? "active" : ""}" data-cluster="${escapeHtml(cluster.name)}"><strong>${escapeHtml(cluster.name)}</strong><span>${escapeHtml(cluster.summary)}</span></button>`).join("");
  document.querySelectorAll(".cluster-row").forEach(row => row.addEventListener("click", () => { state.selectedCluster = row.dataset.cluster; state.filters.cluster = row.dataset.cluster; render(); }));
  const activeCluster = clusters.find(cluster => cluster.name === state.selectedCluster) || clusters[0];
  document.getElementById("serviceList").innerHTML = (state.data.services || []).map(service => `<div class="mini-item"><strong>${escapeHtml(service.name)}</strong><span>${escapeHtml(service.note)}</span><span class="consumer-line"><b>Consumers:</b> ${escapeHtml((service.consumers || []).join(", ") || "None recorded")}</span><span class="consumer-line"><b>Repo:</b> ${escapeHtml(service.repo || "Unidentified")}</span></div>`).join("") || `<div class="mini-item"><span>No shared services recorded.</span></div>`;
}
function renderRepoTable() {
  const repos = sortByMostRecent(state.data.repos || [], repo => repo.last2026Commit);
  document.getElementById("repoTableBody").innerHTML = repos.map(repo => `<tr><td>${escapeHtml(repo.repo)}</td><td>${escapeHtml(repo.branch)}</td><td>${escapeHtml(repo.last2026Commit)}</td><td>${escapeHtml(repo.kind)}</td><td>${escapeHtml(repo.role)}</td></tr>`).join("");
}
function bindSearch() { document.getElementById("searchInput").addEventListener("input", event => { state.filters.search = event.target.value.trim().toLowerCase(); render(); }); }
function render() { renderFilters(); renderAttention(); renderEntities(); renderDetail(); renderClusters(); renderRepoTable(); syncUrl(); }
function applyUrlState() {
  const params = new URLSearchParams(location.search);
  const entity = params.get("entity"), cluster = params.get("cluster"), filter = params.get("filter");
  if (state.data.entities.some(item => item.id === entity)) state.selectedEntityId = entity;
  if (state.data.clusters.some(item => item.name === cluster)) { state.selectedCluster = cluster; state.filters.cluster = cluster; }
  if (reviewFilters.some(item => item.key === filter)) state.filters.review = filter;
}
async function init() {
  const [inventoryResult, taskResult] = await Promise.all([fetch("../current/index.json"), fetch("../tasks/index.json")]);
  if (!inventoryResult.ok) throw new Error(`Inventory load failed (${inventoryResult.status})`);
  state.data = await inventoryResult.json();
  state.tasks = taskResult.ok ? await taskResult.json() : { entryTasks: {} };
  state.selectedEntityId = state.data.entities[0]?.id || null;
  state.selectedCluster = state.data.clusters[0]?.name || null;
  applyUrlState();
  document.getElementById("heroScope").textContent = `Current shared inventory built from ${state.data.scope.roots.join(" and ")}. Last baseline snapshot: ${state.data.scope.dateLabel}.`;
  document.getElementById("footerNote").textContent = `Inventory generated ${state.data.generatedAt}. App Store Connect access during this refresh: ${state.data.scope.appStoreConnectAccess}.`;
  renderStats(); bindSearch(); render();
}
init().catch(error => { document.getElementById("filterNote").textContent = "Unable to load the inventory JSON."; document.getElementById("heroScope").textContent = `Load error: ${error.message}`; });

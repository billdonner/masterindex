const state = { projects: [], selected: null };
const byId = id => document.getElementById(id);

function message(id, text, error = false) {
  const node = byId(id);
  node.textContent = text;
  node.classList.toggle("error", error);
}

async function request(url, options = {}) {
  const response = await fetch(url, { ...options, headers: { "Content-Type": "application/json", ...(options.headers || {}) } });
  const body = await response.json();
  if (!response.ok) throw new Error(body.error || "Request failed.");
  return body;
}

function render() {
  const list = byId("projectList");
  list.replaceChildren();
  byId("count").textContent = `${state.projects.length} captured ${state.projects.length === 1 ? "idea" : "ideas"}`;
  if (!state.projects.length) {
    list.innerHTML = '<p class="empty">Nothing captured yet. Start with a name and one sentence about the job it should do.</p>';
    return;
  }
  state.projects.forEach(project => {
    const fragment = byId("projectTemplate").content.cloneNode(true);
    fragment.querySelector(".state").textContent = project.state.replaceAll("-", " ");
    fragment.querySelector("h3").textContent = project.name;
    fragment.querySelector(".purpose").textContent = project.purpose;
    fragment.querySelector(".directory").textContent = project.proposed.directory;
    fragment.querySelector(".github").textContent = `${project.proposed.github.owner}/${project.proposed.github.name} · ${project.proposed.github.visibility}`;
    const button = fragment.querySelector(".provision");
    const safety = fragment.querySelector(".safety");
    const ready = project.state === "captured";
    button.disabled = !ready;
    safety.textContent = ready ? "Creates no files until you type its name." : project.state === "provisioned" ? "Provisioned and registered." : "Review its intake record before retrying.";
    button.addEventListener("click", () => openProvision(project));
    list.append(fragment);
  });
}

async function refresh() {
  const { projects } = await request("/api/intakes", { headers: {} });
  state.projects = projects;
  render();
}

function openProvision(project) {
  state.selected = project;
  byId("confirmation").value = "";
  message("provisionMessage", "");
  byId("provisionSummary").textContent = `“${project.name}” will be created at ${project.proposed.directory} and pushed to ${project.proposed.github.owner}/${project.proposed.github.name}.`;
  byId("provisionDialog").showModal();
  byId("confirmation").focus();
}

byId("captureForm").addEventListener("submit", async event => {
  event.preventDefault();
  const button = event.submitter;
  button.disabled = true;
  message("captureMessage", "Saving intake…");
  try {
    const form = new FormData(event.currentTarget);
    const result = await request("/api/intakes", { method: "POST", body: JSON.stringify(Object.fromEntries(form)) });
    message("captureMessage", `Captured ${result.project.name}. Review it below before provisioning.`);
    event.currentTarget.reset();
    await refresh();
  } catch (error) {
    message("captureMessage", error.message, true);
  } finally {
    button.disabled = false;
  }
});

byId("cancel").addEventListener("click", () => byId("provisionDialog").close());
byId("provisionForm").addEventListener("submit", async event => {
  event.preventDefault();
  if (!state.selected) return;
  const button = byId("confirm");
  button.disabled = true;
  message("provisionMessage", "Creating project… this can take a moment.");
  try {
    const result = await request(`/api/intakes/${encodeURIComponent(state.selected.id)}/provision`, { method: "POST", body: JSON.stringify({ confirmation: byId("confirmation").value, createGithub: true }) });
    message("provisionMessage", result.message);
    await refresh();
    setTimeout(() => byId("provisionDialog").close(), 900);
  } catch (error) {
    message("provisionMessage", error.message, true);
  } finally {
    button.disabled = false;
  }
});

refresh().catch(error => message("captureMessage", `Could not load Project Intake: ${error.message}`, true));

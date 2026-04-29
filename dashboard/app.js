const API_URL = "http://127.0.0.1:5000/api/jobs";
let jobs = [];

async function loadJobs() {
  try {
    const res = await fetch(API_URL);
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    jobs = await res.json();

    if (!Array.isArray(jobs) || jobs.length === 0) {
      document.getElementById("tableBody").innerHTML =
        `<tr><td colspan="7" style="text-align:center;padding:30px;color:#999;">
           No jobs in database yet. Run the scraper first.
         </td></tr>`;
      return;
    }
    populateFilters();
    renderTable(jobs);
  } catch (err) {
    document.getElementById("tableBody").innerHTML =
      `<tr><td colspan="7" style="text-align:center;padding:30px;color:red;">
         ❌ Cannot reach Flask API at ${API_URL}<br>
         Make sure you ran: <code>python app.py</code>
       </td></tr>`;
  }
}

function populateFilters() {
  const locationSel = document.getElementById("locationFilter");
  const sourceSel   = document.getElementById("sourceFilter");
  locationSel.innerHTML = `<option value="">All Locations</option>`;
  sourceSel.innerHTML   = `<option value="">All Sources</option>`;

  [...new Set(jobs.map(j => j.location).filter(Boolean))]
    .forEach(loc => locationSel.insertAdjacentHTML("beforeend",`<option>${loc}</option>`));
  [...new Set(jobs.map(j => j.source).filter(Boolean))]
    .forEach(src => sourceSel.insertAdjacentHTML("beforeend",`<option>${src}</option>`));
}

function filterTable() {
  const search   = document.getElementById("searchInput").value.toLowerCase();
  const location = document.getElementById("locationFilter").value;
  const source   = document.getElementById("sourceFilter").value;
  const status   = document.getElementById("statusFilter").value;

  renderTable(jobs.filter(j =>
    (!search   || `${j.title} ${j.company}`.toLowerCase().includes(search)) &&
    (!location || j.location === location) &&
    (!source   || j.source   === source)   &&
    (!status   || j.status   === status)
  ));
}

function renderTable(data) {
  const tbody = document.getElementById("tableBody");
  if (!data.length) {
    tbody.innerHTML =
      `<tr><td colspan="7" style="text-align:center;padding:20px;color:#999;">
         No matching jobs found.
       </td></tr>`;
    return;
  }
  tbody.innerHTML = data.map(j => `
    <tr>
      <td>${j.title    || "—"}</td>
      <td>${j.company  || "—"}</td>
      <td>${j.location || "—"}</td>
      <td>${j.source   || "—"}</td>
      <td>${j.posted   || "—"}</td>
      <td><select onchange="updateStatus(${j.id}, this.value)"
                  style="padding:4px 8px;border-radius:4px;border:1px solid #ddd;">
        ${["Pending","Applied","Rejected"].map(s =>
          `<option ${j.status===s?"selected":""}>${s}</option>`).join("")}
      </select></td>
      <td><a href="${j.link}" target="_blank">Apply ↗</a></td>
    </tr>`).join("");
}

async function updateStatus(id, status) {
  try {
    await fetch(`${API_URL}/${id}/status`, {
      method:  "PATCH",
      headers: { "Content-Type": "application/json" },
      body:    JSON.stringify({ status })
    });
    const job = jobs.find(j => j.id === id);
    if (job) job.status = status;
  } catch {
    alert("Failed to update status. Is Flask running?");
  }
}

loadJobs();
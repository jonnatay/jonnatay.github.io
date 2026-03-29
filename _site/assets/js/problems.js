document.addEventListener("DOMContentLoaded", async () => {
  const statusEl = document.getElementById("problems-status");
  const tableEl = document.getElementById("problems-table");
  const detailEl = document.getElementById("problem-detail");
  const searchEl = document.getElementById("problem-search");

  const SUPABASE_URL = "https://xaxyqdxxjifhdrpreoro.supabase.co";
  const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhheHlxZHh4amlmaGRycHJlb3JvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM5MDAzMjcsImV4cCI6MjA3OTQ3NjMyN30.nQR4rcabnJB-3yWIjT_BqNwbbF6OmqFY2r9_1I8voC8";

  const client = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  let allProblems = [];

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function renderTable(rows) {
    if (!rows.length) {
      tableEl.innerHTML = "<p>No matching problems found.</p>";
      return;
    }

    const html = `
      <table class="table">
        <thead>
          <tr>
            <th>Title</th>
            <th>Competition</th>
            <th>Region</th>
            <th>Level</th>
            <th>Year</th>
          </tr>
        </thead>
        <tbody>
          ${rows.map(row => `
            <tr data-problem-id="${escapeHtml(row.id)}" class="problem-row" style="cursor: pointer;">
              <td>${escapeHtml(row.title)}</td>
              <td>${escapeHtml(row.competition)}</td>
              <td>${escapeHtml(row.region)}</td>
              <td>${escapeHtml(row.level)}</td>
              <td>${escapeHtml(row.year)}</td>
            </tr>
          `).join("")}
        </tbody>
      </table>
    `;

    tableEl.innerHTML = html;

    document.querySelectorAll(".problem-row").forEach(rowEl => {
      rowEl.addEventListener("click", () => {
        const problemId = rowEl.getAttribute("data-problem-id");
        const problem = allProblems.find(p => String(p.id) === String(problemId));
        if (problem) {
          renderDetail(problem);
        }
      });
    });
  }

async function renderDetail(problem) {
  let samplesHtml = "<p>No samples available.</p>";

  const { data: samples, error: samplesError } = await client
    .from("samples_new")
    .select("sample_order, input, output")
    .eq("problem_id", problem.id)
    .order("sample_order", { ascending: true });

  if (!samplesError && samples && samples.length > 0) {
    samplesHtml = samples.map(sample => `
      <div style="margin-bottom: 1rem;">
        <h4>Sample ${escapeHtml(sample.sample_order)}</h4>
        <strong>Input</strong>
        <pre>${escapeHtml(sample.input)}</pre>
        <strong>Output</strong>
        <pre>${escapeHtml(sample.output)}</pre>
      </div>
    `).join("");
  }

  detailEl.innerHTML = `
    <h2>${escapeHtml(problem.title)}</h2>
    <p>
      <strong>Competition:</strong> ${escapeHtml(problem.competition)}<br>
      <strong>Region:</strong> ${escapeHtml(problem.region)}<br>
      <strong>Level:</strong> ${escapeHtml(problem.level)}<br>
      <strong>Year:</strong> ${escapeHtml(problem.year)}
    </p>

    <h3>Problem</h3>
    <p>${escapeHtml(problem.body).replace(/\n/g, "<br>")}</p>

    <h3>Input</h3>
    <p>${escapeHtml(problem.input_spec).replace(/\n/g, "<br>")}</p>

    <h3>Output</h3>
    <p>${escapeHtml(problem.output_spec).replace(/\n/g, "<br>")}</p>

    <h3>Samples</h3>
    ${samplesHtml}

    ${
      problem.kattis_url
        ? `<p><a href="${escapeHtml(problem.kattis_url)}" target="_blank" rel="noopener noreferrer">Open on Kattis</a></p>`
        : ""
    }
  `;
}

  function applySearch() {
    const q = searchEl.value.trim().toLowerCase();

    const filtered = allProblems.filter(problem => {
      return [
        problem.title,
        problem.competition,
        problem.region,
        problem.level,
        problem.year
      ]
        .map(v => String(v ?? "").toLowerCase())
        .some(v => v.includes(q));
    });

    renderTable(filtered);
  }

  try {
    const { data, error } = await client
      .from("problems_new")
      .select("id, title, competition, region, level, year, body, input_spec, output_spec, kattis_url")
      .order("year", { ascending: false });

    if (error) {
      throw error;
    }

    allProblems = data || [];

    statusEl.textContent = `Loaded ${allProblems.length} problems.`;
    renderTable(allProblems);

    searchEl.addEventListener("input", applySearch);
  } catch (err) {
    console.error(err);
    statusEl.textContent = `Failed to load problems: ${err.message}`;
  }
});
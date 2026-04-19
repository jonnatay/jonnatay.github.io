document.addEventListener("DOMContentLoaded", async () => {
  const statusEl = document.getElementById("problems-status");
  const tableEl = document.getElementById("problems-table");
  const detailEl = document.getElementById("problem-detail");
  const searchEl = document.getElementById("problem-search");
  const KATEX_CSS_URL = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css";
  const KATEX_JS_URL = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js";
  const KATEX_AUTORENDER_URL = "https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js";

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

  function ensureStylesheet(href) {
    const existing = document.querySelector(`link[data-math-renderer="true"][href="${href}"]`);
    if (existing) {
      return;
    }

    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = href;
    link.dataset.mathRenderer = "true";
    document.head.appendChild(link);
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const existing = document.querySelector(`script[data-math-renderer="true"][src="${src}"]`);
      if (existing) {
        if (existing.dataset.loaded === "true") {
          resolve();
          return;
        }

        existing.addEventListener("load", resolve, { once: true });
        existing.addEventListener("error", () => reject(new Error(`Failed to load ${src}`)), { once: true });
        return;
      }

      const script = document.createElement("script");
      script.src = src;
      script.dataset.mathRenderer = "true";
      script.addEventListener("load", () => {
        script.dataset.loaded = "true";
        resolve();
      }, { once: true });
      script.addEventListener("error", () => reject(new Error(`Failed to load ${src}`)), { once: true });
      document.head.appendChild(script);
    });
  }

  const mathReadyPromise = (async () => {
    ensureStylesheet(KATEX_CSS_URL);
    await loadScript(KATEX_JS_URL);
    await loadScript(KATEX_AUTORENDER_URL);
  })();

  function renderProblemText(value) {
    const normalized = String(value ?? "").replace(/\r\n?/g, "\n").trim();
    if (!normalized) {
      return '<p class="problem-text problem-text--empty">No details provided.</p>';
    }

    const blocks = normalized
      .split(/\n\s*\n/)
      .map(block => `<div class="problem-text__block">${escapeHtml(block)}</div>`)
      .join("");

    return `<div class="problem-text">${blocks}</div>`;
  }

  async function renderMath(container) {
    if (!container) {
      return;
    }

    try {
      await mathReadyPromise;
      if (typeof window.renderMathInElement !== "function") {
        return;
      }

      window.renderMathInElement(container, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "\\[", right: "\\]", display: true },
          { left: "\\(", right: "\\)", display: false },
          { left: "$", right: "$", display: false }
        ],
        throwOnError: false,
        strict: "ignore",
        trust: false
      });
    } catch (error) {
      console.warn("Math rendering is unavailable on the problem page.", error);
    }
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
      ${renderProblemText(problem.body)}

      <h3>Input</h3>
      ${renderProblemText(problem.input_spec)}

      <h3>Output</h3>
      ${renderProblemText(problem.output_spec)}

      <h3>Samples</h3>
      ${samplesHtml}

      ${
        problem.kattis_url
          ? `<p><a href="${escapeHtml(problem.kattis_url)}" target="_blank" rel="noopener noreferrer">Open on Kattis</a></p>`
          : ""
      }
    `;

    await renderMath(detailEl);
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

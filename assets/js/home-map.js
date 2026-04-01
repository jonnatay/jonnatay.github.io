document.addEventListener("DOMContentLoaded", async () => {
  const SUPABASE_URL = "https://xaxyqdxxjifhdrpreoro.supabase.co";
  const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhheHlxZHh4amlmaGRycHJlb3JvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM5MDAzMjcsImV4cCI6MjA3OTQ3NjMyN30.nQR4rcabnJB-3yWIjT_BqNwbbF6OmqFY2r9_1I8voC8";

  const client = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  const titleEl = document.getElementById("region-title");
  const problemsEl = document.getElementById("region-problems");
  const mapObject = document.getElementById("world-map-object");

  let allProblems = [];

  const REGION_MAP = {
    "north-america": [
      "Southeast",
      "South Central",
      "Rocky Mountain",
      "North Central NA",
      "Mid-Atlantic USA",
      "Mid-Central USA",
      "Southern California"
    ],
    "south-america": [],
    "europe": [],
    "africa": [],
    "asia": [],
    "oceania": []
  };

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function renderProblems(mapRegionId) {
    const dbRegions = REGION_MAP[mapRegionId] || [];
    const matches = allProblems.filter(problem => dbRegions.includes(problem.region));

    const readableName = mapRegionId
      .split("-")
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");

    titleEl.textContent = readableName;

    if (!matches.length) {
      problemsEl.innerHTML = "<p>No problems found for this region.</p>";
      return;
    }

    problemsEl.innerHTML = `
      <ul>
        ${matches.map(problem => `
          <li>
            <strong>${escapeHtml(problem.title)}</strong>
            (${escapeHtml(problem.region)}, ${escapeHtml(problem.competition)}, ${escapeHtml(problem.year)})
            ${problem.kattis_url
              ? `- <a href="${escapeHtml(problem.kattis_url)}" target="_blank" rel="noopener noreferrer">Kattis</a>`
              : ""}
          </li>
        `).join("")}
      </ul>
    `;
  }

  try {
    const { data, error } = await client
      .from("problems_new")
      .select("id, title, region, competition, year, kattis_url")
      .order("year", { ascending: false });

    if (error) throw error;
    allProblems = data || [];
  } catch (err) {
    titleEl.textContent = "Error";
    problemsEl.innerHTML = `<p>Failed to load problems: ${escapeHtml(err.message)}</p>`;
    return;
  }

  mapObject.addEventListener("load", () => {
    const svgDoc = mapObject.contentDocument;
    if (!svgDoc) {
      problemsEl.innerHTML = "<p>Could not load map SVG.</p>";
      return;
    }

    Object.keys(REGION_MAP).forEach(regionId => {
      const regionEl = svgDoc.getElementById(regionId);
      if (!regionEl) return;

      regionEl.style.cursor = "pointer";

      regionEl.addEventListener("mouseenter", () => {
        regionEl.style.opacity = "0.7";
      });

      regionEl.addEventListener("mouseleave", () => {
        regionEl.style.opacity = "1";
      });

      regionEl.addEventListener("click", () => {
        renderProblems(regionId);
      });
    });
  });
});
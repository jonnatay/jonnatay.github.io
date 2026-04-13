document.addEventListener("DOMContentLoaded", async () => {
  const titleEl = document.getElementById("region-title");
  const problemsEl = document.getElementById("region-problems");
  const mapObject = document.getElementById("world-map-object");

  if (!titleEl || !problemsEl || !mapObject || !window.supabase) {
    return;
  }

  const SUPABASE_URL = "https://xaxyqdxxjifhdrpreoro.supabase.co";
  const SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhheHlxZHh4amlmaGRycHJlb3JvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjM5MDAzMjcsImV4cCI6MjA3OTQ3NjMyN30.nQR4rcabnJB-3yWIjT_BqNwbbF6OmqFY2r9_1I8voC8";

  const client = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

  const REGION_DEFINITIONS = {
    world: {
      label: "World",
      keywords: ["world", "world finals", "global"]
    },
    "southern-california": {
      label: "Southern California",
      keywords: ["southern california", "socal"]
    },
    "rocky-mountain": {
      label: "Rocky Mountain",
      keywords: ["rocky mountain", "rocky mountain regional"]
    },
    "south-central": {
      label: "South Central",
      keywords: ["south central", "south central usa"]
    },
    "north-central-na": {
      label: "North Central NA",
      keywords: ["north central na", "north central north america", "north central"]
    },
    "mid-central-usa": {
      label: "Mid-Central USA",
      keywords: ["mid central usa", "mid central"]
    },
    "mid-atlantic-usa": {
      label: "Mid-Atlantic USA",
      keywords: ["mid atlantic usa", "mid atlantic"]
    },
    southeast: {
      label: "Southeast",
      keywords: ["southeast", "south east", "southeastern"]
    }
  };

  const GENERIC_NA_TAGS = new Set(["na", "north america", "north american"]);

  let allProblems = [];
  let activeRegionId = null;
  let mapBound = false;

  function escapeHtml(value) {
    return String(value ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }

  function normalizeText(value) {
    return String(value ?? "")
      .toLowerCase()
      .replace(/&/g, " and ")
      .replace(/[^a-z0-9]+/g, " ")
      .trim();
  }

  function pluralizeProblems(count) {
    return count === 1 ? "problem" : "problems";
  }

  function getSearchFields(problem) {
    return [problem.region, problem.competition]
      .map(normalizeText)
      .filter(Boolean);
  }

  function buildProblemList(problems, introMessage) {
    const introHtml = introMessage
      ? `<p>${escapeHtml(introMessage)}</p>`
      : `<p>Found ${problems.length} ${pluralizeProblems(problems.length)} for this region.</p>`;

    return `
      ${introHtml}
      <ul>
        ${problems.map(problem => {
          const displayRegion = problem.region ? escapeHtml(problem.region) : "Unspecified region";
          const kattisLink = problem.kattis_url
            ? ` - <a href="${escapeHtml(problem.kattis_url)}" target="_blank" rel="noopener noreferrer">Kattis</a>`
            : "";

          return `
            <li>
              <strong>${escapeHtml(problem.title)}</strong>
              (${displayRegion}, ${escapeHtml(problem.competition)}, ${escapeHtml(problem.year)})
              ${kattisLink}
            </li>
          `;
        }).join("")}
      </ul>
    `;
  }

  function getExactMatches(regionDefinition) {
    const normalizedKeywords = regionDefinition.keywords.map(normalizeText);

    return allProblems.filter(problem => {
      const searchFields = getSearchFields(problem);
      return normalizedKeywords.some(keyword => searchFields.some(field => field.includes(keyword)));
    });
  }

  function getGenericNorthAmericaMatches() {
    return allProblems.filter(problem => GENERIC_NA_TAGS.has(normalizeText(problem.region)));
  }

  function updateActiveRegion(svgDoc, nextRegionId) {
    if (!svgDoc) {
      return;
    }

    if (activeRegionId) {
      const previousRegion = svgDoc.getElementById(activeRegionId);
      if (previousRegion) {
        previousRegion.classList.remove("is-active");
      }
    }

    const nextRegion = svgDoc.getElementById(nextRegionId);
    if (nextRegion) {
      nextRegion.classList.add("is-active");
      activeRegionId = nextRegionId;
    }
  }

  function renderProblems(regionId, svgDoc) {
    const regionDefinition = REGION_DEFINITIONS[regionId];
    if (!regionDefinition) {
      return;
    }

    updateActiveRegion(svgDoc, regionId);
    titleEl.textContent = regionDefinition.label;

    const exactMatches = getExactMatches(regionDefinition);
    if (exactMatches.length) {
      problemsEl.innerHTML = buildProblemList(exactMatches);
      return;
    }

    const genericNorthAmericaMatches = regionId === "world"
      ? []
      : getGenericNorthAmericaMatches();

    if (genericNorthAmericaMatches.length) {
      problemsEl.innerHTML = buildProblemList(
        genericNorthAmericaMatches,
        `No exact ${regionDefinition.label} matches were found yet, so these North America-tagged problems are shown instead.`
      );
      return;
    }

    problemsEl.innerHTML = "<p>No problems found for this region.</p>";
  }

  function bindMapInteractions() {
    const svgDoc = mapObject.contentDocument;
    if (!svgDoc || mapBound) {
      return mapBound;
    }

    let boundRegions = 0;

    Object.entries(REGION_DEFINITIONS).forEach(([regionId, regionDefinition]) => {
      const regionEl = svgDoc.getElementById(regionId);
      if (!regionEl) {
        return;
      }

      boundRegions += 1;
      regionEl.style.cursor = "pointer";
      regionEl.setAttribute("tabindex", "0");
      regionEl.setAttribute("role", "button");
      regionEl.setAttribute("aria-label", `Show problems for ${regionDefinition.label}`);

      const activateRegion = () => {
        renderProblems(regionId, svgDoc);
      };

      regionEl.addEventListener("click", activateRegion);
      regionEl.addEventListener("keydown", event => {
        if (event.key === "Enter" || event.key === " ") {
          event.preventDefault();
          activateRegion();
        }
      });
    });

    mapBound = boundRegions > 0;
    return mapBound;
  }

  function prepareMap() {
    if (bindMapInteractions()) {
      return;
    }

    mapObject.addEventListener(
      "load",
      () => {
        if (!bindMapInteractions()) {
          problemsEl.innerHTML = "<p>Could not load map SVG.</p>";
        }
      },
      { once: true }
    );
  }

  try {
    const { data, error } = await client
      .from("problems_new")
      .select("id, title, region, competition, year, kattis_url")
      .order("year", { ascending: false });

    if (error) {
      throw error;
    }

    allProblems = data || [];
    prepareMap();
  } catch (err) {
    titleEl.textContent = "Error";
    problemsEl.innerHTML = `<p>Failed to load problems: ${escapeHtml(err.message)}</p>`;
  }
});

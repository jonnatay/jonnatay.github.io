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
      keywords: ["world", "world finals", "global"],
      memberIds: ["world"]
    },
    "pacific-northwest": {
      label: "Pacific Northwest",
      keywords: ["pacific northwest", "pacific northwest regional", "pnw", "northwest"],
      memberIds: ["WA", "OR", "HI", "BC", "YT", "AK"]
    },
    "southern-california": {
      label: "Southern California",
      keywords: ["southern california", "southern california regional", "socal"],
      memberIds: ["CA", "NV"]
    },
    "rocky-mountain": {
      label: "Rocky Mountain",
      keywords: ["rocky mountain", "rocky mountain regional"],
      memberIds: ["CO", "AZ", "ID", "MT", "NM", "UT", "WY", "AB", "SK", "NT"]
    },
    "south-central": {
      label: "South Central",
      keywords: ["south central", "south central usa"],
      memberIds: ["TX", "OK", "LA"]
    },
    "mexico-central-america": {
      label: "Mexico and Central America",
      keywords: ["mexico and central america", "mexico", "central america"],
      memberIds: ["MX"]
    },
    "north-central-na": {
      label: "North Central NA",
      keywords: ["north central na", "north central north america", "north central"],
      memberIds: ["MN", "WI", "IA", "ND", "SD", "NE", "KS", "MB", "ON", "NU"]
    },
    "southeast-usa": {
      label: "Southeast USA",
      keywords: ["southeast usa", "southeast", "south east", "southeastern"],
      memberIds: ["FL", "MS", "AL", "GA", "SC"]
    },
    "mid-central-usa": {
      label: "Mid-Central USA",
      keywords: ["mid central usa", "mid central"],
      memberIds: ["IL", "AR", "TN", "KY", "MO"]
    },
    "mid-atlantic-usa": {
      label: "Mid-Atlantic USA",
      keywords: ["mid atlantic usa", "mid atlantic"],
      memberIds: ["VA", "NC", "WV", "MD", "DE", "NJ", "DC"]
    },
    "east-central": {
      label: "East Central",
      keywords: ["east central", "east central regional", "east central usa"],
      memberIds: ["OH", "MI", "IN", "PA"]
    },
    "northeast-north-america": {
      label: "Northeast North America",
      keywords: ["northeast north america", "northeast north american", "northeast", "northeastern"],
      memberIds: ["NY", "ME", "NH", "VT", "MA", "RI", "CT", "QC", "NB", "NS", "PE", "NL"]
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

  function getRegionElements(svgDoc, regionId) {
    const regionDefinition = REGION_DEFINITIONS[regionId];
    if (!svgDoc || !regionDefinition) {
      return [];
    }

    const elements = [];
    const seen = new Set();

    (regionDefinition.memberIds || [regionId]).forEach(memberId => {
      const memberEl = svgDoc.getElementById(memberId);
      if (memberEl && !seen.has(memberEl)) {
        elements.push(memberEl);
        seen.add(memberEl);
      }
    });

    svgDoc.querySelectorAll(`[data-region-id="${regionId}"]`).forEach(memberEl => {
      if (!seen.has(memberEl)) {
        elements.push(memberEl);
        seen.add(memberEl);
      }
    });

    return elements;
  }

  function updateActiveRegion(svgDoc, nextRegionId) {
    if (!svgDoc) {
      return;
    }

    if (activeRegionId) {
      getRegionElements(svgDoc, activeRegionId).forEach(regionEl => {
        regionEl.classList.remove("is-active");
      });
    }

    const nextRegionElements = getRegionElements(svgDoc, nextRegionId);
    nextRegionElements.forEach(regionEl => {
      regionEl.classList.add("is-active");
    });

    if (nextRegionElements.length) {
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
      const regionElements = getRegionElements(svgDoc, regionId);
      if (!regionElements.length) {
        return;
      }

      boundRegions += 1;
      const activateRegion = () => {
        renderProblems(regionId, svgDoc);
      };

      let focusTargetAssigned = false;

      regionElements.forEach(regionEl => {
        regionEl.style.cursor = "pointer";

        const isFocusable = regionEl.dataset.focusable === "true";
        if (isFocusable || !focusTargetAssigned) {
          regionEl.setAttribute("tabindex", "0");
          regionEl.setAttribute("role", "button");
          regionEl.setAttribute("aria-label", `Show problems for ${regionDefinition.label}`);
          focusTargetAssigned = true;
        }

        regionEl.addEventListener("click", activateRegion);
        regionEl.addEventListener("keydown", event => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            activateRegion();
          }
        });
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

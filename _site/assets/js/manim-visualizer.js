document.addEventListener("DOMContentLoaded", () => {
  const root = document.getElementById("manim-visualizer-root");
  if (!root) {
    return;
  }

  const codeEl = document.getElementById("manim-code-input");
  const exampleButtonsEl = document.getElementById("manim-example-buttons");
  const submitButtonEl = document.getElementById("manim-submit-button");
  const clearButtonEl = document.getElementById("manim-clear-button");
  const statusEl = document.getElementById("manim-status");
  const apiBaseDisplayEl = document.getElementById("manim-api-base-display");
  const jobIdEl = document.getElementById("manim-job-id");
  const jobStatusEl = document.getElementById("manim-job-status");
  const jobMessageEl = document.getElementById("manim-job-message");
  const videoCardEl = document.getElementById("manim-video-card");
  const videoEl = document.getElementById("manim-video");
  const downloadLinkEl = document.getElementById("manim-download-link");
  const errorCardEl = document.getElementById("manim-error-card");
  const errorOutputEl = document.getElementById("manim-error-output");
  const captchaNoteEl = document.getElementById("manim-captcha-note");
  const turnstileEl = document.getElementById("manim-turnstile");

  const apiBase = String(root.dataset.apiBase || "").trim();
  const normalizedApiBase = apiBase.replace(/\/+$/, "").replace(/\/api$/i, "");
  const turnstileSiteKey = String(root.dataset.turnstileSiteKey || "").trim();
  const pollIntervalMs = 3000;

  const exampleFiles = [
    {
      label: "Hello Manim",
      description: "Loads the minimal hello-world Manim example from the attached prototype.",
      url: "/assets/manim-examples/helloManim.py"
    },
    {
      label: "Node Demo",
      description: "Loads the small node example from the attached prototype.",
      url: "/assets/manim-examples/manimTestUserSide.py"
    },
    {
      label: "BFS",
      description: "Loads the BFS example from the attached Manim examples folder.",
      url: "/assets/manim-examples/BFS.py"
    },
    {
      label: "Bubble Sort",
      description: "Loads the bubble sort array animation example from the attached examples.",
      url: "/assets/manim-examples/boobleSort.py"
    }
  ];

  let currentJob = null;
  let pollTimer = null;
  let turnstileWidgetId = null;

  function apiUrl(path) {
    if (!normalizedApiBase) {
      return path;
    }

    return `${normalizedApiBase}${path}`;
  }

  async function readJsonResponse(response, fallbackMessage) {
    const responseText = await response.text();
    if (!responseText) {
      throw new Error(`${fallbackMessage} The server returned an empty response.`);
    }

    try {
      return JSON.parse(responseText);
    } catch (error) {
      const preview = responseText.replace(/\s+/g, " ").trim().slice(0, 180);
      throw new Error(
        `${fallbackMessage} Expected JSON but received ${
          response.headers.get("content-type") || "an unknown content type"
        } (HTTP ${response.status}).${preview ? ` Response preview: ${preview}` : ""}`
      );
    }
  }

  function setStatus(message, tone = "neutral") {
    statusEl.textContent = message;
    statusEl.dataset.tone = tone;
  }

  function setBusy(isBusy) {
    submitButtonEl.disabled = isBusy;
    submitButtonEl.textContent = isBusy ? "Submitting..." : "Render MP4";
  }

  function resetOutput() {
    clearInterval(pollTimer);
    pollTimer = null;
    currentJob = null;
    jobIdEl.textContent = "Not started";
    jobStatusEl.textContent = "Idle";
    jobMessageEl.textContent = "Waiting for a submission.";
    videoEl.removeAttribute("src");
    videoEl.load();
    downloadLinkEl.setAttribute("href", "#");
    videoCardEl.classList.add("manim-hidden");
    errorCardEl.classList.add("manim-hidden");
    errorOutputEl.textContent = "";
  }

  function buildVideoUrl(jobId, accessToken) {
    const url = new URL(apiUrl(`/api/renders/${encodeURIComponent(jobId)}/video`), window.location.href);
    url.searchParams.set("access_token", accessToken);
    return url.toString();
  }

  async function loadExample(file) {
    setStatus(`Loading ${file.label} example...`, "neutral");

    const response = await fetch(file.url, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Failed to load ${file.label}.`);
    }

    codeEl.value = await response.text();
    setStatus(`${file.label} example loaded.`, "neutral");
  }

  function renderExampleButtons() {
    exampleButtonsEl.innerHTML = "";

    exampleFiles.forEach(file => {
      const button = document.createElement("button");
      button.type = "button";
      button.textContent = file.label;
      button.title = file.description;
      button.addEventListener("click", async () => {
        try {
          await loadExample(file);
        } catch (error) {
          console.error(error);
          setStatus(error.message || "Unable to load that example.", "danger");
        }
      });

      exampleButtonsEl.appendChild(button);
    });
  }

  function extractCaptchaToken() {
    if (!turnstileSiteKey || !window.turnstile || turnstileWidgetId === null) {
      return "";
    }

    return window.turnstile.getResponse(turnstileWidgetId) || "";
  }

  function resetCaptcha() {
    if (turnstileSiteKey && window.turnstile && turnstileWidgetId !== null) {
      window.turnstile.reset(turnstileWidgetId);
    }
  }

  function renderCompletedJob(statusPayload) {
    const videoUrl = buildVideoUrl(statusPayload.job_id, currentJob.accessToken);
    videoEl.src = videoUrl;
    videoEl.load();
    downloadLinkEl.href = videoUrl;
    videoCardEl.classList.remove("manim-hidden");
    errorCardEl.classList.add("manim-hidden");
    errorOutputEl.textContent = "";
  }

  function renderFailedJob(statusPayload) {
    videoEl.removeAttribute("src");
    videoEl.load();
    videoCardEl.classList.add("manim-hidden");
    errorCardEl.classList.remove("manim-hidden");
    errorOutputEl.textContent = statusPayload.error_message || "The backend did not return a detailed error message.";
  }

  async function pollJobStatus() {
    if (!currentJob) {
      return;
    }

    try {
      const url = new URL(apiUrl(`/api/renders/${encodeURIComponent(currentJob.jobId)}`), window.location.href);
      url.searchParams.set("access_token", currentJob.accessToken);

      const response = await fetch(url.toString(), { cache: "no-store" });
      const payload = await readJsonResponse(response, "Failed to load render status.");

      if (!response.ok) {
        throw new Error(payload.detail || "Failed to load render status.");
      }

      jobIdEl.textContent = payload.job_id;
      jobStatusEl.textContent = payload.status;
      jobMessageEl.textContent = payload.message || "No status message provided.";

      if (payload.status === "completed") {
        clearInterval(pollTimer);
        pollTimer = null;
        setStatus("Render complete. Your MP4 is ready.", "neutral");
        renderCompletedJob(payload);
        setBusy(false);
        return;
      }

      if (payload.status === "failed" || payload.status === "expired") {
        clearInterval(pollTimer);
        pollTimer = null;
        setStatus(
          payload.status === "expired"
            ? "This render has expired and is no longer available."
            : "Render failed. Review the error output below.",
          "danger"
        );
        renderFailedJob(payload);
        setBusy(false);
        return;
      }

      setStatus(payload.message || `Render is currently ${payload.status}.`, payload.status === "queued" ? "warning" : "neutral");
    } catch (error) {
      console.error(error);
      clearInterval(pollTimer);
      pollTimer = null;
      setStatus(error.message || "Polling failed unexpectedly.", "danger");
      setBusy(false);
    }
  }

  async function submitRender() {
    const code = codeEl.value.trim();
    if (!code) {
      setStatus("Paste or load some visualization code before submitting.", "warning");
      return;
    }

    setBusy(true);
    resetOutput();
    setStatus("Submitting render job...", "neutral");

    try {
      const response = await fetch(apiUrl("/api/renders"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          code,
          format: "custom_harness",
          captcha_token: extractCaptchaToken()
        })
      });

      const payload = await readJsonResponse(response, "The backend rejected this render request.");
      if (!response.ok) {
        throw new Error(payload.detail || "The backend rejected this render request.");
      }

      currentJob = {
        jobId: payload.job_id,
        accessToken: payload.access_token
      };

      jobIdEl.textContent = payload.job_id;
      jobStatusEl.textContent = payload.status;
      jobMessageEl.textContent = "Render queued and waiting for a worker.";
      setStatus("Render job submitted. Polling for status updates...", "warning");

      await pollJobStatus();
      if (currentJob && !pollTimer && !["completed", "failed", "expired"].includes(jobStatusEl.textContent)) {
        pollTimer = setInterval(pollJobStatus, pollIntervalMs);
      }
    } catch (error) {
      console.error(error);
      setStatus(error.message || "Submission failed unexpectedly.", "danger");
      setBusy(false);
    } finally {
      resetCaptcha();
    }
  }

  function initTurnstile() {
    apiBaseDisplayEl.textContent = normalizedApiBase || "Same origin";

    if (!turnstileSiteKey) {
      captchaNoteEl.textContent = "CAPTCHA is not configured on this site. Local development requires backend bypass mode.";
      return;
    }

    captchaNoteEl.textContent = "Complete the CAPTCHA before submitting a public render job.";

    const renderWidget = () => {
      if (!window.turnstile || turnstileWidgetId !== null) {
        return;
      }

      turnstileWidgetId = window.turnstile.render(turnstileEl, {
        sitekey: turnstileSiteKey,
        theme: "dark"
      });
    };

    if (window.turnstile) {
      renderWidget();
      return;
    }

    const waitForTurnstile = window.setInterval(() => {
      if (window.turnstile) {
        window.clearInterval(waitForTurnstile);
        renderWidget();
      }
    }, 250);
  }

  renderExampleButtons();
  initTurnstile();
  resetOutput();

  submitButtonEl.addEventListener("click", submitRender);
  clearButtonEl.addEventListener("click", () => {
    resetOutput();
    setStatus("Output cleared. Ready for another render job.", "neutral");
  });
});

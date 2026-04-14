---
layout: default
title: Manim Visualizer
nav_order: 3
---

# Manim Visualizer

Use the custom Manim harness from this project to submit algorithm visualization code and receive a rendered `.mp4` once the backend job finishes.

<p>
  This v1 visualizer accepts the custom <code>Node</code>, <code>ManimList</code>, and <code>manimScene</code> runtime from <code>manimTest.py</code>. Plain Manim scene classes are not supported in this browser flow yet.
</p>

<div
  id="manim-visualizer-root"
  data-api-base="{{ site.manim_visualizer.api_base | default: '' }}"
  data-turnstile-site-key="{{ site.manim_visualizer.turnstile_site_key | default: '' }}"
>
  <style>
    .manim-visualizer-layout {
      display: grid;
      gap: 1.25rem;
      grid-template-columns: minmax(0, 1.6fr) minmax(280px, 1fr);
      margin-top: 1.5rem;
    }

    .manim-panel {
      background: rgba(15, 23, 42, 0.45);
      border: 1px solid rgba(148, 163, 184, 0.25);
      border-radius: 16px;
      padding: 1rem;
    }

    .manim-panel h2,
    .manim-panel h3 {
      margin-top: 0;
    }

    .manim-toolbar {
      display: flex;
      flex-wrap: wrap;
      gap: 0.75rem;
      margin-bottom: 1rem;
    }

    .manim-toolbar button,
    .manim-submit-row button,
    .manim-download-link {
      appearance: none;
      border: 1px solid rgba(148, 163, 184, 0.35);
      border-radius: 999px;
      background: rgba(59, 130, 246, 0.12);
      color: inherit;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font: inherit;
      gap: 0.4rem;
      min-height: 2.5rem;
      padding: 0.6rem 1rem;
      text-decoration: none;
      transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
    }

    .manim-toolbar button:hover,
    .manim-submit-row button:hover,
    .manim-download-link:hover {
      background: rgba(59, 130, 246, 0.22);
      border-color: rgba(96, 165, 250, 0.6);
      transform: translateY(-1px);
    }

    .manim-toolbar button[disabled],
    .manim-submit-row button[disabled] {
      cursor: not-allowed;
      opacity: 0.6;
      transform: none;
    }

    .manim-code-input {
      min-height: 28rem;
      width: 100%;
      border-radius: 14px;
      border: 1px solid rgba(148, 163, 184, 0.28);
      background: rgba(2, 6, 23, 0.88);
      color: #e2e8f0;
      font-family: Consolas, "Courier New", monospace;
      font-size: 0.95rem;
      line-height: 1.5;
      padding: 1rem;
      resize: vertical;
    }

    .manim-meta-list {
      display: grid;
      gap: 0.75rem;
      margin: 0;
      padding: 0;
      list-style: none;
    }

    .manim-meta-list strong {
      display: block;
      margin-bottom: 0.25rem;
    }

    .manim-status-banner {
      border-radius: 12px;
      margin-bottom: 1rem;
      padding: 0.9rem 1rem;
      background: rgba(15, 118, 110, 0.18);
      border: 1px solid rgba(45, 212, 191, 0.28);
    }

    .manim-status-banner[data-tone="warning"] {
      background: rgba(217, 119, 6, 0.15);
      border-color: rgba(251, 191, 36, 0.28);
    }

    .manim-status-banner[data-tone="danger"] {
      background: rgba(153, 27, 27, 0.18);
      border-color: rgba(248, 113, 113, 0.3);
    }

    .manim-status-banner[data-tone="neutral"] {
      background: rgba(51, 65, 85, 0.32);
      border-color: rgba(148, 163, 184, 0.22);
    }

    .manim-submit-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.9rem;
      margin-top: 1rem;
    }

    .manim-inline-note {
      color: #cbd5e1;
      font-size: 0.95rem;
    }

    .manim-output {
      display: grid;
      gap: 1rem;
      margin-top: 1rem;
    }

    .manim-output video {
      width: 100%;
      border-radius: 14px;
      background: #020617;
    }

    .manim-error {
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      font-family: Consolas, "Courier New", monospace;
      background: rgba(2, 6, 23, 0.88);
      border-radius: 14px;
      border: 1px solid rgba(248, 113, 113, 0.3);
      padding: 1rem;
    }

    .manim-hidden {
      display: none !important;
    }

    @media (max-width: 960px) {
      .manim-visualizer-layout {
        grid-template-columns: 1fr;
      }
    }
  </style>

  <div class="manim-status-banner" id="manim-status" data-tone="neutral">
    Load an example or paste custom harness code, then submit a render job.
  </div>

  <div class="manim-visualizer-layout">
    <section class="manim-panel">
      <h2>Editor</h2>
      <p class="manim-inline-note">
        Example files below are served directly from this site and can be used as a starting point.
      </p>

      <div class="manim-toolbar" id="manim-example-buttons"></div>

      <label for="manim-code-input"><strong>Visualization Code</strong></label>
      <textarea id="manim-code-input" class="manim-code-input" spellcheck="false"></textarea>

      <div class="manim-submit-row">
        <button id="manim-submit-button" type="button">Render MP4</button>
        <button id="manim-clear-button" type="button">Clear Output</button>
        <span class="manim-inline-note" id="manim-captcha-note"></span>
      </div>

      <div id="manim-turnstile" style="margin-top: 1rem;"></div>
    </section>

    <aside class="manim-panel">
      <h2>Job Details</h2>
      <ul class="manim-meta-list">
        <li>
          <strong>API Base</strong>
          <span id="manim-api-base-display">Same origin</span>
        </li>
        <li>
          <strong>Current Job</strong>
          <span id="manim-job-id">Not started</span>
        </li>
        <li>
          <strong>Status</strong>
          <span id="manim-job-status">Idle</span>
        </li>
        <li>
          <strong>Message</strong>
          <span id="manim-job-message">Waiting for a submission.</span>
        </li>
      </ul>

      <div class="manim-output">
        <div id="manim-video-card" class="manim-hidden">
          <h3>Rendered Video</h3>
          <video id="manim-video" controls preload="metadata"></video>
          <p style="margin-top: 0.75rem;">
            <a id="manim-download-link" class="manim-download-link" href="#" download>Download MP4</a>
          </p>
        </div>

        <div id="manim-error-card" class="manim-hidden">
          <h3>Render Error</h3>
          <pre id="manim-error-output" class="manim-error"></pre>
        </div>
      </div>
    </aside>
  </div>
</div>

<script src="https://challenges.cloudflare.com/turnstile/v0/api.js?render=explicit" async defer></script>
<script src="/assets/js/manim-visualizer.js"></script>

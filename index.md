---
layout: home
title: Home
nav_order: 1
---

# Competitive Programming Primer

Welcome to the website!

If you wish to tackle ICPC contest problems from North America, explore the regional map below. If you want to practice curated problems from Kattis or browse the full repository, the Problem Repository is available in the left navigation.

## Explore Problems by North America Region

<div id="map-wrapper" style="margin: 2rem 0;">
  <object
    id="world-map-object"
    type="image/svg+xml"
    data="/assets/images/world-map.svg"
    style="width: 100%; max-width: 960px; height: auto;"
    aria-label="North America ICPC regional map"
  >
    Your browser does not support SVG maps.
  </object>
</div>

<p style="margin-top: -0.5rem; color: #94a3b8;">
  Select a North America region to load matching problems from Supabase.
</p>

<div id="region-info">
  <h2 id="region-title">Select a region</h2>
  <div id="region-problems">Click a region on the map to view problems.</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="/assets/js/home-map.js"></script>

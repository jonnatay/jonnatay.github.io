---
layout: home
title: Home
nav_order: 1
---

# Competitive Programming Primer

Welcome to the website!

If you wish to tackle ICPC contest problems given in a specific region, explore the map below, and if you wish to practice curated problems from Kattis or just wish to browse through problems, our Problem Repository is also available on the left!

## Explore Problems by Region

<div id="map-wrapper" style="margin: 2rem 0;">
    <object
        id="world-map-object"
        type="image/svg+xml"
        data="/assets/images/world-map.svg"
        style="width: 100%; max-width: 1000px; height: auto;"
    >
  Your browser does not support SVG maps.
</object>
</div>

<div id="region-info">
  <h2 id="region-title">Select a region</h2>
  <div id="region-problems">Click a region on the map to view problems.</div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="/assets/js/home-map.js"></script>
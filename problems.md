---
layout: default
title: Problem Repository
nav_order: 2
---

# Problem Repository

<p>Browse practice problems from the database.</p>

<div class="search-box" style="margin-bottom: 1rem;">
  <input id="problem-search" type="text" placeholder="Search by title, region, competition, or level" style="width: 100%; padding: 0.5rem;">
</div>

<div id="problems-status">Loading problems...</div>
<div id="problems-table"></div>

<hr>

<div id="problem-detail"></div>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script src="/assets/js/problems.js"></script>
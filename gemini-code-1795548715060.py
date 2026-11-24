import os

# Build Golf_Analytics_Studio_v3 (index.html) with:
# 1. Empty STARTER_ROUNDS = [] (zero personal rounds embedded for safe public GitHub hosting)
# 2. Round vs. Historical Baseline Comparison Panel (Latest/Selected Round vs All Prior Rounds, Last 5 Prior Rounds, or Same Course Prior Rounds)
# 3. Traditional GIR %, Up & Down %, Scoring Distribution, Gross Scoring Trend, Par 3/4/5 breakdown, SQL console, Round Log

html_v3 = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0" />
<meta name="apple-mobile-web-app-capable" content="yes" />
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
<meta name="apple-mobile-web-app-title" content="Golf Stats" />
<title>Golf Analytics Studio v3 — Custom Garmin Scorecard Intelligence</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/alasql@4.4.0/dist/alasql.min.js"></script>
<style>
  :root {
    --bg: #0f172a;
    --surface: #1e293b;
    --surface-hover: #273549;
    --border: #334155;
    --text: #f8fafc;
    --text-muted: #94a3b8;
    --accent: #10b981;
    --accent-soft: rgba(16, 185, 129, 0.15);
    --blue: #38bdf8;
    --amber: #f59e0b;
    --rose: #f43f5e;
    --purple: #a78bfa;
    --cyan: #22d3ee;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.5;
    padding: 20px;
  }
  .container { max-width: 1440px; margin: 0 auto; }
  header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 16px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 24px;
  }
  .brand h1 { font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
  .brand p { color: var(--text-muted); font-size: 0.88rem; margin-top: 2px; }
  .badge {
    background: var(--accent-soft);
    color: var(--accent);
    border: 1px solid rgba(16, 185, 129, 0.35);
    padding: 2px 10px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
  }
  .actions { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
  button, .file-btn {
    background: var(--surface);
    color: var(--text);
    border: 1px solid var(--border);
    padding: 9px 14px;
    border-radius: 8px;
    font-size: 0.85rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.15s ease;
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }
  button:hover, .file-btn:hover { background: var(--surface-hover); border-color: #475569; }
  .btn-primary { background: var(--accent); color: #052e16; border-color: var(--accent); }
  .btn-primary:hover { background: #059669; color: #fff; }
  .btn-danger { color: var(--rose); border-color: rgba(244, 63, 94, 0.35); }
  .btn-danger:hover { background: rgba(244, 63, 94, 0.15); }
  input[type="file"] { display: none; }

  /* Dropzone Banner */
  .dropzone {
    border: 2px dashed var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    background: rgba(30, 41, 59, 0.5);
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    margin-bottom: 20px;
    transition: border-color 0.2s, background 0.2s;
  }
  .dropzone.dragover { border-color: var(--accent); background: var(--accent-soft); }
  .dropzone-text { font-size: 0.88rem; color: var(--text-muted); }
  .dropzone-text strong { color: var(--text); }

  /* Filter Bar */
  .filters {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
  }
  .filter-group label {
    display: block;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
    margin-bottom: 5px;
    font-weight: 600;
  }
  select, input[type="date"], input[type="text"], textarea {
    width: 100%;
    background: var(--bg);
    color: var(--text);
    border: 1px solid var(--border);
    border-radius: 7px;
    padding: 8px 10px;
    font-size: 0.85rem;
    outline: none;
  }
  select:focus, input:focus, textarea:focus { border-color: var(--accent); }

  /* KPI Grid */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 14px;
    margin-bottom: 16px;
  }
  .kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
  }
  .kpi-label { font-size: 0.76rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; }
  .kpi-value { font-size: 1.85rem; font-weight: 700; margin: 6px 0 4px; letter-spacing: -0.02em; }
  .kpi-sub { font-size: 0.8rem; color: var(--text-muted); }
  .highlight-green { color: var(--accent); }
  .highlight-blue { color: var(--blue); }
  .highlight-amber { color: var(--amber); }
  .highlight-rose { color: var(--rose); }
  .highlight-purple { color: var(--purple); }
  .highlight-cyan { color: var(--cyan); }

  /* Scoring Breakdown Strip */
  .scoring-strip {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(155px, 1fr));
    gap: 12px;
    margin-bottom: 24px;
  }
  .score-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 14px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .score-box-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.74rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--text-muted);
  }
  .score-box-val { font-size: 1.55rem; font-weight: 700; margin: 4px 0 2px; }
  .score-box-sub { font-size: 0.76rem; color: var(--text-muted); }

  /* Panels & Charts Grid */
  .panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 18px;
  }
  .panel-header {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    gap: 12px;
  }
  .panel-title { font-size: 1rem; font-weight: 700; }
  .panel-sub { font-size: 0.8rem; color: var(--text-muted); }
  .charts-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(440px, 1fr));
    gap: 16px;
    margin-bottom: 24px;
  }
  .chart-wrap { position: relative; height: 260px; width: 100%; }

  /* Round vs. Historical Baseline Panel */
  .compare-section { margin-bottom: 24px; }
  .compare-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    align-items: center;
  }
  .compare-controls select {
    width: auto;
    min-width: 210px;
  }
  .compare-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
    gap: 12px;
  }
  .cmp-card {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 14px;
  }
  .cmp-label {
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--text-muted);
    font-weight: 600;
  }
  .cmp-row {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    gap: 8px;
    margin: 5px 0 3px;
  }
  .cmp-val { font-size: 1.45rem; font-weight: 700; }
  .cmp-base { font-size: 0.77rem; color: var(--text-muted); }
  .delta-badge {
    font-size: 0.74rem;
    font-weight: 700;
    padding: 2px 7px;
    border-radius: 6px;
  }
  .delta-good { background: rgba(16, 185, 129, 0.18); color: var(--accent); }
  .delta-bad { background: rgba(244, 63, 94, 0.18); color: var(--rose); }
  .delta-neutral { background: rgba(148, 163, 184, 0.15); color: var(--text-muted); }

  /* SQL Query Console */
  .sql-section { margin-bottom: 24px; }
  .sql-presets { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 10px; }
  .preset-chip {
    background: var(--bg);
    border: 1px solid var(--border);
    color: var(--blue);
    padding: 5px 10px;
    border-radius: 6px;
    font-size: 0.78rem;
    cursor: pointer;
  }
  .preset-chip:hover { border-color: var(--blue); background: rgba(56, 189, 248, 0.1); }
  .sql-box { display: flex; gap: 10px; align-items: stretch; }
  .sql-box textarea { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; min-height: 68px; resize: vertical; }
  .sql-results { margin-top: 14px; overflow-x: auto; max-height: 320px; }

  /* Tables */
  table { width: 100%; border-collapse: collapse; font-size: 0.83rem; }
  th, td { text-align: left; padding: 9px 11px; border-bottom: 1px solid var(--border); white-space: nowrap; }
  th { color: var(--text-muted); font-weight: 600; font-size: 0.74rem; text-transform: uppercase; letter-spacing: 0.04em; background: rgba(15, 23, 42, 0.55); position: sticky; top: 0; }
  tr:hover td { background: rgba(255, 255, 255, 0.025); }
  .pill { padding: 2px 8px; border-radius: 999px; font-size: 0.74rem; font-weight: 600; }
  .pill-green { background: rgba(16, 185, 129, 0.18); color: var(--accent); }
  .pill-blue { background: rgba(56, 189, 248, 0.18); color: var(--blue); }
  .pill-amber { background: rgba(245, 158, 11, 0.18); color: var(--amber); }
  .pill-rose { background: rgba(244, 63, 94, 0.18); color: var(--rose); }
  .pill-purple { background: rgba(167, 139, 250, 0.18); color: var(--purple); }

  /* Modal for Hole-by-Hole Scorecard */
  .modal-backdrop {
    display: none;
    position: fixed;
    inset: 0;
    background: rgba(2, 6, 23, 0.78);
    z-index: 50;
    align-items: center;
    justify-content: center;
    padding: 20px;
  }
  .modal-backdrop.open { display: flex; }
  .modal {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    max-width: 960px;
    width: 100%;
    max-height: 88vh;
    overflow-y: auto;
    padding: 22px;
  }
  @media (max-width: 640px) {
    .charts-grid { grid-template-columns: 1fr; }
    .compare-controls select { width: 100%; }
  }
</style>
</head>
<body>
<div class="container">
  <header>
    <div class="brand">
      <h1>⛳ Golf Analytics Studio <span class="badge">v3 • Private Client-Side Engine</span></h1>
      <p>Traditional GIR, Up &amp; Down Scrambling, Round vs. Historical Baseline Comparison &amp; SQL Querying</p>
    </div>
    <div class="actions">
      <label class="file-btn btn-primary" for="fitInput">📂 Import Garmin .FIT / JSON</label>
      <input type="file" id="fitInput" accept=".fit,.json" multiple />
      <button id="exportJsonBtn">⬇️ Export Clean JSON</button>
      <button id="resetDataBtn" class="btn-danger">🗑️ Clear All Data</button>
    </div>
  </header>

  <div class="dropzone" id="dropzone">
    <div class="dropzone-text" id="dataStatusText">
      <strong>Active Dataset:</strong> Checking local browser storage...
    </div>
    <div class="dropzone-text">
      🔒 <strong>100% Private:</strong> All scorecards stay in your browser's local storage and never upload to any server.
    </div>
  </div>

  <!-- Global Filters -->
  <div class="filters">
    <div class="filter-group">
      <label>Round Length Rule</label>
      <select id="roundScopeFilter">
        <option value="18" selected>18-Hole Rounds Only (Default)</option>
        <option value="all">All Rounds (9 &amp; 18 Holes)</option>
      </select>
    </div>
    <div class="filter-group">
      <label>Course</label>
      <select id="courseFilter">
        <option value="ALL">All Courses</option>
      </select>
    </div>
    <div class="filter-group">
      <label>From Date</label>
      <input type="date" id="dateFrom" />
    </div>
    <div class="filter-group">
      <label>To Date</label>
      <input type="date" id="dateTo" />
    </div>
    <div class="filter-group">
      <label>Hole Par Filter (Hole Stats)</label>
      <select id="parFilter">
        <option value="ALL">All Pars (3, 4, 5)</option>
        <option value="3">Par 3s Only</option>
        <option value="4">Par 4s Only</option>
        <option value="5">Par 5s Only</option>
      </select>
    </div>
    <div class="filter-group">
      <label>Tee Shot Outcome (Par 4/5)</label>
      <select id="firFilter">
        <option value="ALL">All Tee Shots</option>
        <option value="HIT">Fairway Hit</option>
        <option value="LEFT">Missed Left</option>
        <option value="RIGHT">Missed Right</option>
      </select>
    </div>
  </div>

  <!-- Round vs. Historical Baseline Comparison Panel -->
  <div class="panel compare-section" id="compareSection">
    <div class="panel-header">
      <div>
        <div class="panel-title">📊 Round vs. Historical Baseline Comparison</div>
        <div class="panel-sub" id="compareSubtitle">See how your latest round stacks up against your historical averages across every area</div>
      </div>
      <div class="compare-controls">
        <select id="compareRoundSelect" aria-label="Select round to compare"></select>
        <select id="compareBaselineSelect" aria-label="Select historical baseline">
          <option value="all_prior" selected>vs. All Prior Rounds</option>
          <option value="last5_prior">vs. Last 5 Prior Rounds</option>
          <option value="same_course">vs. Same Course Prior Rounds</option>
        </select>
      </div>
    </div>
    <div class="compare-grid" id="compareGrid"></div>
  </div>

  <!-- Core Performance KPI Grid -->
  <div class="kpi-grid" id="kpiGrid"></div>

  <!-- Scoring Breakdown Strip: Albatross -> Double Bogey+ -->
  <div class="scoring-strip" id="scoringStrip"></div>

  <!-- Charts -->
  <div class="charts-grid">
    <div class="panel">
      <div class="panel-header">
        <div>
          <div class="panel-title">Greens in Regulation (GIR %) by Round</div>
          <div class="panel-sub">Traditional GIR: reaching the green putting for birdie, eagle, or better</div>
        </div>
      </div>
      <div class="chart-wrap"><canvas id="girChart"></canvas></div>
    </div>
    <div class="panel">
      <div class="panel-header">
        <div>
          <div class="panel-title">Gross Scoring Trend</div>
          <div class="panel-sub">Gross strokes per round across filtered rounds</div>
        </div>
      </div>
      <div class="chart-wrap"><canvas id="scoreChart"></canvas></div>
    </div>
    <div class="panel">
      <div class="panel-header">
        <div>
          <div class="panel-title">Scoring Average &amp; GIR % by Par</div>
          <div class="panel-sub">Average score over par paired with Traditional GIR % on Par 3s, 4s, and 5s</div>
        </div>
      </div>
      <div class="chart-wrap"><canvas id="parChart"></canvas></div>
    </div>
    <div class="panel">
      <div class="panel-header">
        <div>
          <div class="panel-title">Tee Shot Dispersion &amp; Scoring Impact</div>
          <div class="panel-sub">Par 4 &amp; Par 5 fairway hits vs. left/right misses and resulting score to par</div>
        </div>
      </div>
      <div class="chart-wrap"><canvas id="firChart"></canvas></div>
    </div>
  </div>

  <!-- Custom SQL Query Engine -->
  <div class="panel sql-section">
    <div class="panel-header">
      <div>
        <div class="panel-title">⚡ Ad-Hoc SQL Query Console (AlaSQL)</div>
        <div class="panel-sub">Query your <code>rounds</code> and <code>holes</code> tables directly in-browser</div>
      </div>
    </div>
    <div class="sql-presets">
      <button class="preset-chip" data-sql="SELECT course, COUNT(*) AS rounds, ROUND(AVG(gross),1) AS avg_gross, ROUND(AVG(girPct),1) AS gir_pct, ROUND(AVG(upAndDownPct),1) AS up_down_pct, ROUND(AVG(putts),1) AS avg_putts FROM rounds GROUP BY course ORDER BY rounds DESC">Course Leaderboard</button>
      <button class="preset-chip" data-sql="SELECT par, COUNT(*) AS holes, ROUND(AVG(strokes),2) AS avg_score, ROUND(AVG(strokes - par),2) AS to_par, ROUND(100.0 * SUM(CASE WHEN stdGir THEN 1 ELSE 0 END)/COUNT(*),1) AS gir_pct, ROUND(100.0 * SUM(CASE WHEN NOT stdGir AND strokes <= par THEN 1 ELSE 0 END)/NULLIF(SUM(CASE WHEN NOT stdGir THEN 1 ELSE 0 END),0),1) AS up_down_pct FROM holes GROUP BY par ORDER BY par">Stats by Par (3 / 4 / 5)</button>
      <button class="preset-chip" data-sql="SELECT CASE WHEN yards < 350 THEN 'Under 350y' WHEN yards <= 400 THEN '350-400y' ELSE '400y+' END AS length_band, COUNT(*) AS holes, ROUND(AVG(strokes - par),2) AS avg_to_par, ROUND(100.0 * SUM(CASE WHEN stdGir THEN 1 ELSE 0 END)/COUNT(*),1) AS gir_pct FROM holes WHERE par = 4 AND yards IS NOT NULL GROUP BY CASE WHEN yards < 350 THEN 'Under 350y' WHEN yards <= 400 THEN '350-400y' ELSE '400y+' END">Par 4 Length Brackets</button>
      <button class="preset-chip" data-sql="SELECT fir AS tee_outcome, COUNT(*) AS holes, ROUND(AVG(strokes - par),2) AS avg_to_par, ROUND(100.0 * SUM(CASE WHEN stdGir THEN 1 ELSE 0 END)/COUNT(*),1) AS gir_pct, ROUND(AVG(penalties),2) AS avg_penalties FROM holes WHERE par >= 4 GROUP BY fir">Fairway Hit vs Left/Right Miss</button>
      <button class="preset-chip" data-sql="SELECT date, course, hole, par, yards, strokes, putts, fir FROM holes WHERE strokes >= par + 2 ORDER BY date DESC, hole ASC">All Double-Bogey+ Holes</button>
    </div>
    <div class="sql-box">
      <textarea id="sqlInput">SELECT course, COUNT(*) AS rounds, ROUND(AVG(gross),1) AS avg_gross, ROUND(AVG(girPct),1) AS gir_pct, ROUND(AVG(upAndDownPct),1) AS up_down_pct, ROUND(AVG(putts),1) AS avg_putts FROM rounds GROUP BY course ORDER BY rounds DESC</textarea>
      <button id="runSqlBtn" class="btn-primary">Run Query</button>
    </div>
    <div class="sql-results" id="sqlResults"></div>
  </div>

  <!-- Round Log Table -->
  <div class="panel">
    <div class="panel-header">
      <div>
        <div class="panel-title">Round Log</div>
        <div class="panel-sub">Click any round to inspect hole-by-hole GIR, Up &amp; Downs, and scoring breakdown</div>
      </div>
    </div>
    <div style="overflow-x:auto;">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Course</th>
            <th>Tee</th>
            <th>Par</th>
            <th>Gross</th>
            <th>+/-</th>
            <th>Out / In</th>
            <th>GIR</th>
            <th>Up &amp; Down</th>
            <th>Putts</th>
            <th>FIR</th>
            <th>Alb</th>
            <th>Eag</th>
            <th>Bir</th>
            <th>Par</th>
            <th>Bog</th>
            <th>Dbl+</th>
          </tr>
        </thead>
        <tbody id="roundsTableBody"></tbody>
      </table>
    </div>
  </div>
</div>

<!-- Hole-by-Hole Modal -->
<div class="modal-backdrop" id="roundModal">
  <div class="modal">
    <div class="panel-header">
      <div>
        <div class="panel-title" id="modalTitle">Round Breakdown</div>
        <div class="panel-sub" id="modalSub"></div>
      </div>
      <button id="closeModalBtn">✕ Close</button>
    </div>
    <div style="overflow-x:auto;">
      <table>
        <thead>
          <tr>
            <th>Hole</th>
            <th>Par</th>
            <th>SI</th>
            <th>Yards</th>
            <th>Score</th>
            <th>Result</th>
            <th>FIR</th>
            <th>Putts</th>
            <th>GIR</th>
            <th>Up &amp; Down</th>
            <th>Penalties</th>
          </tr>
        </thead>
        <tbody id="modalTableBody"></tbody>
      </table>
    </div>
  </div>
</div>

<script>
// Empty starter dataset so this file is 100% safe to host on a public GitHub Pages repo
const STARTER_ROUNDS = [];
const STORAGE_KEY = 'golf_analytics_studio_rounds_v1';

let allRounds = [];
let charts = {};

// --- Pure JS Garmin .FIT Binary Parser ---
const FIT_EPOCH_MS = Date.UTC(1989, 11, 31, 0, 0, 0);
const BASE_TYPES = {
  0x00: ['u8', 1, 0xFF], 0x01: ['i8', 1, 0x7F], 0x02: ['u8', 1, 0xFF],
  0x83: ['i16', 2, 0x7FFF], 0x84: ['u16', 2, 0xFFFF], 0x85: ['i32', 4, 0x7FFFFFFF],
  0x86: ['u32', 4, 0xFFFFFFFF], 0x07: ['str', 1, 0], 0x88: ['f32', 4, null],
  0x89: ['f64', 8, null], 0x0A: ['u8', 1, 0x00], 0x8B: ['u16', 2, 0x0000],
  0x8C: ['u32', 4, 0x00000000], 0x0D: ['u8', 1, 0xFF]
};

function readFieldVal(view, offset, typeCode, littleEndian) {
  const spec = BASE_TYPES[typeCode];
  if (!spec) return null;
  const [kind, , invalid] = spec;
  let val = null;
  if (kind === 'u8') val = view.getUint8(offset);
  else if (kind === 'i8') val = view.getInt8(offset);
  else if (kind === 'u16') val = view.getUint16(offset, littleEndian);
  else if (kind === 'i16') val = view.getInt16(offset, littleEndian);
  else if (kind === 'u32') val = view.getUint32(offset, littleEndian);
  else if (kind === 'i32') val = view.getInt32(offset, littleEndian);
  else if (kind === 'f32') val = view.getFloat32(offset, littleEndian);
  else if (kind === 'f64') val = view.getFloat64(offset, littleEndian);
  if (invalid !== null && val === invalid) return null;
  return val;
}

function parseFitBuffer(arrayBuffer, fileName) {
  const view = new DataView(arrayBuffer);
  const bytes = new Uint8Array(arrayBuffer);
  if (bytes.length < 14) return null;
  const headerSize = view.getUint8(0);
  const dataSize = view.getUint32(4, true);
  let pos = headerSize;
  const end = Math.min(bytes.length, headerSize + dataSize);
  const localDefs = {};
  let m190 = null, m191 = null;
  const m192 = [], m193 = [];

  while (pos < end) {
    const hdr = view.getUint8(pos++);
    let isDef = false, hasDev = false, localNum = 0;
    if (hdr & 0x80) {
      localNum = (hdr >> 5) & 0x03;
    } else {
      isDef = Boolean(hdr & 0x40);
      hasDev = Boolean(hdr & 0x20);
      localNum = hdr & 0x0F;
    }

    if (isDef) {
      pos++; // reserved
      const arch = view.getUint8(pos++);
      const le = arch === 0;
      const gNum = view.getUint16(pos, le); pos += 2;
      const numFields = view.getUint8(pos++);
      const fields = [];
      for (let i = 0; i < numFields; i++) {
        fields.push([view.getUint8(pos), view.getUint8(pos + 1), view.getUint8(pos + 2)]);
        pos += 3;
      }
      let devBytes = 0;
      if (hasDev) {
        const numDev = view.getUint8(pos++);
        for (let i = 0; i < numDev; i++) {
          devBytes += view.getUint8(pos + 1);
          pos += 3;
        }
      }
      localDefs[localNum] = { le, gNum, fields, devBytes };
    } else {
      const def = localDefs[localNum];
      if (!def) break;
      const msg = {};
      for (const [fNum, fSize, fType] of def.fields) {
        if (fType === 0x07) {
          let endStr = pos;
          while (endStr < pos + fSize && bytes[endStr] !== 0) endStr++;
          const str = new TextDecoder('utf-8').decode(bytes.subarray(pos, endStr));
          if (str) msg[fNum] = str;
        } else {
          const spec = BASE_TYPES[fType];
          if (spec && fSize === spec[1]) {
            const v = readFieldVal(view, pos, fType, def.le);
            if (v !== null) msg[fNum] = v;
          }
        }
        pos += fSize;
      }
      pos += def.devBytes;
      if (def.gNum === 190) m190 = msg;
      else if (def.gNum === 191) m191 = msg;
      else if (def.gNum === 192) m192.push(msg);
      else if (def.gNum === 193) m193.push(msg);
    }
  }

  if (!m190 || !m191 || m192.length === 0) return null;
  const startTs = m190[3] || m190[253] || 0;
  const dt = new Date(FIT_EPOCH_MS + startTs * 1000);
  const dateStr = dt.toISOString().slice(0, 10);
  const timeStr = dt.toISOString().slice(11, 16);

  const infoMap = {};
  m193.forEach(h => { if (h[0] !== undefined) infoMap[h[0]] = h; });

  const holes = m192.map((hs, idx) => {
    const hNum = hs[1] !== undefined ? hs[1] : idx + 1;
    const hi = infoMap[hNum] || {};
    const par = hi[2] || 4;
    const si = hi[3] || null;
    const distCm = hi[1] || null;
    const yards = distCm ? Math.round(distCm * 0.010936133) : null;
    const strokes = hs[2] !== undefined ? hs[2] : null;
    const putts = hs[5] !== undefined ? hs[5] : null;
    const f6 = hs[6];
    const penalties = hs[9] || 0;

    let fir = 'NA';
    if (par >= 4) {
      if (f6 === 2) fir = 'HIT';
      else if (f6 === 0) fir = 'LEFT';
      else if (f6 === 1) fir = 'RIGHT';
    }

    // Traditional GIR: reaching the green putting for birdie, eagle, or better (strokes - putts <= par - 2)
    let stdGir = false;
    if (strokes !== null && putts !== null) {
      if (putts > 0 && (strokes - putts) <= (par - 2)) stdGir = true;
      else if (putts === 0 && strokes <= (par - 2)) stdGir = true;
    }

    return { hole: hNum, par, si, yards, strokes, putts, fir, penalties, stdGir };
  });

  const rawId = fileName.replace(/^.*RAWDATA-/, '').replace(/\.fit$/i, '') || `${dateStr}_${m190[1]}`;
  return {
    id: rawId,
    fileName,
    date: dateStr,
    time: timeStr,
    course: m190[1] || 'Unknown Course',
    tee: m190[11] || 'Standard',
    courseRating: m190[21] ? Number(m190[21].toFixed(1)) : null,
    slopeRating: m190[12] || null,
    par: m190[10] || holes.reduce((a, b) => a + b.par, 0),
    holesCount: holes.length,
    gross: m191[4] || holes.reduce((a, b) => a + (b.strokes || 0), 0),
    outScore: m191[2] || null,
    inScore: m191[3] || null,
    garminFir: m191[7] !== undefined ? m191[7] : null,
    garminGir: m191[8] !== undefined ? m191[8] : null,
    garminPutts: m191[9] !== undefined ? m191[9] : null,
    holes
  };
}

// --- Storage & State Management ---
function normalizeRound(r) {
  const holes = (r.holes || []).map(h => {
    let stdGir = false;
    if (h.strokes !== null && h.strokes !== undefined && h.putts !== null && h.putts !== undefined) {
      if (h.putts > 0 && (h.strokes - h.putts) <= (h.par - 2)) stdGir = true;
      else if (h.putts === 0 && h.strokes <= (h.par - 2)) stdGir = true;
    }
    return { ...h, stdGir };
  });
  return { ...r, holes };
}

function loadInitialData() {
  const saved = localStorage.getItem(STORAGE_KEY);
  if (saved) {
    try {
      const parsed = JSON.parse(saved);
      if (Array.isArray(parsed) && parsed.length > 0) {
        allRounds = parsed.map(normalizeRound);
        allRounds.sort((a, b) => a.date.localeCompare(b.date));
        updateStatus(`<strong>Active Dataset:</strong> ${allRounds.length} rounds loaded from local browser storage.`);
        return;
      }
    } catch (e) {}
  }
  allRounds = STARTER_ROUNDS.map(normalizeRound);
  updateStatus(`<strong>Ready for Your Data:</strong> 0 rounds stored yet. Click <strong>Import Garmin .FIT / JSON</strong> above to load your backup JSON or <code>.fit</code> scorecards.`);
}

function saveData() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(allRounds));
}

function updateStatus(html) {
  document.getElementById('dataStatusText').innerHTML = html;
}

async function handleFiles(fileList) {
  const files = Array.from(fileList);
  if (!files.length) return;
  const existingIds = new Set(allRounds.map(r => r.id));
  let added = 0, skipped = 0;

  for (const file of files) {
    if (file.name.toLowerCase().endsWith('.fit')) {
      const buf = await file.arrayBuffer();
      const round = parseFitBuffer(buf, file.name);
      if (round) {
        if (!existingIds.has(round.id)) {
          allRounds.push(normalizeRound(round));
          existingIds.add(round.id);
          added++;
        } else {
          skipped++;
        }
      }
    } else if (file.name.toLowerCase().endsWith('.json')) {
      try {
        const txt = await file.text();
        const parsed = JSON.parse(txt);
        const arr = Array.isArray(parsed) ? parsed : (parsed.rounds || []);
        for (const r of arr) {
          if (r && r.holes && !existingIds.has(r.id)) {
            allRounds.push(normalizeRound(r));
            existingIds.add(r.id);
            added++;
          } else if (r && r.holes) {
            skipped++;
          }
        }
      } catch (e) {}
    }
  }

  allRounds.sort((a, b) => a.date.localeCompare(b.date));
  saveData();
  populateCourseFilter();
  refreshDashboard();
  updateStatus(`<strong>Import Complete:</strong> Added <strong>${added}</strong> new round(s)${skipped ? ` (${skipped} duplicate(s) skipped)` : ''}. Total stored: <strong>${allRounds.length}</strong> rounds.`);
}

// --- Enrich Round Stats ---
function enrichRound(r) {
  const girCount = r.holes.filter(h => h.stdGir).length;
  const puttsKnown = r.holes.filter(h => h.putts !== null && h.putts !== undefined);
  const totalPutts = puttsKnown.reduce((s, h) => s + h.putts, 0);

  const missedGirHoles = r.holes.filter(h => !h.stdGir && h.strokes !== null && h.strokes !== undefined);
  const upAndDownMade = missedGirHoles.filter(h => h.strokes <= h.par).length;
  const upAndDownOpps = missedGirHoles.length;
  const upAndDownPct = upAndDownOpps ? Number(((upAndDownMade / upAndDownOpps) * 100).toFixed(1)) : 0;

  const firOpps = r.holes.filter(h => h.par >= 4 && h.fir !== 'NA');
  const firHits = firOpps.filter(h => h.fir === 'HIT').length;
  const firPct = firOpps.length ? Number(((firHits / firOpps.length) * 100).toFixed(1)) : null;

  let albatross = 0, eagles = 0, birdies = 0, pars = 0, bogeys = 0, dblPlus = 0;
  r.holes.forEach(h => {
    if (h.strokes === null || h.strokes === undefined) return;
    const diff = h.strokes - h.par;
    if (diff <= -3) albatross++;
    else if (diff === -2) eagles++;
    else if (diff === -1) birdies++;
    else if (diff === 0) pars++;
    else if (diff === 1) bogeys++;
    else dblPlus++;
  });

  // Par 3, 4, 5 scoring averages over par for the round
  const parAvg = {};
  [3, 4, 5].forEach(p => {
    const sub = r.holes.filter(h => h.par === p && h.strokes !== null && h.strokes !== undefined);
    parAvg[p] = sub.length ? sub.reduce((s, h) => s + (h.strokes - h.par), 0) / sub.length : null;
  });

  return {
    ...r,
    toPar: r.gross - r.par,
    girCount,
    girPct: Number(((girCount / r.holesCount) * 100).toFixed(1)),
    putts: totalPutts,
    hasPutts: puttsKnown.length >= Math.floor(r.holesCount * 0.8),
    upAndDownMade,
    upAndDownOpps,
    upAndDownPct,
    firHits,
    firOpps: firOpps.length,
    firPct,
    albatross,
    eagles,
    birdies,
    pars,
    bogeys,
    dblPlus,
    par3ToPar: parAvg[3],
    par4ToPar: parAvg[4],
    par5ToPar: parAvg[5]
  };
}

// --- Filtering & Metrics Computation ---
function populateCourseFilter() {
  const sel = document.getElementById('courseFilter');
  const current = sel.value;
  const courses = [...new Set(allRounds.map(r => r.course))].sort();
  sel.innerHTML = '<option value="ALL">All Courses (' + courses.length + ')</option>' +
    courses.map(c => `<option value="${c}">${c}</option>`).join('');
  if (courses.includes(current)) sel.value = current;
}

function getFilteredData() {
  const scope = document.getElementById('roundScopeFilter').value;
  const course = document.getElementById('courseFilter').value;
  const dateFrom = document.getElementById('dateFrom').value;
  const dateTo = document.getElementById('dateTo').value;
  const parFilter = document.getElementById('parFilter').value;
  const firFilter = document.getElementById('firFilter').value;

  const filteredRounds = allRounds.filter(r => {
    if (scope === '18' && r.holesCount !== 18) return false;
    if (course !== 'ALL' && r.course !== course) return false;
    if (dateFrom && r.date < dateFrom) return false;
    if (dateTo && r.date > dateTo) return false;
    return true;
  }).map(enrichRound);

  const filteredHoles = [];
  filteredRounds.forEach(r => {
    r.holes.forEach(h => {
      if (parFilter !== 'ALL' && String(h.par) !== parFilter) return;
      if (firFilter !== 'ALL' && h.fir !== firFilter) return;
      const isUpAndDownOpp = !h.stdGir && h.strokes !== null && h.strokes !== undefined;
      const isUpAndDownMade = isUpAndDownOpp && h.strokes <= h.par;
      filteredHoles.push({
        date: r.date,
        course: r.course,
        tee: r.tee,
        isUpAndDownOpp,
        isUpAndDownMade,
        ...h
      });
    });
  });

  return { filteredRounds, filteredHoles };
}

function refreshDashboard() {
  const { filteredRounds, filteredHoles } = getFilteredData();
  populateCompareSelector(filteredRounds);
  renderComparisonPanel(filteredRounds);
  renderKPIs(filteredRounds, filteredHoles);
  renderScoringStrip(filteredRounds, filteredHoles);
  renderCharts(filteredRounds, filteredHoles);
  renderRoundsTable(filteredRounds);
  syncSqlTables(filteredRounds, filteredHoles);
  runCurrentSql();
}

// --- Round vs. Historical Baseline Comparison ---
function populateCompareSelector(rounds) {
  const sel = document.getElementById('compareRoundSelect');
  const prevVal = sel.value;
  if (!rounds.length) {
    sel.innerHTML = '<option value="">No rounds loaded</option>';
    return;
  }
  const desc = [...rounds].sort((a, b) => b.date.localeCompare(a.date));
  sel.innerHTML = desc.map((r, idx) =>
    `<option value="${r.id}">${idx === 0 ? 'Latest: ' : ''}${r.date} — ${r.course} (${r.gross})</option>`
  ).join('');
  if (desc.some(r => r.id === prevVal)) {
    sel.value = prevVal;
  } else {
    sel.value = desc[0].id;
  }
}

function renderComparisonPanel(rounds) {
  const grid = document.getElementById('compareGrid');
  const sub = document.getElementById('compareSubtitle');
  if (!rounds.length) {
    sub.textContent = 'Import your Garmin scorecards to compare your latest round against your historical baseline.';
    grid.innerHTML = '';
    return;
  }

  const targetId = document.getElementById('compareRoundSelect').value;
  const baselineMode = document.getElementById('compareBaselineSelect').value;
  const target = rounds.find(r => r.id === targetId) || rounds[rounds.length - 1];

  // Prior rounds in chronological order before the selected round (or all other rounds if earliest is selected)
  const sortedAsc = [...rounds].sort((a, b) => a.date.localeCompare(b.date));
  const targetIdx = sortedAsc.findIndex(r => r.id === target.id);
  let pool = sortedAsc.slice(0, targetIdx);
  if (!pool.length) {
    pool = sortedAsc.filter(r => r.id !== target.id);
  }
  if (baselineMode === 'last5_prior') {
    pool = pool.slice(-5);
  } else if (baselineMode === 'same_course') {
    const sameCourse = pool.filter(r => r.course === target.course);
    if (sameCourse.length) pool = sameCourse;
  }

  if (!pool.length) {
    sub.textContent = `Showing ${target.date} (${target.course}) — add more rounds to unlock historical baseline deltas.`;
    grid.innerHTML = '';
    return;
  }

  const modeLabel = baselineMode === 'last5_prior'
    ? `last ${pool.length} prior round(s)`
    : baselineMode === 'same_course'
      ? `${pool.length} prior round(s) at ${target.course}`
      : `${pool.length} prior round(s)`;
  sub.textContent = `Comparing ${target.date} at ${target.course} against your average across ${modeLabel}`;

  const avg = arr => arr.reduce((a, b) => a + b, 0) / arr.length;
  const baseGross = avg(pool.map(r => r.gross));
  const baseToPar = avg(pool.map(r => r.toPar));
  const baseGir = avg(pool.map(r => r.girPct));
  const baseUd = avg(pool.map(r => r.upAndDownPct));
  const puttPool = pool.filter(r => r.hasPutts);
  const basePutts = puttPool.length ? avg(puttPool.map(r => r.putts)) : null;
  const firPool = pool.filter(r => r.firPct !== null);
  const baseFir = firPool.length ? avg(firPool.map(r => r.firPct)) : null;
  const baseBirdies = avg(pool.map(r => r.birdies + r.eagles + r.albatross));
  const basePars = avg(pool.map(r => r.pars));
  const baseBogeys = avg(pool.map(r => r.bogeys));
  const baseDbl = avg(pool.map(r => r.dblPlus));

  const p3Pool = pool.filter(r => r.par3ToPar !== null);
  const baseP3 = p3Pool.length ? avg(p3Pool.map(r => r.par3ToPar)) : null;
  const p4Pool = pool.filter(r => r.par4ToPar !== null);
  const baseP4 = p4Pool.length ? avg(p4Pool.map(r => r.par4ToPar)) : null;
  const p5Pool = pool.filter(r => r.par5ToPar !== null);
  const baseP5 = p5Pool.length ? avg(p5Pool.map(r => r.par5ToPar)) : null;

  function makeCard(label, val, base, unit, lowerIsBetter, decimals = 1, signed = false) {
    if (val === null || val === undefined || base === null || base === undefined) {
      return `<div class="cmp-card"><div class="cmp-label">${label}</div><div class="cmp-row"><span class="cmp-val">—</span></div><div class="cmp-base">Insufficient data</div></div>`;
    }
    const diff = val - base;
    const absDiff = Math.abs(diff);
    const fmtVal = (signed && val > 0 ? '+' : '') + val.toFixed(decimals) + unit;
    const fmtBase = (signed && base > 0 ? '+' : '') + base.toFixed(decimals) + unit;
    let cls = 'delta-neutral';
    if (absDiff >= 0.05) {
      const isGood = lowerIsBetter ? diff < 0 : diff > 0;
      cls = isGood ? 'delta-good' : 'delta-bad';
    }
    const signStr = diff > 0.04 ? '+' : (diff < -0.04 ? '' : '±');
    return `
      <div class="cmp-card">
        <div class="cmp-label">${label}</div>
        <div class="cmp-row">
          <span class="cmp-val">${fmtVal}</span>
          <span class="delta-badge ${cls}">${signStr}${diff.toFixed(decimals)}${unit}</span>
        </div>
        <div class="cmp-base">Hist. avg: <strong>${fmtBase}</strong></div>
      </div>
    `;
  }

  const targetBirdiesPlus = target.birdies + target.eagles + target.albatross;
  grid.innerHTML = [
    makeCard('Gross Score', target.gross, baseGross, '', true, 1, false),
    makeCard('Score to Par', target.toPar, baseToPar, '', true, 1, true),
    makeCard('GIR %', target.girPct, baseGir, '%', false, 1, false),
    makeCard('Up & Down %', target.upAndDownPct, baseUd, '%', false, 1, false),
    makeCard('Putts / Round', target.hasPutts ? target.putts : null, basePutts, '', true, 1, false),
    makeCard('Fairways Hit %', target.firPct, baseFir, '%', false, 1, false),
    makeCard('Birdies or Better', targetBirdiesPlus, baseBirdies, '', false, 1, false),
    makeCard('Pars', target.pars, basePars, '', false, 1, false),
    makeCard('Bogeys', target.bogeys, baseBogeys, '', true, 1, false),
    makeCard('Double Bogey+', target.dblPlus, baseDbl, '', true, 1, false),
    makeCard('Par 3 Avg (+/-)', target.par3ToPar, baseP3, '', true, 2, true),
    makeCard('Par 4 Avg (+/-)', target.par4ToPar, baseP4, '', true, 2, true),
    makeCard('Par 5 Avg (+/-)', target.par5ToPar, baseP5, '', true, 2, true)
  ].join('');
}

function renderKPIs(rounds, holes) {
  const grid = document.getElementById('kpiGrid');
  if (!rounds.length) {
    grid.innerHTML = '<div class="kpi-card"><div class="kpi-label">No Rounds Loaded</div><div class="kpi-sub">Click <strong>Import Garmin .FIT / JSON</strong> above to load your scorecards</div></div>';
    return;
  }
  const n = rounds.length;
  const avgGross = (rounds.reduce((s, r) => s + r.gross, 0) / n).toFixed(1);
  const avgToPar = (rounds.reduce((s, r) => s + r.toPar, 0) / n).toFixed(1);
  const bestGross = Math.min(...rounds.map(r => r.gross));

  const totalHoles = holes.length || 1;
  const girs = holes.filter(h => h.stdGir).length;
  const girPct = ((girs / totalHoles) * 100).toFixed(1);
  const avgGirsPerRound = (girs / n).toFixed(1);

  const udOpps = holes.filter(h => h.isUpAndDownOpp).length;
  const udMade = holes.filter(h => h.isUpAndDownMade).length;
  const udPct = udOpps ? ((udMade / udOpps) * 100).toFixed(1) : '—';

  const puttRounds = rounds.filter(r => r.hasPutts);
  const avgPutts = puttRounds.length ? (puttRounds.reduce((s, r) => s + r.putts, 0) / puttRounds.length).toFixed(1) : '—';

  const firOpps = holes.filter(h => h.par >= 4 && h.fir !== 'NA');
  const firHits = firOpps.filter(h => h.fir === 'HIT').length;
  const firPct = firOpps.length ? ((firHits / firOpps.length) * 100).toFixed(1) : '—';

  grid.innerHTML = `
    <div class="kpi-card">
      <div class="kpi-label">Scoring Average (${n} Rounds)</div>
      <div class="kpi-value">${avgGross} <span style="font-size:1rem;color:var(--text-muted)">(+${avgToPar})</span></div>
      <div class="kpi-sub">Best round in view: <strong>${bestGross}</strong></div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Greens in Regulation (GIR %)</div>
      <div class="kpi-value highlight-green">${girPct}%</div>
      <div class="kpi-sub"><strong>${girs}}</strong> / ${holes.length} holes (${avgGirsPerRound} per round)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Up &amp; Down % (Scrambling)</div>
      <div class="kpi-value highlight-amber">${udPct}%</div>
      <div class="kpi-sub"><strong>${udMade}</strong> / ${udOpps} missed GIRs saved for par+</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Average Putts / Round</div>
      <div class="kpi-value highlight-blue">${avgPutts}</div>
      <div class="kpi-sub">Across ${puttRounds.length} putt-tracked rounds</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Fairways Hit %</div>
      <div class="kpi-value">${firPct}%</div>
      <div class="kpi-sub"><strong>${firHits}</strong> / ${firOpps.length} Par 4 &amp; 5 tee shots</div>
    </div>
  `;
}

function renderScoringStrip(rounds, holes) {
  const strip = document.getElementById('scoringStrip');
  if (!rounds.length) {
    strip.innerHTML = '';
    return;
  }
  const n = rounds.length;
  let albatross = 0, eagles = 0, birdies = 0, pars = 0, bogeys = 0, dblPlus = 0;
  holes.forEach(h => {
    if (h.strokes === null || h.strokes === undefined) return;
    const diff = h.strokes - h.par;
    if (diff <= -3) albatross++;
    else if (diff === -2) eagles++;
    else if (diff === -1) birdies++;
    else if (diff === 0) pars++;
    else if (diff === 1) bogeys++;
    else dblPlus++;
  });

  const items = [
    { label: 'Albatross', total: albatross, color: 'highlight-purple' },
    { label: 'Eagles', total: eagles, color: 'highlight-cyan' },
    { label: 'Birdies', total: birdies, color: 'highlight-blue' },
    { label: 'Pars', total: pars, color: 'highlight-green' },
    { label: 'Bogeys', total: bogeys, color: 'highlight-amber' },
    { label: 'Double Bogey+', total: dblPlus, color: 'highlight-rose' }
  ];

  strip.innerHTML = items.map(it => `
    <div class="score-box">
      <div class="score-box-top"><span>${it.label}</span><span>${(it.total / n).toFixed(1)} / rd</span></div>
      <div class="score-box-val ${it.color}">${it.total}</div>
      <div class="score-box-sub">${((it.total / (holes.length || 1)) * 100).toFixed(1)}% of holes</div>
    </div>
  `).join('');
}

function renderCharts(rounds, holes) {
  Object.values(charts).forEach(c => c.destroy());
  charts = {};

  const labels = rounds.map(r => `${r.date.slice(5)} ${r.course.split(' ')[0]}`);

  // 1. Traditional GIR % Only
  charts.gir = new Chart(document.getElementById('girChart'), {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'GIR %', data: rounds.map(r => r.girPct), backgroundColor: '#10b981', borderRadius: 4 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        y: { beginAtZero: true, max: 100, grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
        x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
      },
      plugins: { legend: { labels: { color: '#f8fafc' } } }
    }
  });

  // 2. Gross Score Only
  charts.score = new Chart(document.getElementById('scoreChart'), {
    type: 'line',
    data: {
      labels,
      datasets: [
        { label: 'Gross Score', data: rounds.map(r => r.gross), borderColor: '#38bdf8', backgroundColor: 'rgba(56, 189, 248, 0.15)', fill: true, tension: 0.25 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        y: { grid: { color: '#334155' }, ticks: { color: '#38bdf8' } },
        x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
      },
      plugins: { legend: { labels: { color: '#f8fafc' } } }
    }
  });

  // 3. Par 3 / 4 / 5 Breakdown
  const pars = [3, 4, 5];
  const parToPar = pars.map(p => {
    const sub = holes.filter(h => h.par === p && h.strokes !== null && h.strokes !== undefined);
    return sub.length ? Number((sub.reduce((s, h) => s + (h.strokes - h.par), 0) / sub.length).toFixed(2)) : 0;
  });
  const parGir = pars.map(p => {
    const sub = holes.filter(h => h.par === p);
    return sub.length ? Number(((sub.filter(h => h.stdGir).length / sub.length) * 100).toFixed(1)) : 0;
  });

  charts.par = new Chart(document.getElementById('parChart'), {
    type: 'bar',
    data: {
      labels: ['Par 3s', 'Par 4s', 'Par 5s'],
      datasets: [
        { label: 'Avg Score Over Par', data: parToPar, backgroundColor: '#a78bfa', yAxisID: 'y', borderRadius: 4 },
        { label: 'GIR %', data: parGir, backgroundColor: '#10b981', yAxisID: 'y1', borderRadius: 4 }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        y: { position: 'left', beginAtZero: true, grid: { color: '#334155' }, ticks: { color: '#a78bfa' } },
        y1: { position: 'right', beginAtZero: true, max: 100, grid: { drawOnChartArea: false }, ticks: { color: '#10b981' } },
        x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
      },
      plugins: { legend: { labels: { color: '#f8fafc' } } }
    }
  });

  // 4. Tee Shot Dispersion
  const outcomes = ['HIT', 'LEFT', 'RIGHT'];
  const outcomeCounts = outcomes.map(o => holes.filter(h => h.par >= 4 && h.fir === o).length);
  const outcomeToPar = outcomes.map(o => {
    const sub = holes.filter(h => h.par >= 4 && h.fir === o && h.strokes !== null && h.strokes !== undefined);
    return sub.length ? Number((sub.reduce((s, h) => s + (h.strokes - h.par), 0) / sub.length).toFixed(2)) : 0;
  });

  charts.fir = new Chart(document.getElementById('firChart'), {
    type: 'bar',
    data: {
      labels: ['Fairway Hit', 'Missed Left', 'Missed Right'],
      datasets: [
        { label: 'Hole Count', data: outcomeCounts, backgroundColor: ['#10b981', '#f43f5e', '#f59e0b'], yAxisID: 'y', borderRadius: 4 },
        { label: 'Avg Score to Par', data: outcomeToPar, type: 'line', borderColor: '#38bdf8', backgroundColor: '#38bdf8', yAxisID: 'y1' }
      ]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      scales: {
        y: { position: 'left', beginAtZero: true, grid: { color: '#334155' }, ticks: { color: '#94a3b8' } },
        y1: { position: 'right', beginAtZero: true, grid: { drawOnChartArea: false }, ticks: { color: '#38bdf8' } },
        x: { ticks: { color: '#94a3b8' }, grid: { display: false } }
      },
      plugins: { legend: { labels: { color: '#f8fafc' } } }
    }
  });
}

function renderRoundsTable(rounds) {
  const tbody = document.getElementById('roundsTableBody');
  const sorted = [...rounds].sort((a, b) => b.date.localeCompare(a.date));
  tbody.innerHTML = sorted.map(r => {
    return `
      <tr style="cursor:pointer;" onclick="openRoundModal('${r.id}')">
        <td><strong>${r.date}</strong></td>
        <td>${r.course}</td>
        <td>${r.tee}</td>
        <td>${r.par}</td>
        <td><strong>${r.gross}</strong></td>
        <td><span class="pill ${r.toPar <= 12 ? 'pill-green' : r.toPar <= 20 ? 'pill-amber' : 'pill-rose'}">+${r.toPar}</span></td>
        <td>${r.outScore ?? '—'} / ${r.inScore ?? '—'}</td>
        <td><span class="pill pill-green">${r.girCount}/${r.holesCount} (${r.girPct}%)</span></td>
        <td>${r.upAndDownMade}/${r.upAndDownOpps} (${r.upAndDownPct}%)</td>
        <td>${r.putts}</td>
        <td>${r.firHits}/${r.firOpps}</td>
        <td>${r.albatross}</td>
        <td>${r.eagles}</td>
        <td>${r.birdies}</td>
        <td>${r.pars}</td>
        <td>${r.bogeys}</td>
        <td>${r.dblPlus}</td>
      </tr>
    `;
  }).join('');
}

function openRoundModal(roundId) {
  const r = allRounds.find(x => x.id === roundId);
  if (!r) return;
  document.getElementById('modalTitle').textContent = `${r.course} — ${r.date} (${r.tee} Tees)`;
  const girCount = r.holes.filter(h => h.stdGir).length;
  const missed = r.holes.filter(h => !h.stdGir && h.strokes !== null && h.strokes !== undefined);
  const udMade = missed.filter(h => h.strokes <= h.par).length;
  document.getElementById('modalSub').textContent = `Gross: ${r.gross} (+${r.gross - r.par}) | GIR: ${girCount}/${r.holesCount} | Up & Down: ${udMade}/${missed.length} | Putts: ${r.garminPutts ?? '—'}`;

  document.getElementById('modalTableBody').innerHTML = r.holes.map(h => {
    const diff = h.strokes - h.par;
    const label = diff <= -3 ? 'Albatross' : diff === -2 ? 'Eagle' : diff === -1 ? 'Birdie' : diff === 0 ? 'Par' : diff === 1 ? 'Bogey' : `+${diff}`;
    const pillClass = diff <= -2 ? 'pill-purple' : diff === -1 ? 'pill-blue' : diff === 0 ? 'pill-green' : diff === 1 ? 'pill-amber' : 'pill-rose';
    const udText = h.stdGir ? '—' : (h.strokes !== null && h.strokes <= h.par ? '<span class="pill pill-green">✓ Saved</span>' : '✕');
    return `
      <tr>
        <td><strong>${h.hole}</strong></td>
        <td>${h.par}</td>
        <td>${h.si ?? '—'}</td>
        <td>${h.yards ? h.yards + 'y' : '—'}</td>
        <td><strong>${h.strokes ?? '—'}</strong></td>
        <td><span class="pill ${pillClass}">${label}</span></td>
        <td>${h.fir}</td>
        <td>${h.putts ?? '—'}</td>
        <td>${h.stdGir ? '<span class="pill pill-green">✓</span>' : '✕'}</td>
        <td>${udText}</td>
        <td>${h.penalties || 0}</td>
      </tr>
    `;
  }).join('');

  document.getElementById('roundModal').classList.add('open');
}

// --- SQL Engine (AlaSQL) ---
function syncSqlTables(rounds, holes) {
  alasql('DROP TABLE IF EXISTS rounds');
  alasql('DROP TABLE IF EXISTS holes');
  alasql('CREATE TABLE rounds');
  alasql('CREATE TABLE holes');
  alasql.tables.rounds.data = rounds;
  alasql.tables.holes.data = holes;
}

function runCurrentSql() {
  const query = document.getElementById('sqlInput').value.trim();
  const container = document.getElementById('sqlResults');
  if (!query) return;
  try {
    const res = alasql(query);
    if (!Array.isArray(res) || !res.length) {
      container.innerHTML = '<p style="color:var(--text-muted);font-size:0.85rem;">Query returned 0 rows.</p>';
      return;
    }
    const cols = Object.keys(res[0]);
    container.innerHTML = `
      <table>
        <thead><tr>${cols.map(c => `<th>${c}</th>`).join('')}</tr></thead>
        <tbody>
          ${res.map(row => `<tr>${cols.map(c => `<td>${row[c] !== null && row[c] !== undefined ? row[c] : '—'}</td>`).join('')}</tr>`).join('')}
        </tbody>
      </table>
    `;
  } catch (err) {
    container.innerHTML = `<p style="color:var(--rose);font-size:0.85rem;">SQL Error: ${err.message}</p>`;
  }
}

// --- Event Wiring ---
document.getElementById('fitInput').addEventListener('change', e => handleFiles(e.target.files));

const dropzone = document.getElementById('dropzone');
dropzone.addEventListener('dragover', e => { e.preventDefault(); dropzone.classList.add('dragover'); });
dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
dropzone.addEventListener('drop', e => {
  e.preventDefault();
  dropzone.classList.remove('dragover');
  handleFiles(e.dataTransfer.files);
});

['roundScopeFilter', 'courseFilter', 'dateFrom', 'dateTo', 'parFilter', 'firFilter'].forEach(id => {
  document.getElementById(id).addEventListener('change', refreshDashboard);
});

['compareRoundSelect', 'compareBaselineSelect'].forEach(id => {
  document.getElementById(id).addEventListener('change', () => {
    const { filteredRounds } = getFilteredData();
    renderComparisonPanel(filteredRounds);
  });
});

document.getElementById('runSqlBtn').addEventListener('click', runCurrentSql);
document.querySelectorAll('.preset-chip').forEach(btn => {
  btn.addEventListener('click', () => {
    document.getElementById('sqlInput').value = btn.dataset.sql;
    runCurrentSql();
  });
});

document.getElementById('resetDataBtn').addEventListener('click', () => {
  if (confirm('Clear all stored rounds from this dashboard?')) {
    allRounds = [];
    saveData();
    populateCourseFilter();
    refreshDashboard();
    updateStatus('<strong>Database Cleared:</strong> 0 rounds stored. Drop your Garmin <code>.fit</code> or <code>.json</code> files above to load.');
  }
});

document.getElementById('exportJsonBtn').addEventListener('click', () => {
  const blob = new Blob([JSON.stringify(allRounds, null, 2)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = `garmin_golf_scorecards_${new Date().toISOString().slice(0, 10)}.json`;
  a.click();
});

document.getElementById('closeModalBtn').addEventListener('click', () => {
  document.getElementById('roundModal').classList.remove('open');
});
document.getElementById('roundModal').addEventListener('click', e => {
  if (e.target.id === 'roundModal') document.getElementById('roundModal').classList.remove('open');
});

// Boot
loadInitialData();
populateCourseFilter();
refreshDashboard();
</script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_v3)

print("Generated index.html successfully. Size:", len(html_v3), "bytes")
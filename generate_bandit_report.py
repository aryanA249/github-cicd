import json
from datetime import datetime, timezone
from html import escape
from pathlib import Path


def _load_report(json_path: Path) -> dict:
    default_report = {"results": [], "metrics": {"_totals": {"loc": 0, "nosec": 0}}}
    if not json_path.exists():
        return default_report

    with json_path.open(encoding="utf-8-sig") as file_handle:
        return json.load(file_handle)


def _format_context(code: str | None) -> str:
    if not code:
        return ""

    lines = [line.rstrip() for line in code.splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)


def _format_issue(issue: dict) -> str:
    test_name = issue.get("test_name", "unknown_issue")
    issue_text = issue.get("issue_text", "No description available.")
    test_id = issue.get("test_id", "N/A")
    severity = issue.get("issue_severity", "UNKNOWN")
    confidence = issue.get("issue_confidence", "UNKNOWN")
    cwe = issue.get("cwe", {}) or {}
    cwe_id = cwe.get("id", "N/A")
    filename = issue.get("filename", "Unknown file")
    line_number = issue.get("line_number", "N/A")
    more_info = issue.get("more_info", "")
    context = _format_context(issue.get("code"))

    lines = [
        f"{test_name}: {issue_text}",
        f"Test ID: {test_id}",
        f"Severity: {severity}",
        f"Confidence: {confidence}",
        f"CWE: CWE-{cwe_id}",
        f"File: {filename}",
        f"Line number: {line_number}",
    ]

    if more_info:
        lines.append(f"More info: {more_info}")

    if context:
        lines.append(context)

    return "\n".join(lines)


def build_report(json_path: Path, html_path: Path) -> None:
    report = _load_report(json_path)
    results = report.get("results", [])
    metrics = report.get("metrics", {}) or {}
    totals = metrics.get("_totals", {}) or {}

    loc = totals.get("loc", 0)
    nosec = totals.get("nosec", 0)
    issues = len(results)
    high = sum(1 for issue in results if issue.get("issue_severity") == "HIGH")
    medium = sum(1 for issue in results if issue.get("issue_severity") == "MEDIUM")
    low = sum(1 for issue in results if issue.get("issue_severity") == "LOW")

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    issue_blocks = "\n\n".join(_format_issue(issue) for issue in results)
    if not issue_blocks:
        issue_blocks = "No vulnerabilities identified."

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Bandit Security Report</title>
  <style>
    :root {{
      color-scheme: dark;
      --bg: #071018;
      --panel: #0c1520;
      --panel-2: #0f1b29;
      --border: rgba(255, 181, 72, 0.22);
      --text: #f2eee6;
      --muted: #a6afbd;
      --accent: #ffb347;
      --accent-2: #ff6f61;
      --code: #dfe7f1;
      --shadow: 0 20px 60px rgba(0, 0, 0, 0.45);
    }}

    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: "Consolas", "SFMono-Regular", "Menlo", monospace;
      background:
        radial-gradient(circle at top left, rgba(255, 179, 71, 0.16), transparent 28%),
        radial-gradient(circle at 85% 15%, rgba(255, 111, 97, 0.12), transparent 22%),
        linear-gradient(135deg, #05080e 0%, #0a1320 48%, #0f1726 100%);
      color: var(--text);
    }}

    .wrap {{ max-width: 1120px; margin: 0 auto; padding: 32px 18px 56px; }}
    .report {{
      background: linear-gradient(180deg, rgba(11, 18, 28, 0.96), rgba(8, 13, 22, 0.98));
      border: 1px solid var(--border);
      border-radius: 24px;
      box-shadow: var(--shadow);
      overflow: hidden;
    }}

    .header {{
      padding: 26px 28px 20px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      background: linear-gradient(180deg, rgba(255, 179, 71, 0.08), transparent);
    }}

    .eyebrow {{
      text-transform: uppercase;
      letter-spacing: 0.34em;
      font-size: 0.74rem;
      color: var(--accent);
      margin-bottom: 10px;
    }}

    h1 {{ margin: 0; font-size: clamp(1.8rem, 4vw, 3.2rem); line-height: 1; }}
    .sub {{ margin: 12px 0 0; color: var(--muted); line-height: 1.6; max-width: 900px; }}

    .stats {{
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
      margin-top: 20px;
    }}

    .stat {{
      padding: 14px 16px;
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 16px;
      background: rgba(255,255,255,0.03);
    }}

    .stat span {{ display: block; color: var(--muted); text-transform: uppercase; letter-spacing: 0.16em; font-size: 0.72rem; }}
    .stat strong {{ display: block; margin-top: 8px; font-size: 1.4rem; color: var(--code); }}

    .body {{ padding: 22px 28px 28px; }}
    .section-label {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: baseline;
      margin-bottom: 14px;
    }}

    .section-label h2 {{
      margin: 0;
      font-size: 0.95rem;
      text-transform: uppercase;
      letter-spacing: 0.22em;
      color: var(--accent);
    }}

    .timestamp {{ color: var(--muted); font-size: 0.82rem; }}

    .panel {{
      background: var(--panel);
      border: 1px solid rgba(255,255,255,0.08);
      border-radius: 18px;
      padding: 18px;
    }}

    .plain-report {{
      margin: 0;
      white-space: pre-wrap;
      word-break: break-word;
      line-height: 1.55;
      font-size: 0.93rem;
      color: var(--code);
    }}

    .report-line {{ display: block; }}
    .metrics {{ color: #cfd8e3; }}
    .issue {{ color: #f7efe4; }}
    .test-id, .severity, .confidence, .cwe, .file, .line-number, .more-info {{ color: #d9e3ef; }}
    .label {{ color: var(--accent); }}
    .snippet {{
      display: block;
      margin: 8px 0 0;
      padding-left: 0;
      color: #c8d2de;
      opacity: 0.95;
    }}

    .issue-block {{
      padding: 16px 0;
      border-top: 1px solid rgba(255,255,255,0.08);
    }}

    .issue-block:first-child {{ border-top: 0; padding-top: 0; }}
    .empty {{ color: #dff0e7; }}

    @media (max-width: 900px) {{
      .stats {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}

    @media (max-width: 640px) {{
      .wrap {{ padding-inline: 12px; }}
      .header, .body {{ padding-inline: 16px; }}
      .stats {{ grid-template-columns: 1fr; }}
    }}
  </style>
</head>
<body>
  <main class="wrap">
    <section class="report">
      <header class="header">
        <div class="eyebrow">Cowboy Bebop / Bandit Output</div>
        <h1>Bandit Security Report</h1>
        <p class="sub">Styled to preserve Bandit's original text-format structure while presenting it in a darker, cinematic, Bebop-inspired HTML layout.</p>
        <div class="stats">
          <div class="stat"><span>Total findings</span><strong>{issues}</strong></div>
          <div class="stat"><span>High</span><strong>{high}</strong></div>
          <div class="stat"><span>Medium</span><strong>{medium}</strong></div>
          <div class="stat"><span>Low</span><strong>{low}</strong></div>
          <div class="stat"><span>LOC</span><strong>{loc}</strong></div>
        </div>
      </header>

      <div class="body">
        <div class="section-label">
          <h2>Bandit Text Report</h2>
          <div class="timestamp">Generated {generated_at} | #nosec skipped: {nosec}</div>
        </div>
        <div class="panel">
          <pre class="plain-report">Metrics:
Total lines of code: {loc}
Total lines skipped (#nosec): {nosec}

{escape(issue_blocks)}</pre>
        </div>
      </div>
    </section>
  </main>
</body>
</html>"""

    html_path.write_text(html, encoding="utf-8")


if __name__ == "__main__":
    build_report(Path("bandit-report.json"), Path("bandit-report.html"))

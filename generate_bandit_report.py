import json
from pathlib import Path


def main() -> None:
    report_path = Path("bandit-report.json")
    if not report_path.exists():
        print("Could not parse Bandit results")
        return

    with report_path.open(encoding="utf-8-sig") as file_handle:
        data = json.load(file_handle)

    results = data.get("results", [])
    metrics = data.get("metrics", {}) or {}
    totals = metrics.get("_totals", {}) or {}

    print("### Vulnerabilities Found:")

    if results:
        for issue in results:
            test_name = issue.get("test_name", "unknown_issue")
            severity = issue.get("issue_severity", "UNKNOWN")
            line_number = issue.get("line_number", "N/A")
            print(f"- **{test_name}** ({severity}) at line {line_number}")
    else:
        print("✅ No vulnerabilities detected!")

    print("")
    print(f"Metrics:")
    print(f"Total lines of code: {totals.get('loc', 0)}")
    print(f"Total lines skipped (#nosec): {totals.get('nosec', 0)}")


if __name__ == "__main__":
    main()

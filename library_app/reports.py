"""Markdown, text and CSV report exporters."""
import csv
from pathlib import Path
from datetime import datetime
from .core import summary, overdue_transactions, find_by_id

REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"

def export_reports(db):
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stats = summary(db)
    md = ["# CampusSolve Library Report", "", f"Generated: {datetime.now():%Y-%m-%d %H:%M}", "",
          "## Executive Summary", ""]
    md += [f"- **{k.replace('_', ' ').title()}:** {v}" for k, v in stats.items() if k != "categories"]
    md += ["", "## Category Breakdown", ""]
    md += [f"- {k}: {v} title(s)" for k, v in stats["categories"].items()] or ["- No books recorded."]
    md += ["", "## Overdue Issues", ""]
    overdue = overdue_transactions(db)
    for t in overdue:
        b, m = find_by_id(db["books"], t["book_id"]), find_by_id(db["members"], t["member_id"])
        md.append(f"- {t['id']}: {b['title'] if b else t['book_id']} — {m['name'] if m else t['member_id']} (due {t['due_date']})")
    (REPORT_DIR / f"library_report_{stamp}.md").write_text("\n".join(md), encoding="utf-8")

    txt = ["CAMPUSSOLVE LIBRARY AUDIT", f"Generated: {datetime.now().isoformat(timespec='minutes')}", "=" * 42]
    txt += [f"{k}: {v}" for k, v in stats.items()]
    txt += ["", "TRANSACTIONS"]
    txt += [f"{t['id']} | {t['book_id']} | {t['member_id']} | {t['status']} | due {t['due_date']}" for t in db["transactions"]]
    (REPORT_DIR / f"audit_{stamp}.txt").write_text("\n".join(txt), encoding="utf-8")

    with (REPORT_DIR / f"transactions_{stamp}.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["id", "book_id", "member_id", "issue_date", "due_date", "return_date", "status"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(db["transactions"])
    return [f"reports/library_report_{stamp}.md", f"reports/audit_{stamp}.txt", f"reports/transactions_{stamp}.csv"]

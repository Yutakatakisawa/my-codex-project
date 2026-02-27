#!/usr/bin/env python3
"""
週次KPI CSVからMarkdownレポートを生成する。
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


TARGETS = {
    "sessions": 2000,
    "leads": 50,
    "consultations": 20,
    "deals": 5,
}


def to_int(value: str) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return 0


def pct_change(current: int, previous: int) -> float:
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100.0


def progress(current: int, target: int) -> float:
    if target == 0:
        return 0.0
    return (current / target) * 100.0


def lead_to_consult_rate(leads: int, consultations: int) -> float:
    if leads == 0:
        return 0.0
    return (consultations / leads) * 100.0


def consult_to_deal_rate(consultations: int, deals: int) -> float:
    if consultations == 0:
        return 0.0
    return (deals / consultations) * 100.0


def build_actions(latest: dict[str, int]) -> list[str]:
    actions: list[str] = []

    if latest["sessions"] < TARGETS["sessions"]:
        actions.append("SEO記事公開本数を増やし、SNS再利用投稿を週次固定する。")
    if latest["leads"] < TARGETS["leads"]:
        actions.append("診断ページのCTA位置を再調整し、結果ページのLINE訴求を強化する。")
    if latest["consultations"] < TARGETS["consultations"]:
        actions.append("LINE配信Day5/Day6の相談誘導文を改善し、予約動線を短縮する。")
    if latest["deals"] < TARGETS["deals"]:
        actions.append("商談台本の機会損失提示を強化し、追客3回ルールを徹底する。")

    if not actions:
        actions.append("現状の勝ちパターンを維持し、運用工数削減の自動化比率を上げる。")

    return actions[:3]


def main() -> None:
    parser = argparse.ArgumentParser(description="週次レポート生成")
    parser.add_argument("--input", required=True, help="metrics CSV")
    parser.add_argument("--output", required=True, help="output markdown")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with in_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise SystemExit("metrics CSV has no rows")

    latest_row = rows[-1]
    prev_row = rows[-2] if len(rows) > 1 else rows[-1]

    latest = {
        "sessions": to_int(latest_row.get("sessions")),
        "leads": to_int(latest_row.get("leads")),
        "consultations": to_int(latest_row.get("consultations")),
        "deals": to_int(latest_row.get("deals")),
    }
    previous = {
        "sessions": to_int(prev_row.get("sessions")),
        "leads": to_int(prev_row.get("leads")),
        "consultations": to_int(prev_row.get("consultations")),
        "deals": to_int(prev_row.get("deals")),
    }

    lead_consult = lead_to_consult_rate(latest["leads"], latest["consultations"])
    consult_deal = consult_to_deal_rate(latest["consultations"], latest["deals"])

    actions = build_actions(latest)

    report = f"""# 週次KPIレポート

対象週: {latest_row.get("week", "N/A")}

## KPIサマリー

| 指標 | 今週 | 先週比 | 目標進捗 |
|---|---:|---:|---:|
| Sessions | {latest["sessions"]} | {pct_change(latest["sessions"], previous["sessions"]):+.1f}% | {progress(latest["sessions"], TARGETS["sessions"]):.1f}% |
| Leads | {latest["leads"]} | {pct_change(latest["leads"], previous["leads"]):+.1f}% | {progress(latest["leads"], TARGETS["leads"]):.1f}% |
| Consultations | {latest["consultations"]} | {pct_change(latest["consultations"], previous["consultations"]):+.1f}% | {progress(latest["consultations"], TARGETS["consultations"]):.1f}% |
| Deals | {latest["deals"]} | {pct_change(latest["deals"], previous["deals"]):+.1f}% | {progress(latest["deals"], TARGETS["deals"]):.1f}% |

## 変換率

- Leads -> Consultations: {lead_consult:.1f}%
- Consultations -> Deals: {consult_deal:.1f}%

## 来週の優先アクション

1. {actions[0]}
2. {actions[1] if len(actions) > 1 else actions[0]}
3. {actions[2] if len(actions) > 2 else actions[0]}
"""

    out_path.write_text(report, encoding="utf-8")
    print(f"output={out_path}")


if __name__ == "__main__":
    main()


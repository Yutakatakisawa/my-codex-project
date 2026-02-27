#!/usr/bin/env python3
"""
見込み客CSVを HOT / WARM / COLD にスコアリングする。
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def to_float(value: str, default: float = 0.0) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def normalize_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(max_value, value))


def score_lead(row: dict[str, str]) -> tuple[int, str]:
    diagnosis_score = clamp(to_float(row.get("diagnosis_score")), 0, 100)
    line_clicks = clamp(to_float(row.get("line_clicks")), 0, 5)
    page_views = clamp(to_float(row.get("page_views")), 0, 10)
    consultation_booked = normalize_bool(row.get("consultation_booked", "false"))
    last_active_days = clamp(to_float(row.get("last_active_days")), 0, 60)

    score = 0.0
    score += diagnosis_score * 0.4  # max 40
    score += (line_clicks / 5) * 20  # max 20
    score += (page_views / 10) * 20  # max 20
    score += 20 if consultation_booked else 0  # max 20

    if last_active_days > 14:
        penalty = min((last_active_days - 14) * 1.2, 15)
        score -= penalty

    score = clamp(score, 0, 100)
    rounded = int(round(score))

    if rounded >= 70:
        bucket = "HOT"
    elif rounded >= 40:
        bucket = "WARM"
    else:
        bucket = "COLD"

    return rounded, bucket


def main() -> None:
    parser = argparse.ArgumentParser(description="見込み客スコアリング")
    parser.add_argument("--input", required=True, help="入力CSV")
    parser.add_argument("--output", required=True, help="出力CSV")
    args = parser.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with in_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        raise SystemExit("input CSV has no rows")

    fieldnames = list(rows[0].keys()) + ["lead_score", "lead_segment"]
    scored_rows: list[dict[str, str]] = []

    for row in rows:
        score, segment = score_lead(row)
        new_row = dict(row)
        new_row["lead_score"] = str(score)
        new_row["lead_segment"] = segment
        scored_rows.append(new_row)

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scored_rows)

    print(f"scored_leads={len(scored_rows)}")
    print(f"output={out_path}")


if __name__ == "__main__":
    main()


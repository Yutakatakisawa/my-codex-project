#!/usr/bin/env python3
"""
ABテストCSVを読み込み、優先順位レポートを出力する。
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def to_float(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def score_row(row: dict[str, str]) -> float:
    impact = to_float(row.get("impact"))
    confidence = to_float(row.get("confidence"))
    ease = to_float(row.get("ease"))
    ice = impact * confidence * ease
    return ice


def build_report(rows: list[dict[str, str]], top_n: int) -> str:
    ranked = sorted(rows, key=score_row, reverse=True)
    top = ranked[:top_n]

    lines = [
        "# ABテスト優先順位レポート",
        "",
        f"対象テスト数: {len(rows)}",
        f"上位表示: {len(top)}",
        "",
        "| Rank | ID | Area | Hypothesis | ICE |",
        "|---:|---|---|---|---:|",
    ]

    for idx, row in enumerate(top, start=1):
        lines.append(
            f"| {idx} | {row.get('id','')} | {row.get('area','')} | {row.get('hypothesis','')} | {score_row(row):.0f} |"
        )

    lines.extend(
        [
            "",
            "## 実行ルール",
            "",
            "1. 上位3件を同時に走らせない（同時は最大2件）",
            "2. 最低1週間はデータを取り、早期判断しない",
            "3. 勝ち施策はテンプレ化して全ページに展開する",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="ABテスト優先順位レポート作成")
    parser.add_argument("--input", required=True, help="ab_test_backlog.csv")
    parser.add_argument("--output", required=True, help="output markdown path")
    parser.add_argument("--top", type=int, default=8, help="top N tests")
    args = parser.parse_args()

    rows = load_rows(Path(args.input))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_report(rows, args.top), encoding="utf-8")

    print(f"tests={len(rows)}")
    print(f"output={output}")


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
自動集客システムの最低限パイプラインを実行する。
1) 記事ブリーフ生成
2) リードスコアリング
3) 週次レポート生成
4) 地域ページ生成（任意）
5) ABテスト優先順位算出（任意）
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(command: list[str]) -> None:
    print("run:", " ".join(command))
    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise SystemExit(result.returncode)


def main() -> None:
    parser = argparse.ArgumentParser(description="自動集客パイプライン実行")
    parser.add_argument("--keywords", required=True)
    parser.add_argument("--calendar", required=True)
    parser.add_argument("--leads", required=True)
    parser.add_argument("--metrics", required=True)
    parser.add_argument("--cities")
    parser.add_argument("--area-template")
    parser.add_argument("--ab-tests")
    parser.add_argument("--ab-top", type=int, default=8)
    parser.add_argument("--output-root", default="outputs")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    root = Path(args.output_root).resolve()
    briefs_dir = root / "briefs"
    scored_leads = root / "leads_scored.csv"
    weekly_report = root / "weekly_report.md"
    areas_dir = root / "area_pages"
    ab_report = root / "ab_test_priority.md"
    root.mkdir(parents=True, exist_ok=True)

    run(
        [
            sys.executable,
            str(script_dir / "build_article_briefs.py"),
            "--keywords",
            str(Path(args.keywords).resolve()),
            "--calendar",
            str(Path(args.calendar).resolve()),
            "--outdir",
            str(briefs_dir),
        ]
    )
    run(
        [
            sys.executable,
            str(script_dir / "lead_scoring.py"),
            "--input",
            str(Path(args.leads).resolve()),
            "--output",
            str(scored_leads),
        ]
    )
    run(
        [
            sys.executable,
            str(script_dir / "weekly_report.py"),
            "--input",
            str(Path(args.metrics).resolve()),
            "--output",
            str(weekly_report),
        ]
    )

    if args.cities and args.area_template:
        run(
            [
                sys.executable,
                str(script_dir / "generate_area_pages.py"),
                "--cities",
                str(Path(args.cities).resolve()),
                "--template",
                str(Path(args.area_template).resolve()),
                "--outdir",
                str(areas_dir),
            ]
        )

    if args.ab_tests:
        run(
            [
                sys.executable,
                str(script_dir / "prioritize_ab_tests.py"),
                "--input",
                str(Path(args.ab_tests).resolve()),
                "--output",
                str(ab_report),
                "--top",
                str(args.ab_top),
            ]
        )

    print("pipeline_done=true")
    print(f"briefs_dir={briefs_dir}")
    print(f"leads_scored={scored_leads}")
    print(f"weekly_report={weekly_report}")
    if args.cities and args.area_template:
        print(f"area_pages={areas_dir}")
    if args.ab_tests:
        print(f"ab_report={ab_report}")


if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""
自動集客システムの最低限パイプラインを実行する。
1) 記事ブリーフ生成
2) リードスコアリング
3) 週次レポート生成
4) 地域ページ生成（任意）
5) ABテスト優先順位算出（任意）
6) DMキュー生成（任意）
7) DM送信（任意 / dry-run可）
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
    parser.add_argument("--dm-prospects")
    parser.add_argument("--dm-templates")
    parser.add_argument("--dm-webhook-url")
    parser.add_argument("--dm-dry-run", action="store_true")
    parser.add_argument("--output-root", default="outputs")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    root = Path(args.output_root).resolve()
    briefs_dir = root / "briefs"
    scored_leads = root / "leads_scored.csv"
    weekly_report = root / "weekly_report.md"
    areas_dir = root / "area_pages"
    ab_report = root / "ab_test_priority.md"
    dm_queue = root / "dm_queue.csv"
    dm_preview = root / "dm_preview.md"
    dm_send_results = root / "dm_send_results.csv"
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

    if args.dm_prospects and args.dm_templates:
        run(
            [
                sys.executable,
                str(script_dir / "build_dm_queue.py"),
                "--prospects",
                str(Path(args.dm_prospects).resolve()),
                "--templates",
                str(Path(args.dm_templates).resolve()),
                "--output",
                str(dm_queue),
                "--preview",
                str(dm_preview),
            ]
        )

        if args.dm_webhook_url or args.dm_dry_run:
            command = [
                sys.executable,
                str(script_dir / "send_dm_webhook.py"),
                "--queue",
                str(dm_queue),
                "--output",
                str(dm_send_results),
            ]
            if args.dm_webhook_url:
                command.extend(["--webhook-url", args.dm_webhook_url])
            if args.dm_dry_run:
                command.append("--dry-run")
            run(command)

    print("pipeline_done=true")
    print(f"briefs_dir={briefs_dir}")
    print(f"leads_scored={scored_leads}")
    print(f"weekly_report={weekly_report}")
    if args.cities and args.area_template:
        print(f"area_pages={areas_dir}")
    if args.ab_tests:
        print(f"ab_report={ab_report}")
    if args.dm_prospects and args.dm_templates:
        print(f"dm_queue={dm_queue}")
        print(f"dm_preview={dm_preview}")
    if args.dm_webhook_url or args.dm_dry_run:
        print(f"dm_send_results={dm_send_results}")


if __name__ == "__main__":
    main()


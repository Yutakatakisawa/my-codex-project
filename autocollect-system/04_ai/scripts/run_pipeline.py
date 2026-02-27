#!/usr/bin/env python3
"""
自動集客システムの最低限パイプラインを実行する。
1) 記事ブリーフ生成
2) リードスコアリング
3) 週次レポート生成
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
    parser.add_argument("--output-root", default="outputs")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    root = Path(args.output_root).resolve()
    briefs_dir = root / "briefs"
    scored_leads = root / "leads_scored.csv"
    weekly_report = root / "weekly_report.md"
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

    print("pipeline_done=true")
    print(f"briefs_dir={briefs_dir}")
    print(f"leads_scored={scored_leads}")
    print(f"weekly_report={weekly_report}")


if __name__ == "__main__":
    main()


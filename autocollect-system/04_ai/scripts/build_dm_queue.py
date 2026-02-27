#!/usr/bin/env python3
"""
DM見込み客CSVとテンプレートJSONから配信キューを生成する。
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


JST = timezone(timedelta(hours=9))


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def load_templates(path: Path) -> dict[str, dict[str, str]]:
    return json.loads(path.read_text(encoding="utf-8"))


def to_int(value: str, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def to_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def segment_of(row: dict[str, str]) -> str:
    last_contact_days = to_int(row.get("last_contact_days", "0"))
    follower_count = to_int(row.get("follower_count", "0"))
    website_status = row.get("website_status", "").strip()

    score = 0
    if last_contact_days <= 7:
        score += 3
    elif last_contact_days <= 21:
        score += 2
    else:
        score += 1

    if follower_count >= 2000:
        score += 3
    elif follower_count >= 800:
        score += 2
    else:
        score += 1

    if website_status == "あり":
        score += 2
    else:
        score += 1

    if score >= 7:
        return "hot"
    if score >= 5:
        return "warm"
    return "cold"


def build_message(template: str, row: dict[str, str]) -> str:
    return template.format(
        name=row.get("name", "").strip() or "ご担当者",
        business_type=row.get("business_type", "").strip() or "職人",
        prefecture=row.get("prefecture", "").strip(),
        city=row.get("city", "").strip(),
        pain_point=row.get("pain_point", "").strip() or "集客課題",
    )


def schedule_time(base: datetime, index: int) -> datetime:
    # 1通目: base + index*3分, 09:00-20:00 の範囲に丸める
    dt = base + timedelta(minutes=index * 3)
    if dt.hour < 9:
        dt = dt.replace(hour=9, minute=0, second=0, microsecond=0)
    if dt.hour >= 20:
        dt = (dt + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    return dt


def save_queue(rows: list[dict[str, str]], path: Path) -> None:
    fieldnames = [
        "queue_id",
        "prospect_id",
        "channel",
        "segment",
        "scheduled_at",
        "message",
        "status",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def save_preview(rows: list[dict[str, str]], path: Path) -> None:
    lines = [
        "# DM配信プレビュー",
        "",
        f"生成件数: {len(rows)}",
        "",
        "| queue_id | channel | segment | scheduled_at | message |",
        "|---|---|---|---|---|",
    ]
    for row in rows[:20]:
        msg = row["message"].replace("|", "｜")
        lines.append(
            f"| {row['queue_id']} | {row['channel']} | {row['segment']} | {row['scheduled_at']} | {msg} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="DM配信キュー生成")
    parser.add_argument("--prospects", required=True, help="prospects CSV")
    parser.add_argument("--templates", required=True, help="templates JSON")
    parser.add_argument("--output", required=True, help="queue CSV output")
    parser.add_argument("--preview", required=True, help="preview markdown output")
    args = parser.parse_args()

    prospects = load_csv(Path(args.prospects))
    templates = load_templates(Path(args.templates))

    now = datetime.now(tz=JST).replace(second=0, microsecond=0)
    queue_rows: list[dict[str, str]] = []
    idx = 0

    for p in prospects:
        if to_bool(p.get("reply_optout", "false")):
            continue
        channel = p.get("channel", "").strip()
        if channel not in templates:
            continue
        segment = segment_of(p)
        template = templates[channel].get(segment)
        if not template:
            continue

        message = build_message(template, p)
        scheduled = schedule_time(now, idx)
        idx += 1

        queue_rows.append(
            {
                "queue_id": f"Q{idx:04d}",
                "prospect_id": p.get("prospect_id", "").strip(),
                "channel": channel,
                "segment": segment,
                "scheduled_at": scheduled.isoformat(),
                "message": message,
                "status": "ready",
            }
        )

    save_queue(queue_rows, Path(args.output))
    save_preview(queue_rows, Path(args.preview))

    print(f"dm_queue={len(queue_rows)}")
    print(f"output={args.output}")
    print(f"preview={args.preview}")


if __name__ == "__main__":
    main()


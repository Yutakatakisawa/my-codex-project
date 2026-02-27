#!/usr/bin/env python3
"""
DMキューCSVをWebhookへ送信する。
dry-run時は送信せず、結果のみ出力。
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib import request


def load_queue(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def now_iso() -> str:
    return datetime.now(tz=timezone.utc).isoformat()


def should_send(row: dict[str, str]) -> bool:
    return row.get("status", "").strip() == "ready"


def post_webhook(webhook: str, payload: dict[str, str]) -> tuple[bool, str]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = request.Request(
        webhook,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8", errors="ignore")
            return True, body[:300]
    except Exception as exc:  # pragma: no cover
        return False, str(exc)


def write_results(rows: list[dict[str, str]], path: Path) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="DMキュー送信")
    parser.add_argument("--queue", required=True, help="dm_queue.csv")
    parser.add_argument("--output", required=True, help="result csv output")
    parser.add_argument("--webhook-url", help="make/zapier webhook")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows = load_queue(Path(args.queue))
    if not rows:
        raise SystemExit("queue is empty")

    if not args.dry_run and not args.webhook_url:
        raise SystemExit("webhook-url is required unless --dry-run")

    sent = 0
    failed = 0
    skipped = 0

    updated_rows: list[dict[str, str]] = []
    for row in rows:
        new_row = dict(row)
        if not should_send(row):
            new_row["status"] = row.get("status", "skipped")
            new_row["sent_at"] = ""
            new_row["send_result"] = "skipped"
            skipped += 1
            updated_rows.append(new_row)
            continue

        payload = {
            "queue_id": row.get("queue_id", ""),
            "prospect_id": row.get("prospect_id", ""),
            "channel": row.get("channel", ""),
            "message": row.get("message", ""),
            "scheduled_at": row.get("scheduled_at", ""),
        }

        if args.dry_run:
            new_row["status"] = "dry_run_sent"
            new_row["sent_at"] = now_iso()
            new_row["send_result"] = "dry_run"
            sent += 1
            updated_rows.append(new_row)
            continue

        ok, response_text = post_webhook(args.webhook_url or "", payload)
        if ok:
            new_row["status"] = "sent"
            new_row["sent_at"] = now_iso()
            new_row["send_result"] = response_text
            sent += 1
        else:
            new_row["status"] = "failed"
            new_row["sent_at"] = now_iso()
            new_row["send_result"] = response_text
            failed += 1
        updated_rows.append(new_row)

    write_results(updated_rows, Path(args.output))
    print(f"sent={sent}")
    print(f"failed={failed}")
    print(f"skipped={skipped}")
    print(f"output={args.output}")


if __name__ == "__main__":
    main()


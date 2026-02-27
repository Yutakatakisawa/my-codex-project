#!/usr/bin/env python3
"""
コンテンツカレンダーから30記事の下書きMarkdownを生成する。
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def safe_filename(slug: str) -> str:
    value = slug.strip().strip("/")
    if not value:
        return "draft"
    return value.replace("/", "_")


def build_draft(row: dict[str, str]) -> str:
    title = row.get("title", "").strip()
    keyword = row.get("target_keyword", "").strip()
    stage = row.get("stage", "").strip()
    cta = row.get("primary_cta", "").strip()
    slug = row.get("slug", "").strip()
    week = row.get("week", "").strip()
    day = row.get("day", "").strip()

    return f"""---
title: "{title}"
keyword: "{keyword}"
stage: "{stage}"
week: "{week}"
day: "{day}"
slug: "{slug}"
primary_cta: "{cta}"
status: "draft"
---

# {title}

## 導入

「{keyword}」で検索する人は、すでに課題を認識しています。  
この記事では、ITが苦手な職人でも実行できるように、要点だけを絞って解説します。

## 結論（先出し）

最初にやるべきことは次の3つです。

1. 現状の導線を確認する
2. 1つの改善施策を今週中に実装する
3. 数字を見て次の改善に進む

## なぜ必要か

現場業務が忙しいと、Web導線は後回しになりがちです。  
しかし、紹介依存の状態が続くと、紹介が止まった瞬間に売上が落ちます。  
そのため、最小の導線を先に作ることが重要です。

## 実行手順

### Step1. 現状確認

- サイトに電話・LINE・フォームの導線があるか
- 施工事例が更新されているか
- 問い合わせ後の返信速度が明記されているか

### Step2. 今週1つだけ直す

例:
- フォーム項目を5つ以下にする
- 記事下CTAを追加する
- 結果ページにLINEボタンを置く

### Step3. 計測する

- クリック率
- 診断完了率
- LINE登録率
- 相談化率

## 失敗例と回避策

### 失敗例1: 施策を同時に増やしすぎる

回避策: 週1改善に絞る

### 失敗例2: 計測せずに感覚で判断する

回避策: KPIを固定して毎週レビューする

## 事例（記入テンプレ）

- Before: （例）月間問い合わせ2件
- 施策: （例）診断ページ導線追加
- After: （例）月間問い合わせ6件

## FAQ

### Q1. ITが苦手でもできますか？
できます。最初は導線を3つ置くところから始めてください。

### Q2. 更新頻度はどれくらい必要ですか？
最低でも週1回の更新を目安にしてください。

### Q3. どこから着手すべきですか？
診断ページ -> LINE導線 -> 相談導線の順で着手してください。

## まとめ

「{keyword}」で成果を出すには、派手な施策よりも導線の基本整備が先です。  
まずは今週1つの改善を完了し、来週の数字で評価しましょう。

## CTA

- 3分診断を受ける
- LINEで7日改善プランを受け取る
- {cta}
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="記事下書き自動生成")
    parser.add_argument("--calendar", required=True, help="content_calendar_30.csv")
    parser.add_argument("--outdir", required=True, help="出力先ディレクトリ")
    args = parser.parse_args()

    calendar = load_csv(Path(args.calendar))
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    count = 0
    for row in calendar:
        filename = safe_filename(row.get("slug", ""))
        out_file = outdir / f"{filename}.md"
        out_file.write_text(build_draft(row), encoding="utf-8")
        count += 1

    print(f"generated_drafts={count}")
    print(f"output_dir={outdir}")


if __name__ == "__main__":
    main()


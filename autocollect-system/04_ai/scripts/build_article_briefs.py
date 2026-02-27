#!/usr/bin/env python3
"""
content_calendar_30.csv と keywords_master.csv から記事ブリーフを自動生成する。
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def normalize_filename(slug: str) -> str:
    value = slug.strip().strip("/")
    if not value:
        return "brief"
    return value.replace("/", "_")


def build_brief(article: dict[str, str], keyword_row: dict[str, str] | None) -> str:
    target_keyword = article.get("target_keyword", "").strip()
    stage = article.get("stage", "").strip()
    title = article.get("title", "").strip()
    cta = article.get("primary_cta", "").strip()
    slug = article.get("slug", "").strip()

    persona = keyword_row.get("persona", "職人経営者") if keyword_row else "職人経営者"
    cluster = keyword_row.get("cluster", "一般") if keyword_row else "一般"

    return f"""# 記事ブリーフ: {title}

## 基本情報

- ターゲットキーワード: {target_keyword}
- 検索段階: {stage}
- 想定読者: {persona}
- クラスター: {cluster}
- 想定URL: {slug}
- 主CTA: {cta}

## 記事ゴール

1. 読者の課題を明確化する
2. 具体的な実行手順を提示する
3. 診断 / LINE / 相談のいずれかへ遷移させる

## 見出し案（H2/H3）

### H2: 結論（先に答える）
- H3: この施策が効く理由

### H2: 実行手順
- H3: 準備
- H3: 実装
- H3: 計測

### H2: 失敗例と回避策
- H3: よくある失敗
- H3: 改善ポイント

### H2: 事例
- H3: Before
- H3: After

### H2: FAQ
- H3: よくある質問3つ

## 内部リンク指示

- 親ピラー1本
- 関連記事2本
- CTAページ1本

## CTA文案

- 25%: 3分診断で弱点を確認する
- 60%: LINEで7日改善プランを受け取る
- 100%: 無料相談を予約する
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="記事ブリーフ自動生成")
    parser.add_argument("--keywords", required=True, help="keywords_master.csv のパス")
    parser.add_argument("--calendar", required=True, help="content_calendar_30.csv のパス")
    parser.add_argument("--outdir", required=True, help="出力ディレクトリ")
    args = parser.parse_args()

    keywords_path = Path(args.keywords)
    calendar_path = Path(args.calendar)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    keywords = load_csv(keywords_path)
    calendar = load_csv(calendar_path)
    keyword_map = {row.get("keyword", "").strip(): row for row in keywords}

    created = 0
    for row in calendar:
        slug = row.get("slug", "")
        filename = normalize_filename(slug)
        out_path = outdir / f"{filename}.md"
        keyword_row = keyword_map.get(row.get("target_keyword", "").strip())
        out_path.write_text(build_brief(row, keyword_row), encoding="utf-8")
        created += 1

    print(f"generated_briefs={created}")
    print(f"output_dir={outdir}")


if __name__ == "__main__":
    main()


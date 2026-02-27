#!/usr/bin/env python3
"""
city_expansion_list.csv とテンプレートから地域ページを自動生成する。
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def load_cities(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def slugify(city: str) -> str:
    return city.replace(" ", "").replace("　", "")


def render(template: str, row: dict[str, str]) -> str:
    city = row.get("city", "").strip()
    prefecture = row.get("prefecture", "").strip()
    keyword_prefix = row.get("keyword_prefix", "").strip()
    priority = row.get("priority", "").strip()
    return template.format(
        city=city,
        prefecture=prefecture,
        keyword_prefix=keyword_prefix,
        priority=priority,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="地域ページ自動生成")
    parser.add_argument("--cities", required=True, help="city_expansion_list.csv")
    parser.add_argument("--template", required=True, help="area template markdown")
    parser.add_argument("--outdir", required=True, help="output directory")
    args = parser.parse_args()

    cities = load_cities(Path(args.cities))
    template_text = Path(args.template).read_text(encoding="utf-8")
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    created = 0
    for row in cities:
        city = row.get("city", "").strip()
        if not city:
            continue
        filename = f"area-{slugify(city)}.md"
        (outdir / filename).write_text(render(template_text, row), encoding="utf-8")
        created += 1

    print(f"generated_area_pages={created}")
    print(f"output_dir={outdir}")


if __name__ == "__main__":
    main()


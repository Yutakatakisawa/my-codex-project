"""
記事プレビューツール
====================
outputs/ フォルダ内の Markdown 記事を HTML に変換し、
ブラウザで表示します。

使い方:
    python preview.py                  # 最新の記事をプレビュー
    python preview.py --list           # 記事一覧を表示
    python preview.py --file 記事.md   # 指定した記事をプレビュー
"""

import argparse
import html
import re
import sys
import tempfile
import webbrowser
from pathlib import Path

OUTPUTS_DIR = Path(__file__).parent / "outputs"

# ============================================================
# Markdown → HTML 変換（外部ライブラリ不要）
# ============================================================

def markdown_to_html(md_text: str) -> str:
    """簡易 Markdown → HTML 変換（標準ライブラリのみ使用）"""

    # フロントマター（---で囲まれたメタ情報）を抽出して除去
    frontmatter = {}
    fm_match = re.match(r"^---\s*\n([\s\S]*?)\n---\s*\n", md_text)
    if fm_match:
        fm_block = fm_match.group(1)
        for line in fm_block.split("\n"):
            if ":" in line:
                key, val = line.split(":", 1)
                frontmatter[key.strip().strip('"')] = val.strip().strip('"')
        md_text = md_text[fm_match.end():]

    lines = md_text.split("\n")
    html_lines = []
    in_code_block = False
    in_ul = False
    in_ol = False
    in_table = False
    table_rows = []
    ol_counter = 0

    def close_list():
        nonlocal in_ul, in_ol, ol_counter
        result = []
        if in_ul:
            result.append("</ul>")
            in_ul = False
        if in_ol:
            result.append("</ol>")
            in_ol = False
            ol_counter = 0
        return result

    def close_table():
        nonlocal in_table, table_rows
        if not in_table:
            return []
        result = ['<div class="table-wrap"><table>']
        for i, row in enumerate(table_rows):
            cells = [c.strip() for c in row.strip("|").split("|")]
            if i == 0:
                result.append("<thead><tr>")
                for c in cells:
                    result.append(f"<th>{inline_format(c)}</th>")
                result.append("</tr></thead><tbody>")
            elif i == 1:
                continue  # separator row
            else:
                result.append("<tr>")
                for c in cells:
                    result.append(f"<td>{inline_format(c)}</td>")
                result.append("</tr>")
        result.append("</tbody></table></div>")
        in_table = False
        table_rows = []
        return result

    def inline_format(text: str) -> str:
        """インライン要素（太字、イタリック、コード、リンク）の変換"""
        text = html.escape(text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"__(.+?)__", r"<strong>\1</strong>", text)
        text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
        text = re.sub(r"_(.+?)_", r"<em>\1</em>", text)
        text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
        text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)
        return text

    for line in lines:
        # コードブロック
        if line.strip().startswith("```"):
            if in_code_block:
                html_lines.append("</code></pre>")
                in_code_block = False
            else:
                html_lines.extend(close_list())
                html_lines.extend(close_table())
                lang = line.strip().lstrip("`").strip()
                html_lines.append(f'<pre><code class="language-{lang}">' if lang else "<pre><code>")
                in_code_block = True
            continue

        if in_code_block:
            html_lines.append(html.escape(line))
            continue

        stripped = line.strip()

        # 空行
        if not stripped:
            if in_table:
                html_lines.extend(close_table())
            html_lines.extend(close_list())
            continue

        # テーブル行
        if "|" in stripped and stripped.startswith("|"):
            if not in_table:
                html_lines.extend(close_list())
                in_table = True
            table_rows.append(stripped)
            continue
        elif in_table:
            html_lines.extend(close_table())

        # 見出し
        heading_match = re.match(r"^(#{1,6})\s+(.*)", stripped)
        if heading_match:
            html_lines.extend(close_list())
            level = len(heading_match.group(1))
            text = inline_format(heading_match.group(2))
            anchor = re.sub(r"<[^>]+>", "", text).strip().replace(" ", "-").lower()
            html_lines.append(f'<h{level} id="{anchor}">{text}</h{level}>')
            continue

        # 水平線
        if re.match(r"^[-*_]{3,}\s*$", stripped):
            html_lines.extend(close_list())
            html_lines.append("<hr>")
            continue

        # 順序なしリスト
        ul_match = re.match(r"^[-*+]\s+(.*)", stripped)
        if ul_match:
            if in_ol:
                html_lines.extend(close_list())
            if not in_ul:
                html_lines.append("<ul>")
                in_ul = True
            html_lines.append(f"<li>{inline_format(ul_match.group(1))}</li>")
            continue

        # 順序付きリスト
        ol_match = re.match(r"^\d+\.\s+(.*)", stripped)
        if ol_match:
            if in_ul:
                html_lines.extend(close_list())
            if not in_ol:
                html_lines.append("<ol>")
                in_ol = True
                ol_counter = 0
            ol_counter += 1
            html_lines.append(f"<li>{inline_format(ol_match.group(1))}</li>")
            continue

        # 引用
        if stripped.startswith(">"):
            html_lines.extend(close_list())
            text = inline_format(stripped.lstrip("> "))
            html_lines.append(f"<blockquote><p>{text}</p></blockquote>")
            continue

        # 通常の段落
        html_lines.extend(close_list())
        html_lines.append(f"<p>{inline_format(stripped)}</p>")

    # 末尾の閉じ忘れを処理
    if in_code_block:
        html_lines.append("</code></pre>")
    html_lines.extend(close_list())
    html_lines.extend(close_table())

    body_html = "\n".join(html_lines)

    # フロントマターをヘッダーバナーとして表示
    fm_html = ""
    if frontmatter:
        fm_items = []
        for k, v in frontmatter.items():
            fm_items.append(f"<span class='fm-key'>{html.escape(k)}:</span> {html.escape(str(v))}")
        fm_html = '<div class="frontmatter">' + "<br>".join(fm_items) + "</div>"

    return fm_html + body_html


# ============================================================
# HTML テンプレート
# ============================================================

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
  :root {{
    --bg: #fafafa;
    --card: #ffffff;
    --text: #1a1a2e;
    --muted: #6b7280;
    --accent: #2563eb;
    --accent-light: #dbeafe;
    --border: #e5e7eb;
    --code-bg: #f3f4f6;
  }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: "Segoe UI", "Hiragino Kaku Gothic ProN", "Noto Sans JP", "Meiryo", sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.8;
    padding: 2rem 1rem;
  }}
  .container {{
    max-width: 820px;
    margin: 0 auto;
    background: var(--card);
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 4px 24px rgba(0,0,0,0.04);
    padding: 3rem 3.5rem;
  }}
  .header {{
    text-align: center;
    margin-bottom: 2rem;
    padding-bottom: 1.5rem;
    border-bottom: 2px solid var(--border);
  }}
  .header .badge {{
    display: inline-block;
    background: var(--accent);
    color: #fff;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.75rem;
    border-radius: 999px;
    margin-bottom: 0.5rem;
    letter-spacing: 0.05em;
  }}
  .header .filename {{
    font-size: 0.85rem;
    color: var(--muted);
  }}
  .frontmatter {{
    background: var(--accent-light);
    border-left: 4px solid var(--accent);
    padding: 1rem 1.25rem;
    border-radius: 0 8px 8px 0;
    margin-bottom: 2rem;
    font-size: 0.9rem;
    line-height: 1.7;
  }}
  .fm-key {{
    font-weight: 600;
    color: var(--accent);
  }}
  h1 {{
    font-size: 1.85rem;
    font-weight: 800;
    margin: 1.5rem 0 1rem;
    line-height: 1.4;
    color: #111827;
  }}
  h2 {{
    font-size: 1.4rem;
    font-weight: 700;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid var(--accent);
    color: #1e3a5f;
  }}
  h3 {{
    font-size: 1.15rem;
    font-weight: 600;
    margin: 1.5rem 0 0.5rem;
    color: #374151;
  }}
  h4, h5, h6 {{
    font-size: 1.05rem;
    font-weight: 600;
    margin: 1.2rem 0 0.4rem;
  }}
  p {{
    margin: 0.75rem 0;
    font-size: 1rem;
  }}
  ul, ol {{
    margin: 0.75rem 0 0.75rem 1.5rem;
  }}
  li {{
    margin: 0.35rem 0;
  }}
  blockquote {{
    border-left: 4px solid var(--accent);
    background: var(--code-bg);
    margin: 1rem 0;
    padding: 0.75rem 1.25rem;
    border-radius: 0 6px 6px 0;
    color: #374151;
  }}
  blockquote p {{ margin: 0; }}
  pre {{
    background: #1e293b;
    color: #e2e8f0;
    padding: 1.25rem;
    border-radius: 8px;
    overflow-x: auto;
    margin: 1rem 0;
    font-size: 0.9rem;
    line-height: 1.6;
  }}
  pre code {{
    background: none;
    padding: 0;
    color: inherit;
    font-size: inherit;
  }}
  code {{
    background: var(--code-bg);
    padding: 0.15rem 0.4rem;
    border-radius: 4px;
    font-size: 0.9em;
    font-family: "Consolas", "Source Code Pro", monospace;
  }}
  a {{
    color: var(--accent);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
  }}
  a:hover {{ border-bottom-color: var(--accent); }}
  hr {{
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
  }}
  strong {{ font-weight: 700; }}
  .table-wrap {{
    overflow-x: auto;
    margin: 1rem 0;
  }}
  table {{
    border-collapse: collapse;
    width: 100%;
    font-size: 0.95rem;
  }}
  th, td {{
    border: 1px solid var(--border);
    padding: 0.6rem 1rem;
    text-align: left;
  }}
  th {{
    background: var(--code-bg);
    font-weight: 600;
  }}
  .footer {{
    text-align: center;
    margin-top: 2.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
    font-size: 0.8rem;
    color: var(--muted);
  }}
  @media (max-width: 640px) {{
    .container {{ padding: 1.5rem 1.25rem; }}
    h1 {{ font-size: 1.5rem; }}
    h2 {{ font-size: 1.2rem; }}
  }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="badge">AI社員システム — 記事プレビュー</div>
    <div class="filename">{filename}</div>
  </div>
  {content}
  <div class="footer">
    屋根工事会社 AI社員システムにより自動生成
  </div>
</div>
</body>
</html>
"""


# ============================================================
# メイン処理
# ============================================================


def list_articles() -> list[Path]:
    """outputs/ フォルダ内の .md ファイルを更新日時降順で取得"""
    if not OUTPUTS_DIR.exists():
        return []
    files = sorted(OUTPUTS_DIR.glob("*.md"), key=lambda f: f.stat().st_mtime, reverse=True)
    return files


def preview_article(filepath: Path) -> None:
    """Markdown ファイルを HTML に変換してブラウザで開く"""
    if not filepath.exists():
        print(f"[ERROR] ファイルが見つかりません: {filepath}")
        sys.exit(1)

    md_text = filepath.read_text(encoding="utf-8")
    body_html = markdown_to_html(md_text)

    title = filepath.stem.replace("_", " ")
    full_html = HTML_TEMPLATE.format(
        title=html.escape(title),
        filename=html.escape(filepath.name),
        content=body_html,
    )

    # 一時 HTML ファイルを作成してブラウザで開く
    tmp = tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".html",
        prefix="preview_",
        delete=False,
        encoding="utf-8",
    )
    tmp.write(full_html)
    tmp.close()

    tmp_path = Path(tmp.name)
    print(f"  プレビューファイル: {tmp_path}")
    print(f"  ブラウザで開きます...")
    webbrowser.open(tmp_path.as_uri())
    print(f"\n  ブラウザが開かない場合は、以下のファイルを直接開いてください:")
    print(f"    {tmp_path}")


def main():
    parser = argparse.ArgumentParser(description="記事プレビューツール")
    parser.add_argument(
        "--list",
        action="store_true",
        help="outputs/ 内の記事一覧を表示",
    )
    parser.add_argument(
        "--file",
        type=str,
        default=None,
        help="プレビューする .md ファイル名またはパス",
    )
    args = parser.parse_args()

    print()
    print("=" * 50)
    print("  記事プレビューツール")
    print("=" * 50)

    articles = list_articles()

    # --- 一覧表示モード ---
    if args.list:
        if not articles:
            print("\n  outputs/ フォルダに記事がありません。")
            print("  先に python run.py で記事を生成してください。")
            return
        print(f"\n  {len(articles)} 件の記事が見つかりました:\n")
        for i, a in enumerate(articles, 1):
            size = a.stat().st_size
            print(f"  {i}. {a.name}  ({size:,} bytes)")
        print(f"\n  プレビューするには:")
        print(f'    python preview.py --file "{articles[0].name}"')
        return

    # --- ファイル指定モード ---
    if args.file:
        target = Path(args.file)
        if not target.is_absolute() and not target.exists():
            target = OUTPUTS_DIR / args.file
        preview_article(target)
        return

    # --- デフォルト: 最新の記事をプレビュー ---
    if not articles:
        print("\n  outputs/ フォルダに記事がありません。")
        print("  先に python run.py で記事を生成してください。")
        return

    latest = articles[0]
    print(f"\n  最新の記事をプレビューします:")
    print(f"    {latest.name}")
    preview_article(latest)


if __name__ == "__main__":
    main()

"""
屋根工事会社向け AI社員システム
=================================
3つのAIエージェント（Jarvis / Alice / Taro）が連携して
SEO記事を自動生成するパイプラインスクリプトです。

使い方:
    python run.py
    python run.py --theme "盛岡市 雨漏り 修理"
"""

import argparse
import json
import os
import re
import sys
import datetime
from pathlib import Path

from openai import OpenAI

# ============================================================
# 設定
# ============================================================

# デフォルトのテーマ（コマンドライン引数で上書き可能）
DEFAULT_THEME = "盛岡市 雨漏り 修理"

# 使用する OpenAI モデル
MODEL = "gpt-4o"

# 各エージェントのプロンプトファイル
AGENTS_DIR = Path(__file__).parent / "agents"
OUTPUTS_DIR = Path(__file__).parent / "outputs"

# ============================================================
# ユーティリティ
# ============================================================


def load_agent_prompt(filename: str) -> str:
    """agents/ ディレクトリからエージェントのシステムプロンプトを読み込む"""
    filepath = AGENTS_DIR / filename
    if not filepath.exists():
        print(f"[ERROR] エージェントファイルが見つかりません: {filepath}")
        sys.exit(1)
    return filepath.read_text(encoding="utf-8")


def call_openai(
    client: OpenAI,
    system_prompt: str,
    user_message: str,
    agent_name: str,
) -> str:
    """OpenAI API を呼び出してレスポンスを取得する"""
    print(f"\n{'='*60}")
    print(f"  {agent_name} が作業中...")
    print(f"{'='*60}")

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.7,
        max_tokens=4096,
    )

    result = response.choices[0].message.content
    print(f"  {agent_name} の作業が完了しました。")
    return result


def extract_json(text: str) -> dict:
    """レスポンスから JSON 部分を抽出してパースする"""
    # ```json ... ``` ブロックを探す
    pattern = r"```json\s*([\s\S]*?)\s*```"
    match = re.search(pattern, text)
    if match:
        json_str = match.group(1)
    else:
        # ブロックが無い場合はテキスト全体を JSON としてパースを試みる
        json_str = text

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        # JSON パース失敗時は最初の { から最後の } までを抽出して再試行
        start = json_str.find("{")
        end = json_str.rfind("}") + 1
        if start != -1 and end > start:
            try:
                return json.loads(json_str[start:end])
            except json.JSONDecodeError:
                pass
        print("[WARN] JSON のパースに失敗しました。生テキストをそのまま使用します。")
        return {"raw_response": text}


def save_article(content: str, theme: str) -> Path:
    """生成された記事を outputs/ フォルダに保存する"""
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    # ファイル名をテーマ＋日時で生成
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_theme = re.sub(r"[^\w\s-]", "", theme).strip().replace(" ", "_")
    if not safe_theme:
        safe_theme = "article"
    filename = f"{safe_theme}_{timestamp}.md"
    filepath = OUTPUTS_DIR / filename

    filepath.write_text(content, encoding="utf-8")
    return filepath


# ============================================================
# パイプライン
# ============================================================


def run_pipeline(theme: str) -> None:
    """メインパイプライン: Jarvis → Alice → Taro"""

    # --- OpenAI クライアント初期化 ---
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("[ERROR] 環境変数 OPENAI_API_KEY が設定されていません。")
        print("  Windows:  set OPENAI_API_KEY=sk-xxxxxxx")
        print("  PowerShell: $env:OPENAI_API_KEY='sk-xxxxxxx'")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print("\n" + "=" * 60)
    print("  屋根工事会社 AI社員システム")
    print(f"  テーマ: {theme}")
    print("=" * 60)

    # --- Step 1: Jarvis（マネージャー）がタスクを分解 ---
    jarvis_prompt = load_agent_prompt("jarvis.md")
    jarvis_user_msg = (
        f"以下のテーマでSEO記事を制作します。\n"
        f"タスクを分解し、各メンバーへの指示を作成してください。\n\n"
        f"テーマ: 「{theme}」"
    )
    jarvis_response = call_openai(client, jarvis_prompt, jarvis_user_msg, "Jarvis（マネージャー）")
    jarvis_data = extract_json(jarvis_response)

    print("\n[Jarvis] タスク分解結果:")
    if "raw_response" not in jarvis_data:
        print(f"  ターゲット読者: {jarvis_data.get('target_reader', 'N/A')}")
        print(f"  検索意図: {jarvis_data.get('search_intent', 'N/A')}")
        print(f"  記事の目的: {jarvis_data.get('article_goal', 'N/A')}")
        sections = jarvis_data.get("section_outline", [])
        print(f"  セクション構成: {len(sections)} セクション")
        for i, sec in enumerate(sections, 1):
            print(f"    {i}. {sec}")
    else:
        print("  (構造化データ取得失敗 — 生テキストで続行)")

    # --- Step 2: Alice（SEOリサーチ）が記事構成を作成 ---
    alice_prompt = load_agent_prompt("alice.md")

    # Jarvis の出力を Alice への入力メッセージに組み込む
    alice_instructions = jarvis_data.get("alice_instructions", "")
    section_outline = jarvis_data.get("section_outline", [])
    alice_user_msg = (
        f"Jarvis（マネージャー）からの指示に基づき、SEO最適化された記事構成を作成してください。\n\n"
        f"【テーマ】{theme}\n"
        f"【ターゲット読者】{jarvis_data.get('target_reader', '屋根工事を検討している一般消費者')}\n"
        f"【検索意図】{jarvis_data.get('search_intent', '情報収集')}\n"
        f"【セクション案】\n"
        + "\n".join(f"  - {s}" for s in section_outline)
        + f"\n\n【Aliceへの調査指示】\n{alice_instructions}"
    )
    alice_response = call_openai(client, alice_prompt, alice_user_msg, "Alice（SEOリサーチ）")
    alice_data = extract_json(alice_response)

    print("\n[Alice] SEO構成結果:")
    if "raw_response" not in alice_data:
        print(f"  タイトル: {alice_data.get('title', 'N/A')}")
        print(f"  メタディスクリプション: {alice_data.get('meta_description', 'N/A')}")
        keywords = alice_data.get("keywords", {})
        print(f"  メインKW: {keywords.get('primary', 'N/A')}")
        print(f"  サブKW: {keywords.get('secondary', [])}")
        headings = alice_data.get("headings", [])
        print(f"  見出し数: {len(headings)}")
        for h in headings:
            print(f"    [{h.get('level', '?')}] {h.get('text', '?')}")
    else:
        print("  (構造化データ取得失敗 — 生テキストで続行)")

    # --- Step 3: Taro（記事作成）が本文を執筆 ---
    taro_prompt = load_agent_prompt("taro.md")

    # Jarvis + Alice の出力を Taro への入力に組み込む
    taro_instructions = jarvis_data.get("taro_instructions", "")
    taro_user_msg = (
        f"以下の情報をもとに、高品質なSEO記事をMarkdown形式で執筆してください。\n\n"
        f"【テーマ】{theme}\n"
        f"【Jarvisからの執筆指示】\n{taro_instructions}\n\n"
        f"【Aliceが作成したSEO構成】\n{json.dumps(alice_data, ensure_ascii=False, indent=2)}\n\n"
        f"上記の構成（タイトル・見出し・キーワード・方向性）に忠実に従い、\n"
        f"Markdown形式で記事全文を出力してください。\n"
        f"フロントマター（---で囲まれたメタ情報）も含めてください。"
    )
    taro_response = call_openai(client, taro_prompt, taro_user_msg, "Taro（記事作成）")

    # Markdown コードブロックで囲まれている場合は中身を取り出す
    article_content = taro_response
    md_block = re.search(r"```markdown\s*([\s\S]*?)\s*```", taro_response)
    if md_block:
        article_content = md_block.group(1)

    # --- Step 4: 記事を保存 ---
    output_path = save_article(article_content, theme)

    print("\n" + "=" * 60)
    print("  全工程完了！")
    print(f"  記事保存先: {output_path}")
    print("=" * 60)

    # 記事のプレビュー（先頭500文字）
    preview = article_content[:500]
    print(f"\n--- 記事プレビュー（先頭500文字）---\n{preview}\n...")


# ============================================================
# エントリポイント
# ============================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="屋根工事会社向け AI社員システム — SEO記事自動生成"
    )
    parser.add_argument(
        "--theme",
        type=str,
        default=DEFAULT_THEME,
        help=f"記事のテーマ（デフォルト: {DEFAULT_THEME}）",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help=f"使用するOpenAIモデル（デフォルト: {MODEL}）",
    )
    args = parser.parse_args()

    if args.model:
        MODEL = args.model

    run_pipeline(args.theme)

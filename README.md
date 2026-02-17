# 屋根工事会社向け AI社員システム

3つのAIエージェントが連携してSEO記事を自動生成するシステムです。

## AI社員紹介

| 名前 | 役割 | 担当 |
|------|------|------|
| **Jarvis** | マネージャー | テーマを受け取り、タスクを分解。各メンバーへ指示を出す |
| **Alice** | SEOリサーチ | キーワード調査、見出し構成、メタ情報を作成 |
| **Taro** | 記事作成 | 構成に基づき、高品質なMarkdown記事を執筆 |

## フォルダ構成

```
project/
├── agents/
│   ├── jarvis.md      # Jarvis のシステムプロンプト
│   ├── alice.md       # Alice のシステムプロンプト
│   └── taro.md        # Taro のシステムプロンプト
├── outputs/           # 生成された記事の保存先
│   └── .gitkeep
├── run.py             # メイン実行スクリプト（記事生成）
├── preview.py         # プレビューツール（HTML変換＆ブラウザ表示）
├── requirements.txt   # Python依存パッケージ
├── .gitignore
└── README.md          # このファイル
```

## セットアップ手順

### 1. Python のインストール

Python 3.10 以上が必要です。以下からダウンロードしてください:  
https://www.python.org/downloads/

インストール時に **「Add Python to PATH」にチェック** を入れてください。

### 2. プロジェクトのクローン・展開

```powershell
cd C:\Users\あなたのユーザー名\Documents
git clone <リポジトリURL>
cd <プロジェクトフォルダ>
```

### 3. 仮想環境の作成（推奨）

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **コマンドプロンプトの場合:**
> ```cmd
> python -m venv venv
> venv\Scripts\activate.bat
> ```

### 4. 依存パッケージのインストール

```powershell
pip install -r requirements.txt
```

### 5. OpenAI API キーの設定

OpenAI の API キーを環境変数に設定します。

**PowerShell（一時的）:**
```powershell
$env:OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"
```

**コマンドプロンプト（一時的）:**
```cmd
set OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**永続的に設定する場合:**
```powershell
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "sk-xxxxxxxxxxxxxxxxxxxxxxxx", "User")
```

> Cursor で使う場合は、Cursor の設定画面またはプロジェクト直下に `.env` ファイルを作成しても構いません（run.py は `os.environ` から読み取ります）。

## 実行方法

### 基本実行（デフォルトテーマ: 「盛岡市 雨漏り 修理」）

```powershell
python run.py
```

### テーマを指定して実行

```powershell
python run.py --theme "横浜市 屋根 葺き替え"
python run.py --theme "福岡市 瓦屋根 修理 費用"
python run.py --theme "札幌市 雪害 屋根修理"
```

### モデルを指定して実行

```powershell
python run.py --theme "名古屋市 屋根塗装" --model gpt-4o-mini
```

## 記事のプレビュー

生成された記事をブラウザで確認できます。

### 最新の記事をプレビュー

```powershell
python preview.py
```

### 記事一覧を表示

```powershell
python preview.py --list
```

### 特定の記事をプレビュー

```powershell
python preview.py --file "盛岡市_雨漏り_修理_20260211_143022.md"
```

記事はきれいにスタイリングされた HTML に変換され、デフォルトブラウザで自動的に開きます。外部ライブラリ不要（Python 標準ライブラリのみ使用）です。

## 処理フロー

```
テーマ入力
    │
    ▼
┌─────────────────────┐
│  Jarvis（マネージャー）  │  タスク分解・指示作成
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Alice（SEOリサーチ）   │  キーワード調査・構成作成
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│  Taro（記事作成）       │  Markdown記事を執筆
└─────────┬───────────┘
          │
          ▼
    outputs/ に保存
```

## 出力例

生成された記事は `outputs/` フォルダに以下の形式で保存されます:

```
outputs/盛岡市_雨漏り_修理_20260211_143022.md
```

記事はMarkdown形式で、フロントマター（メタ情報）付きです。

## カスタマイズ

### エージェントのプロンプトを変更する

`agents/` フォルダ内の各 `.md` ファイルを編集することで、
AIの振る舞いを自由にカスタマイズできます。

- `agents/jarvis.md` — タスク分解の方針を変更
- `agents/alice.md` — SEO調査の観点を変更
- `agents/taro.md` — 文体・トーン・文字数などを変更

### デフォルトテーマを変更する

`run.py` の先頭付近にある以下の変数を編集してください:

```python
DEFAULT_THEME = "盛岡市 雨漏り 修理"
```

### モデルを変更する

`run.py` の以下の変数を編集してください:

```python
MODEL = "gpt-4o"
```

## トラブルシューティング

| 問題 | 解決方法 |
|------|----------|
| `OPENAI_API_KEY が設定されていません` | 環境変数を正しく設定してください |
| `openai.AuthenticationError` | APIキーが正しいか確認してください |
| `openai.RateLimitError` | しばらく待ってから再実行してください |
| JSON パースエラーの警告 | 動作には影響ありません。AIの出力形式が想定と異なった場合に表示されます |

## 必要な環境

- Python 3.10+
- OpenAI API キー（GPT-4o 推奨）
- インターネット接続

## ライセンス

社内利用を想定しています。

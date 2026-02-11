# AI Employee System - 運用ガイド

## 目次

1. [このシステムとは何か](#1-このシステムとは何か)
2. [セットアップ手順](#2-セットアップ手順)
3. [APIキーの取得方法](#3-apiキーの取得方法)
4. [起動方法](#4-起動方法)
5. [使い方の具体例](#5-使い方の具体例)
6. [ダッシュボードの見方](#6-ダッシュボードの見方)
7. [Telegram連携の設定](#7-telegram連携の設定)
8. [Mac Miniでの24時間運用](#8-mac-miniでの24時間運用)
9. [カスタマイズ方法](#9-カスタマイズ方法)
10. [トラブルシューティング](#10-トラブルシューティング)

---

## 1. このシステムとは何か

MacBook + Mac Mini だけで **7人のAI従業員** を24時間稼働させるシステムです。

### 仕組み

```
あなた（人間）
  │
  │ "SaaS製品を作って" と指示
  │
  ▼
Jarvis（CSO / 社長AI）  ← Claude Opus（最高性能）
  │
  │ 自分では作業しない。考えて、指示を出すだけ。
  │
  ├─→ Alice（リサーチ）   → 市場調査・競合分析
  ├─→ Pixel（デザイン）   → UI/UX・マーケ画像
  ├─→ Max（エンジニア）   → コーディング
  ├─→ Nova（マーケ）      → 戦略・広告企画
  ├─→ Quinn（分析）       → データ分析・KPI
  ├─→ Riley（CS）         → 顧客対応・FAQ
  └─→ Sam（コンテンツ）   → ブログ・SNS・メール
```

### なぜ Jarvis に全部やらせないのか？

| 問題 | 解決策 |
|------|--------|
| Opus のトークンコストが爆増 | Jarvis は思考のみ、作業は安いモデルに委譲 |
| API利用制限でアカウントBAN | 複数のAPIプロバイダーに作業を分散 |
| 1つのモデルの限界 | 得意分野ごとに専門AIを配置 |

---

## 2. セットアップ手順

### 必要なもの

- Mac（MacBook / Mac Mini / どちらでも可）
- Python 3.10 以上
- インターネット接続

### ワンコマンドセットアップ

```bash
git clone <このリポジトリ>
cd my-codex-project
bash setup.sh
```

これだけで以下が自動的に行われます：
1. Python環境チェック
2. 仮想環境（venv）作成
3. 全パッケージインストール
4. `.env` ファイル作成
5. 出力ディレクトリ作成

### 手動セットアップ（上記がうまくいかない場合）

```bash
# 1. 仮想環境
python3 -m venv venv
source venv/bin/activate

# 2. パッケージ
pip install -r requirements.txt

# 3. 環境変数
cp .env.example .env

# 4. ディレクトリ
mkdir -p logs/agents output/{images,code,analytics,content}
```

---

## 3. APIキーの取得方法

### まずはAPIキーなしで試す

**APIキーがなくてもデモモードで動作します。** 各エージェントがモック（擬似）応答を返すので、システムの動きを確認できます。

### 本格運用する場合のAPIキー

`.env` ファイルを編集します：

```bash
nano .env   # または好みのエディタ
```

#### 必須（1つ以上）

| キー | 取得先 | 対象エージェント | 料金目安 |
|------|--------|-----------------|---------|
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com/) | Jarvis, Max, Sam | $3-15/100万トークン |
| `GOOGLE_API_KEY` | [aistudio.google.com](https://aistudio.google.com/apikey) | Pixel, Riley | 無料枠あり |
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com/api-keys) | Nova | $2.5-10/100万トークン |

#### 任意（機能強化）

| キー | 取得先 | 用途 |
|------|--------|------|
| `GLM_API_KEY` | [open.bigmodel.cn](https://open.bigmodel.cn/) | Alice, Quinn（中国語モデル）|
| `FIRECRAWL_API_KEY` | [firecrawl.dev](https://firecrawl.dev/) | Aliceのウェブスクレイピング |
| `TELEGRAM_BOT_TOKEN` | [@BotFather](https://t.me/BotFather) | リアルタイム報告 |

#### `.env` 設定例（最小構成）

```env
# Anthropicキーだけで Jarvis + Max + Sam が動く
ANTHROPIC_API_KEY=sk-ant-api03-xxxxxxxx

# GoogleキーでPixel + Rileyも追加
GOOGLE_API_KEY=AIzaSyxxxxxxxx
```

---

## 4. 起動方法

仮想環境を有効化してから実行します：

```bash
source venv/bin/activate
```

### モード一覧

#### デモモード（おすすめ・最初に試す）

```bash
# ダッシュボードなし（ターミナルだけ）
python main.py --demo --no-dashboard

# ダッシュボード付き（ブラウザで見る）
python main.py --demo
# → http://localhost:8080 を開く
```

サンプルタスクが自動的にJarvisに送られ、チーム全体が動く様子を確認できます。

#### 対話モード（自分でタスクを入力）

```bash
python main.py --no-dashboard
```

```
📋 Objective > AIを使った新しいSaaS製品の企画書を作ってください
  → Submitted to Jarvis (ID: obj-a3f2b1c0)

📋 Objective > status
--- System Status ---
Jarvis: idle | Tasks: 1
  Alice: idle | Tasks: 1 | Tokens: 2,340
  Pixel: idle | Tasks: 1 | Tokens: 1,890
  Max: working | Tasks: 0 | Tokens: 0
  ...
---

📋 Objective > quit
```

#### 単発タスク

```bash
python main.py -o "競合他社を5社リストアップし、それぞれの強み弱みを分析して"
```

#### ダッシュボードだけ

```bash
python main.py --dashboard-only --port 3000
# → http://localhost:3000
```

---

## 5. 使い方の具体例

### 例1: 新規SaaS製品の立ち上げ

```
Objective > AI搭載のプロジェクト管理ツールを立ち上げたい。
           市場調査、競合分析、MVP設計、マーケティング戦略を
           包括的に作成してください。
```

Jarvisの動き：
1. Alice に市場調査と競合分析を依頼
2. Pixel にUI/UXモックアップを依頼
3. Max に技術アーキテクチャ設計を依頼
4. Nova にマーケティング戦略を依頼
5. Sam にランディングページのコピーを依頼
6. 全結果を統合して報告

### 例2: コンテンツマーケティング

```
Objective > 今月のコンテンツカレンダーを作ってください。
           ブログ4本、Twitter投稿20本、LinkedIn投稿8本、
           ニュースレター2通を企画して。
```

### 例3: 技術開発

```
Objective > REST APIの設計書を作成してください。
           ユーザー認証、CRUD操作、WebSocket通知を含む。
           Python/FastAPIで実装方針も提案して。
```

### 例4: 顧客分析

```
Objective > 当社SaaS製品のチャーン率が上がっている。
           原因を分析し、改善策を5つ提案してください。
           カスタマーサクセスのフローも見直して。
```

---

## 6. ダッシュボードの見方

ブラウザで `http://localhost:8080` を開くと、SF映画のようなリアルタイムUIが表示されます。

### 画面の構成

```
┌─────────────────────────────────────────┐
│          AI EMPLOYEE SYSTEM             │  ← ヘッダー
│  Agents Online: 7/7  Tasks: 12          │
├─────────────────────────────────────────┤
│ [Jarvis - CSO]  ← 全幅のメインカード     │
│  Status: DELEGATING                     │
│  Current: Analyzing market research...  │
├──────────────────┬──────────────────────┤
│ [Alice]          │ [Pixel]              │  ← エージェント
│  🔵 WORKING     │  🟢 IDLE            │     カード
│  Researching...  │  Waiting...          │
├──────────────────┼──────────────────────┤
│ [Max]            │ [Nova]               │
│  🔵 WORKING     │  🟢 IDLE            │
│  Coding API...   │  Waiting...          │
├──────────────────┴──────────────────────┤
│ [ Event Log ]                           │  ← イベントログ
│  10:23:45  Alice  ✅ task completed     │
│  10:23:40  Jarvis 📤 delegated to Max  │
│  10:23:35  Pixel  🔵 task started      │
└─────────────────────────────────────────┘
```

### ステータスの意味

| 表示 | 色 | 意味 |
|------|-----|------|
| 🟢 IDLE | 緑 | 待機中（タスク受付可能） |
| 🔵 WORKING | 青 | 作業中（光るアニメーション） |
| 🟡 THINKING | 紫 | 推論中（Jarvisが考え中） |
| 🟠 DELEGATING | オレンジ | 委譲中（Jarvisが指示出し中） |
| 🔴 ERROR | 赤 | エラー発生 |
| ⚫ OFFLINE | グレー | オフライン |

---

## 7. Telegram連携の設定

Jarvisからのレポートをスマホのtelegramで24時間受け取れます。

### 手順

1. Telegramで [@BotFather](https://t.me/BotFather) にメッセージ
2. `/newbot` でボットを作成
3. ボットトークンをコピー
4. ボットにメッセージを送信（チャットを開始）
5. `https://api.telegram.org/bot<TOKEN>/getUpdates` でチャットIDを取得
6. `.env` に設定：

```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqr
TELEGRAM_CHAT_ID=987654321
```

### 届く通知の例

```
🚀 AI Employee System Started
7 AI employees are now online and ready to work.

📊 Task Report from Jarvis
Task: SaaS製品の企画
Summary: Alice が市場調査を完了、Pixel がUI設計...

⚠️ Task Failed - Alice
Error: Firecrawl API rate limit exceeded
```

---

## 8. Mac Miniでの24時間運用

### Mac Mini の設定

1. **スリープを無効化**
   - システム設定 → 省エネルギー → スリープしない

2. **自動ログイン**
   - システム設定 → ユーザとグループ → 自動ログイン

3. **再起動後の自動起動（launchd）**

```bash
# ~/Library/LaunchAgents/com.ai-employees.plist を作成
cat > ~/Library/LaunchAgents/com.ai-employees.plist << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.ai-employees</string>
    <key>ProgramArguments</key>
    <array>
        <string>/path/to/venv/bin/python</string>
        <string>/path/to/main.py</string>
        <string>--demo</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/project</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/ai-employees.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/ai-employees-error.log</string>
</dict>
</plist>
EOF

# 有効化
launchctl load ~/Library/LaunchAgents/com.ai-employees.plist
```

4. **SSH でリモートアクセス**
   - システム設定 → 共有 → リモートログイン を有効化
   - MacBook から: `ssh username@mac-mini.local`

5. **ダッシュボードにリモートアクセス**
   - Mac Mini で `python main.py --demo` を実行
   - MacBook のブラウザで `http://mac-mini.local:8080`

---

## 9. カスタマイズ方法

### エージェントの性格を変える

`ai_employee_system/mindsets/` フォルダの `.md` ファイルを編集：

```bash
nano ai_employee_system/mindsets/jarvis.md
```

例：Jarvisをより攻撃的な戦略家にする
```markdown
## Core Principles
- 常に市場シェア拡大を最優先
- リスクを恐れず、大胆な戦略を取る
- スピード重視、完璧より実行
```

### 新しいエージェントを追加する

1. `ai_employee_system/agents/` に新しいファイルを作成
2. `BaseAgent` を継承
3. `execute_task()` と `call_llm()` を実装
4. `mindsets/` にマインドセットファイルを作成
5. `orchestrator.py` に登録

### ツールを追加する

`ai_employee_system/tools/` に新しいツールクラスを作成し、エージェントのMCPサーバーに登録：

```python
# 新しいツールの例
class SlackTool:
    async def send_message(self, channel, text):
        ...
    
    def get_mcp_tools(self):
        return [{"name": "slack_send", ...}]
```

---

## 10. トラブルシューティング

### よくある問題

| 症状 | 原因 | 解決策 |
|------|------|--------|
| `ModuleNotFoundError` | パッケージ未インストール | `pip install -r requirements.txt` |
| `API key not configured` | `.env` 未設定 | `.env` にキーを追加 |
| Agent が全部 OFFLINE | 起動していない | `python main.py --demo` で起動 |
| Token limit exceeded | APIの利用制限 | プロバイダーの料金プランを確認 |
| ダッシュボードが開かない | ポート競合 | `--port 3000` で別ポートを指定 |

### ログの確認

```bash
# システム全体のログ
cat logs/system.log

# エージェントのログ
cat logs/agents/all_agents.log

# リアルタイムでログを見る
tail -f logs/system.log
```

### APIキーなしで動かない場合

デモモードでは全エージェントがモック応答を使います。APIを呼ばないので、キーは不要です：

```bash
python main.py --demo --no-dashboard
```

---

## まとめ

```
Step 1:  bash setup.sh          ← 環境構築
Step 2:  nano .env               ← APIキー設定（任意）
Step 3:  python main.py --demo   ← 起動！
Step 4:  http://localhost:8080   ← ダッシュボードを見る
```

これだけで7人のAI従業員が24時間稼働を始めます。

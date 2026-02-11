#!/bin/bash
# ============================================================
#  AI Employee System - セットアップスクリプト
#  ワンコマンドで環境構築: bash setup.sh
# ============================================================

set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color
BOLD='\033[1m'

echo ""
echo -e "${BLUE}${BOLD}=========================================${NC}"
echo -e "${BLUE}${BOLD}  AI Employee System - Setup${NC}"
echo -e "${BLUE}${BOLD}  7人のAI従業員を起動する準備${NC}"
echo -e "${BLUE}${BOLD}=========================================${NC}"
echo ""

# ---- Step 1: Python チェック ----
echo -e "${YELLOW}[1/5]${NC} Python 環境を確認中..."
if command -v python3 &> /dev/null; then
    PY_VERSION=$(python3 --version 2>&1)
    echo -e "  ${GREEN}✓${NC} $PY_VERSION が見つかりました"
else
    echo -e "  ${RED}✗ Python3 がインストールされていません${NC}"
    echo "  → brew install python3 (Mac) または apt install python3 (Linux)"
    exit 1
fi

# ---- Step 2: venv 作成 ----
echo ""
echo -e "${YELLOW}[2/5]${NC} 仮想環境を作成中..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "  ${GREEN}✓${NC} venv を作成しました"
else
    echo -e "  ${GREEN}✓${NC} venv は既に存在します"
fi

# Activate
source venv/bin/activate
echo -e "  ${GREEN}✓${NC} venv を有効化しました"

# ---- Step 3: 依存パッケージ ----
echo ""
echo -e "${YELLOW}[3/5]${NC} 依存パッケージをインストール中..."
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "  ${GREEN}✓${NC} 全パッケージをインストールしました"

# ---- Step 4: .env ファイル ----
echo ""
echo -e "${YELLOW}[4/5]${NC} 環境設定ファイルを確認中..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo -e "  ${GREEN}✓${NC} .env ファイルを作成しました"
    echo -e "  ${YELLOW}⚠  .env にAPIキーを設定してください（後述）${NC}"
else
    echo -e "  ${GREEN}✓${NC} .env は既に存在します"
fi

# ---- Step 5: ディレクトリ作成 ----
echo ""
echo -e "${YELLOW}[5/5]${NC} 出力ディレクトリを作成中..."
mkdir -p logs/agents output/{images,code,analytics,content}
echo -e "  ${GREEN}✓${NC} logs/ と output/ を作成しました"

# ---- 完了 ----
echo ""
echo -e "${GREEN}${BOLD}=========================================${NC}"
echo -e "${GREEN}${BOLD}  セットアップ完了！${NC}"
echo -e "${GREEN}${BOLD}=========================================${NC}"
echo ""
echo -e "${BOLD}次のステップ:${NC}"
echo ""
echo -e "  ${BOLD}1. APIキーを設定する（任意）${NC}"
echo -e "     nano .env"
echo ""
echo -e "     ${YELLOW}※ APIキーなしでもデモモードで動作します${NC}"
echo ""
echo -e "  ${BOLD}2. システムを起動する${NC}"
echo ""
echo -e "     ${GREEN}# デモモード（APIキー不要）${NC}"
echo -e "     source venv/bin/activate"
echo -e "     python main.py --demo --no-dashboard"
echo ""
echo -e "     ${GREEN}# ダッシュボード付きデモ${NC}"
echo -e "     python main.py --demo"
echo -e "     → ブラウザで http://localhost:8080 を開く"
echo ""
echo -e "     ${GREEN}# 対話モード（自分でタスクを入力）${NC}"
echo -e "     python main.py --no-dashboard"
echo ""
echo -e "     ${GREEN}# 単発タスク${NC}"
echo -e "     python main.py -o \"SaaS製品のランディングページを企画して\""
echo ""
echo -e "  ${BOLD}3. APIキーの入手先${NC}"
echo -e "     Anthropic : https://console.anthropic.com/"
echo -e "     Google    : https://aistudio.google.com/apikey"
echo -e "     OpenAI    : https://platform.openai.com/api-keys"
echo -e "     Firecrawl : https://firecrawl.dev/"
echo ""

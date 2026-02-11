# AI Employee System

**MacBook + Mac Mini で「7人のAI従業員」を24時間稼働させるシステム**

```
┌─────────────────────────────────────────────────────────────┐
│                    AI EMPLOYEE SYSTEM                        │
│              7 AI Agents · 24/7 Operations                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  👔 JARVIS (CSO)          Claude Opus 4.6                   │
│  ├── Thinks & Delegates   "自分で作業するな、委譲しろ"        │
│  │                                                          │
│  ├── 🔬 Alice             GLM 4.7 + Firecrawl              │
│  │   Research Analyst      リサーチ・競合分析                 │
│  │                                                          │
│  ├── 🎨 Pixel             Gemini Pro + Image Gen            │
│  │   Product Designer      UI/UX・マーケティング画像          │
│  │                                                          │
│  ├── 💻 Max               Claude Sonnet                     │
│  │   Software Engineer     コーディング・アーキテクチャ        │
│  │                                                          │
│  ├── 📈 Nova              GPT-4o                            │
│  │   Marketing Strategist  マーケティング戦略                 │
│  │                                                          │
│  ├── 📊 Quinn             GLM 4.7                           │
│  │   Data Analyst          データ分析・レポート               │
│  │                                                          │
│  ├── 🤝 Riley             Gemini Flash                      │
│  │   Customer Success      カスタマーサクセス                 │
│  │                                                          │
│  └── ✍️  Sam              Claude Haiku                      │
│      Content Creator       コンテンツ制作                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Architecture

### Core Design: Jarvis は考える。部下が働く。

```
Human → Objective → Jarvis (CSO/Opus)
                      │
                      ├─ 分析: タスクの本質を理解
                      ├─ 分解: サブタスクに分割
                      ├─ 委譲: 最適な従業員に割り当て
                      ├─ 監督: 結果を確認
                      └─ 報告: Telegram で通知
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
          Alice(Research)  Max(Code)  Sam(Content) ...
              │            │            │
          [MCP Server] [MCP Server] [MCP Server]
              │            │            │
          [Firecrawl]  [CodeExec]  [ContentGen]
```

### Why this architecture?

1. **コスト最適化**: Opus (高性能) は思考のみ → トークンコスト削減
2. **レート制限回避**: 作業を分散 → API BAN リスク低減
3. **専門性**: 各エージェントが得意分野に集中
4. **MCP サーバー**: ツール連携の標準プロトコル

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run the System

```bash
# Interactive mode (with web dashboard)
python main.py

# Demo mode (sample tasks, no API keys needed for mock mode)
python main.py --demo

# Single objective
python main.py --objective "Build a SaaS landing page for AI tools"

# Dashboard only
python main.py --dashboard-only
```

### 4. Open Dashboard

Navigate to `http://localhost:8080` to see the real-time agent dashboard.

## Configuration

### Required API Keys

| Agent | Provider | Environment Variable |
|-------|----------|---------------------|
| Jarvis (CSO) | Anthropic (Claude Opus) | `ANTHROPIC_API_KEY` |
| Alice (Research) | GLM (ZhipuAI) | `GLM_API_KEY` |
| Pixel (Design) | Google (Gemini) | `GOOGLE_API_KEY` |
| Max (Engineer) | Anthropic (Claude Sonnet) | `ANTHROPIC_API_KEY` |
| Nova (Marketing) | OpenAI (GPT-4o) | `OPENAI_API_KEY` |
| Quinn (Analytics) | GLM (ZhipuAI) | `GLM_API_KEY` |
| Riley (Support) | Google (Gemini Flash) | `GOOGLE_API_KEY` |
| Sam (Content) | Anthropic (Claude Haiku) | `ANTHROPIC_API_KEY` |

### Optional

| Service | Variable | Purpose |
|---------|----------|---------|
| Firecrawl | `FIRECRAWL_API_KEY` | Web scraping for Alice |
| Telegram | `TELEGRAM_BOT_TOKEN` | Real-time notifications |
| Telegram | `TELEGRAM_CHAT_ID` | Chat for reports |

### Mock Mode

The system works **without API keys** using built-in mock responses. Perfect for testing and development.

## Project Structure

```
ai_employee_system/
├── agents/                     # AI Employee implementations
│   ├── base_agent.py          # Base class with task queue & events
│   ├── jarvis.py              # CSO - Orchestrator (Opus)
│   ├── alice.py               # Research Analyst (GLM)
│   ├── pixel.py               # Product Designer (Gemini)
│   ├── max_dev.py             # Software Engineer (Sonnet)
│   ├── nova.py                # Marketing Strategist (GPT-4o)
│   ├── quinn.py               # Data Analyst (GLM)
│   ├── riley.py               # Customer Success (Gemini Flash)
│   └── sam.py                 # Content Creator (Haiku)
│
├── mcp_servers/               # MCP Server infrastructure
│   ├── base_mcp.py           # Per-agent MCP server
│   └── tool_registry.py      # Global tool registry
│
├── tools/                     # Agent tools
│   ├── firecrawl_tool.py     # Web scraping (Alice)
│   ├── image_gen_tool.py     # Image generation (Pixel)
│   ├── code_tool.py          # Code execution (Max)
│   ├── web_search_tool.py    # Web search (Nova)
│   ├── analytics_tool.py     # Data analysis (Quinn)
│   └── content_tool.py       # Content creation (Sam)
│
├── mindsets/                  # Agent persona MD files
│   ├── jarvis.md             # "君はCSOだ。委譲しろ。"
│   ├── alice.md              # Research analyst mindset
│   ├── pixel.md              # Designer mindset
│   ├── max.md                # Engineer mindset
│   ├── nova.md               # Marketing mindset
│   ├── quinn.md              # Analyst mindset
│   ├── riley.md              # Customer success mindset
│   └── sam.md                # Content creator mindset
│
├── dashboard/                 # Real-time web dashboard
│   └── app.py                # FastAPI + WebSocket + HTML
│
├── utils/                     # Shared utilities
│   ├── config.py             # Configuration management
│   ├── events.py             # Event bus for inter-agent comms
│   ├── logger.py             # Structured logging
│   └── telegram.py           # Telegram reporting
│
└── orchestrator.py            # Main engine

main.py                        # CLI entry point
```

## Key Concepts

### 1. MCP Servers (per-agent)

Each AI employee has their own MCP server. This is NOT just passing API keys - it's a structured protocol that lets each AI properly use tools and external resources.

```python
# Alice's MCP server with Firecrawl tools
alice.mcp_server.register_tool("firecrawl_scrape", ...)
alice.mcp_server.register_tool("firecrawl_search", ...)
alice.mcp_server.register_tool("web_search", ...)
```

### 2. Event Bus

Agents communicate via an event-driven system:
- `TASK_ASSIGNED` → Agent starts working
- `TASK_COMPLETED` → Jarvis collects results
- `DELEGATION_REQUEST` → Jarvis sends work to an employee
- `HEARTBEAT` → Dashboard updates

### 3. Mindset Files

Each agent's personality and behavior is defined in Markdown files:
- Jarvis: "自分で作業するな、推論して部下に委譲しろ"
- Alice: "事実に基づいた正確な情報を提供する"
- Max: "クリーンで保守性の高いコードを書く"

### 4. Telegram Reporting

Jarvis sends regular reports to Telegram:
- Task completion notifications
- Team status updates
- Error alerts
- Daily summaries

## Hardware Requirements

As described in the original concept:
- **MacBook**: Your workstation (design, code review)
- **Mac Mini**: Runs the 7 AI agents 24/7

Minimum specs for Mac Mini:
- Apple M2 or later
- 16GB RAM
- Always-on internet connection

## License

MIT

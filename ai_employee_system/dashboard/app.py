"""
Real-time Dashboard for AI Employee System.
Shows agents working in real-time with a modern UI.
Like the SF movie interface described in the video.
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from ..utils.events import Event, EventType, event_bus
from ..utils.logger import get_agent_logger

logger = get_agent_logger("Dashboard")

app = FastAPI(title="AI Employee System Dashboard")

# Connected WebSocket clients
connected_clients: List[WebSocket] = []

# Current system state for new connections
system_state: Dict[str, Any] = {
    "agents": {},
    "events": [],
    "stats": {
        "total_tasks": 0,
        "active_tasks": 0,
        "total_tokens": 0,
    },
}


def get_dashboard_html() -> str:
    """Return the dashboard HTML."""
    return DASHBOARD_HTML


@app.get("/")
async def root():
    return HTMLResponse(get_dashboard_html())


@app.get("/api/status")
async def get_status():
    return system_state


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.append(websocket)
    logger.info(f"Dashboard client connected ({len(connected_clients)} total)")

    # Send current state
    try:
        await websocket.send_json({
            "type": "init",
            "data": system_state,
        })
    except Exception:
        pass

    try:
        while True:
            # Keep connection alive and handle incoming messages
            data = await websocket.receive_text()
            msg = json.loads(data)
            if msg.get("type") == "ping":
                await websocket.send_json({"type": "pong"})
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        logger.info(f"Dashboard client disconnected ({len(connected_clients)} total)")
    except Exception:
        if websocket in connected_clients:
            connected_clients.remove(websocket)


async def broadcast_event(event: Event) -> None:
    """Broadcast an event to all connected dashboard clients."""
    # Update system state
    _update_state(event)

    # Broadcast to WebSocket clients
    message = {
        "type": "event",
        "data": {
            "event_type": event.event_type.value,
            "source": event.source,
            "target": event.target,
            "data": _serialize_data(event.data),
            "timestamp": event.timestamp.isoformat(),
        },
    }

    disconnected = []
    for client in connected_clients:
        try:
            await client.send_json(message)
        except Exception:
            disconnected.append(client)

    for client in disconnected:
        connected_clients.remove(client)


def _update_state(event: Event) -> None:
    """Update the system state based on events."""
    if event.event_type == EventType.AGENT_ONLINE:
        system_state["agents"][event.source] = {
            "name": event.source,
            "role": event.data.get("role", ""),
            "status": "idle",
            "current_task": None,
            "tasks_completed": 0,
            "tokens_used": 0,
            "last_update": datetime.now().isoformat(),
        }
    elif event.event_type == EventType.AGENT_OFFLINE:
        if event.source in system_state["agents"]:
            system_state["agents"][event.source]["status"] = "offline"
    elif event.event_type == EventType.TASK_STARTED:
        if event.source in system_state["agents"]:
            system_state["agents"][event.source]["status"] = "working"
            system_state["agents"][event.source]["current_task"] = event.data.get("description", "")[:60]
            system_state["stats"]["active_tasks"] += 1
    elif event.event_type == EventType.TASK_COMPLETED:
        if event.source in system_state["agents"]:
            system_state["agents"][event.source]["status"] = "idle"
            system_state["agents"][event.source]["current_task"] = None
            system_state["agents"][event.source]["tasks_completed"] += 1
            system_state["stats"]["total_tasks"] += 1
            system_state["stats"]["active_tasks"] = max(0, system_state["stats"]["active_tasks"] - 1)
    elif event.event_type == EventType.TASK_FAILED:
        if event.source in system_state["agents"]:
            system_state["agents"][event.source]["status"] = "idle"
            system_state["agents"][event.source]["current_task"] = None
            system_state["stats"]["active_tasks"] = max(0, system_state["stats"]["active_tasks"] - 1)
    elif event.event_type == EventType.HEARTBEAT:
        if event.source in system_state["agents"]:
            system_state["agents"][event.source]["tokens_used"] = event.data.get("tokens_used", 0)
            system_state["agents"][event.source]["last_update"] = datetime.now().isoformat()

    # Keep recent events
    system_state["events"].append({
        "type": event.event_type.value,
        "source": event.source,
        "timestamp": datetime.now().isoformat(),
        "data": str(event.data)[:200],
    })
    system_state["events"] = system_state["events"][-100:]


def _serialize_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Serialize event data for JSON."""
    serialized = {}
    for key, value in data.items():
        if isinstance(value, datetime):
            serialized[key] = value.isoformat()
        elif isinstance(value, (str, int, float, bool, type(None))):
            serialized[key] = value
        elif isinstance(value, dict):
            serialized[key] = _serialize_data(value)
        elif isinstance(value, list):
            serialized[key] = [str(v)[:200] for v in value]
        else:
            serialized[key] = str(value)[:200]
    return serialized


def setup_dashboard_events() -> None:
    """Subscribe dashboard to all events."""
    event_bus.subscribe_all(broadcast_event)


# ============================================================================
# Dashboard HTML - A beautiful, modern, real-time UI
# ============================================================================

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Employee System - Dashboard</title>
    <style>
        :root {
            --bg-primary: #0a0a1a;
            --bg-secondary: #111133;
            --bg-card: #1a1a3e;
            --bg-card-hover: #222255;
            --accent-blue: #4f8cff;
            --accent-purple: #a855f7;
            --accent-green: #22c55e;
            --accent-orange: #f97316;
            --accent-red: #ef4444;
            --accent-cyan: #06b6d4;
            --accent-pink: #ec4899;
            --text-primary: #e2e8f0;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border: #2a2a5a;
            --glow-blue: rgba(79, 140, 255, 0.3);
            --glow-purple: rgba(168, 85, 247, 0.3);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
            background: var(--bg-primary);
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
        }

        /* Animated background grid */
        body::before {
            content: '';
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background:
                linear-gradient(rgba(79, 140, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(79, 140, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: 0;
        }

        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 20px;
            position: relative;
            z-index: 1;
        }

        /* Header */
        .header {
            text-align: center;
            padding: 30px 0;
            border-bottom: 1px solid var(--border);
            margin-bottom: 30px;
        }

        .header h1 {
            font-size: 2rem;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 8px;
            letter-spacing: 2px;
        }

        .header .subtitle {
            color: var(--text-secondary);
            font-size: 0.85rem;
        }

        .status-bar {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 15px;
        }

        .status-item {
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 0.8rem;
        }

        .status-dot {
            width: 8px; height: 8px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        .status-dot.online { background: var(--accent-green); box-shadow: 0 0 10px var(--accent-green); }
        .status-dot.warning { background: var(--accent-orange); box-shadow: 0 0 10px var(--accent-orange); }
        .status-dot.error { background: var(--accent-red); box-shadow: 0 0 10px var(--accent-red); }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }

        /* Office Layout - Grid of agent cards */
        .office {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        /* Jarvis gets a special wider card */
        .agent-card.jarvis {
            grid-column: 1 / -1;
            background: linear-gradient(135deg, var(--bg-card), #1a1a50);
            border: 1px solid var(--accent-purple);
            box-shadow: 0 0 30px var(--glow-purple);
        }

        .agent-card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .agent-card:hover {
            background: var(--bg-card-hover);
            transform: translateY(-2px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
        }

        .agent-card.working {
            border-color: var(--accent-blue);
            box-shadow: 0 0 20px var(--glow-blue);
        }

        .agent-card.working::after {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 200%; height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent-blue), transparent);
            animation: scan 2s linear infinite;
        }

        @keyframes scan {
            0% { left: -100%; }
            100% { left: 100%; }
        }

        .agent-header {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 15px;
        }

        .agent-avatar {
            width: 48px; height: 48px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.4rem;
            font-weight: bold;
            position: relative;
        }

        .agent-avatar.jarvis-avatar { background: linear-gradient(135deg, #7c3aed, #4f8cff); }
        .agent-avatar.alice-avatar { background: linear-gradient(135deg, #06b6d4, #22c55e); }
        .agent-avatar.pixel-avatar { background: linear-gradient(135deg, #ec4899, #f97316); }
        .agent-avatar.max-avatar { background: linear-gradient(135deg, #4f8cff, #06b6d4); }
        .agent-avatar.nova-avatar { background: linear-gradient(135deg, #f97316, #eab308); }
        .agent-avatar.quinn-avatar { background: linear-gradient(135deg, #22c55e, #06b6d4); }
        .agent-avatar.riley-avatar { background: linear-gradient(135deg, #a855f7, #ec4899); }
        .agent-avatar.sam-avatar { background: linear-gradient(135deg, #ef4444, #f97316); }

        .agent-status-ring {
            position: absolute;
            top: -2px; left: -2px;
            width: 52px; height: 52px;
            border-radius: 50%;
            border: 2px solid transparent;
        }

        .agent-status-ring.idle { border-color: var(--accent-green); }
        .agent-status-ring.working { border-color: var(--accent-blue); animation: rotate 3s linear infinite; }
        .agent-status-ring.thinking { border-color: var(--accent-purple); animation: rotate 2s linear infinite; }
        .agent-status-ring.error { border-color: var(--accent-red); }
        .agent-status-ring.offline { border-color: var(--text-muted); }

        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .agent-info h3 {
            font-size: 1.1rem;
            margin-bottom: 2px;
        }

        .agent-info .role {
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        .agent-info .model {
            font-size: 0.65rem;
            color: var(--text-muted);
            margin-top: 2px;
        }

        .agent-status-badge {
            margin-left: auto;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .badge-idle { background: rgba(34, 197, 94, 0.15); color: var(--accent-green); }
        .badge-working { background: rgba(79, 140, 255, 0.15); color: var(--accent-blue); }
        .badge-thinking { background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); }
        .badge-delegating { background: rgba(249, 115, 22, 0.15); color: var(--accent-orange); }
        .badge-error { background: rgba(239, 68, 68, 0.15); color: var(--accent-red); }
        .badge-offline { background: rgba(100, 116, 139, 0.15); color: var(--text-muted); }

        .agent-task {
            margin-top: 12px;
            padding: 10px;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            font-size: 0.8rem;
            color: var(--text-secondary);
            min-height: 40px;
        }

        .agent-task .label {
            color: var(--text-muted);
            font-size: 0.7rem;
            margin-bottom: 4px;
        }

        .agent-stats {
            display: flex;
            gap: 15px;
            margin-top: 12px;
            font-size: 0.75rem;
            color: var(--text-muted);
        }

        .agent-stats span {
            display: flex;
            align-items: center;
            gap: 4px;
        }

        /* Event Log */
        .event-log {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 20px;
            max-height: 400px;
            overflow-y: auto;
        }

        .event-log h2 {
            font-size: 1rem;
            margin-bottom: 15px;
            color: var(--accent-cyan);
        }

        .event-item {
            display: flex;
            gap: 10px;
            padding: 6px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.03);
            font-size: 0.75rem;
            animation: fadeIn 0.3s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .event-time {
            color: var(--text-muted);
            white-space: nowrap;
            min-width: 70px;
        }

        .event-source {
            color: var(--accent-blue);
            min-width: 80px;
            font-weight: 600;
        }

        .event-message {
            color: var(--text-secondary);
            flex: 1;
        }

        /* Connection indicator */
        .connection-status {
            position: fixed;
            top: 10px;
            right: 10px;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.7rem;
            z-index: 100;
        }

        .connection-status.connected {
            background: rgba(34, 197, 94, 0.15);
            color: var(--accent-green);
            border: 1px solid var(--accent-green);
        }

        .connection-status.disconnected {
            background: rgba(239, 68, 68, 0.15);
            color: var(--accent-red);
            border: 1px solid var(--accent-red);
        }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: var(--bg-primary); }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

        /* Responsive */
        @media (max-width: 768px) {
            .office { grid-template-columns: 1fr; }
            .agent-card.jarvis { grid-column: 1; }
            .header h1 { font-size: 1.5rem; }
            .status-bar { flex-wrap: wrap; }
        }
    </style>
</head>
<body>
    <div class="connection-status disconnected" id="connectionStatus">CONNECTING...</div>

    <div class="container">
        <div class="header">
            <h1>AI EMPLOYEE SYSTEM</h1>
            <div class="subtitle">7 AI Agents - 24/7 Autonomous Operations</div>
            <div class="status-bar">
                <div class="status-item">
                    <span class="status-dot online" id="systemDot"></span>
                    <span id="systemStatus">System: Starting...</span>
                </div>
                <div class="status-item">
                    <span>Agents Online: <strong id="agentCount">0</strong>/7</span>
                </div>
                <div class="status-item">
                    <span>Tasks: <strong id="taskCount">0</strong></span>
                </div>
                <div class="status-item">
                    <span>Tokens: <strong id="tokenCount">0</strong></span>
                </div>
            </div>
        </div>

        <div class="office" id="officeGrid">
            <!-- Jarvis (CSO) - Main card -->
            <div class="agent-card jarvis" id="agent-Jarvis">
                <div class="agent-header">
                    <div class="agent-avatar jarvis-avatar">
                        <div class="agent-status-ring idle" id="ring-Jarvis"></div>
                        J
                    </div>
                    <div class="agent-info">
                        <h3>Jarvis</h3>
                        <div class="role">CSO - Chief Strategy Officer</div>
                        <div class="model">Claude Opus 4.6 | Thinks & Delegates</div>
                    </div>
                    <span class="agent-status-badge badge-idle" id="badge-Jarvis">IDLE</span>
                </div>
                <div class="agent-task" id="task-Jarvis">
                    <div class="label">Current Activity</div>
                    <div id="taskText-Jarvis">Waiting for instructions...</div>
                </div>
                <div class="agent-stats">
                    <span>Tasks: <strong id="completed-Jarvis">0</strong></span>
                    <span>Tokens: <strong id="tokens-Jarvis">0</strong></span>
                    <span>Employees: <strong>7</strong></span>
                </div>
            </div>

            <!-- Alice (Research) -->
            <div class="agent-card" id="agent-Alice">
                <div class="agent-header">
                    <div class="agent-avatar alice-avatar">
                        <div class="agent-status-ring offline" id="ring-Alice"></div>
                        A
                    </div>
                    <div class="agent-info">
                        <h3>Alice</h3>
                        <div class="role">Research Analyst</div>
                        <div class="model">GLM 4.7 + Firecrawl</div>
                    </div>
                    <span class="agent-status-badge badge-offline" id="badge-Alice">OFFLINE</span>
                </div>
                <div class="agent-task" id="task-Alice">
                    <div class="label">Current Activity</div>
                    <div id="taskText-Alice">-</div>
                </div>
                <div class="agent-stats">
                    <span>Tasks: <strong id="completed-Alice">0</strong></span>
                    <span>Tokens: <strong id="tokens-Alice">0</strong></span>
                </div>
            </div>

            <!-- Pixel (Designer) -->
            <div class="agent-card" id="agent-Pixel">
                <div class="agent-header">
                    <div class="agent-avatar pixel-avatar">
                        <div class="agent-status-ring offline" id="ring-Pixel"></div>
                        P
                    </div>
                    <div class="agent-info">
                        <h3>Pixel</h3>
                        <div class="role">Product Designer</div>
                        <div class="model">Gemini Pro + Image Gen</div>
                    </div>
                    <span class="agent-status-badge badge-offline" id="badge-Pixel">OFFLINE</span>
                </div>
                <div class="agent-task" id="task-Pixel">
                    <div class="label">Current Activity</div>
                    <div id="taskText-Pixel">-</div>
                </div>
                <div class="agent-stats">
                    <span>Tasks: <strong id="completed-Pixel">0</strong></span>
                    <span>Tokens: <strong id="tokens-Pixel">0</strong></span>
                </div>
            </div>

            <!-- Max (Engineer) -->
            <div class="agent-card" id="agent-Max">
                <div class="agent-header">
                    <div class="agent-avatar max-avatar">
                        <div class="agent-status-ring offline" id="ring-Max"></div>
                        M
                    </div>
                    <div class="agent-info">
                        <h3>Max</h3>
                        <div class="role">Software Engineer</div>
                        <div class="model">Claude Sonnet</div>
                    </div>
                    <span class="agent-status-badge badge-offline" id="badge-Max">OFFLINE</span>
                </div>
                <div class="agent-task" id="task-Max">
                    <div class="label">Current Activity</div>
                    <div id="taskText-Max">-</div>
                </div>
                <div class="agent-stats">
                    <span>Tasks: <strong id="completed-Max">0</strong></span>
                    <span>Tokens: <strong id="tokens-Max">0</strong></span>
                </div>
            </div>

            <!-- Nova (Marketing) -->
            <div class="agent-card" id="agent-Nova">
                <div class="agent-header">
                    <div class="agent-avatar nova-avatar">
                        <div class="agent-status-ring offline" id="ring-Nova"></div>
                        N
                    </div>
                    <div class="agent-info">
                        <h3>Nova</h3>
                        <div class="role">Marketing Strategist</div>
                        <div class="model">GPT-4o</div>
                    </div>
                    <span class="agent-status-badge badge-offline" id="badge-Nova">OFFLINE</span>
                </div>
                <div class="agent-task" id="task-Nova">
                    <div class="label">Current Activity</div>
                    <div id="taskText-Nova">-</div>
                </div>
                <div class="agent-stats">
                    <span>Tasks: <strong id="completed-Nova">0</strong></span>
                    <span>Tokens: <strong id="tokens-Nova">0</strong></span>
                </div>
            </div>

            <!-- Quinn (Analytics) -->
            <div class="agent-card" id="agent-Quinn">
                <div class="agent-header">
                    <div class="agent-avatar quinn-avatar">
                        <div class="agent-status-ring offline" id="ring-Quinn"></div>
                        Q
                    </div>
                    <div class="agent-info">
                        <h3>Quinn</h3>
                        <div class="role">Data Analyst</div>
                        <div class="model">GLM 4.7</div>
                    </div>
                    <span class="agent-status-badge badge-offline" id="badge-Quinn">OFFLINE</span>
                </div>
                <div class="agent-task" id="task-Quinn">
                    <div class="label">Current Activity</div>
                    <div id="taskText-Quinn">-</div>
                </div>
                <div class="agent-stats">
                    <span>Tasks: <strong id="completed-Quinn">0</strong></span>
                    <span>Tokens: <strong id="tokens-Quinn">0</strong></span>
                </div>
            </div>

            <!-- Riley (Customer Success) -->
            <div class="agent-card" id="agent-Riley">
                <div class="agent-header">
                    <div class="agent-avatar riley-avatar">
                        <div class="agent-status-ring offline" id="ring-Riley"></div>
                        R
                    </div>
                    <div class="agent-info">
                        <h3>Riley</h3>
                        <div class="role">Customer Success</div>
                        <div class="model">Gemini Flash</div>
                    </div>
                    <span class="agent-status-badge badge-offline" id="badge-Riley">OFFLINE</span>
                </div>
                <div class="agent-task" id="task-Riley">
                    <div class="label">Current Activity</div>
                    <div id="taskText-Riley">-</div>
                </div>
                <div class="agent-stats">
                    <span>Tasks: <strong id="completed-Riley">0</strong></span>
                    <span>Tokens: <strong id="tokens-Riley">0</strong></span>
                </div>
            </div>

            <!-- Sam (Content) -->
            <div class="agent-card" id="agent-Sam">
                <div class="agent-header">
                    <div class="agent-avatar sam-avatar">
                        <div class="agent-status-ring offline" id="ring-Sam"></div>
                        S
                    </div>
                    <div class="agent-info">
                        <h3>Sam</h3>
                        <div class="role">Content Creator</div>
                        <div class="model">Claude Haiku</div>
                    </div>
                    <span class="agent-status-badge badge-offline" id="badge-Sam">OFFLINE</span>
                </div>
                <div class="agent-task" id="task-Sam">
                    <div class="label">Current Activity</div>
                    <div id="taskText-Sam">-</div>
                </div>
                <div class="agent-stats">
                    <span>Tasks: <strong id="completed-Sam">0</strong></span>
                    <span>Tokens: <strong id="tokens-Sam">0</strong></span>
                </div>
            </div>
        </div>

        <!-- Event Log -->
        <div class="event-log" id="eventLog">
            <h2>[ Event Log ]</h2>
            <div id="events"></div>
        </div>
    </div>

    <script>
        let ws = null;
        let reconnectAttempts = 0;
        const maxReconnectAttempts = 50;

        function connect() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            ws = new WebSocket(`${protocol}//${window.location.host}/ws`);

            ws.onopen = () => {
                document.getElementById('connectionStatus').className = 'connection-status connected';
                document.getElementById('connectionStatus').textContent = 'CONNECTED';
                document.getElementById('systemStatus').textContent = 'System: Online';
                reconnectAttempts = 0;
            };

            ws.onclose = () => {
                document.getElementById('connectionStatus').className = 'connection-status disconnected';
                document.getElementById('connectionStatus').textContent = 'DISCONNECTED';
                if (reconnectAttempts < maxReconnectAttempts) {
                    reconnectAttempts++;
                    setTimeout(connect, Math.min(1000 * reconnectAttempts, 10000));
                }
            };

            ws.onmessage = (event) => {
                const msg = JSON.parse(event.data);
                if (msg.type === 'init') {
                    handleInit(msg.data);
                } else if (msg.type === 'event') {
                    handleEvent(msg.data);
                }
            };

            // Ping every 30s
            setInterval(() => {
                if (ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({type: 'ping'}));
                }
            }, 30000);
        }

        function handleInit(state) {
            // Update all agents from state
            for (const [name, agent] of Object.entries(state.agents || {})) {
                updateAgent(name, agent.status, agent.current_task, agent.tasks_completed, agent.tokens_used);
            }
            // Update stats
            updateStats(state.stats);
            // Show recent events
            for (const evt of (state.events || []).slice(-20)) {
                addEventToLog(evt.source, evt.type, evt.data, evt.timestamp);
            }
        }

        function handleEvent(data) {
            const { event_type, source, target, data: eventData, timestamp } = data;

            // Update agent UI based on event
            if (event_type === 'agent_online') {
                updateAgent(source, 'idle', null);
            } else if (event_type === 'agent_offline') {
                updateAgent(source, 'offline', null);
            } else if (event_type === 'task_started') {
                updateAgent(source, 'working', eventData.description);
            } else if (event_type === 'task_completed') {
                updateAgent(source, 'idle', null);
                incrementCompleted(source);
            } else if (event_type === 'task_failed') {
                updateAgent(source, 'idle', null);
            } else if (event_type === 'heartbeat') {
                updateTokens(source, eventData.tokens_used);
            } else if (event_type === 'delegation_request') {
                updateAgent(source, 'delegating', `Delegating to ${target}`);
            }

            // Add to event log
            addEventToLog(source, event_type, JSON.stringify(eventData).substring(0, 100), timestamp);
        }

        function updateAgent(name, status, task, completed, tokens) {
            const card = document.getElementById(`agent-${name}`);
            if (!card) return;

            // Update status badge
            const badge = document.getElementById(`badge-${name}`);
            if (badge) {
                badge.textContent = status.toUpperCase();
                badge.className = `agent-status-badge badge-${status}`;
            }

            // Update ring
            const ring = document.getElementById(`ring-${name}`);
            if (ring) {
                ring.className = `agent-status-ring ${status}`;
            }

            // Update card class
            card.className = card.className.replace(/\\b(working|idle|error|offline)\\b/g, '');
            if (status === 'working') {
                card.classList.add('working');
            }

            // Update task text
            const taskText = document.getElementById(`taskText-${name}`);
            if (taskText) {
                taskText.textContent = task || (status === 'idle' ? 'Waiting for assignment...' : '-');
            }

            if (completed !== undefined) {
                const el = document.getElementById(`completed-${name}`);
                if (el) el.textContent = completed;
            }
            if (tokens !== undefined) {
                const el = document.getElementById(`tokens-${name}`);
                if (el) el.textContent = tokens.toLocaleString();
            }
        }

        function incrementCompleted(name) {
            const el = document.getElementById(`completed-${name}`);
            if (el) el.textContent = parseInt(el.textContent || '0') + 1;
            const totalEl = document.getElementById('taskCount');
            if (totalEl) totalEl.textContent = parseInt(totalEl.textContent || '0') + 1;
        }

        function updateTokens(name, tokens) {
            const el = document.getElementById(`tokens-${name}`);
            if (el) el.textContent = (tokens || 0).toLocaleString();
        }

        function updateStats(stats) {
            if (!stats) return;
            document.getElementById('taskCount').textContent = stats.total_tasks || 0;
            document.getElementById('tokenCount').textContent = (stats.total_tokens || 0).toLocaleString();
        }

        function addEventToLog(source, type, data, timestamp) {
            const eventsEl = document.getElementById('events');
            const time = timestamp ? new Date(timestamp).toLocaleTimeString() : new Date().toLocaleTimeString();

            const typeEmojis = {
                'agent_online': '🟢',
                'agent_offline': '🔴',
                'task_started': '🔵',
                'task_completed': '✅',
                'task_failed': '❌',
                'delegation_request': '📤',
                'report_generated': '📊',
                'heartbeat': '💓',
            };

            const emoji = typeEmojis[type] || '📌';
            const shortType = type.replace('_', ' ');

            const item = document.createElement('div');
            item.className = 'event-item';
            item.innerHTML = `
                <span class="event-time">${time}</span>
                <span class="event-source">${source}</span>
                <span class="event-message">${emoji} ${shortType}: ${data || ''}</span>
            `;

            eventsEl.insertBefore(item, eventsEl.firstChild);

            // Keep max 100 events
            while (eventsEl.children.length > 100) {
                eventsEl.removeChild(eventsEl.lastChild);
            }

            // Update agent count
            const onlineCount = document.querySelectorAll('.agent-status-ring.idle, .agent-status-ring.working, .agent-status-ring.thinking').length;
            document.getElementById('agentCount').textContent = onlineCount;
        }

        // Start connection
        connect();
    </script>
</body>
</html>"""

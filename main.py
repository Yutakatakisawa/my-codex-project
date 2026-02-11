#!/usr/bin/env python3
"""
AI Employee System - Main Entry Point
======================================
Run the 7 AI Employee system with Jarvis as CSO.

Usage:
    # Start the system with dashboard
    python main.py

    # Start with a specific objective
    python main.py --objective "Build a SaaS landing page"

    # Demo mode (no API keys needed)
    python main.py --demo

    # Start only the dashboard
    python main.py --dashboard-only
"""
import argparse
import asyncio
import signal
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ai_employee_system.orchestrator import Orchestrator, run_with_dashboard
from ai_employee_system.utils.config import get_config
from ai_employee_system.utils.logger import setup_logger, get_agent_logger

logger = get_agent_logger("Main")


async def run_demo(orchestrator: Orchestrator) -> None:
    """Run a demo showing all agents working."""
    logger.info("Starting DEMO mode...")

    await orchestrator.start()

    # Wait for agents to come online
    await asyncio.sleep(2)

    # Submit demo objectives
    demo_objectives = [
        "AIを活用したSaaS製品のランディングページを企画・設計してください。"
        "ターゲットは中小企業のマネージャーです。",

        "競合他社の分析レポートを作成し、当社の差別化ポイントを明確にしてください。",

        "新製品ローンチのマーケティングキャンペーンを企画してください。"
        "SNS、ブログ、メールマーケティングを含む包括的な計画を。",
    ]

    for i, objective in enumerate(demo_objectives):
        logger.info(f"Submitting demo objective {i+1}/{len(demo_objectives)}")
        await orchestrator.submit_objective(objective)
        await asyncio.sleep(3)  # Space out submissions

    # Let the system run
    logger.info("Demo objectives submitted. System is processing...")
    logger.info("Press Ctrl+C to stop.")

    try:
        while True:
            await asyncio.sleep(10)
            status = orchestrator.get_system_status()
            total_completed = sum(
                e.get("total_completed", 0)
                for e in status["employees"].values()
            )
            logger.info(f"System running... Total tasks completed: {total_completed}")
    except asyncio.CancelledError:
        pass
    finally:
        await orchestrator.stop()


async def run_interactive(orchestrator: Orchestrator) -> None:
    """Run in interactive mode - accept objectives from stdin."""
    await orchestrator.start()

    # Wait for agents to come online
    await asyncio.sleep(1)

    print("\n" + "=" * 60)
    print("  AI Employee System - Interactive Mode")
    print("  Type an objective and press Enter.")
    print("  Type 'status' for system status.")
    print("  Type 'quit' to exit.")
    print("=" * 60 + "\n")

    try:
        while True:
            try:
                # Read input in a non-blocking way
                objective = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: input("📋 Objective > ")
                )
            except EOFError:
                break

            objective = objective.strip()
            if not objective:
                continue

            if objective.lower() == "quit":
                break

            if objective.lower() == "status":
                status = orchestrator.get_system_status()
                print("\n--- System Status ---")
                print(f"Running: {status['system']['running']}")
                print(f"\nJarvis: {status['jarvis']['status']}")
                for name, emp in status["employees"].items():
                    print(f"  {name}: {emp['status']} | Tasks: {emp['total_completed']} | Tokens: {emp['total_tokens']}")
                print("---\n")
                continue

            task_id = await orchestrator.submit_objective(objective)
            print(f"  → Submitted to Jarvis (ID: {task_id})\n")

    except asyncio.CancelledError:
        pass
    finally:
        await orchestrator.stop()


def main():
    parser = argparse.ArgumentParser(
        description="AI Employee System - 7 AI Agents for 24/7 Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                                    # Interactive mode with dashboard
  python main.py --demo                             # Demo mode with sample tasks
  python main.py --objective "Build a landing page" # Single objective
  python main.py --dashboard-only                   # Dashboard only
        """,
    )
    parser.add_argument(
        "--objective", "-o",
        type=str,
        help="Submit a specific objective to Jarvis",
    )
    parser.add_argument(
        "--demo", "-d",
        action="store_true",
        help="Run in demo mode with sample objectives",
    )
    parser.add_argument(
        "--dashboard-only",
        action="store_true",
        help="Start only the web dashboard",
    )
    parser.add_argument(
        "--no-dashboard",
        action="store_true",
        help="Run without the web dashboard",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Dashboard port (default: 8080)",
    )

    args = parser.parse_args()

    # Setup
    config = get_config()
    setup_logger(config.log_level)
    orchestrator = Orchestrator()

    # Handle graceful shutdown
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def signal_handler(sig, frame):
        logger.info("Received shutdown signal...")
        for task in asyncio.all_tasks(loop):
            task.cancel()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        if args.demo:
            if args.no_dashboard:
                loop.run_until_complete(run_demo(orchestrator))
            else:
                # Run demo + dashboard together
                async def demo_with_dashboard():
                    import uvicorn
                    from ai_employee_system.dashboard.app import app as dashboard_app

                    await orchestrator.start()
                    await asyncio.sleep(2)

                    # Submit demo tasks in background
                    async def submit_demos():
                        objectives = [
                            "AIを活用したSaaS製品のランディングページを企画・設計してください。",
                            "競合他社の分析レポートを作成してください。",
                            "新製品ローンチのマーケティングキャンペーンを企画してください。",
                        ]
                        for obj in objectives:
                            await orchestrator.submit_objective(obj)
                            await asyncio.sleep(5)

                    asyncio.create_task(submit_demos())

                    # Run dashboard
                    server_config = uvicorn.Config(
                        dashboard_app, host="0.0.0.0", port=args.port, log_level="warning"
                    )
                    server = uvicorn.Server(server_config)
                    await server.serve()

                loop.run_until_complete(demo_with_dashboard())

        elif args.objective:
            async def run_single():
                await orchestrator.start()
                await asyncio.sleep(1)
                task_id = await orchestrator.submit_objective(args.objective)
                logger.info(f"Objective submitted (ID: {task_id})")
                # Wait for completion
                await asyncio.sleep(60)
                await orchestrator.stop()

            loop.run_until_complete(run_single())

        elif args.dashboard_only:
            async def dashboard_only():
                import uvicorn
                from ai_employee_system.dashboard.app import app as dashboard_app

                server_config = uvicorn.Config(
                    dashboard_app, host="0.0.0.0", port=args.port, log_level="info"
                )
                server = uvicorn.Server(server_config)
                await server.serve()

            loop.run_until_complete(dashboard_only())

        else:
            # Default: interactive mode with dashboard
            if args.no_dashboard:
                loop.run_until_complete(run_interactive(orchestrator))
            else:
                loop.run_until_complete(run_with_dashboard(orchestrator))

    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    finally:
        # Cleanup
        try:
            loop.run_until_complete(orchestrator.stop())
        except Exception:
            pass
        loop.close()


if __name__ == "__main__":
    main()

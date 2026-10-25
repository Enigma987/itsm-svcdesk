# ai-generated: 95% - Codex implemented a CLI adapter to the unmodified course MCP server, with actual tool-call logging.
"""Call the course read-only MCP server against the separately served saved snapshot."""
import asyncio
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

from mcp import Client, StdioServerParameters

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "Laboratory 4/agent/prom_mcp.py"
OUTPUT = ROOT / "ai-rca/second"
ALLOWED = {"list_metrics", "label_values", "query", "query_range", "alerts_at"}


async def main():
    name = sys.argv[1]
    assert name in ALLOWED or name == "--list-tools", name
    environment = {**os.environ, "PROMETHEUS_URL": "http://localhost:19090"}
    async with Client(StdioServerParameters(command=sys.executable, args=[str(SERVER)], env=environment)) as client:
        if name == "--list-tools":
            definitions = await client.list_tools()
            print(json.dumps([{"name": item.name, "description": item.description, "input_schema": item.input_schema} for item in definitions.tools], indent=2))
            return
        arguments = json.loads(sys.argv[2]) if len(sys.argv) > 2 else {}
        response = await client.call_tool(name, arguments)
        content = "\n".join(item.text for item in response.content if getattr(item, "type", "") == "text")
        event = {"at": datetime.now(timezone.utc).isoformat(), "tool": name, "arguments": arguments, "is_error": response.is_error, "response": content}
        OUTPUT.mkdir(parents=True, exist_ok=True)
        with (OUTPUT / "tool-events.jsonl").open("a", encoding="utf-8") as file:
            file.write(json.dumps(event) + "\n")
        with (OUTPUT / "transcript-tools.md").open("a", encoding="utf-8") as file:
            file.write(f"## MCP tool: {name}\n\nArguments:\n\n```json\n{json.dumps(arguments, indent=2)}\n```\n\nReturned:\n\n```json\n{content}\n```\n\n")
        print(content, flush=True)
        if response.is_error:
            raise SystemExit(1)


if __name__ == "__main__":
    asyncio.run(main())

"""Small protocol-level smoke test; run with python3 mcp/test_server.py."""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "mcp" / "server.py"


def call(process, request):
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()
    return json.loads(process.stdout.readline())


def main():
    process = subprocess.Popen([sys.executable, str(SERVER)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    try:
        init = call(process, {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "smoke", "version": "0"}}})
        assert init["result"]["serverInfo"]["name"] == "masterindex"
        tools = call(process, {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        names = {tool["name"] for tool in tools["result"]["tools"]}
        assert names >= {"search_portfolio", "get_entity", "get_freshness", "check_local_sources", "verify_public_links", "capture_project_idea", "provision_project"}
        capture_tool = next(tool for tool in tools["result"]["tools"] if tool["name"] == "capture_project_idea")
        assert capture_tool["annotations"]["readOnlyHint"] is False
        search = call(process, {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "search_portfolio", "arguments": {"query": "PickleFamilia"}}})
        assert search["result"]["structuredContent"]["resultCount"] >= 1
        freshness = call(process, {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "get_freshness", "arguments": {"staleAfterDays": 7}}})
        assert "sources" in freshness["result"]["structuredContent"]
        local_sources = call(process, {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "check_local_sources", "arguments": {}}})
        assert local_sources["result"]["structuredContent"]["masterIndex"]["status"] == "observed-local"
        links_tool = next(tool for tool in tools["result"]["tools"] if tool["name"] == "verify_public_links")
        assert links_tool["annotations"]["openWorldHint"] is True
        resources = call(process, {"jsonrpc": "2.0", "id": 6, "method": "resources/list", "params": {}})
        assert "masterindex://inventory/narrative" in {resource["uri"] for resource in resources["result"]["resources"]}
        narrative = call(process, {"jsonrpc": "2.0", "id": 7, "method": "resources/read", "params": {"uri": "masterindex://inventory/narrative"}})
        assert narrative["result"]["contents"][0]["mimeType"] == "text/markdown"
        print("MCP smoke test passed")
    finally:
        process.terminate()
        process.wait(timeout=5)


if __name__ == "__main__":
    main()

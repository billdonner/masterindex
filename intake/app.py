#!/usr/bin/env python3
"""Local browser front end for reviewable MasterIndex project intake."""

from __future__ import annotations

import json
import mimetypes
import sys
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mcp"))
from project_intake import IntakeError, ProjectIntakeStore  # noqa: E402

STORE = ProjectIntakeStore(ROOT)
STATIC = ROOT / "intake" / "site"


class IntakeHandler(BaseHTTPRequestHandler):
    server_version = "MasterIndexIntake/0.1"

    def log_message(self, format, *args):
        print(f"[intake] {format % args}")

    def send_json(self, status: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def read_body(self) -> dict:
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            raise IntakeError("Use application/json.")
        length = int(self.headers.get("Content-Length", "0"))
        if not 0 < length <= 65_536:
            raise IntakeError("Request body must be between 1 and 65,536 bytes.")
        return json.loads(self.rfile.read(length))

    def do_GET(self):
        route = urlparse(self.path).path
        if route == "/api/intakes":
            return self.send_json(HTTPStatus.OK, {"projects": STORE.list_projects()})
        if route == "/health":
            return self.send_json(HTTPStatus.OK, {"status": "ok"})
        relative = "index.html" if route == "/" else route.lstrip("/")
        candidate = (STATIC / relative).resolve()
        if candidate.parent != STATIC.resolve() or not candidate.is_file():
            return self.send_error(HTTPStatus.NOT_FOUND)
        content = candidate.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", mimetypes.guess_type(candidate.name)[0] or "application/octet-stream")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        try:
            origin = self.headers.get("Origin")
            if origin and origin not in {"http://127.0.0.1:8787", "http://localhost:8787"}:
                raise IntakeError("Requests must come from this local Project Intake app.")
            route, payload = urlparse(self.path).path, self.read_body()
            if route == "/api/intakes":
                return self.send_json(HTTPStatus.CREATED, {"project": STORE.capture(name=payload.get("name", ""), purpose=payload.get("purpose", ""), slug=payload.get("slug") or None, kind=payload.get("kind", "project"))})
            if route.startswith("/api/intakes/") and route.endswith("/provision"):
                project_id = route.removeprefix("/api/intakes/").removesuffix("/provision").strip("/")
                return self.send_json(HTTPStatus.OK, STORE.provision(project_id=project_id, confirmation=payload.get("confirmation", ""), create_github=payload.get("createGithub", True)))
            self.send_error(HTTPStatus.NOT_FOUND)
        except (IntakeError, ValueError, json.JSONDecodeError) as exc:
            self.send_json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        except Exception as exc:
            print(f"[intake] unexpected error: {exc}", file=sys.stderr)
            self.send_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Provisioning encountered an unexpected error; inspect the intake record before retrying."})


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 8787), IntakeHandler)
    print("MasterIndex Project Intake listening at http://127.0.0.1:8787")
    server.serve_forever()


if __name__ == "__main__":
    main()

"""
Tiny HTTP server to keep the bot alive on Render's free Web Service tier.

Render free Web Services require the process to bind to $PORT, and they spin the
service down after ~15 minutes without inbound HTTP traffic. This module starts a
minimal HTTP endpoint in a background thread so that:
  1. Render's health check passes (an open port exists), and
  2. an external uptime pinger (e.g. UptimeRobot) can hit the URL to prevent sleep.

Uses only the standard library — no extra dependencies.
"""

from __future__ import annotations

import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class _PingHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'Valorant bot is alive')

    def do_HEAD(self) -> None:
        self.send_response(200)
        self.end_headers()

    def log_message(self, *args: object) -> None:  # noqa: ARG002
        """Silence the default per-request access logging."""


def keep_alive() -> None:
    """Start the keep-alive HTTP server in a daemon thread."""
    port = int(os.getenv('PORT', '10000'))
    server = HTTPServer(('0.0.0.0', port), _PingHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print(f'[keep_alive] HTTP server listening on :{port}')

#!/usr/bin/env python3
"""
Simple HTTP server to preview the Windcave Terminal Simulator
Run this file and open http://localhost:8080 in your browser
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8080
DIRECTORY = Path(__file__).parent / "simulator"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def log_message(self, format, *args):
        # Cleaner logging
        print(f"  {args[0]}")

def main():
    os.chdir(DIRECTORY)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print()
        print("=" * 60)
        print("  WINDCAVE TERMINAL SIMULATOR")
        print("=" * 60)
        print()
        print(f"  Open in browser: http://localhost:{PORT}")
        print()
        print("  Press Ctrl+C to stop")
        print()
        print("=" * 60)
        print()

        # Open browser automatically
        webbrowser.open(f"http://localhost:{PORT}")

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n  Server stopped.")

if __name__ == "__main__":
    main()

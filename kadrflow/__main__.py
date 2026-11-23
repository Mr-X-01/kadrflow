"""Запуск: python -m kadrflow [--port 8765] [--host 127.0.0.1]"""
from __future__ import annotations

import argparse
import os
import threading
import time
import webbrowser


def _open_when_ready(server, url: str) -> None:
    """Do not open a browser for an occupied port or failed application startup."""
    while not server.started:
        if server.should_exit:
            return
        time.sleep(0.1)
    webbrowser.open(url)


def main() -> None:
    parser = argparse.ArgumentParser(description="KadrFlow")
    parser.add_argument("--host", default=os.environ.get("KADRFLOW_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.environ.get("KADRFLOW_PORT", "8765")))
    parser.add_argument("--reload", action="store_true")
    parser.add_argument("--open-browser", action="store_true", help="Open the local website after server startup")
    args = parser.parse_args()
    os.environ["KADRFLOW_BIND_HOST"] = args.host
    if args.open_browser and args.reload:
        parser.error("--open-browser cannot be combined with --reload")

    import uvicorn

    if args.open_browser:
        config = uvicorn.Config("kadrflow.main:app", host=args.host, port=args.port, log_level="info")
        server = uvicorn.Server(config)
        browser_host = "127.0.0.1" if args.host in ("0.0.0.0", "::") else args.host
        if ":" in browser_host:
            browser_host = f"[{browser_host}]"
        threading.Thread(target=_open_when_ready,
                         args=(server, f"http://{browser_host}:{args.port}/"), daemon=True).start()
        server.run()
        return

    uvicorn.run("kadrflow.main:app", host=args.host, port=args.port, reload=args.reload,
                log_level="info")


if __name__ == "__main__":
    main()

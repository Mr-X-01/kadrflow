"""Browser request boundary for the local HTTP API."""
from __future__ import annotations

import ipaddress
import os
from urllib.parse import urlsplit


def _host_name(value: str) -> str | None:
    """Return a validated Host name, excluding ports and userinfo."""
    if not value or any(c in value for c in "/\\@, \t\r\n"):
        return None
    try:
        parsed = urlsplit("//" + value)
        if parsed.path or parsed.query or parsed.fragment:
            return None
        _ = parsed.port  # Reject malformed ports.
        return parsed.hostname.lower().rstrip(".") if parsed.hostname else None
    except ValueError:
        return None


def _allowed_host(name: str) -> bool:
    if name == "localhost":
        return True
    try:
        address = ipaddress.ip_address(name)
        bind = os.environ.get("KADRFLOW_BIND_HOST", "127.0.0.1")
        return address.is_loopback or bind in ("0.0.0.0", "::") or name == bind
    except ValueError:
        pass
    allowed = {h.strip().lower().rstrip(".") for h in
               os.environ.get("KADRFLOW_ALLOWED_HOSTS", "").split(",") if h.strip()}
    bind = os.environ.get("KADRFLOW_BIND_HOST", "127.0.0.1").lower().rstrip(".")
    return name in allowed or (bind not in ("0.0.0.0", "::") and name == bind)


def trusted_request(host: str, origin: str | None, method: str,
                    fetch_site: str | None = None, scheme: str = "http") -> bool:
    """Reject DNS rebinding and browser requests from another origin."""
    name = _host_name(host)
    if name is None or not _allowed_host(name):
        return False
    if origin:
        try:
            parsed = urlsplit(origin)
            target = urlsplit("//" + host)
            if (parsed.scheme != scheme or parsed.username or
                    parsed.password or parsed.path or parsed.query or parsed.fragment or
                    parsed.hostname != target.hostname or parsed.port != target.port):
                return False
        except ValueError:
            return False
    elif method.upper() not in ("GET", "HEAD", "OPTIONS") and fetch_site in ("cross-site", "same-site"):
        return False
    return True

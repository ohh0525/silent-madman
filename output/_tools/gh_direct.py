#!/usr/bin/env python3
"""HTTPS to GitHub over a hand-picked IP, with retry against network flakiness.

On this machine `github.com` resolves to 20.205.243.166, which times out, while
other GitHub IPs answer in well under a second. Worse, the block comes and goes
on a minute timescale, so a single attempt is a coin flip.

This module connects directly to a caller-supplied IP while keeping SNI/Host as
github.com, and retries across the IP pool until one request succeeds. Used for
endpoints that only exist on github.com (the OAuth device flow), since
api.github.com is reachable normally.
"""
from __future__ import annotations

import http.client
import json
import random
import socket
import ssl
import time

CONTEXT = ssl.create_default_context()

# GitHub edge IPs measured reachable from this machine (fastest first).
GITHUB_IPS = [
    "20.200.245.247",
    "20.205.243.165",
    "140.82.116.3",
    "20.207.73.82",
    "140.82.112.3",
    "140.82.112.4",
    "140.82.113.3",
    "140.82.113.4",
    "140.82.114.4",
    "4.237.22.38",
    "20.205.243.168",
    "20.27.177.113",
    "20.201.28.151",
    "20.233.83.145",
    "20.26.156.215",
    "20.175.192.147",
]


class GitHubUnreachable(RuntimeError):
    pass


def _once(ip: str, method: str, path: str, host: str, body: bytes | None,
          headers: dict[str, str], timeout: float) -> tuple[int, bytes]:
    """Single attempt: connect to `ip`, speak TLS as `host`."""
    raw = socket.create_connection((ip, 443), timeout)
    try:
        tls = CONTEXT.wrap_socket(raw, server_hostname=host)
        conn = http.client.HTTPSConnection(host, timeout=timeout)
        conn.sock = tls
        conn.request(method, path, body=body, headers=headers)
        resp = conn.getresponse()
        data = resp.read()
        status = resp.status
        conn.close()
        return status, data
    finally:
        try:
            raw.close()
        except OSError:
            pass


def request(path: str, method: str = "GET", body: bytes | None = None,
            headers: dict[str, str] | None = None, host: str = "github.com",
            attempts: int = 14, timeout: float = 8.0,
            verbose: bool = True) -> tuple[int, bytes]:
    """Issue a request to github.com, retrying across IPs until it lands.

    Retries are unavoidable here: the same IP that works now may be blackholed
    five seconds later, so we rotate through the pool and shuffle to avoid
    burning all attempts on whichever IP is currently blocked.
    """
    hdrs = {"User-Agent": "Mozilla/5.0", "Accept": "application/json",
            "Host": host}
    hdrs.update(headers or {})

    pool = GITHUB_IPS[:]
    random.shuffle(pool)
    last_err = "no attempt made"

    for i in range(attempts):
        ip = pool[i % len(pool)]
        t0 = time.time()
        try:
            status, data = _once(ip, method, path, host, body, hdrs, timeout)
            if verbose:
                print(f"    attempt {i+1}/{attempts} via {ip}: "
                      f"HTTP {status} in {time.time()-t0:.1f}s")
            return status, data
        except Exception as e:  # noqa: BLE001 - any failure means "try next IP"
            last_err = f"{type(e).__name__}: {str(e)[:60]}"
            if verbose:
                print(f"    attempt {i+1}/{attempts} via {ip}: "
                      f"{type(e).__name__} ({time.time()-t0:.1f}s)")

    raise GitHubUnreachable(f"all {attempts} attempts failed; last error: {last_err}")


def post_form(path: str, fields: dict[str, str], **kw) -> tuple[int, bytes]:
    body = "&".join(f"{k}={v}" for k, v in fields.items()).encode()
    return request(path, method="POST", body=body,
                   headers={"Content-Type": "application/x-www-form-urlencoded",
                            "Accept": "application/json"}, **kw)


if __name__ == "__main__":
    print("探测 github.com 主机的连通性（经直连 IP + 重试）...")
    st, data = request("/login/device/code", method="POST",
                       body=b"client_id=0&scope=repo",
                       headers={"Content-Type": "application/x-www-form-urlencoded"})
    print("HTTP", st)
    print(data[:300].decode("utf-8", "replace"))

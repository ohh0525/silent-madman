#!/usr/bin/env python3
"""Minimal local CONNECT proxy that pins blocked GitHub hosts to reachable IPs.

github.com resolves to 20.205.243.166 on this machine, which is blackholed at the
network layer (TCP timeout), while other GitHub IPs respond in <1s. This proxy
rewrites the DNS target for the affected hosts and relays bytes verbatim, so
ordinary `git push` / OAuth device flow work without touching system DNS or the
hosts file.

Usage:
    python gh_proxy.py [--port 8877] [--host 20.200.245.247]
    git -c http.proxy=http://127.0.0.1:8877 push origin main
"""
from __future__ import annotations

import argparse
import random
import select
import socket
import socketserver
import sys
import threading
import time

# Hosts that need pinning -> candidate IPs (tried in order, first live one wins).
PINNED = {
    "github.com": [
        "20.200.245.247", "20.205.243.165", "140.82.116.3",
        "20.207.73.82", "140.82.112.3", "4.237.22.38",
    ],
    "ssh.github.com": ["20.205.243.165", "20.200.245.247"],
    "codeload.github.com": ["20.205.243.165", "20.200.245.247"],
}

CONNECT_TIMEOUT = 12
_resolved: dict[str, str] = {}
_lock = threading.Lock()
_verbose = True


def log(msg: str) -> None:
    if _verbose:
        sys.stdout.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        sys.stdout.flush()


def pick_ip(host: str) -> str | None:
    """Return a TCP-reachable IP for a pinned host, cached after first success."""
    with _lock:
        if host in _resolved:
            return _resolved[host]
    for ip in PINNED.get(host, []):
        try:
            s = socket.create_connection((ip, 443), 4)
            s.close()
            with _lock:
                _resolved[host] = ip
            log(f"pinned {host} -> {ip}")
            return ip
        except OSError:
            continue
    return None


def resolve(host: str, port: int) -> str:
    """Resolve a target: pinned override when applicable, normal DNS otherwise."""
    if port == 443 and host in PINNED:
        ip = pick_ip(host)
        if ip:
            return ip
        log(f"WARN no reachable pin for {host}, falling back to DNS")
    return host


def connect_upstream(host: str, port: int) -> tuple[socket.socket, str]:
    """Open a connection to the real origin, rotating IPs until one accepts.

    Blocking here is per-connection and unpredictable: an IP that answered a
    second ago may be blackholed for the next attempt. So every single connection
    walks the candidate pool rather than trusting a cached "good" IP.
    """
    if port == 443 and host in PINNED:
        candidates = PINNED[host]
        start = random.randrange(len(candidates))
        ordered = candidates[start:] + candidates[:start]
    else:
        ordered = [host]

    last_err: Exception | None = None
    for ip in ordered:
        try:
            sock = socket.create_connection((ip, port), 6)
            with _lock:
                _resolved[host] = ip
            return sock, ip
        except OSError as e:
            last_err = e
            continue
    raise last_err or OSError(f"no route to {host}:{port}")


def relay(a: socket.socket, b: socket.socket) -> None:
    """Pump bytes both ways until either side closes."""
    socks = [a, b]
    try:
        while True:
            readable, _, errored = select.select(socks, [], socks, 30)
            if errored:
                break
            if not readable:
                continue
            for src in readable:
                dst = b if src is a else a
                try:
                    data = src.recv(65536)
                except OSError:
                    return
                if not data:
                    return
                try:
                    dst.sendall(data)
                except OSError:
                    return
    finally:
        for s in (a, b):
            try:
                s.close()
            except OSError:
                pass


class Handler(socketserver.BaseRequestHandler):
    def handle(self) -> None:
        client = self.request
        client.settimeout(30)
        try:
            head = b""
            while b"\r\n\r\n" not in head:
                chunk = client.recv(4096)
                if not chunk:
                    return
                head += chunk
                if len(head) > 65536:
                    return

            first_line = head.split(b"\r\n", 1)[0].decode("latin-1")
            parts = first_line.split()
            if len(parts) < 3:
                return
            method, target, _version = parts[0], parts[1], parts[2]

            if method.upper() == "CONNECT":
                host, _, port_s = target.partition(":")
                port = int(port_s or 443)

                if host in ("127.0.0.1", "localhost"):
                    return  # never proxy to ourselves

                upstream, ip = connect_upstream(host, port)
                client.sendall(b"HTTP/1.1 200 Connection Established\r\n\r\n")
                log(f"CONNECT {host}:{port} -> {ip}")
                leftover = head.split(b"\r\n\r\n", 1)[1]
                if leftover:
                    upstream.sendall(leftover)
                relay(client, upstream)
            else:
                # Plain HTTP: forward verbatim to the resolved origin.
                host = ""
                for line in head.split(b"\r\n"):
                    if line.lower().startswith(b"host:"):
                        host = line.split(b":", 1)[1].strip().decode("latin-1")
                        break
                if not host:
                    return
                ip = resolve(host, 80)
                upstream = socket.create_connection((ip, 80), CONNECT_TIMEOUT)
                upstream.sendall(head)
                relay(client, upstream)
        except OSError:
            pass
        finally:
            try:
                client.close()
            except OSError:
                pass


class Server(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8877)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    global _verbose
    _verbose = not args.quiet

    with Server((args.host, args.port), Handler) as srv:
        log(f"listening on http://{args.host}:{args.port}  (pinned: {', '.join(PINNED)})")
        try:
            srv.serve_forever()
        except KeyboardInterrupt:
            log("shutting down")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

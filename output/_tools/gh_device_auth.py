#!/usr/bin/env python3
"""Complete a GitHub OAuth device-flow login and store the token for git.

Polls github.com/login/oauth/access_token until the user approves the code in a
browser, then writes the resulting access token straight into ~/.git-credentials
in git's `store` format. The token is never printed to stdout or the terminal.

Run with a device code obtained from gh_direct.post_form("/login/device/code").
"""
from __future__ import annotations

import argparse
import base64
import json
import pathlib
import sys
import time

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gh_direct import GitHubUnreachable, post_form  # noqa: E402

CLIENT_ID = "178c6fc778ccc68e1d6a"  # GitHub CLI's public OAuth client id


def poll(device_code: str, deadline_s: float, interval: int, username: str) -> str | None:
    """Poll until approved, expired, or out of time. Returns token or None."""
    started = time.time()
    delay = interval
    round_no = 0

    while time.time() - started < deadline_s:
        round_no += 1
        elapsed = int(time.time() - started)
        try:
            status, data = post_form(
                "/login/oauth/access_token",
                {
                    "client_id": CLIENT_ID,
                    "device_code": device_code,
                    "grant_type": "urn:ietf:params:oauth:grant-type:device_code",
                },
                attempts=5,           # keep each round short so polling stays live
                timeout=6.0,
                verbose=False,
            )
            payload = json.loads(data.decode("utf-8", "replace"))
        except GitHubUnreachable:
            print(f"[{elapsed:4d}s] 本轮网络不通，稍后重试")
            time.sleep(delay)
            continue
        except Exception as e:  # noqa: BLE001
            print(f"[{elapsed:4d}s] 响应解析失败: {type(e).__name__}")
            time.sleep(delay)
            continue

        err = payload.get("error")
        if "access_token" in payload:
            return payload["access_token"]
        if err == "authorization_pending":
            if round_no % 6 == 1:
                print(f"[{elapsed:4d}s] 等待你在浏览器里授权…")
        elif err == "slow_down":
            delay += 5
            print(f"[{elapsed:4d}s] 服务端要求放慢，间隔调整为 {delay}s")
        elif err == "expired_token":
            print(f"[{elapsed:4d}s] 授权码已过期")
            return None
        elif err == "access_denied":
            print(f"[{elapsed:4d}s] 你取消了授权")
            return None
        else:
            print(f"[{elapsed:4d}s] 未预期响应: {json.dumps(payload, ensure_ascii=False)[:120]}")

        time.sleep(delay)

    return None


def store_token(username: str, token: str) -> pathlib.Path:
    """Write ~/.git-credentials in git-store format, without echoing the secret."""
    path = pathlib.Path.home() / ".git-credentials"
    line = f"https://{username}:{token}@github.com\n"
    path.write_text(line, encoding="utf-8")
    try:
        path.chmod(0o600)
    except OSError:
        pass
    return path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--device-code", required=True)
    ap.add_argument("--username", default="ohh0525")
    ap.add_argument("--interval", type=int, default=5)
    ap.add_argument("--timeout", type=float, default=840)
    args = ap.parse_args()

    print("开始轮询授权状态（token 不会打印到屏幕）…")
    token = poll(args.device_code, args.timeout, args.interval, args.username)
    if not token:
        print("RESULT=FAILED")
        return 1

    path = store_token(args.username, token)
    print(f"RESULT=OK 已写入 {path}")
    print(f"token 长度 {len(token)}，前缀 {token[:4]}…（已隐藏）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

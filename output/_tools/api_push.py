#!/usr/bin/env python3
"""Push local commits to GitHub via the REST Git Data API.

Why not `git push`: on this machine github.com resolves to a blackholed IP,
TCP connections to it succeed only ~1 attempt in 10, and even when the CONNECT
succeeds the git protocol stream stalls or gets reset. api.github.com, by
contrast, answered 5/5 probes in under 1.2s.

The Git Data API is what a push does under the hood, so replicating it here
reproduces the same history: for each local commit we upload the changed blobs,
build a tree on top of the previous one, create a commit with the original
author/committer/message, and advance the branch ref.

The token is read from ~/.git-credentials inside this process and never printed.
State is checkpointed after every commit, so a failure mid-way is resumable by
simply re-running the script.
"""
from __future__ import annotations

import base64
import json
import pathlib
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

REPO_DIR = pathlib.Path(r"D:\桌面\silent-madman")
OWNER_REPO = "ohh0525/silent-madman"
API = f"https://api.github.com/repos/{OWNER_REPO}"
BRANCH = "main"
BASE_COMMIT = "fdfe09321d5982626ddeb0790c07b1c62f06f4e8"
STATE_FILE = pathlib.Path(__file__).parent / ".api_push_state.json"

RETRIES = 4


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def load_token() -> str:
    """Read the OAuth token straight out of the git credential store."""
    raw = (pathlib.Path.home() / ".git-credentials").read_text(encoding="utf-8").strip()
    m = re.match(r"^https://([^:]+):(.+)@github\.com$", raw)
    if not m:
        raise SystemExit("无法解析 ~/.git-credentials")
    return m.group(2)


TOKEN = load_token()


def api(method: str, path: str, payload: dict | None = None) -> dict:
    """Call the GitHub API with retries; never logs headers or the token."""
    url = path if path.startswith("http") else API + path
    body = json.dumps(payload).encode() if payload is not None else None
    last = None

    for attempt in range(1, RETRIES + 1):
        req = urllib.request.Request(url, data=body, method=method, headers={
            "Authorization": f"Bearer {TOKEN}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "silent-madman-push",
            "Content-Type": "application/json",
        })
        try:
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read() or b"{}")
        except urllib.error.HTTPError as e:
            detail = e.read().decode("utf-8", "replace")[:300]
            # 4xx (except rate limiting) will not fix themselves on retry
            if 400 <= e.code < 500 and e.code != 429:
                raise SystemExit(f"HTTP {e.code} on {method} {url}\n{detail}")
            last = f"HTTP {e.code}: {detail}"
        except Exception as e:  # noqa: BLE001 - transient network
            last = f"{type(e).__name__}: {str(e)[:120]}"

        wait = 2 ** attempt
        print(f"      retry {attempt}/{RETRIES} in {wait}s ({last})")
        time.sleep(wait)

    raise SystemExit(f"API 调用反复失败: {method} {url}\n{last}")


def git(*args: str) -> bytes:
    r = subprocess.run(["git", *args], cwd=REPO_DIR,
                       capture_output=True, check=False)
    if r.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} 失败:\n{r.stderr.decode('utf-8','replace')}")
    return r.stdout


def parse_raw_diff(parent: str, commit: str) -> list[tuple[str, str, str, str]]:
    """Return (status, mode, blob_sha, path) for every change in `commit`.

    Uses -z + core.quotePath=false so non-ASCII paths (this repo has Chinese
    filenames) come through as literal UTF-8 instead of octal escapes.
    """
    out = git("-c", "core.quotePath=false", "diff-tree", "-r", "--no-commit-id",
              "--raw", "-z", parent, commit)
    parts = out.decode("utf-8").split("\0")
    changes = []
    i = 0
    while i < len(parts):
        head = parts[i]
        if head.startswith(":"):
            fields = head[1:].split()
            old_mode, new_mode, _old_sha, new_sha, status = fields[:5]
            path = parts[i + 1] if i + 1 < len(parts) else ""
            mode = new_mode if status[0] != "D" else old_mode
            changes.append((status[0], mode, new_sha, path))
            i += 2
        else:
            i += 1
    return changes


def commit_meta(sha: str) -> dict:
    fmt = "%an%x00%ae%x00%aI%x00%cn%x00%ce%x00%cI%x00%B"
    an, ae, ad, cn, ce, cd, msg = git("log", "-1", f"--format={fmt}", sha
                                      ).decode("utf-8").split("\0", 6)
    return {
        "message": msg.rstrip("\n"),
        "author": {"name": an, "email": ae, "date": ad},
        "committer": {"name": cn, "email": ce, "date": cd},
    }


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main() -> int:
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    blob_cache: dict[str, str] = state.get("blob_cache", {})
    pushed: dict[str, str] = state.get("pushed", {})   # local sha -> remote sha

    local_commits = git("rev-list", "--reverse", f"{BASE_COMMIT}..HEAD"
                        ).decode().split()
    print(f"待推送提交: {len(local_commits)} 个")

    # Verify the remote base actually matches our local base, so we never
    # build on a tree that has moved underneath us.
    remote_base = api("GET", f"/git/commits/{BASE_COMMIT}")
    local_base_tree = git("rev-parse", f"{BASE_COMMIT}^{{tree}}").decode().strip()
    if remote_base["tree"]["sha"] != local_base_tree:
        raise SystemExit("远端基线与本地不一致，先 git fetch 再重试")

    parent_remote = BASE_COMMIT
    parent_tree = remote_base["tree"]["sha"]

    for idx, csha in enumerate(local_commits, 1):
        subject = git("log", "-1", "--format=%s", csha).decode().strip()

        if csha in pushed:
            print(f"[{idx}/{len(local_commits)}] 已推送，跳过  {csha[:8]} {subject[:40]}")
            parent_remote = pushed[csha]
            parent_tree = api("GET", f"/git/commits/{parent_remote}")["tree"]["sha"]
            continue

        local_parent = git("rev-parse", f"{csha}^").decode().strip()
        changes = parse_raw_diff(local_parent, csha)
        print(f"[{idx}/{len(local_commits)}] {csha[:8]} {subject[:44]}")
        print(f"      变更 {len(changes)} 个文件")

        tree_entries = []
        for status, mode, blob_sha, path in changes:
            if status == "D":
                # sha=None removes the path from the tree
                tree_entries.append({"path": path, "mode": mode,
                                     "type": "blob", "sha": None})
                print(f"      - 删除 {path}")
                continue

            if blob_sha in blob_cache:
                remote_blob = blob_cache[blob_sha]
            else:
                content = git("cat-file", "blob", blob_sha)
                remote_blob = api("POST", "/git/blobs", {
                    "content": base64.b64encode(content).decode(),
                    "encoding": "base64",
                })["sha"]
                blob_cache[blob_sha] = remote_blob
                print(f"      + {path}  ({len(content):,} B)")

            tree_entries.append({"path": path, "mode": mode,
                                 "type": "blob", "sha": remote_blob})

        new_tree = api("POST", "/git/trees", {
            "base_tree": parent_tree,
            "tree": tree_entries,
        })["sha"]

        meta = commit_meta(csha)
        new_commit = api("POST", "/git/commits", {
            "message": meta["message"],
            "tree": new_tree,
            "parents": [parent_remote],
            "author": meta["author"],
            "committer": meta["committer"],
        })["sha"]

        # Advance the branch immediately so progress survives a later failure.
        api("PATCH", f"/git/refs/heads/{BRANCH}", {"sha": new_commit, "force": False})

        pushed[csha] = new_commit
        parent_remote, parent_tree = new_commit, new_tree
        print(f"      -> 远端 {new_commit[:8]}  分支已前进")

        STATE_FILE.write_text(json.dumps(
            {"blob_cache": blob_cache, "pushed": pushed}, indent=1))

    head_remote = api("GET", f"/git/ref/heads/{BRANCH}")["object"]["sha"]
    print()
    print(f"完成。远端 {BRANCH} = {head_remote}")
    local_head = git("rev-parse", "HEAD").decode().strip()
    status = git("status", "--short").decode().strip()
    print(f"本地 HEAD      = {local_head}")
    print(f"本地主提交一致 = {head_remote == local_head}")
    print(f"本地未提交改动 = {'无' if not status else status}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

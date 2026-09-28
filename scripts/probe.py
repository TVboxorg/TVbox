#!/usr/bin/env python3
"""Probe TVBox interface URLs from sources.yaml."""
from __future__ import annotations

import json
import re
import ssl
import sys
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources.yaml"
OUT = ROOT / "dist" / "probe.json"
TIMEOUT = 12
UA = "TVboxorg-TVbox-probe/1.0 (+https://www.tvbox.org/; +https://github.com/TVboxorg/TVbox)"


def load_sources(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    items: list[dict] = []
    cur: dict | None = None
    for line in text.splitlines():
        if line.startswith("  - id:"):
            if cur:
                items.append(cur)
            cur = {"id": line.split(":", 1)[1].strip().strip('"'), "enabled": True}
            continue
        if cur is None or not line.startswith("    "):
            continue
        m = re.match(r"\s+(\w+):\s*(.*)$", line)
        if not m:
            continue
        key, val = m.group(1), m.group(2).strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1].replace('\\"', '"')
        if key == "enabled":
            cur[key] = val.lower() == "true"
        else:
            cur[key] = val
    if cur:
        items.append(cur)
    return items


def looks_like_config(body: bytes, content_type: str) -> str:
    sample = body[:8000].lstrip()
    ct = (content_type or "").lower()
    text = sample.decode("utf-8", errors="replace")
    if "json" in ct or text.startswith("{") or text.startswith("["):
        if re.search(r'"(sites|lives|spider|parses|wallpaper)"\s*:', text):
            return "ok"
        if text.startswith("{") or text.startswith("["):
            return "json"
        return "suspect"
    if "http" in text[:200] and (".json" in text or "sites" in text):
        return "text"
    return "suspect"


def probe_one(url: str) -> dict:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            raw = resp.read(65536)
            ms = int((time.time() - t0) * 1000)
            kind = looks_like_config(raw, resp.headers.get("Content-Type", ""))
            code = getattr(resp, "status", None) or resp.getcode()
            return {
                "ok": 200 <= int(code) < 400 and kind in ("ok", "json", "text"),
                "status": int(code),
                "ms": ms,
                "kind": kind,
                "error": "",
            }
    except Exception as e:
        ms = int((time.time() - t0) * 1000)
        return {
            "ok": False,
            "status": 0,
            "ms": ms,
            "kind": "error",
            "error": f"{type(e).__name__}: {e}"[:200],
        }


def main() -> int:
    sources = [s for s in load_sources(SOURCES) if s.get("enabled", True)]
    results = []
    for i, src in enumerate(sources, 1):
        print(f"[{i}/{len(sources)}] {src.get('name')} ...", flush=True)
        r = probe_one(src["url"])
        results.append(
            {
                "id": src["id"],
                "name": src.get("name", ""),
                "group": src.get("group", ""),
                "url": src["url"],
                "desc": src.get("desc", ""),
                **r,
            }
        )
        print(f"  -> ok={r['ok']} status={r['status']} {r['ms']}ms {r['kind']}", flush=True)

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "homepage": "https://www.tvbox.org/",
        "repo": "https://github.com/TVboxorg/TVbox",
        "count": len(results),
        "up": sum(1 for x in results if x["ok"]),
        "items": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {OUT} up={payload['up']}/{payload['count']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

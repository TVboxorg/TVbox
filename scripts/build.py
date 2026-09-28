#!/usr/bin/env python3
"""Build dist/list.json, dist/tvbox.json, dist/status.md from probe results."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "dist" / "probe.json"
DIST = ROOT / "dist"


def main() -> int:
    if not PROBE.is_file():
        print("missing dist/probe.json — run scripts/probe.py first", file=sys.stderr)
        return 1
    data = json.loads(PROBE.read_text(encoding="utf-8"))
    items = data.get("items") or []
    up_items = [x for x in items if x.get("ok")]
    pref_up = [x for x in up_items if x.get("group") == "pref"]
    back_up = [x for x in up_items if x.get("group") != "pref"]

    list_payload = {
        "name": "TVboxorg/TVbox",
        "homepage": "https://www.tvbox.org/",
        "repo": "https://github.com/TVboxorg/TVbox",
        "generated_at": data.get("generated_at")
        or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "summary": {
            "total": len(items),
            "up": len(up_items),
            "down": len(items) - len(up_items),
        },
        "items": items,
    }
    (DIST / "list.json").write_text(
        json.dumps(list_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    # TVBox-friendly flat list: prefer working pref, then working back
    ordered = pref_up + back_up
    if not ordered:
        ordered = items  # fallback all
    tvbox_payload = {
        "urls": [
            {
                "url": x["url"],
                "name": x.get("name") or x["url"],
            }
            for x in ordered
        ],
        "homepage": "https://www.tvbox.org/",
        "generated_at": list_payload["generated_at"],
    }
    (DIST / "tvbox.json").write_text(
        json.dumps(tvbox_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# 接口探测状态",
        "",
        f"- 官网：https://www.tvbox.org/",
        f"- 仓库：https://github.com/TVboxorg/TVbox",
        f"- 生成时间（UTC）：`{list_payload['generated_at']}`",
        f"- 可用：**{len(up_items)}** / {len(items)}",
        "",
        "| 状态 | 分组 | 名称 | 耗时 | 说明 |",
        "| --- | --- | --- | --- | --- |",
    ]
    for x in items:
        mark = "UP" if x.get("ok") else "DOWN"
        ms = x.get("ms", 0)
        desc = (x.get("desc") or x.get("error") or x.get("kind") or "").replace("|", "/")
        name = (x.get("name") or "").replace("|", "/")
        lines.append(
            f"| {mark} | {x.get('group','')} | {name} | {ms}ms | {desc[:60]} |"
        )
    lines.append("")
    (DIST / "status.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"built list.json tvbox.json status.md (up={len(up_items)}/{len(items)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

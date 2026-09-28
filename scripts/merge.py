#!/usr/bin/env python3
"""Merge working upstream TVBox configs into one pasteable official.json."""
from __future__ import annotations

import json
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "dist" / "probe.json"
OUT = ROOT / "dist" / "official.json"
META = ROOT / "dist" / "merge-meta.json"
TIMEOUT = 18
UA = "TVboxorg-TVbox-merge/1.0 (+https://www.tvbox.org/; +https://github.com/TVboxorg/TVbox)"
MAX_SITES = 160
MAX_SOURCES = 12  # fetch budget: pref first, then back


def strip_json_noise(text: str) -> str:
    """Strip // and /* */ comments outside strings; tolerate trailing commas."""
    out: list[str] = []
    i = 0
    n = len(text)
    in_str = False
    esc = False
    while i < n:
        ch = text[i]
        if in_str:
            out.append(ch)
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            i += 1
            continue
        if ch == '"':
            in_str = True
            out.append(ch)
            i += 1
            continue
        if ch == "/" and i + 1 < n:
            nxt = text[i + 1]
            if nxt == "/":
                i += 2
                while i < n and text[i] not in "\r\n":
                    i += 1
                continue
            if nxt == "*":
                i += 2
                while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                    i += 1
                i = min(i + 2, n)
                continue
        out.append(ch)
        i += 1
    cleaned = "".join(out)
    cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
    return cleaned


def fetch(url: str) -> bytes:
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
        return resp.read(2_000_000)


def parse_config(raw: bytes) -> dict[str, Any] | None:
    text = raw.decode("utf-8", errors="replace").lstrip("\ufeff").strip()
    if not text:
        return None
    for candidate in (text, strip_json_noise(text)):
        try:
            data = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict) and (
            "sites" in data or "lives" in data or "spider" in data
        ):
            return data
    return None


def abs_url(base: str, value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if value.startswith("./") or value.startswith("../") or value.startswith("/"):
        return urllib.parse.urljoin(base, value)
    # jar;md5 or jar;md5;key style — take first segment if looks like path
    first = value.split(";")[0].strip()
    if first.startswith("http://") or first.startswith("https://"):
        return value  # keep full spider string with md5
    if first.startswith("./") or first.startswith("/"):
        joined = urllib.parse.urljoin(base, first)
        rest = value[len(first) :]
        return joined + rest
    return value


def spider_http(spider: str) -> str:
    """Extract http(s) jar URL from spider field (may include ;md5)."""
    if not spider:
        return ""
    first = spider.split(";")[0].strip()
    if first.startswith("http://") or first.startswith("https://"):
        return first
    return ""


def is_http_api(api: Any) -> bool:
    if not isinstance(api, str):
        return False
    api = api.strip()
    return api.startswith("http://") or api.startswith("https://")


def site_score(site: dict[str, Any], group: str, from_primary: bool) -> int:
    score = 0
    if from_primary:
        score += 40
    if group == "pref":
        score += 20
    name = str(site.get("name") or "")
    api = str(site.get("api") or "")
    stype = site.get("type")
    if site.get("searchable") in (1, True, "1"):
        score += 8
    if site.get("quickSearch") in (1, True, "1"):
        score += 4
    if stype in (1, 4):
        score += 15  # portable CMS
    if stype == 3 and site.get("jar"):
        score += 6
    low = name.lower()
    for token, pts in (
        ("4k", 10),
        ("高清", 6),
        ("蓝光", 6),
        ("官", 3),
        ("推荐", 3),
        ("vip", 2),
    ):
        if token in low or token in name:
            score += pts
    # deprioritize adult / noisy markers lightly (still include if space)
    for bad in ("伦理", "福利", "色情", "成人"):
        if bad in name:
            score -= 30
    if is_http_api(api):
        score += 5
    return score


def normalize_key(raw: str, source_id: str) -> str:
    key = re.sub(r"[^\w\u4e00-\u9fff\-]+", "_", raw or "site")
    key = key.strip("_")[:40] or "site"
    return f"tv_{source_id}_{key}"


def adapt_site(
    site: dict[str, Any],
    *,
    source_id: str,
    source_name: str,
    spider: str,
    primary: bool,
) -> dict[str, Any] | None:
    if not isinstance(site, dict):
        return None
    api = site.get("api")
    stype = site.get("type")
    try:
        stype_i = int(stype) if stype is not None else -1
    except (TypeError, ValueError):
        stype_i = -1

    out = dict(site)
    out["type"] = stype_i if stype_i >= 0 else stype

    if primary:
        # keep original key/name; still ensure key uniqueness handled later
        return out

    # Non-primary: only keep mergeable sites
    jar = spider_http(spider)
    if stype_i in (0, 1, 4) and is_http_api(api):
        pass
    elif stype_i == 3 and jar and isinstance(api, str) and api.startswith("csp_"):
        out["jar"] = jar
    else:
        return None

    orig_key = str(site.get("key") or site.get("name") or "site")
    out["key"] = normalize_key(orig_key, source_id)
    name = str(site.get("name") or orig_key)
    tag = source_name[:8]
    if tag and tag not in name:
        out["name"] = f"{name}·{tag}"
    return out


def merge_list(dst: list, src: list, keyfn) -> None:
    seen = {keyfn(x) for x in dst if isinstance(x, dict)}
    for item in src:
        if not isinstance(item, dict):
            continue
        k = keyfn(item)
        if not k or k in seen:
            continue
        seen.add(k)
        dst.append(item)


def pick_sources(items: list[dict]) -> list[dict]:
    up = [x for x in items if x.get("ok")]
    pref = [x for x in up if x.get("group") == "pref"]
    back = [x for x in up if x.get("group") != "pref"]
    ordered = pref + back
    return ordered[:MAX_SOURCES]


def main() -> int:
    if not PROBE.is_file():
        print("missing dist/probe.json — run scripts/probe.py first", file=sys.stderr)
        return 1

    probe = json.loads(PROBE.read_text(encoding="utf-8"))
    sources = pick_sources(probe.get("items") or [])
    if not sources:
        print("no UP sources to merge", file=sys.stderr)
        return 1

    fetched: list[dict[str, Any]] = []
    for i, src in enumerate(sources, 1):
        name = src.get("name") or src.get("id")
        url = src["url"]
        print(f"[{i}/{len(sources)}] fetch {name} ...", flush=True)
        try:
            raw = fetch(url)
            cfg = parse_config(raw)
            if not cfg:
                print("  -> skip (parse fail)", flush=True)
                continue
            spider = abs_url(url, str(cfg.get("spider") or ""))
            sites = cfg.get("sites") if isinstance(cfg.get("sites"), list) else []
            print(f"  -> sites={len(sites)} spider={spider[:60]!r}", flush=True)
            fetched.append(
                {
                    "src": src,
                    "cfg": cfg,
                    "spider": spider,
                    "base": url,
                    "site_count": len(sites),
                }
            )
        except Exception as e:
            print(f"  -> err {type(e).__name__}: {e}", flush=True)

    if not fetched:
        print("no configs fetched", file=sys.stderr)
        return 1

    # Primary: prefer pref with most sites and http spider
    def primary_rank(row: dict) -> tuple:
        src = row["src"]
        has_jar = 1 if spider_http(row["spider"]) else 0
        pref = 1 if src.get("group") == "pref" else 0
        return (pref, has_jar, row["site_count"])

    fetched.sort(key=primary_rank, reverse=True)
    primary = fetched[0]
    primary_id = str(primary["src"].get("id") or "primary")

    sites_scored: list[tuple[int, dict]] = []
    parses: list = []
    lives: list = []
    rules: list = []
    flags: list = []
    ads: list = []
    doh: list = []

    meta_sources = []

    for idx, row in enumerate(fetched):
        src = row["src"]
        cfg = row["cfg"]
        is_primary = idx == 0
        sid = str(src.get("id") or f"s{idx}")
        sname = str(src.get("name") or sid)
        spider = row["spider"]
        added = 0
        skipped = 0
        for site in cfg.get("sites") or []:
            adapted = adapt_site(
                site,
                source_id=sid,
                source_name=sname,
                spider=spider,
                primary=is_primary,
            )
            if not adapted:
                skipped += 1
                continue
            score = site_score(adapted, str(src.get("group") or ""), is_primary)
            sites_scored.append((score, adapted))
            added += 1

        if isinstance(cfg.get("parses"), list):
            merge_list(parses, cfg["parses"], lambda x: str(x.get("url") or x.get("name") or ""))
        if isinstance(cfg.get("lives"), list):
            # absolutize common url fields
            fixed = []
            for live in cfg["lives"]:
                if not isinstance(live, dict):
                    continue
                live = dict(live)
                for field in ("url", "epg", "logo"):
                    if isinstance(live.get(field), str):
                        live[field] = abs_url(row["base"], live[field]) or live[field]
                fixed.append(live)
            merge_list(lives, fixed, lambda x: str(x.get("url") or x.get("name") or ""))
        if is_primary:
            if isinstance(cfg.get("rules"), list):
                rules = list(cfg["rules"])
            if isinstance(cfg.get("flags"), list):
                flags = list(cfg["flags"])
            if isinstance(cfg.get("ads"), list):
                ads = list(cfg["ads"])
            if isinstance(cfg.get("doh"), list):
                doh = list(cfg["doh"])

        meta_sources.append(
            {
                "id": sid,
                "name": sname,
                "group": src.get("group"),
                "url": src.get("url"),
                "primary": is_primary,
                "sites_added": added,
                "sites_skipped": skipped,
                "spider": spider_http(spider) or spider[:120],
            }
        )

    # Deduplicate sites by api+type or key
    sites_scored.sort(key=lambda x: x[0], reverse=True)
    final_sites: list[dict] = []
    seen_api: set[str] = set()
    seen_key: set[str] = set()
    for score, site in sites_scored:
        key = str(site.get("key") or "")
        api = str(site.get("api") or "")
        stype = str(site.get("type"))
        api_sig = f"{stype}|{api}"
        if key in seen_key:
            continue
        if api and api_sig in seen_api:
            continue
        seen_key.add(key)
        if api:
            seen_api.add(api_sig)
        final_sites.append(site)
        if len(final_sites) >= MAX_SITES:
            break

    # Ensure douban / config helpers stay near top if present
    def pin_rank(site: dict) -> tuple:
        name = str(site.get("name") or "")
        key = str(site.get("key") or "")
        pin = 0
        for token in ("豆瓣", "Douban", "配置", "本地", "预告"):
            if token in name or token in key:
                pin = 1
                break
        return (0 if pin else 1, name)

    # Keep score order mostly; only stable pin known helpers to front among equals — simpler: move 豆瓣 to index 0
    pinned = []
    rest = []
    for s in final_sites:
        n = str(s.get("name") or "") + str(s.get("key") or "")
        if "豆瓣" in n or "Douban" in n:
            pinned.append(s)
        else:
            rest.append(s)
    final_sites = pinned + rest

    pcfg = primary["cfg"]
    official = {
        "spider": primary["spider"] or pcfg.get("spider") or "",
        "wallpaper": pcfg.get("wallpaper") or "",
        "logo": pcfg.get("logo") or "",
        "sites": final_sites,
        "parses": parses,
        "lives": lives,
        "homepage": "https://www.tvbox.org/",
        "warning": "聚合自公开接口，自动筛选；若部分站失效请换多仓或单线路。仅供学习交流。",
    }
    if rules:
        official["rules"] = rules
    if flags:
        official["flags"] = flags
    if ads:
        official["ads"] = ads
    if doh:
        official["doh"] = doh
    # retain headers if primary has them
    if isinstance(pcfg.get("headers"), list):
        official["headers"] = pcfg["headers"]

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(official, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    meta = {
        "generated_at": generated_at,
        "homepage": "https://www.tvbox.org/",
        "repo": "https://github.com/TVboxorg/TVbox",
        "primary": meta_sources[0]["name"] if meta_sources else "",
        "sites": len(final_sites),
        "parses": len(parses),
        "lives": len(lives),
        "sources": meta_sources,
        "subscribe": "https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/official.json",
        "subscribe_cdn": "https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/official.json",
    }
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"wrote {OUT} sites={len(final_sites)} parses={len(parses)} lives={len(lives)} "
        f"primary={meta['primary']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

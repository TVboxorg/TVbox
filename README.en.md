# TVbox — TVBox Interface Index

**Languages:** [简体中文](README.md) | **English** | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

> Website: **[tvbox.org](https://www.tvbox.org/)**  
> Maintained by [TVboxorg](https://github.com/TVboxorg). This repository collects, organizes, and periodically probes available TVBox interface URLs.

## Website

- Home: <https://www.tvbox.org/>
- Interfaces: <https://www.tvbox.org/portal.php>
- Apps & downloads: <https://www.tvbox.org/>

Prefer the official website for apps and guides. This repo focuses on **interface lists and availability probing**.

## Subscribe URLs (paste into TVBox)

| Purpose | URL | Where to paste |
| --- | --- | --- |
| **Merged single config (recommended)** | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/official.json` | Config / Interface |
| Multi-repo list | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/tvbox.json` | Multi-repo / Store |
| Full list + status | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/list.json` | View only |
| Status table | [`dist/status.md`](./dist/status.md) | View only |

`official.json` fetches working public sources and merges `sites` (CMS sources merge directly; CSP sources keep their original `jar` when possible) into one pasteable TVBox config.

If GitHub raw is slow, try mirrors:

```text
https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/official.json
https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/tvbox.json
```

## Repository layout

| Path | Description |
| --- | --- |
| [`sources.yaml`](./sources.yaml) | Manually maintained source list |
| [`dist/`](./dist/) | Probe results & generated subscribe files (CI) |
| [`dist/official.json`](./dist/official.json) | Cross-source merged single config |
| [`scripts/probe.py`](./scripts/probe.py) | Probe script |
| [`scripts/build.py`](./scripts/build.py) | Build list / tvbox / status |
| [`scripts/merge.py`](./scripts/merge.py) | Merge sites → official.json |

## Run locally

```bash
python3 scripts/probe.py
python3 scripts/build.py
python3 scripts/merge.py
```

## Disclaimer

- This repository **only aggregates third-party public interface URLs** and probes connectivity/format. It does **not** host or distribute media content.
- Sources are maintained by third parties; availability changes. Probe results are for reference only.
- Follow local laws and platform terms.
- Apps, tutorials, and community: [https://www.tvbox.org/](https://www.tvbox.org/)

## Contributing

1. Edit `sources.yaml` (`name` / `url` / `group` / `desc`)
2. Open a PR or Issue
3. GitHub Actions probes on a schedule and refreshes `dist/`

## License

Docs and lists are published for indexing purposes. Third-party interfaces remain copyrighted by their authors.

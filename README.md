# TVbox — TVBox 接口汇总

**Languages:** **简体中文** | [English](README.en.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

> 官网：**[tvbox.org](https://www.tvbox.org/)**  
> 本仓库由 [TVboxorg](https://github.com/TVboxorg) 维护，用于收集、整理并定期探测可用的 TVBox 接口地址。

## 官网

- 网站首页：<https://www.tvbox.org/>
- 接口页：<https://www.tvbox.org/portal.php>
- 盒子软件与下载：<https://www.tvbox.org/>
- 静态官网源码：[`docs/index.html`](./docs/index.html)（约 18KB 单文件，无外链字体/脚本）

请优先通过官网获取软件与说明；本仓库专注于**接口清单与可用性探测**。

### 把静态首页发布到网站

`www.tvbox.org` 目前走 Cloudflare，**不会**随本仓库自动更新。可选：

1. **Cloudflare Pages（推荐）**：在仓库 Settings → Secrets 添加 `CLOUDFLARE_API_TOKEN`、`CLOUDFLARE_ACCOUNT_ID`，合并到 `main` 后由 [`.github/workflows/cloudflare-pages.yml`](./.github/workflows/cloudflare-pages.yml) 发布；再在 Cloudflare 把 `www`/`@` 指到该 Pages 项目。
2. **GitHub Pages**：仓库 Settings → Pages 启用 GitHub Actions，合并后由 [`.github/workflows/pages.yml`](./.github/workflows/pages.yml) 发布；自定义域见 [`docs/CNAME`](./docs/CNAME)。
3. **手动**：把 `docs/index.html` 上传覆盖站点根目录首页。

本地预览：

```bash
python3 -m http.server 8080 --directory docs
```



## 订阅地址（可直接填入 TVBox）

| 用途 | 地址 | 填哪里 |
| --- | --- | --- |
| **单仓聚合（推荐直用）** | `https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/official.json` | 「配置地址 / 接口」 |
| 多仓列表 | `https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/tvbox.json` | 「多仓 / 仓库」 |
| 完整列表（含状态） | `https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/list.json` | 仅查看 |
| 可读状态表 | [`dist/status.md`](./dist/status.md) | 仅查看 |

`official.json` 会自动拉取探测可用的公开线路，跨源拼合 `sites`（标准 CMS 源直接合并；CSP 源尽量带上原线路 `jar`），生成一份可粘贴进 TVBox 的配置。

国内默认使用 jsDelivr；若需 GitHub raw：

```text
https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/official.json
https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/tvbox.json
```


## 仓库内容

| 路径 | 说明 |
| --- | --- |
| [`sources.yaml`](./sources.yaml) | 人工维护的接口源（权威数据） |
| [`dist/`](./dist/) | 探测结果与生成的订阅文件（CI 定时更新） |
| [`dist/official.json`](./dist/official.json) | 跨线路聚合的单仓配置 |
| [`scripts/probe.py`](./scripts/probe.py) | 探测脚本 |
| [`scripts/build.py`](./scripts/build.py) | 生成 list / tvbox / status |
| [`scripts/merge.py`](./scripts/merge.py) | 跨线路拼 sites → official.json |

## 本地运行

```bash
python3 scripts/probe.py
python3 scripts/build.py
python3 scripts/merge.py
```

## 说明与免责

- 本仓库**只汇总第三方公开接口 URL**，并做连通性/格式探测，**不托管、不分发**具体影视或直播内容。
- 接口由第三方维护，可用性会变化；探测结果仅供参考。
- 请遵守当地法律法规与平台条款，合理使用。
- 软件下载、教程与社区请访问官网：[https://www.tvbox.org/](https://www.tvbox.org/)

## 贡献

1. 编辑 `sources.yaml` 增删接口（填写 `name` / `url` / `group` / `desc`）
2. 提交 PR，或在本仓库提 Issue
3. Actions 会定时探测并刷新 `dist/`

## License

文档与清单以收集整理为目的公开；第三方接口版权归原作者所有。

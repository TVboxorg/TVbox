# TVbox — TVBox 介面彙總

**Languages:** [简体中文](README.md) | [English](README.en.md) | **繁體中文** | [日本語](README.ja.md) | [한국어](README.ko.md)

> 官網：**[tvbox.org](https://www.tvbox.org/)**  
> 本倉庫由 [TVboxorg](https://github.com/TVboxorg) 維護，用於收集、整理並定期探測可用的 TVBox 介面位址。

## 官網

- 網站首頁：<https://www.tvbox.org/>
- 介面頁：<https://www.tvbox.org/portal.php>
- 盒子軟體與下載：<https://www.tvbox.org/>

請優先透過官網取得軟體與說明；本倉庫專注於**介面清單與可用性探測**。

## 訂閱位址（可直接填入 TVBox）

| 用途 | 位址 | 填哪裡 |
| --- | --- | --- |
| **單倉聚合（建議直用）** | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/official.json` | 「配置位址 / 介面」 |
| 多倉列表 | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/tvbox.json` | 「多倉 / 倉庫」 |
| 完整列表（含狀態） | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/list.json` | 僅查看 |
| 可讀狀態表 | [`dist/status.md`](./dist/status.md) | 僅查看 |

`official.json` 會自動拉取探測可用的公開線路，跨源拼合 `sites`（標準 CMS 源直接合併；CSP 源盡量帶上原線路 `jar`），產生一份可貼進 TVBox 的配置。

若 GitHub raw 較慢，可嘗試鏡像：

```text
https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/official.json
https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/tvbox.json
```

## 倉庫內容

| 路徑 | 說明 |
| --- | --- |
| [`sources.yaml`](./sources.yaml) | 人工維護的介面源 |
| [`dist/`](./dist/) | 探測結果與產生的訂閱檔（CI 定時更新） |
| [`dist/official.json`](./dist/official.json) | 跨線路聚合的單倉配置 |
| [`scripts/probe.py`](./scripts/probe.py) | 探測腳本 |
| [`scripts/build.py`](./scripts/build.py) | 產生 list / tvbox / status |
| [`scripts/merge.py`](./scripts/merge.py) | 跨線路拼 sites → official.json |

## 本機執行

```bash
python3 scripts/probe.py
python3 scripts/build.py
python3 scripts/merge.py
```

## 說明與免責

- 本倉庫**只彙總第三方公開介面 URL**，並做連通性／格式探測，**不託管、不分發**具體影視或直播內容。
- 介面由第三方維護，可用性會變化；探測結果僅供參考。
- 請遵守當地法律法規與平台條款，合理使用。
- 軟體下載、教學與社群請造訪官網：[https://www.tvbox.org/](https://www.tvbox.org/)

## 貢獻

1. 編輯 `sources.yaml` 增刪介面（填寫 `name` / `url` / `group` / `desc`）
2. 提交 PR，或在本倉庫提 Issue
3. Actions 會定時探測並刷新 `dist/`

## License

文件與清單以收集整理為目的公開；第三方介面版權歸原作者所有。

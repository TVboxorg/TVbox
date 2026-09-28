# TVbox — TVBox インターフェース一覧

**Languages:** [简体中文](README.md) | [English](README.en.md) | [繁體中文](README.zh-TW.md) | **日本語** | [한국어](README.ko.md)

> 公式サイト：**[tvbox.org](https://www.tvbox.org/)**  
> [TVboxorg](https://github.com/TVboxorg) が管理。利用可能な TVBox インターフェース URL を収集・整理し、定期的に死活監視します。

## 公式サイト

- ホーム：<https://www.tvbox.org/>
- インターフェース：<https://www.tvbox.org/portal.php>
- アプリ／ダウンロード：<https://www.tvbox.org/>

ソフトや案内は公式サイトを優先してください。本リポジトリは**インターフェース一覧と可用性の検知**に特化しています。

## 購読 URL（TVBox に貼り付け）

| 用途 | URL | 貼り付け先 |
| --- | --- | --- |
| **統合シングル設定（推奨）** | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/official.json` | 設定／インターフェース |
| マルチリポジトリ一覧 | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/tvbox.json` | マルチ倉庫 |
| 完全一覧＋状態 | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/list.json` | 閲覧のみ |
| 状態表 | [`dist/status.md`](./dist/status.md) | 閲覧のみ |

`official.json` は稼働中の公開ソースを取得し、`sites` を横断マージします（CMS はそのまま、CSP は可能な限り元の `jar` を付与）。

GitHub raw が遅い場合はミラーを試してください：

```text
https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/official.json
https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/tvbox.json
```

## リポジトリ構成

| パス | 説明 |
| --- | --- |
| [`sources.yaml`](./sources.yaml) | 手動管理のソース一覧 |
| [`dist/`](./dist/) | 検知結果と生成ファイル（CI） |
| [`dist/official.json`](./dist/official.json) | 横断統合シングル設定 |
| [`scripts/probe.py`](./scripts/probe.py) | 検知スクリプト |
| [`scripts/build.py`](./scripts/build.py) | list / tvbox / status 生成 |
| [`scripts/merge.py`](./scripts/merge.py) | sites 統合 → official.json |

## ローカル実行

```bash
python3 scripts/probe.py
python3 scripts/build.py
python3 scripts/merge.py
```

## 免責事項

- 本リポジトリは**第三者の公開インターフェース URL の集約と疎通／形式検知のみ**を行い、映像・配信コンテンツ自体は**ホスト／配布しません**。
- ソースは第三者が管理し、可用性は変動します。検知結果は参考情報です。
- 現地の法令および利用規約を守ってください。
- アプリ・チュートリアル・コミュニティ：[https://www.tvbox.org/](https://www.tvbox.org/)

## コントリビュート

1. `sources.yaml` を編集（`name` / `url` / `group` / `desc`）
2. PR または Issue を作成
3. Actions が定期実行し `dist/` を更新します

## License

文書と一覧は整理・公開目的です。第三者インターフェースの権利は各作者に帰属します。

# TVbox — TVBox 接口汇总

> 官网：**[tvbox.org](https://www.tvbox.org/)**  
> 本仓库由 [TVboxorg](https://github.com/TVboxorg) 维护，用于收集、整理并定期探测可用的 TVBox 接口地址。

## 官网

- 网站首页：<https://www.tvbox.org/>
- 接口页：<https://www.tvbox.org/portal.php>
- 盒子软件与下载：<https://www.tvbox.org/>

请优先通过官网获取软件与说明；本仓库专注于**接口清单与可用性探测**。

## 订阅地址（可直接填入 TVBox）

| 用途 | 地址 |
| --- | --- |
| 优选列表（探测可用优先） | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/tvbox.json` |
| 完整列表（含状态） | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/list.json` |
| 可读状态表 | [`dist/status.md`](./dist/status.md) |

国内若 raw 较慢，可尝试镜像（自行替换）：

```text
https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/tvbox.json
```

## 仓库内容

| 路径 | 说明 |
| --- | --- |
| [`sources.yaml`](./sources.yaml) | 人工维护的接口源（权威数据） |
| [`dist/`](./dist/) | 探测结果与生成的订阅文件（CI 定时更新） |
| [`scripts/probe.py`](./scripts/probe.py) | 探测脚本 |
| [`scripts/build.py`](./scripts/build.py) | 生成 list / tvbox / status |

## 本地运行

```bash
python3 scripts/probe.py
python3 scripts/build.py
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

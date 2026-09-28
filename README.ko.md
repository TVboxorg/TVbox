# TVbox — TVBox 인터페이스 모음

**Languages:** [简体中文](README.md) | [English](README.en.md) | [繁體中文](README.zh-TW.md) | [日本語](README.ja.md) | **한국어**

> 공식 사이트：**[tvbox.org](https://www.tvbox.org/)**  
> [TVboxorg](https://github.com/TVboxorg) 에서 유지보수합니다. 사용 가능한 TVBox 인터페이스 URL을 수집·정리하고 주기적으로 점검합니다.

## 공식 사이트

- 홈：<https://www.tvbox.org/>
- 인터페이스：<https://www.tvbox.org/portal.php>
- 앱·다운로드：<https://www.tvbox.org/>

앱과 안내는 공식 사이트를 우선 이용하세요. 이 저장소는 **인터페이스 목록과 가용성 점검**에 집중합니다.

## 구독 주소 (TVBox에 붙여넣기)

| 용도 | 주소 | 입력 위치 |
| --- | --- | --- |
| **단일 설정 병합 (권장)** | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/official.json` | 설정 / 인터페이스 |
| 멀티 저장소 목록 | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/tvbox.json` | 멀티 저장소 |
| 전체 목록 + 상태 | `https://raw.githubusercontent.com/TVboxorg/TVbox/main/dist/list.json` | 조회 전용 |
| 상태 표 | [`dist/status.md`](./dist/status.md) | 조회 전용 |

`official.json`은 동작 중인 공개 소스를 가져와 `sites`를 병합합니다(CMS는 직접 병합, CSP는 가능하면 원본 `jar` 유지).

GitHub raw가 느리면 미러를 사용하세요:

```text
https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/official.json
https://cdn.jsdelivr.net/gh/TVboxorg/TVbox@main/dist/tvbox.json
```

## 저장소 구성

| 경로 | 설명 |
| --- | --- |
| [`sources.yaml`](./sources.yaml) | 수동 관리 소스 목록 |
| [`dist/`](./dist/) | 점검 결과 및 생성 파일 (CI) |
| [`dist/official.json`](./dist/official.json) | 교차 소스 단일 설정 |
| [`scripts/probe.py`](./scripts/probe.py) | 점검 스크립트 |
| [`scripts/build.py`](./scripts/build.py) | list / tvbox / status 생성 |
| [`scripts/merge.py`](./scripts/merge.py) | sites 병합 → official.json |

## 로컬 실행

```bash
python3 scripts/probe.py
python3 scripts/build.py
python3 scripts/merge.py
```

## 고지 사항

- 이 저장소는 **제3자 공개 인터페이스 URL 수집과 연결/형식 점검만** 하며, 영상·방송 콘텐츠를 **호스팅하거나 배포하지 않습니다**.
- 소스는 제3자가 관리하며 가용성은 변할 수 있습니다. 점검 결과는 참고용입니다.
- 현지 법규와 플랫폼 약관을 지켜 주세요.
- 앱·튜토리얼·커뮤니티: [https://www.tvbox.org/](https://www.tvbox.org/)

## 기여

1. `sources.yaml` 편집 (`name` / `url` / `group` / `desc`)
2. PR 또는 Issue 등록
3. Actions가 주기적으로 `dist/`를 갱신합니다

## License

문서와 목록은 정리·공개 목적입니다. 제3자 인터페이스 저작권은 원작자에게 있습니다.

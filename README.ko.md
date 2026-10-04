<div align="center">
  <h1>dot-agents</h1>
  <p>개인 바이브 코딩 워크플로에 활용하는 설정, 프롬프트, 도구를 공개 가능한 형태로 모아 관리하는 저장소입니다.</p>
  <p><a href="./README.md">English</a> | 한국어</p>
</div>

## [OpenCode 설정](./opencode/opencode.json)

개인정보를 제거한 `opencode.json`에는 다음 내용이 포함되어 있습니다.

- **플러그인 및 MCP** — 플러그인과 MCP 서버 설정
- **Provider** — `commandcode`와 `opencodex` 설정
- **모델** — 모델 한도 및 런타임 환경설정
- **인증정보** — 민감한 값을 위한 환경변수 참조

## [Codex 설정](./codex/config.toml)

`codex/`에는 공개 가능한 사용자 수준 설정 일부인 `config.toml`,
`keybindings.json`, `AGENTS.md`, 참조 파일 `RTK.md`, [사용자 에이전트](./codex/agents/)와
[Blastoise 펫](./codex/pets/blastoise/)을 담았습니다. 사용자 에이전트의 `combo/...` 모델 선택자는
다른 기기에서 사용 가능한 모델로 조정해야 합니다. 플러그인 설치 대상은
[가이드](./codex/PLUGINS.md)에 정리했습니다.
사용 환경에 맞는 파일을 검토한 뒤 `~/.codex/`에 복사해 사용하세요.
원본 `config.toml`의 기기 경로, 프로젝트 신뢰 설정, provider 및 MCP 연결,
권한 설정은 제외했습니다.

## [OpenCodex 설정](./opencodex/README.md)

`opencodex/`에는 [OpenCodex](https://github.com/lidge-jun/opencodex)의 공개 가능한
환경설정, 모델 선택, 6개 `sp-*` 장애 시 대체 모델 조합을 담았습니다.
[`config.public.json`](./opencodex/config.public.json)은 부분 설정이므로,
사용 환경에 맞게 검토한 항목만 기존 OpenCodex 설정에 적용하세요.
제공자 연결과 인증 방식, 인증정보, 계정 상태, 런타임 데이터는 제외했습니다.

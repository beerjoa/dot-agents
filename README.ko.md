<div align="center">
  <h1>dot-agents</h1>
  <p>개인 바이브 코딩 워크플로에 활용하는 설정, 프롬프트, 도구를 공개 가능한 형태로 모아 관리하는 저장소입니다.</p>
  <p><a href="./README.md">English</a> | 한국어</p>
</div>

## [신규 PC 설치와 안전한 병합](./docs/SETUP.md)

설정을 적용하는 에이전트는 이 가이드부터 확인하세요. 백업·선택적 병합,
provider 로그인과 환경변수, 기기별 advisor 동의, OpenCode native free 모델,
설치 후 검증과 인계 절차를 정리했습니다.

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
[Superpowers 호환성 문서](./docs/SUPERPOWERS.md)에 검토한 워크플로 버전과
Codex·OpenCode 에이전트의 OpenCodex combo 연결을 기록했습니다.
[프롬프트](./codex/prompts/)에는 develop 통합, 계획 작성, Task 실행 지침을 담았습니다.
[start-build](./codex/prompts/start-build.md)는 subagent 구현,
[start-build-native](./codex/prompts/start-build-native.md)는 현재 세션의 직접 구현과 최종 브랜치 리뷰에 사용합니다.
계획·실행에는 Superpowers가 필요하며, 실행은 `git-commit-from-instructions`와 구현 위임·최종 리뷰용 사용자 에이전트를 사용합니다.
사용 환경에 맞는 파일을 검토한 뒤 `~/.codex/`에 복사해 사용하세요.
원본 `config.toml`의 기기 경로, 프로젝트 신뢰 설정, provider 및 MCP 연결,
권한 설정은 제외했습니다.

## [OpenCodex 설정](./opencodex/README.md)

`opencodex/`에는 [OpenCodex](https://github.com/lidge-jun/opencodex)의 공개 가능한
환경설정, 모델 선택, 기본 subagent용 3개 `jev` 조합(`default`, `explorer`, `worker`)과
6개 `sp-*` 역할용 `jev` 모델 조합을 담았습니다.
[`config.public.json`](./opencodex/config.public.json)은 부분 설정이므로,
사용 환경에 맞게 검토한 항목만 기존 OpenCodex 설정에 적용하세요.
제공자 연결과 인증 방식, 인증정보, 계정 상태, 런타임 데이터는 제외했습니다.

## [Magpie 라우팅](./magpie/README.md)

`magpie/`에는 [`providers.public.json`](./magpie/providers.public.json)의 공개 가능한
부분 설정만 담았습니다. 10개 라우팅 그룹(`jev-auto`와 subagent용 9개 역할)의
멤버 모델, 라우팅 동작, 토큰·의도 규칙, Jev 분류기 설정이 포함되며, provider 연결과
인증정보, 계정 상태, 런타임 데이터는 제외했습니다. Magpie에는 JSON 가져오기가
없으므로 파일을 검토한 뒤 `magpie group add/set/rule` 명령으로 필요한 그룹만 다시 만드세요.

## [Claude Code 에이전트](./claude/README.md)

`claude/agents/`에는 Magpie 그룹에 `model: group/<id>`로 연결된 9개 subagent 정의를
담았습니다. 내장 에이전트를 오버라이드하는 `Explore`·`Plan`이 포함됩니다.
검토한 파일만 `~/.claude/agents/`에 복사해 사용하세요. `settings.json`은 provider
인증정보와 기기별 상태를 포함하므로 제외했습니다.

## [공통 테마](./themes/README.md)

`themes/`에는 Kanagawa Wave 다크·사용자 지정 Lotus 라이트 팔레트와,
여기서 생성하는 브라우저·Dark Reader·Codex·터미널 색상 설정을 모았습니다.
브라우저 전환 확장, 고정 버전 Dark Reader 패치와 Native Messaging 소스도
포함합니다. Linux/Omarchy 연동과 macOS 재사용 안내는 구분했습니다.
개인 프로필·사이트 목록·기기별 등록 파일은 제외하며, Python 3.11+로 색상
파일을 생성할 수 있습니다. 저장소 복제만으로 기존 기기 설정이 변경되지는 않습니다.

# 신규 PC 설치와 기존 설정 병합

이 문서는 설치를 맡은 에이전트의 시작점이다. 저장소는 **부분 설정과 소스**를
제공하며, 복제만으로 설치가 끝나지 않는다. 기존 사용자 설정을 통째로 덮어쓰지 않는다.
OpenCodex 2.91.0, Codex CLI 0.163.0, OpenCode 1.18.33, Magpie 0.1.1603에서 확인한 절차이며,
다른 버전에서는 해당 기기의 `--help`와 공식 문서로 지원 여부를 먼저 확인한다.

## 1. 적용 전 확인

1. 사용자가 요청한 앱과 기능, OS, 설치 버전, 실행 중인 세션을 확인한다.
   테마·외부 서비스 연결은 선택 사항이며 전부 설치한다고 가정하지 않는다.
2. 실제 설정 위치를 확인한다. 기본값은 `~/.codex`, `~/.opencodex`,
   `~/.config/opencode`, `~/.config/magpie`, `~/.claude`지만 `CODEX_HOME`,
   `OPENCODEX_HOME`, XDG 또는 별도
   실행 설정으로 달라질 수 있다. 실행 중인 서비스와 CLI가 같은 홈을 쓰는지도 확인한다.
3. 수정할 파일과 키, 유지할 항목을 먼저 설명한다. 대상 파일을 Git 밖의 비공개
   디렉터리에 백업하고 복원 경로를 기록한다. 백업에는 인증정보가 있을 수 있다.
4. 공식 배포 경로로 도구를 설치한다. [OpenCodex](https://github.com/lidge-jun/opencodex),
   [OpenCode](https://opencode.ai/docs/), [Codex](https://developers.openai.com/codex/)
   설치 안내와 현재 패키지 출처를 확인하고, 기존 런타임을 임의로 교체하지 않는다.

## 2. 안전한 병합

- `codex/config.toml`은 기존 TOML을 파싱해서 선택한 키·테이블만 병합한다.
  같은 테이블을 단순히 뒤에 붙이지 않는다. provider, 기본 main model, 인증·권한,
  프로젝트 trust, MCP, 개인 경로와 기존 사용자 지침을 보존한다.
- `codex/agents/`의 선택한 역할 파일과 `prompts/`를 실제 Codex 홈으로 설치한다.
  기존 동명 파일은 diff를 보고 병합한다. `AGENTS.md`의 `RTK.md` 참조를 함께
  충족시키고, 다른 사용자 지침이나 무관한 에이전트를 삭제하지 않는다.
- `opencodex/config.public.json`은 전체 `config.json`의 대체물이 아니다.
  선택한 최상위 키만 적용하고 `combos`는 이름별로 병합한다. 무관한 로컬 조합,
  provider·계정·토큰·서비스·클라이언트 연동·카탈로그 상태를 보존한다.
  `advisor`도 하위 키별로 병합해 기존 동의와 활성화 상태를 훼손하지 않는다.
- `opencode/opencode.json`, `tui.json`, agents, commands, plugins는 선택해서
  실제 OpenCode 설정 위치에 병합한다. 배열은 중복을 검토하고 기존 항목을 보존한다.
  `tui.json`에는 JSONC 주석이 있으므로 일반 JSON 파서로 재작성하지 않는다.
  `commands/`와 `snippet/`는 사용 중인 명령/스니펫 방식에 맞춰 선택한다.
- `magpie/providers.public.json`은 `~/.config/magpie/providers.json`의 부분 설정이다.
  JSON 가져오기가 없으므로 공개 파일의 그룹 정의를 검토한 뒤 `magpie group add`로
  멤버부터 만들고 `magpie group set`·`magpie group rule add`로 라우팅과 규칙을 재현한다.
  기존 provider·계정·키 설정을 보존하고 무관한 로컬 그룹을 삭제하지 않는다.
  그룹 id는 `group/<id>` 참조와 일치해야 한다.
- `claude/agents/`의 선택한 파일을 `~/.claude/agents/`에 설치한다. 기존 동명 파일은
  diff를 보고 병합한다. `Explore`·`Plan`은 정확히 그 이름일 때만 내장을 오버라이드하며,
  `model: group/<id>`는 같은 id의 Magpie 그룹이 있어야 동작한다. `settings.json`은
  인증정보와 기기별 상태를 포함하므로 공개 대상이 아니다.
- 포트 `10100`이 충돌하면 OpenCodex listener와 OpenCode의 `baseURL`, Codex의
  로컬 provider URL을 함께 맞춘다. 원격 노출·자동 시작·shim 설치는 개별 검토한다.
  `ocx setup`/`ocx sync`도 클라이언트 설정을 변경하므로 백업과 diff 확인 대상이다.
- `default`는 Codex의 기본 **subagent 역할**이다. 메인 세션 모델 변경 여부는
  별도 클라이언트 연동 설정으로 확인한다. 역할 문서 복사만으로 메인 모델을 바꾸지 않는다.

## 3. 파일 밖에서 필요한 인증과 환경

인증은 대상 PC에서 수행한다. 다른 PC의 OAuth 저장소·키체인·플러그인 캐시·
DB를 복사하지 않으며 키 값을 채팅, Git, 명령 로그나 검증 보고서에 출력하지 않는다.

| 항목 | 대상 PC에서 할 일 |
| --- | --- |
| OpenAI / ChatGPT | `ocx login codex` 등 설치 버전의 계정 연결 절차로 인증한다. 구독 로그인과 플랫폼 API 과금을 혼동하지 않는다. |
| Anthropic | `anthropic/claude-opus-5-5`용 계정을 연결한다. 현재 Opus는 `sp-spec-review`의 고난도 검토 후보이다. |
| Cursor | Cursor 계정을 연결하고 해당 모델 사용 가능 여부를 확인한다. |
| Google Antigravity | 계정을 연결하고 Gemini와 Sonnet의 접근·잔여량을 확인한다. agy/Opus는 사용하지 않으며 agy/Sonnet은 worker류에서 제외한다. |
| OpenCode Go | Go 계정/API 키를 로컬로 연결한다. 프록시의 `opencode-go/*`는 유료 Go 사용량을 소비한다. |
| TypeSafe Jev | 공식 [TypeSafe](https://typesafe.ai/) 키를 `TYPESAFE_API_KEY`로 전달하거나 `ocx login jev` / Providers의 TypeSafe JEV에서 등록한다. 공식 `jev-decision` 연결을 사용한다. |
| OpenCode → OpenCodex | `OPENCODEX_API_KEY`는 대상 프록시의 클라이언트 인증 토큰이다. provider 키나 TypeSafe 키로 대체하지 않는다. 주소·포트와 함께 확인한다. |
| Context7 MCP | `CONTEXT7_API_KEY`를 OpenCode 프로세스에 전달한다. Codex 연결은 해당 PC의 MCP/플러그인 방식으로 별도 구성한다. |
| Notion MCP | 선택한 경우 `NOTION_TOKEN`을 전달하고 필요한 페이지 접근만 연결한다. 미사용이면 이 MCP를 비활성화한다. 로컬 명령 실행에는 Node/npx가 필요하다. |
| Figma Desktop MCP | 선택한 경우 Figma Desktop의 MCP를 켜고 `127.0.0.1:3845` 연결을 확인한다. 데스크톱 앱/지원이 없으면 비활성화하거나 공식 원격 방식을 별도로 설정한다. |

환경변수는 **실제 실행 프로세스**에 전달되어야 한다. 터미널의 `export`가
GUI·로그인 서비스·이미 실행 중인 프록시에 자동 적용되지는 않는다. OS의 비공개
credential/environment 방식으로 등록하고, 필요한 서비스만 사용자와 조율해 재시작한다.
키 존재 여부만 확인하며 값을 출력하지 않는다. 저장된 키를 사용할 때는 같은 키를
여러 위치에 중복 저장할 필요가 없다.

Jev 라우팅도 판단을 위해 제한된 작업 컨텍스트를 TypeSafe로 보낼 수 있다.
대상 PC의 작업·데이터 정책에 맞는지 확인하며, 키 등록만으로 이 경계를 생략하지 않는다.

Codex 플러그인은 [PLUGINS.md](../codex/PLUGINS.md), Superpowers와 커밋 스킬 등
워크플로 의존성은 [SUPERPOWERS.md](SUPERPOWERS.md)를 확인한다. 설치 경로는
대상 PC에서 찾아 사용하고 캐시 버전의 절대 경로를 복사하지 않는다. OpenCode의
선택한 플러그인·provider 패키지와 `plugins/rtk.ts` 의존성도 설치 여부를 확인한다.
RTK는 선택 사항이며 없으면 일반 명령을 사용한다. `commandcode` provider와
`build` 등 primary agent의 직접 모델은 combo와 별도이므로 사용 시 따로 인증한다.

## 4. Advisor와 라우팅 후속 단계

공개 설정에는 advisor의 모델·정책만 있으며 `enabled`와 `contextSharingConsent`는
포함하지 않는다. 복사 후 자동으로 활성화되었다고 보고하지 않는다.
Advisor는 작업 컨텍스트를 설정된 모델 provider로 전송한다. **새 PC에서 사용자가
이 공유를 승인한 후에만** 다음 명령으로 동의를 기록하고 켠다.

```sh
ocx advisor on --ack-context-sharing
ocx advisor status --json
```

현재 조합은 Gemini 4 Argon/high, `adaptive`, task당 최대 2회이다.
`adaptive`는 검증 실패 → 수정 → 재검증 실패 같은 실행 증거를 사용하며, 임의의
의미적 난이도 판단을 보장하지 않는다. 동의 전에는 보류 상태로 보고한다.

추가 설정은 공개 JSON에 있으나 실제 적용 여부를 각각 읽어서 확인한다.

```sh
ocx agent compaction-routing show
ocx agent subagents status --json
ocx agent injection status --json
```

기대값은 compaction Gemini 3.8 Flash/high, roster 5개
(`combo/default`, `combo/explorer`, `combo/worker`, `combo/sp-worker`,
`combo/sp-worker-pro`), injection `combo/default`/high이다.
Jev의 `modelProfile`과 effort allowlist는 선택의 지침이며 고정 순번을 보장하지 않는다.
Jev 실패 시에도 fallback으로 응답할 수 있으므로 응답 성공만으로 Jev 동작을 판정하지 않는다.

### 선택: Jev quota 신호와 저-quota 알림 (OpenCodex 2.89+)

둘 다 기본 off이며 공개 JSON에 포함하지 않는다. 대상 PC에서 필요할 때만 켠다.

**Jev quota 신호**는 콤보별 opt-in이다. 켜면 후보 타깃마다 캐시된 quota 관측치를
healthy/moderate/limited/nearly_exhausted 단계로 Jev 판단 입력에 붙인다.
적합한 후보들 중에서 잔여가 많은 쪽을 선호하도록 유도할 뿐이며, 타깃·effort
허용 목록을 바꾸지 않는다. 관측치가 없는 제공업체는 unknown이며 healthy와
동급 취급이라 불이익이 없다. 기본 임계값은 limited 70%, nearlyExhausted 90%이다.

```sh
ocx combo set <id> --decision-quota-signals on
ocx combo show <id>  # decisionQuotaSignals: true 확인
ocx combo stats <id>  # 실트래픽 결정 요약에서 tier 분포 확인
```

임계값을 바꾸려면 `--decision-quota-tiers '{"limited":70,"nearlyExhausted":90}'`를
붙인다. 끄려면 `--decision-quota-signals -`로 되돌린다. 고사용량 콤보 1~2개부터
켜고 `stats`로 관찰한 뒤 확대한다. 같은 작업도 quota 상태에 따라 라우팅이
달라질 수 있다.

**저-quota 알림**은 Codex 풀 계정의 5시간/weekly 윈도우에만 반응하며
Antigravity·Anthropic·opencode-go quota는 대상이 아니다. `codexPool` 키가
없으면 보호 기능 전체가 꺼진 상태이다. 계정이 하나뿐인 PC에서는 일시정지 없이
알림 전용으로 설정한다.

```sh
ocx config set codexPool '{"lowQuotaProtection":{"enabled":true,"threshold":85,"actions":{"pause":false,"notify":true,"desktop":true},"windows":{"short":true,"weekly":true}}}'
ocx config validate
ocx service restart  # 파일 변경은 재시작 후 적용된다
```

Linux 데스크톱 알림에는 `notify-send`가 필요하며 알림에는 가명 계정 라벨만
들어간다. 테스트 핑 한 번으로 경로를 확인하고, 실제 quota 이벤트와 혼동하지
않는다. 끄려면 `ocx config unset codexPool.lowQuotaProtection` 후 재시작한다.
수정 전에는 `~/.opencodex/backups/` 같은 Git 밖 비공개 위치에
`config.json`을 백업한다.

### OpenCode native free 모델

2026-10-19 확인에서 native OpenCode의 `opencode/deepseek-v4.1-flash-free`는
동작했지만 OpenCodex의 `opencode-zen/*-free` 경로는 `FreeTierError` 403이었다.
free를 원하면 대상 PC의 `opencode models`로 현재 목록을 확인하고 **OpenCode
agent의 native 모델 선택자**로 개별 지정한다. Codex용 공유 combo에 섞거나
세션 헤더를 위조해서 우회하지 않는다. 기존 combo는 Go 경로를 유지한다.
free 목록·가용성·데이터 보존 정책은 바뀔 수 있으므로 현재 제공자 정책과 작업을 확인한다.
이 랩탑의 비-ZDR 허용 결정을 다른 PC의 모든 작업에 자동 적용하지 않는다.

## 5. 완료 검증과 인계

1. 병합 전후 diff로 요청한 키·파일만 달라졌는지 확인한다. JSON/JSONC/TOML,
   역할 frontmatter, 모든 `combo/...` 참조와 설치된 provider/model/effort를 검증한다.
2. `ocx status`, `codex doctor --summary`, 선택한 MCP·플러그인의 상태를 확인한다.
   새 클라이언트 세션에서 역할을 확인한다. resume 세션은 기존 모델·지침 상태가
   남을 수 있으므로 별도로 확인하며 새 설정 적용을 가정하지 않는다.
3. 사용량을 최소화한 합성 프롬프트로 실제 선택한 provider와 native free 경로를
   확인한다. Jev는 `ocx combo test --combo worker --json` 같은 probe의 receipt에서
   실제 decision 적용 여부를 확인한다. 이 probe는 구현 모델 호출 검증과 별개다.
4. 테마는 [themes/README.md](../themes/README.md)와 OS별 가이드에 따라 선택한다.
   `python3 themes/scripts/generate.py --check`는 생성물 검증이며 설치·화면 검증은
   별도다. 브라우저 native host 등록, Paseo 플러그인 활성화·테마 선택, Omarchy
   사용자 hook은 각 가이드의 기기별 단계가 필요하다. package 소유 파일을 덮어쓰지 않는다.
5. 변경 파일, 백업/복원 위치, 검증 결과, 미인증·미설치·미검증 항목을 인계한다.
   실패하면 해당 변경만 복원하고 다른 설정을 유지한다. 정적 검증 통과를 모든 계정과
   OS에서의 실행 성공으로 표현하지 않는다.

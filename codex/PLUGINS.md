# Codex 플러그인 설치 가이드

이 목록은 2026-09-24에 `codex plugin list --json`으로 확인한 **설치·활성화 상태**를 기준으로 합니다. `~/.codex/plugins/cache/`와 인증 상태는 복사하지 않습니다. 설치 가능 여부와 버전은 사용하는 Codex 및 계정에 따라 달라질 수 있습니다.

## 직접 선택할 플러그인

Codex의 `/plugins` 화면에서 이름을 찾아 설치하고, 필요한 앱 연결을 완료합니다. CLI에서는 `codex plugin add <plugin@marketplace>` 형식을 사용할 수 있습니다.

| 용도 | 플러그인 선택자 |
| --- | --- |
| GitHub | `github@openai-curated-remote` |
| 디자인 | `canva@openai-curated-remote`, `figma@openai-curated-remote` |
| 개발 서비스 | `supabase@openai-curated-remote`, `cloudflare@openai-curated-remote`, `atlassian-rovo@openai-curated-remote` |
| 문서 작업 | `documents@openai-primary-runtime`, `pdf@openai-primary-runtime`, `spreadsheets@openai-primary-runtime`, `presentations@openai-primary-runtime`, `template-creator@openai-primary-runtime` |
| 도구 | `openai-templates@openai-curated-remote`, `plugin-management@openai-curated-remote`, `visualize@openai-bundled` |

`openai-primary-runtime`과 `openai-bundled`는 앱이 제공하는 로컬 소스입니다. 그 캐시의 절대 경로를 다른 기기에 복사하지 말고, 새 환경의 플러그인 화면에서 설치 가능 항목을 확인합니다.

## 별도 마켓플레이스

현재 설치되어 활성화된 외부 마켓플레이스 플러그인입니다. 마켓플레이스를 등록한 뒤 해당 플러그인을 설치합니다.

```sh
codex plugin marketplace add https://github.com/mksglu/context-mode.git
codex plugin marketplace add https://github.com/obra/superpowers.git
codex plugin add context-mode@context-mode
codex plugin add superpowers@superpowers-dev
```

설치 후 `codex plugin list --json`에서 `installed`와 `enabled`를 확인하고 새 세션에서 사용합니다. `ouroboros@ouroboros`는 현재 설치되어 있지만 비활성화되어 있어 설치 대상에서 뺐습니다.

Codex 앱에 함께 제공되는 `codex-app-tools`, `browser`, `unified-computer-use`, `chrome`, `computer-use`의 캐시는 이 저장소에 포함하지 않습니다. 앱이나 계정이 제공하는 항목을 새 환경에서 확인합니다.

한 번에 실행하는 설치 스크립트는 두지 않습니다. 마켓플레이스 등록, 설치 가능 항목, 앱 인증이 환경마다 달라서 각 단계를 확인하며 설치하는 편이 재현하기 쉽습니다.

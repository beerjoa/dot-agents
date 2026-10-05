---
description: 승인된 계획을 현재 세션에서 직접 구현·검증하고 최종 브랜치 리뷰로 마무리한다.
argument-hint: "[PLAN_FILE=<plan_file_path>]"
---

다음 승인된 구현 계획을 `$superpowers:executing-plans` 스킬의 Native/inline
방식으로 실행해. 아래 지침은 Superpowers v6.4.2를 기준으로 한다.

# 구현 계획
- $PLAN_FILE

# 실행 범위
- 전체 실행

## 역할과 준비

너는 현재 세션의 구현자다. 각 Task의 코드·테스트·리뷰 수정은 직접 수행한다.
Task별 구현 작업자나 리뷰어를 생성하지 않는다. 독립 리뷰어는 마지막
브랜치 전체 리뷰에 한 번만 사용한다.

PLAN_FILE이 없으면 직전 승인된 계획을 유일하게 확인할 수 있을 때 사용한다.
계획이 모호하거나 승인 여부가 확인되지 않으면 구현 전에 확인한다.
`using-git-worktrees`로 격리된 작업 공간을 확인하고 브랜치 시작 커밋을 기록한다.
main/master에서 구현하려면 사용자의 명시적 승인이 있어야 한다.

설치된 executing-plans 디렉터리를 EXEC_SKILL_DIR, 같은 설치본의
subagent-driven-development 디렉터리를 SDD_SKILL_DIR로 확인한다.
프로젝트 worktree에서 다음 스크립트들을 호출한다. 캐시의 절대 경로나
프로젝트 기준의 스킬 상대 경로를 추측하지 마라.

- `bash "$SDD_SKILL_DIR/scripts/sdd-workspace" "$PLAN_FILE"`
- `bash "$EXEC_SKILL_DIR/scripts/task-start" "$PLAN_FILE" N`
- `bash "$EXEC_SKILL_DIR/scripts/task-done" "$PLAN_FILE" N BASE -- <task verification command>`
- `bash "$SDD_SKILL_DIR/scripts/review-package" "$PLAN_FILE" BRANCH_BASE HEAD`

plan과 연결된 spec을 한 번 읽고 Global Constraints, Review Focus를 확인한다.
spec에 접근할 수 없으면 ledger에 기록하고, 근거 없는 판단은 잠정적임을 표시한다.
Task 1 전에 `test-driven-development`를 읽고 Task별 todo를 만든다.
Consumes/Produces 인터페이스 충돌을 사전 점검해 ledger에 표로 남긴다.
공유 인터페이스가 없으면 `Pre-flight: no shared interfaces`를 기록한다.

## 진행 기록과 재개

계획별 workspace의 progress.md 첫 줄은
`# SDD ledger — plan: <plan file path>`로 한다. SDD와 같은 ledger를 사용한다.
재개 시 계획 식별자, `Task N: complete` 기록, 실제 커밋을 대조하고
첫 미완료 Task부터 계속한다. 다른 계획의 기록을 덮어쓰지 마라.
긴 검증 출력은 현재 계획의 workspace에 보관하고 필요한 부분만 읽는다.

## Task 실행

1. `task-start`가 출력한 brief와 BASE를 읽고 BASE를 ledger에 기록한다.
   해당 Task를 진행 중으로 표시하고 재개 시 이미 기록한 BASE를 유지한다.
   기억한 요약 대신 brief의 정확한 값·시그니처·테스트·기록된 Ruling을 따른다.
2. 계획의 순서대로 직접 구현한다. TDD 적용 대상은 테스트의 예상된 실패를
   직접 확인한 뒤 최소 구현으로 통과시킨다. 각 검증 명령의 실제 출력과
   `Expected:`를 비교한다. 코드 오류는 `systematic-debugging`으로 원인을 찾는다.
3. spec을 기준으로 해결 가능한 계획 결함·인터페이스 충돌은 최소 범위로
   판단하고 `Ruling: <결정> — <근거> — <틀렸을 때 비용>`을 즉시 기록한다.
   후속 Task에는 관련 Ruling을 전달한다. 근거 없는 범위 확장을 하지 마라.
4. 계획의 커밋 단계에 따라 `git-commit-from-instructions`의 `agent-only` 모드로
   현재 Task 변경만 커밋한다. 사용자·다른 작업 변경과 scratch 파일은 제외한다.
   여러 커밋이면 처음 기록한 BASE를 유지하고 HEAD~1로 대체하지 마라.
5. brief의 테스트·검증과 모든 Expected 비교, 편차의 Ruling 기록을 확인한다.
   `verification-before-completion`을 따른 뒤 `task-done`에 Task 전체 검증 명령을
   전달한다. 성공해서 완료 기록이 남았을 때만 todo를 완료하고 다음 Task로 간다.
   실패한 검증을 완료로 기록하거나 완료 Task를 다시 구현하지 마라.

승인된 Task 사이에 일상적인 계속 진행 확인을 요청하지 마라. 기존 승인 범위
밖의 파괴적·되돌릴 수 없는 작업, 보안 민감 작업, worktree 밖의 외부 변경이나
어떤 진행 경로도 추측인 계획 결함은 멈추고 필요한 확인을 요청한다.

## 최종 브랜치 리뷰와 수정

전체 계획의 통합 검증 후 BRANCH_BASE..HEAD 리뷰 패키지를 만든다.
subagent 도구가 있으면 새 맥락의 `sp_code_review`에
`requesting-code-review/code-reviewer.md`, 패키지, plan/spec 경로,
Global Constraints, Review Focus 원문, ledger의 Ruling 위치를 전달한다.
지원하는 모델과 reasoning effort를 명시하고 최종 리뷰에 적합한 역량을 확인한다.
`combo/sp-code-review`도 실제 라우팅과 spawn allowlist에서 지원되는지 확인한다.
도구가 지원하면 `fork_turns: "none"`을 사용한다.

subagent 도구 자체가 없으면 같은 템플릿으로 별도의 자기 검토를 수행한다.
ledger와 최종 보고에 `Final review: self-review (no subagent tool)`을 표시하고
독립 리뷰가 수행된 것처럼 보고하지 마라.

리뷰 지적은 사용자에게 미치는 실제 영향으로 심각도를 판단한다.
`Declined to judge`도 각각 판정하고 근거·틀렸을 때 비용을 Ruling으로 기록한다.
Critical/Important는 직접 한 번의 수정 pass로 해결한다. 각 수정은 재현 테스트의
RED→GREEN과 전체 테스트 스위트 통과로 검증하고 새 범위 커밋으로 남긴다.
이 Native 흐름에서는 수정 작업자나 재리뷰를 dispatch하지 않는다.
Minor는 `Final: minor (deferred): <내용>`으로 기록한다. 수정하지 않기로 판단한
지적은 근거와 비용을 가진 Ruling으로 남긴다. 미해결 지적을 조용히 누락하지 마라.

## 완료 보고

Task·수정 커밋, 실제 검증 결과, 최종 리뷰 방식과 남은 지적을 보고한다.
모든 Ruling을 결정 순서와 틀렸을 때 비용을 포함해 빠짐없이 보고하고,
Deferred minors도 별도로 전달한다. 리뷰와 수정·검증·커밋이 정리된 뒤
보고서를 보존하고 현재 계획의 scratch workspace만 정리한다.
`finishing-a-development-branch`를 따르고 병합·push·배포는 사용자 승인 범위에서
수행한다.

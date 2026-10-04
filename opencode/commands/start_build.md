---
description: 작성된 plan 기준으로 실제 구현을 진행한다.
agent: sp-build
---

Use superpowers/subagent-driven-development.
계획 파일: $ARGUMENTS
생략했으면 직전 승인된 계획을 유일하게 확인할 수 있을 때 사용해.

Superpowers v6.4.2와 @sp-build 지침에 따라 승인된 계획 전체를 실행해.
프로젝트 worktree에서 설치된 SDD 스킬의 sdd-workspace, task-brief,
review-package 스크립트를 사용해 계획별 ledger와 파일 기반 보고서를 관리해.

구현은 @sp-worker 또는 @sp-worker-pro, 조사는 @sp-explorer,
원인 분석은 @sp-debug에 맡겨. 각 역할의 combo/sp-* 모델과
reasoning effort를 명시하고 실제 라우팅의 지원 여부와 역량을 확인해.
작업자가 테스트 후 현재 Task만 agent-only 모드로 커밋하게 하고,
@sp-code-review 한 명이 task-reviewer-prompt.md로 명세와 품질을 모두 검사하게 해.
@sp-spec-review는 plan/spec 검토 또는 별도로 요청된 명세 감사에 사용해.

DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, BLOCKED를 구분하고,
최대 5회 수정 루프와 FIX_BASE..HEAD 범위 재리뷰를 수행해.
완료 Task를 재실행하거나 작업자가 자체 리뷰어를 생성하게 하지 마.
마지막에는 전체 브랜치 리뷰와 최대 한 번의 최종 수정·재리뷰를 수행하고,
커밋·검증 증거·Ruling·남은 지적을 보고해.

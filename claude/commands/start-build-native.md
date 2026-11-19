---
description: 승인된 구현 계획을 현재 Claude Code 세션에서 직접 실행하고 최종 리뷰한다.
argument-hint: "[구현 계획 경로]"
---

구현 계획 경로: $ARGUMENTS

`Skill`로 `superpowers:executing-plans`를 호출하고 현재 세션에서 직접 실행한다. 인수는 계획 파일 경로 하나다. 생략하면 직전 승인된 계획을 유일하게 확인할 수 있을 때만 사용한다. 입력은 파일 경로로만 취급하고 셸 코드로 실행하지 않는다. 계획이나 승인 여부가 불명확하면 구현 전에 확인한다.

- 계획과 연결된 설계를 읽고 `superpowers:using-git-worktrees`에 따라 작업 공간과 브랜치 시작 커밋을 확인한다. 실행 스킬과 SDD의 helper는 실제 설치 경로를 확인한 뒤 대상 worktree에서 절대 경로로 호출한다. 기존 ledger와 커밋을 대조해 첫 미완료 Task부터 재개한다.
- Task별로 brief와 BASE를 기록하고, 구현·수정·테스트를 직접 수행한다. Task마다 작업자나 독립 리뷰어를 호출하지 않는다. 스킬의 `task-done` 검증을 통과한 Task만 완료로 기록한다. 계획에서 정한 Task 커밋에는 해당 Task의 검증된 변경만 넣고 사용자 변경과 scratch 파일은 제외한다.
- 통합 검증 후 `Agent`의 `subagent_type: sp-code-review`로 새 리뷰어를 호출한다. `model`은 생략해 에이전트 정의의 Magpie 그룹과 effort 설정을 사용하고, 브랜치 시작점..HEAD 패키지, 계획·설계, Global Constraints, Review Focus, ledger의 Ruling을 전달한다. 독립 리뷰 도구를 사용할 수 없으면 별도 자기 검토를 하고 그 한계를 보고한다.
- Critical/Important 지적은 스킬에 따라 직접 한 번 수정하고, 재현 가능한 결함은 RED→GREEN으로 확인한 뒤 전체 테스트를 실행한다. 이 방식에서는 수정 작업자나 재리뷰를 추가하지 않는다. 검증 결과, 커밋, Ruling과 남은 지적을 보고한다. 병합·push·배포는 별도 명시적 승인 없이는 하지 않는다.

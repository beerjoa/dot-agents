---
description: 승인된 구현 계획을 Claude Code 작업자와 독립 리뷰어로 실행한다.
argument-hint: "[구현 계획 경로]"
---

구현 계획 경로: $ARGUMENTS

`Skill`로 `superpowers:subagent-driven-development`를 호출하고, 아래 역할 매핑으로 설치된 스킬의 절차를 따른다. 인수는 계획 파일 경로 하나다. 생략하면 직전 승인된 계획을 유일하게 확인할 수 있을 때만 사용한다. 입력은 파일 경로로만 취급하고 셸 코드로 실행하지 않는다. 계획이나 승인 여부가 불명확하면 구현 전에 확인한다.

- 승인된 계획과 연결된 설계를 읽고 `superpowers:using-git-worktrees`에 따라 작업 공간을 확인한다. 대상 worktree에서 설치된 스킬의 helper를 확인된 절대 경로로 호출한다. 계획별 ledger, BASE, Task brief, report, 리뷰 패키지를 사용하고, 재개할 때 완료된 Task를 다시 실행하지 않는다.
- `Agent`의 `subagent_type`으로 일반 구현은 `sp-worker`, 복잡한 구현은 `sp-worker-pro`를 사용한다. 필요할 때만 조사에 `sp-explorer`, 원인 분석에 `sp-debug`, 별도 명세·계획 검토에 `sp-spec-review`를 사용한다. 독립 Task 리뷰, 수정 범위 재리뷰, 최종 브랜치 리뷰는 `sp-code-review`에 맡긴다.
- 호출 시 `model`을 생략해 각 에이전트 정의의 Magpie 그룹과 effort 설정을 사용한다. `fork`로 대체하지 않는다. 역할이 없거나 실제 라우팅의 역량을 확인할 수 없으면 그 공백을 보고한다. 더 강한 라우팅이 필요한 경우 같은 그룹을 다시 호출한 것만으로 승격을 인정하지 않는다.
- 작업자는 순차 실행한다. 새 작업자에게 brief, 관련 인터페이스·제약·Ruling, report 경로만 전달한다. 검증한 자신의 Task 변경만 커밋하도록 명시하고, 사용자 변경과 scratch 파일은 제외한다. 컨트롤러는 구현·수정을 직접 하지 않는다.
- 독립 리뷰어에게 brief, report, BASE..HEAD 패키지와 스킬의 리뷰 지침을 전달한다. 명세·품질 판정과 검증 불가 항목을 각각 확인한다. 지적은 스킬의 최대 5회 수정·범위 재리뷰 절차에 따라 새 범위 커밋으로 해결한다. 보류한 지적과 Ruling은 ledger에 남긴다.
- 통합 검증 후 새 `sp-code-review`에 브랜치 전체를 검토시킨다. 필요하면 수정 작업자 한 번과 범위 재리뷰 한 번으로 마무리한다. 실제 검증 결과, 커밋, Ruling과 남은 지적을 보고한다. 병합·push·배포는 별도 명시적 승인 없이는 하지 않는다.

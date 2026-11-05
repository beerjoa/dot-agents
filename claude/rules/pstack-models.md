# pstack model configuration
# budget: Jev (auto)
# Claude Code aliases select Magpie groups; they do not name the model actually served.
# haiku -> group/pstack-explore; sonnet -> group/pstack-code; opus -> group/pstack-reasoning.
# The request uses high to keep reasoning enabled. Magpie's effort=auto classifier chooses
# the actual per-turn reasoning effort, mapped to the selected model's supported levels.
# Do not pin member-model effort, force max, or replace a role's alias with inherit-parent.

feature, refactoring: sonnet high
bug-fix: sonnet high
perf-issue: sonnet high
hillclimb: sonnet high
judgment and prose: opus high
hardest tasks: opus high
how explorer: haiku high
how explainer: opus high
why investigators: haiku high
why synthesizer: opus high
reflect tooling: sonnet high
reflect judgment, divergent, synthesizer: opus high
arena runners: sonnet high, opus high
arena cross-judge pool: opus high, sonnet high
swarm workers: sonnet high
architect runners: opus high, sonnet high
interrogate reviewers: opus high, sonnet high

## Routing constraints

- Use pstack's Claude Code adapter. Do not pass group IDs directly as the Agent tool's model argument.
- Explore contains only Codex Luna and Antigravity Gemini Flash. Escalate difficult causal analysis to the reasoning role.
- Sol is the default technical reasoner; Muse handles prose and ordinary synthesis. Opus and Astra are exceptional escalations, not defaults.
- Model-family diversity is not guaranteed by different aliases: two groups can select the same model, and each group contains multiple families.
- Do not claim a cross-family judge ran unless the actual served models and their families are known. Skip that judge when its family requirement cannot be established.
- Mixed-group fallback may reach any ready member, including Muse after technical members fail. A successful response is not proof that the required technical capability was available; check the served route before accepting a high-risk review.
- The parent controls delegation count. Explicit fan-out or panel instructions determine how many agents run; the role configuration does not authorize extra agents by itself.

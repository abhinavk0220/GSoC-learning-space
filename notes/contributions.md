# GSoC 2026 Contributions

## Mesa-LLM PRs

| PR | Title | Status | Notes |
|---|---|---|---|
| #153 | fix: migrate codebase to Mesa 4.x API | Open | Waiting on wang-boyu review |
| #170 | improve: add type hints to LLMAgent + ModuleLLM | Open | Waiting on colinfrisch response |
| #179 | improve: add type hints to reasoning module | Open | Needs peer review |
| #195 | Add __repr__ methods + Mesa 4.x compatibility fixes | Open | Reviewer feedback addressed, awaiting merge |
| #199 | fix: ReActReasoning AttributeError + STLTMemory Mesa 4.x | Open | Needs peer review |
| #217 | fix: Reasoning.execute_tool_call() uses model.time | Open | Full audit done, awaiting merge |

## Mesa-Examples PRs

| PR | Title | Status | Notes |
|---|---|---|---|
| #360 | feat: LLM Opinion Dynamics | Open | Screenshot added, needs peer review |
| #363 | feat: LLM Schelling Segregation | Open | Needs peer review |
| #372 | feat: LLM Epidemic (SIR) model | Open | Screenshot added, needs peer review |
| #378 | feat: LLM Prisoner's Dilemma | Open | Screenshot added, needs serious peer review (#390) |

## Issues Opened

| Issue | Title | Repo |
|---|---|---|
| #152 | fix: codebase incompatible with Mesa 4.x | mesa-llm |
| #197 | bug: move_one_step() moves agents in wrong direction | mesa-llm |
| #198 | bug: ContinuousSpace boundary check allows agents outside bounds | mesa-llm |
| #204 | bug: ReActReasoning.__repr__() crashes with AttributeError | mesa-llm |
| #205 | bug: STLTMemory uses model.steps which does not exist in Mesa 4.x | mesa-llm |
| #216 | bug: Reasoning.execute_tool_call() uses model.steps | mesa-llm |

## Peer Reviews Done

| PR | Repo | Summary |
|---|---|---|
| #384 | mesa-examples | Misinformation spread model — reviewed against #390 checklist |
| #365 | mesa-examples | Swarm Minefield Mapper — full review of agents.py, model.py, server.py, tests; flagged custom grid design, formation offset reassignment risk, test coverage gaps |

## Key Technical Contributions

### Mesa 4.x Coordinate System Bug
Found and fixed a bug where `move_one_step()` was moving agents in the
wrong direction on real `OrthogonalMooreGrid` cells. Root cause: real
Mesa cells and SimpleNamespace test cells both have a `connections` dict
but with incompatible coordinate conventions. Fixed by using
`isinstance(cell, SimpleNamespace)` as the distinguisher.

### `model.steps` → `model.time` Full Audit (PR #217)
Identified and fixed `model.steps` usage across 8 files in mesa-llm:
`reasoning.py`, `llm_agent.py`, `st_lt_memory.py`, `st_memory.py`,
`lt_memory.py`, `episodic_memory.py`, `memory.py`, `simulation_recorder.py`.
This was a silent breaking change in Mesa 4.x — 15 occurrences total.

### `__repr__` Safety Fixes (PR #195)
- Added `reprlib.repr()` for `internal_state` in `LLMAgent.__repr__`
  to prevent terminal bloat and recursion on large nested objects
- Added `_safe_api_base()` to `ModuleLLM` to redact inline auth tokens
  (e.g. `?key=`, Azure SAS params) from URLs before logging
- Rebased onto upstream after PR #226 merged (seed= → rng= changes)

### LLM Example Models
Built 4 LLM example models demonstrating how LLM reasoning changes
emergent behavior compared to rule-based equivalents:
- Opinion Dynamics (#360) — LLM agents more resistant to opinion change
- Schelling Segregation (#363) — weaker segregation with reasoning agents
- Epidemic SIR (#372) — flatter curves due to behavioral heterogeneity
- Prisoner's Dilemma (#378) — emergent reputation and trust dynamics

# GSoC 2026 Contributions

## Mesa-LLM PRs

| PR | Title | Status |
|---|---|---|
| #153 | fix: migrate codebase to Mesa 4.x API | Open |
| #170 | improve: add type hints to LLMAgent + ModuleLLM | Open |
| #179 | improve: add type hints to reasoning module | Open |
| #195 | Add __repr__ methods + Mesa 4.x compatibility fixes | Open |
| #199 | fix: ReActReasoning AttributeError + STLTMemory Mesa 4.x | Open |
| #217 | fix: Reasoning.execute_tool_call() uses model.time | Open |

## Mesa-Examples PRs

| PR | Title | Status |
|---|---|---|
| #360 | feat: LLM Opinion Dynamics | Open |
| #363 | feat: LLM Schelling Segregation | Open |
| #372 | feat: LLM Epidemic (SIR) model | Open |
| #378 | feat: LLM Prisoner's Dilemma | Open |

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
| #384 | mesa-examples | Misinformation spread model reviewed against #390 checklist |

## Key Technical Contributions

### Mesa 4.x Coordinate System Bug
Found and fixed a bug where `move_one_step()` was moving agents in the
wrong direction on real `OrthogonalMooreGrid` cells. Root cause: real
Mesa cells and SimpleNamespace test cells both have a `connections` dict
but with incompatible coordinate conventions. Fixed by using
`isinstance(cell, SimpleNamespace)` as the distinguisher.

### `model.steps` → `model.time` Audit
Identified and fixed `model.steps` usage across 3 files in mesa-llm
(`reasoning.py`, `st_lt_memory.py`, `record_model.py`). This was a
silent breaking change in Mesa 4.x.

### LLM Example Models
Built 4 LLM example models demonstrating how LLM reasoning changes
emergent behavior compared to rule-based equivalents:
- Opinion Dynamics LLM agents more resistant to opinion change
- Schelling Segregation weaker segregation with reasoning agents
- Epidemic SIR flatter curves due to behavioral heterogeneity
- Prisoner's Dilemma emergent reputation and trust dynamics

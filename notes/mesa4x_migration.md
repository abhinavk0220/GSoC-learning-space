# Mesa 4.x Migration Notes

## Overview

Mesa 4.x introduced breaking changes that removed the entire `mesa.space`
module. This document captures what I learned while migrating mesa-llm
and building LLM example models against Mesa 4.x.

---

## Breaking Change 1: `mesa.space` Removed

**Old API:**
```python
from mesa.space import MultiGrid, SingleGrid, ContinuousSpace
```

**New API:**
```python
from mesa.discrete_space import OrthogonalMooreGrid, OrthogonalVonNeumannGrid
from mesa.experimental.continuous_space import ContinuousSpace
```

The new discrete space uses a **cell-based architecture** — agents live in
`Cell` objects rather than coordinates directly.

**Old agent placement:**
```python
grid.place_agent(agent, (x, y))
```

**New agent placement:**
```python
cell = grid._cells[(x, y)]
cell.add_agent(agent)
agent.cell = cell
agent.pos = cell.coordinate
```

---

## Breaking Change 2: `model.steps` Removed

`model.steps` was removed in Mesa 4.x. The correct step counter is
`model.time` (public API introduced in Mesa 3.4).

```python
# Wrong - crashes in Mesa 4.x
plan = Plan(step=self.agent.model.steps, ...)

# Correct
plan = Plan(step=int(self.agent.model.time), ...)
```

This bug was present in multiple places across mesa-llm:
- `mesa_llm/reasoning/reasoning.py` — both `execute_tool_call()` and `aexecute_tool_call()`
- `mesa_llm/memory/st_lt_memory.py` — memory consolidation path
- `mesa_llm/recording/record_model.py` — step recording

---

## Breaking Change 3: `Model(seed=42)` Constructor

The `seed` kwarg conflicts with `mesa_signals` in Mesa 4.x:

```python
# Wrong
model = Model(seed=42)

# Correct
model = Model()
```

---

## Breaking Change 4: `ContinuousSpace` API Changed

**Old API:**
```python
space = ContinuousSpace(x_max=10, y_max=10, torus=False)
```

**New API:**
```python
space = ContinuousSpace(dimensions=[[0, 10], [0, 10]], torus=False)
```

---

## The Coordinate System Bug (Subtle)

This was the trickiest bug I found. Real `OrthogonalMooreGrid` cells
have a `connections` dict populated internally — but it uses `(row, col)`
keys, while the grid's `_cells` dict uses `(x, y)` keys.

The previous `move_one_step()` implementation used `connections` for all
cell types, causing agents to move in the wrong direction on real grids:

```python
# Agent at (2,2) moving North
# connections[(-1, 0)] gives cell at row-1 → (1, 2)  ← WRONG
# _cells[(2, 3)] gives cell at y+1 → (2, 3)          ← CORRECT
```

**Fix:** Check `isinstance(cell, SimpleNamespace)` to distinguish
real Mesa `Cell` objects (use `direction_map_xy` + `_cells`) from
`SimpleNamespace` dummy test cells (use `connections` with row/col deltas).

This bug only surfaces when actually running agents on a real grid —
it wouldn't be caught by reading the code or running unit tests with
dummy grids.

---

## Key Lessons

1. **Mesa 4.x is a breaking change release** — don't assume backward
   compatibility. Always check against the actual installed version.

2. **Private attributes (`_time`, `_cells`) are private for a reason**
   — use public APIs (`model.time`, documented cell methods).

3. **Building models finds bugs that reading code doesn't** — the
   coordinate system bug and `model.steps` bugs were all found by
   actually running simulations, not by code review.

4. **Upstream merges can reintroduce fixed bugs** — always sync and
   rerun tests after pulling from upstream.

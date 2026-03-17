# Peer Review: PR #365 — Swarm Minefield Mapper

**Repo:** mesa/mesa-examples
**PR:** https://github.com/mesa/mesa-examples/pull/365
**Author:** apfine (Adarsh Pandey)
**Reviewed:** 2026-03-17

Files reviewed: `agents.py`, `model.py`, `server.py`, `README.md`, `tests/test_model.py`

---

## Overall

Production-quality swarm coordination example. Heterogeneous agents with dynamic leadership,
checkpoint-based retreat, and distributed pathfinding. README is one of the most thorough in
the repo. A few items worth discussing before merge.

---

## Mesa API Usage

Mesa 4.x APIs used correctly — `super().__init__(rng=seed)`, `self.agents.shuffle_do("step")`,
and DataCollector are all right.

**Main structural concern:** The model implements a custom `SimpleMultiGrid` class instead of
Mesa's native `OrthogonalMooreGrid`. The comment says "across Mesa versions" suggesting
intentional compatibility design. Asked author to clarify if migration to native grid is planned.

---

## Agent Cooperation Logic

Leader-follower state machine is sound:
- Frustration counter correctly detects horizontal loops
- Checkpoint creation only when full 3×3 Moore neighborhood is mine-free ✅
- Dead-end immutability logic is correct and tested ✅

**Potential issue:** After `leadership_handoff()`, followers are reassigned formation offsets
sorted by `(x, unique_id)`. If a drone's physical position doesn't match the newly assigned
offset, it could rally toward a mismatched target temporarily. The existing handoff test checks
that promotion occurs but doesn't verify offset correctness during subsequent rally.

---

## Pathfinding

Both A* implementations correct:
- Local movement: Manhattan heuristic ✅
- Global final-path: Chebyshev distance — correct for Moore-neighborhood movement ✅
- Verified-safe cell rule (all Moore neighbors must be explicitly known) ✅

---

## Test Coverage

13 tests covering core scenarios. Gaps worth filling:
- Formation offset correctness after leadership handoff
- Checkpoint retirement workflow (stack exhaustion)
- Airborne override (`safety_override`) behavior during rally

---

## Visualization

Portrayal function handles all agent/cell types with distinct colors and layers. HTML status
panel showing battery, mines discovered, and path length is a nice debugging aid.

---

## Summary

Ready for merge pending clarification on `SimpleMultiGrid` design choice. Formation offset
test is optional but would strengthen confidence in handoff logic. Great work overall.

Review posted: https://github.com/mesa/mesa-examples/pull/365#issuecomment-4072917350

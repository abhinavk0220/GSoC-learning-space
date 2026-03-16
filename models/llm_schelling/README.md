# LLM Schelling Segregation

## What this model does

This model reimplements the classic Schelling Segregation model with LLM
agents that reason about whether to move rather than applying a fixed
satisfaction threshold. Each agent observes its neighborhood composition
and uses LLM reasoning to decide: stay, or move to a random empty cell.

In the classic model, an agent moves if fewer than X% of its neighbors are
the same type. In this version, the agent thinks about it considering
factors like neighborhood quality, attachment to location, and social
context before deciding.

## Mesa features used

- `OrthogonalMooreGrid` for the city grid
- `LLMAgent` with `ReActReasoning` for reasoning-then-acting decisions
- `move_one_step` and `teleport_to_location` tools for movement
- `DataCollector` for tracking segregation index over time

## What I learned building it

The LLM version produces weaker segregation than the rule-based version
under equivalent conditions. This makes intuitive sense: LLM agents weigh
multiple factors, not just neighbor composition. An agent might stay in a
mixed neighborhood because it values stability, even if the classic threshold
rule would tell it to move.

This is actually a more realistic model of human behavior. Real people don't
move purely based on neighbor ratios they consider moving costs, attachment,
and uncertainty. LLM agents naturally incorporate this complexity without
needing explicit parameters for each factor.

The interesting emergent pattern: LLM agents form smaller, more stable mixed
clusters rather than the large homogeneous patches the classic model produces.

## What was hard

The movement logic in `inbuilt_tools.py` had a coordinate system bug I
discovered while building this model agents were moving in the wrong
direction on real `OrthogonalMooreGrid` cells. Fixing this required
understanding how Mesa builds its internal cell graph, which was a deep
dive into the Mesa 4.x discrete space architecture.

## What I'd do differently

Add an explicit "attachment" parameter to the agent's internal state that
influences how reluctant it is to move. This would let researchers study
how place attachment affects segregation outcomes something the classic
model can't represent at all.

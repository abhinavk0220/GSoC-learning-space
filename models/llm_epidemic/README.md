# LLM Epidemic (SIR) Model

## What this model does

This model simulates disease spread through a population of LLM agents using
the classic SIR (Susceptible-Infected-Recovered) framework. Unlike rule-based
SIR models where infection probability is a fixed parameter, agents here
reason about their situation at each step deciding whether to isolate,
continue normal movement, or interact with others based on their health state
and knowledge of the outbreak.

Agents can be in one of three states: Susceptible, Infected, or Recovered.
Infected agents know their status and reason about whether to self-isolate.
Susceptible agents assess their risk based on neighbor states and decide how
cautiously to behave.

## Mesa features used

- `OrthogonalMooreGrid` for spatial population layout
- `LLMAgent` with `CoTReasoning` for multi-step health decision reasoning
- `internal_state` for tracking agent health status
- `move_one_step` tool for agent movement
- `DataCollector` for SIR curve tracking over time

## What I learned building it

The most striking result: LLM agents produce slower, flatter epidemic curves
than rule-based agents with equivalent transmission parameters. The reason is
behavioral heterogeneity some agents take the outbreak seriously and isolate
immediately, others rationalize continued normal behavior. This mirrors real
epidemic dynamics far better than homogeneous rule-based models.

The gap between *knowing* you are infected and *acting* on that knowledge is
where LLM reasoning becomes genuinely interesting. An agent with high
"social_value" in its internal state will reason differently about isolation
than one with high "risk_aversion" producing individual variation in
compliance that rule-based models can only approximate with population-level
parameters.

## What was hard

Calibrating the system prompt so agents behave plausibly was non-trivial.
Early versions produced agents that always isolated immediately (too
cautious) or never isolated (ignoring their health state entirely). The
right balance required iterating on how the observation is presented to
the agent what information it sees about itself and its neighbors.

## What I'd do differently

Add a vaccination mechanic where agents reason about whether to get
vaccinated based on perceived risk and social norms. This would make the
model directly comparable to published LLM agent epidemic research and
more useful as a research starting point.

# LLM Opinion Dynamics

## What this model does

This model simulates how opinions spread and evolve in a population of LLM
agents. Each agent holds an opinion on a topic and can communicate with its
neighbors. At each step, agents observe the opinions around them and use LLM
reasoning to decide whether to update their own position factoring in
social pressure, argument quality, and their own internal state.

The model is based on the classic Opinion Dynamics framework in ABM, where
macro-level consensus or polarization emerges from micro-level individual
interactions.

## Mesa features used

- `OrthogonalMooreGrid` for spatial agent placement
- `LLMAgent` with `CoTReasoning` for step-by-step opinion reasoning
- `speak_to` tool for agent-to-agent communication
- `DataCollector` for tracking opinion distribution over time

## What I learned building it

The most interesting finding: LLM agents are significantly more resistant to
opinion change than rule-based agents with equivalent parameters. A rule-based
agent updates its opinion if a threshold of neighbors disagree. An LLM agent
reasons about *why* its neighbors hold different opinions before deciding to
update — and often finds reasons to stay put.

This means LLM Opinion Dynamics produces more stable minority opinions than
the classical model. Small clusters of agents with strong reasoning can
maintain their position against majority pressure indefinitely.

I also learned that the system prompt design matters enormously. Framing the
agent as "open-minded" vs "confident in its views" produces dramatically
different macro outcomes a parameter that simply doesn't exist in rule-based
models.

## What was hard

Getting agents to produce consistent, parseable opinion updates was the main
challenge. LLMs sometimes reason themselves into nuanced positions that don't
map cleanly to a discrete opinion value. Handling this gracefully in the
simulation loop required careful prompt engineering.

## What I'd do differently

Add a visualization that shows opinion clusters forming in real time on the
grid. The spatial dimension of opinion spread is hard to see from data
collectors alone.

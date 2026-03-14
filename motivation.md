# Motivation

## Who I am

I'm Abhinav Kumar, an AI Engineer at LTIMindtree (since September 2025),
where I work on RAG architectures and agentic workflows for a client project
with Archer Daniels Midland (ADM). I graduated in 2025 from Sikkim Manipal
Institute of Technology with a B.Tech in AI and Data Science.

## How I found Mesa

I work on agentic systems professionally that's my day job. So when I was
looking at GSoC 2026 organizations, I wasn't looking for something to learn
from scratch. I was looking for something that connected to work I was
already doing.

I had been watching Mesa's GSoC projects since 2025. That year, mesa-llm was
created as a GSoC project the idea of bringing LLM agents into agent-based
simulations was exactly the intersection I was interested in. I watched it
develop through 2025, saw it remain experimental, and decided 2026 was the
right time to contribute. It wasn't a random choice. It was deliberate.

## Why mesa-llm and mesa-examples

I work with LLM agents at LTIMindtree every day. But professional agentic
work is mostly about pipelines RAG, tool use, orchestration. What Mesa-LLM
is trying to do is different and more interesting: agents that don't just
execute tasks but reason, negotiate, and adapt inside a simulation alongside
other agents.

The thing that genuinely excites me is what this unlocks for research. We
can't always run human trials. We can't test every social or economic theory
in the real world. But LLM agents in a simulation can stand in for humans in
ways rule-based agents never could. Classical ABM agents follow rules. LLM
agents reason. That's not a small difference it changes what questions you
can ask with a simulation.

Nobody has fully cracked this yet. Mesa-LLM is experimental. That's not a
warning to me, that's the point. I want to be part of figuring it out.

My interest splits roughly 65-35 between Mesa Examples Revival and Mesa-LLM
iteration. The examples side excites me more building models that
demonstrate what LLM agents can actually do, ideally sourced from real
research. But I've learned through contributing that you can't build good
examples without fixing the underlying library. The two are inseparable.

## What I've built so far

During this contribution sprint I built four LLM example models:

- **LLM Opinion Dynamics** — agents form and update opinions through LLM
  reasoning and neighbor influence. Emergent consensus or polarization
  arises from individual reasoning steps, not fixed rules.

- **LLM Schelling Segregation** — agents decide whether to move based on
  LLM-driven satisfaction reasoning. The model produces different
  segregation patterns than the rule-based version because agents reason
  rather than just check a threshold.

- **LLM Epidemic (SIR)** — agents reason about infection risk and decide
  whether to isolate or interact. The gap between "agent knows it's
  infected" and "agent acts on that knowledge" is where LLM reasoning
  becomes genuinely interesting.

- **LLM Prisoner's Dilemma** — agents negotiate cooperation vs defection
  across repeated interactions. LLM agents develop something resembling
  reputation and trust over time in a way rule-based agents don't.

Building these taught me how Mesa's pieces actually fit together spaces,
agent scheduling, data collection in a way that reading documentation
never could. It also showed me where mesa-llm has real friction points that
need fixing.

## What I want to work on this summer

My focus would be two things that reinforce each other:

**On the mesa-examples side:** Build a collection of LLM example models
sourced from real published research social dynamics, economic behavior,
epidemiology. Models that researchers could actually use as starting points
for their own work, with proper documentation and comparison against
non-LLM baselines to show what LLM agents add.

**On the mesa-llm side:** Help push it toward production stability. The
Mesa 4.x migration is partially done but not complete. Test coverage has
gaps. The reasoning architecture has rough edges I've found firsthand while
building models. These aren't abstract problems I've hit them, debugged
them, and fixed several already.

The goal by the end of summer: mesa-llm that researchers can actually
depend on, and a set of example models that show them why they'd want to.

I also intend to actively participate in peer reviews reading other
contributors' code, giving specific feedback, and engaging in the
collaborative side of open source. I've found that reviewing a PR teaches
me things about the codebase that writing one doesn't. That's not busywork,
it's how understanding actually deepens.

## What I struggled with and what it taught me

The biggest challenge was keeping up with upstream merges. Every time the
main repo updated, my branches would break especially around the Mesa 4.x
API migration where `mesa.space` was removed entirely. I had to iterate over
the same tests repeatedly just to stay current with a codebase that hadn't
merged my fixes yet.

The most interesting bug I found: `move_one_step()` was moving agents in the
wrong direction on real `OrthogonalMooreGrid` cells. The root cause was that
real Mesa cells and test dummy cells both have a `connections` dict, but with
incompatible coordinate conventions `(row, col)` internally vs `(x, y)` in
`_cells`. The fix required understanding how Mesa builds its cell graph
internally, not just reading the public API.

That kind of bug where the code looks right but the mental model is wrong 
is only findable by someone who actually builds things with the library. That's
what building models gives you. That's why I fully align with the
examples-first approach Ewout described building these models first is what
allowed me to find these core issues.

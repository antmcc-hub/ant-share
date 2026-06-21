Here is the clean provenance breakdown.

The spec-writing skill is not a straight copy of a standalone Nate repo skill. It is built from Nate B. Jones' specification and agent-communication patterns, then extended with our own execution architecture.

The source split is:

- **Specification Precision / Goal Prompt Generator:** Nate's framing. This is the underlying idea that good delegation starts with clear intent, constraints, proof, and a definition of done.
- **Stupid Button / Strategic Gate:** from Nate's PromptKit #161. That gave us the "should we even build/spec this?" pre-flight gate.
- **Model Router / Model Tiering:** also from Nate's PromptKit #161. That gave us the principle that different work should route to different model tiers based on cognitive load and risk.
- **Shape vs Execute / Six-Field Brief / Flashlight Must-Nots:** from Nate's PromptKit #247. That added the distinction between work that is ready to execute and work that still needs shaping, plus the idea that exclusions often matter as much as instructions.
- **Session planning and execution architecture:** our addition. The patterns like inline vs parallel vs sequential execution, run specs, permission boundaries, required proof, Day 0 probes, review budgets, source hierarchy, and closeout handoff were derived by applying Nate's gating/routing ideas to real multi-agent operating work.

So the short version is: Nate supplied the core specification discipline and routing primitives. We turned those into an operational skill for agent delegation, session planning, proof review, and repeatable closeout.


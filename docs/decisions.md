# Decision Log

Record accepted architectural and rules decisions here. Use short IDs so code, tests, and discussions can cite them. “Prototype” decisions are reversible hypotheses.

## Accepted

### DEC-001 — One command API for every controller

**Status:** Accepted, foundational.

Human, policy AI, scripted tests, replay, and future network clients submit the same typed commands. The simulation validates all commands.

**Consequences:** No controller-only powers; UI and AI need shared legal-action queries; controller changes do not alter the rules.

### DEC-002 — Headless authoritative simulation

**Status:** Accepted, foundational.

Rules and state transitions are independent of rendering and input.

**Consequences:** Enables automated tests, AI-vs-AI runs, replay, alternative clients, and eventual multiplayer. Presentation must not own combat truth.

### DEC-003 — Seeded, logged randomness

**Status:** Accepted, foundational.

All random draws use an injected versioned generator and appear in the causal log.

**Consequences:** Replays and debugging are practical. Changing RNG algorithm or draw order is a compatibility change.

### DEC-004 — Turn-based first prototype

**Status:** Accepted for prototype; reevaluate after premise test.

Use rolled initiative and discrete decisions rather than simultaneous or real-time-with-pause combat.

**Why now:** It isolates the manual/automation question, makes complete legal action selection tractable, and prevents timing/interface complexity from dominating the first test.

**Cost:** It does not yet test rapid mid-action intervention or simultaneous autonomous behavior.

### DEC-005 — Controller changes at decision boundaries

**Status:** Accepted for prototype.

A requested takeover or release becomes active at the next decision/reaction boundary, never halfway through resolution.

**Consequences:** Seamless and deterministic without rollback. The UI must clearly show pending control changes.

### DEC-006 — Ordered policy rules with candidate scoring

**Status:** Accepted for prototype.

Priority rules choose intent; scoring chooses among legal candidates within the first applicable rule.

**Consequences:** Explanations remain legible while targeting can still be tactical. A full behavior tree or planner is deferred.

### DEC-007 — Structured commands and atomic events

**Status:** Accepted.

Commands express intent; events record resolved facts. Human-readable combat logs are projections of structured events.

**Consequences:** Clear validation, replay, testing, and debugging at the cost of disciplined schema/version management.

### DEC-008 — Data-driven content over a general scripting language

**Status:** Accepted for prototype.

Representative abilities compose a small set of rule primitives. Add explicit hooks when necessary.

**Consequences:** Faster iteration and safer determinism. The model should not pretend every future ability can be represented without code.

## Proposed, awaiting evidence

### PROP-001 — Perfect information except occlusion

This keeps the first AI problem tactical rather than epistemic. Reconsider after hybrid control works.

### PROP-002 — One-tile creatures and flat maps

This sharply bounds pathing and targeting. Large creatures, elevation, and flight should be introduced only with dedicated tactical tests.

### PROP-003 — One nested reaction level

A bounded reaction stack tests counters and interception without risking pathological chains.

### PROP-004 — Every diagonal costs one tile

Simple and readable, but distorts circles and movement reach. Compare against alternating diagonal costs during grid playtests.

## Decision template

```markdown
### DEC-NNN — Title

**Status:** Proposed | Accepted | Rejected | Superseded

**Context:** What pressure created this choice?

**Options:** What credible alternatives exist?

**Decision:** What are we choosing, and for what scope?

**Consequences:** What improves, what worsens, and what becomes harder to change?

**Evidence/revisit trigger:** What test or milestone could change it?
```

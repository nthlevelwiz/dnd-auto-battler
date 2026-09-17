# Concise Design Specification

Status: **Prototype baseline**. Revisit after each playtest milestone.

## Vision

Build a party-based tactical RPG where controlling a character manually and automating that character are interchangeable controller choices over one rules engine. Automation is itself a tactical construction system: players express intent through inspectable policies rather than surrendering control to an opaque agent.

## Player experience

Before combat, the player builds characters and configures optional behavior policies. During combat, the player may:

- control all party members manually;
- assign AI per character;
- take over an AI character at its next decision boundary;
- return a character to AI control;
- pause at supported prompts to inspect state and issue commands;
- inspect every AI choice, rejected rule, score, and tie-break.

The first prototype is turn-based. “Pause” therefore means halting automatic advancement at a decision or reaction window, not freezing continuous simulation.

## Core loop

1. Load an encounter, party, automation policies, and random seed.
2. Determine initiative.
3. At each decision boundary, ask the actor’s current controller for a command.
4. Validate the command against the authoritative state.
5. Resolve it into atomic state changes and emitted events.
6. Open and resolve any reaction windows.
7. Append commands, random draws, events, and controller explanations to the log.
8. Continue until a victory or defeat condition is met.
9. Replay or compare the battle using the seed and command stream.

## Design pillars and constraints

| Pillar | Design consequence |
|---|---|
| Shared simulation | Controllers never mutate state and never bypass validation. |
| Full manual agency | The UI derives choices from the engine’s legal-action query. |
| Inspectable automation | Every AI decision produces a structured explanation. |
| Emergent synergy | Abilities operate on shared primitives: position, damage, conditions, surfaces, forced movement, visibility, and resources. |
| Determinism | All randomness comes from an injected, logged seeded source. |
| Small prototype | New content must test a system or a hybrid-control behavior. |

## Prototype rules stance

Keep mechanics that create spatial, timing, or resource decisions: initiative, movement, ranges, areas, reactions, concentration, conditions, limited resources, and risky saves.

Simplify mechanics that mostly compensate for tabletop constraints:

- use explicit grid distances and computed line of sight;
- calculate modifiers and effect durations automatically;
- enumerate legal targets rather than relying on conversational adjudication;
- replace ambiguous natural-language exceptions with composable data and explicit rule hooks.

Defer mechanics that add bookkeeping without yet testing the premise: ammunition counts, encumbrance, detailed components, food, travel pace, and long-term resting.

Use computer-only possibilities selectively: full causal logs, exact threat maps, projected action previews, exhaustive reaction prompts, policy traces, batch simulation, and deterministic replay.

## Representative content

Use mechanically distinct test pieces, not a balanced mini-campaign:

- **Guardian:** melee strike, intercept reaction, shove.
- **Skirmisher:** ranged attack, disengage-like quick action, positional bonus damage.
- **Controller:** cantrip, small area blast, concentration-based hindering zone, short teleport.
- **Support:** heal, protective mark, limited burst strike.
- **Enemies:** bruiser, archer, fragile caster, and simple swarm unit.
- **Environment:** wall, difficult ground, damaging hazard, and movable/triggerable object.

## Acceptance test

One authored encounter can be completed in manual, hybrid, and automatic modes without changing scenario or character definitions. Switching controllers never changes the action vocabulary or invalidates replay. At least two player-authored policies produce recognizably different behavior, and the log explains those differences.

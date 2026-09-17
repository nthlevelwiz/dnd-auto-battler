# Prototype Milestones

Each milestone should end in a runnable artifact and a short written finding. Do not add content unless it exercises the milestone’s system.

## M0 — Executable simulation skeleton

Deliver:

- versioned encounter state;
- typed command and event unions;
- seeded RNG service;
- append-only log;
- one actor able to end a turn;
- state checksum and replay test.

Exit test: given the same initial state, seed, and commands, two runs emit identical events and checksums.

## M1 — Spatial combat kernel

Deliver:

- square map, occupancy, walls, and difficult terrain;
- initiative and turn cursor;
- path validation and split movement;
- melee and ranged basic attacks;
- HP, defense, line of sight, range, and victory objective;
- CLI or developer harness.

Scenario: two allies versus two enemies around one wall.

Exit test: illegal paths and attacks are rejected with stable reasons; a recorded battle replays exactly.

## M2 — Shared controller boundary

Deliver:

- legal-action/candidate query;
- human controller adapter;
- deterministic scripted controller;
- controller assignment per character;
- controller-switch command effective at the next decision boundary;
- UI indicator for manual, AI, and pending control.

Scenario: manually move one character, allow another to act through a script, then exchange their controller assignments.

Exit test: both controllers submit the same command types and neither can bypass validation.

## M3 — First configurable automation

Deliver:

- ordered policy rules;
- conditions, candidate generators, scoring, thresholds, reserves, and stable tie-breaks;
- reaction-specific policy section;
- structured decision trace;
- two reusable role templates.

Tactical probes:

1. ranged unit maintains distance and chooses a legal target;
2. support heals only below its configured threshold;
3. controller uses an area effect only when target and friendly-fire thresholds pass.

Exit test: changing one visible policy parameter predictably changes behavior, and the trace explains both outcomes.

## M4 — Representative tactical depth

Deliver:

- primary/quick/reaction budgets;
- opportunity attack;
- one protective reaction;
- forced movement and damaging hazard;
- area targeting;
- conditions and explicit duration phases;
- concentration and interruption;
- limited resources.

Scenario: four-character party against a bruiser, archer, caster, and swarm around a chokepoint and hazard.

Exit test: at least three emergent combinations work without bespoke synergy bonuses, including forced movement into a hazard and protection of a fragile ranged ally.

## M5 — First playable interface

Deliver:

- readable grid and turn order;
- selection, paths, ranges, areas, and target preview;
- full legal manual action menu;
- per-character manual/AI toggle;
- pause-before-turn and manual reaction prompts;
- policy editor for supported controls;
- combat log and expandable AI explanation;
- restart with seed and replay controls.

Exit test: a new tester completes the same encounter fully manually, hybrid, and fully automated without developer assistance.

## M6 — Premise evaluation

Run structured playtests rather than expanding content.

Collect:

- time spent configuring versus fighting;
- frequency and reason for takeovers;
- reaction-prompt burden;
- whether explanations answer “why?”;
- policy mistakes players can diagnose;
- meaningful differences among manual, hybrid, and automatic outcomes;
- moments where literal tabletop rules create friction;
- desired automation expressiveness.

Decision gate:

- **Continue:** hybrid control is enjoyable and policies create a legible optimization game.
- **Revise:** core promise is attractive but handoff or policy authoring is cumbersome.
- **Stop/pivot:** automation removes rather than adds meaningful decisions.

Only after this gate choose the long-term time model, campaign loop, technology stack, and content-production strategy.

## First playable content budget

Hard cap before M6:

- 4 player characters;
- 4 enemy archetypes;
- 8–12 total active abilities;
- 4 terrain/object types;
- 1 authored encounter plus small tactical test fixtures;
- 2 reusable AI templates.

If a proposed feature does not help answer the premise, record it in a backlog rather than adding it.

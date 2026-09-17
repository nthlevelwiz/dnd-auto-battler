# Consequential Open Questions

Do not answer these all upfront. Resolve each with the cheapest prototype or playtest that exposes its consequences.

## Highest priority

| Question | Credible alternatives | Consequence | Earliest useful test |
|---|---|---|---|
| What is the long-term time model? | discrete initiative; phase/simultaneous turns; real-time with pause | Shapes controller cadence, reactions, path conflicts, UI, and replay | After the turn-based hybrid prototype is fun |
| How expressive should player automation become? | ordered rules; behavior tree; utility scorer; planner; restricted scripting | Trades accessibility and explainability against power | Policy milestone with 3 tactical probes |
| When may control switch? | next decision; next actor turn; interrupt at declared checkpoints; immediate rollback | Determines responsiveness and deterministic complexity | First UI handoff playtest |
| How are reactions presented? | always pause; policy-only; conditional prompts; limited reaction queue | Too many prompts make manual play tedious; too few reduce agency | Opportunity attack + intercept scenario |
| What information may AI use? | player-visible only; faction-shared perception; omniscient | Determines fairness and future stealth/visibility architecture | Before adding hidden information |
| How close should numerical rules remain to 5e? | recognizable baseline; heavily revised action economy; original system | Affects familiarity, balance burden, and identity | After basic movement/attack prototype |

## Tactical model

### Grid geometry

Options include square grid with simple diagonals, square grid with alternating diagonal cost, hexes, or continuous navigation. Square tiles are the prototype default, but area shape, reach, chokepoints, and UI precision should be compared before locking it down.

### Initiative and tempo

Rolled individual initiative is recognizable but can produce long gaps and focus-fire. Alternatives include side initiative, interleaving, action-time systems, and simultaneous planning. Any replacement must preserve clear manual takeover points and understandable reaction order.

### Movement commitment

Should movement be one committed path, stepwise commands, or freely splittable? Stepwise movement permits precise reaction and hazard choices but increases command volume and AI branching. The prototype can submit a full path while resolving it tile by tile.

### Reactions and interrupts

Which events can be interrupted, who gets priority, and can reactions trigger reactions? A universal stack is expressive but hard to explain. A small catalog of explicit windows may be better game design.

### Randomness and prediction

How much outcome probability should the UI and AI see? Exact probabilities improve inspectability, while detailed expected-value previews may turn play into calculation. Decide whether AI is allowed deterministic expectation calculations that the UI does not surface.

### Friendly fire

Should area abilities permit ally targets, penalize them, or forbid them? The rules engine should permit mechanically valid friendly fire; controller policies decide acceptability. Content can still define explicitly selective effects.

### Downed characters and lethality

Death saves are suspenseful at a table but may encourage repetitive stabilization routines in an automated party. Alternatives include a short bleed-out timer, injuries, encounter defeat states, or immediate death for some units.

## Automation UX

- Are policies edited per character, per role, per party, or inherited across all three?
- Should policy order be strictly first-match, weighted, or a visible combination?
- How are spatial goals expressed without requiring programming?
- Can a player issue temporary directives without changing the saved policy?
- Should resource reserves be absolute, percentage-based, encounter-aware, or rest-aware?
- How do policies refer safely to changing party members and ability loadouts?
- When should the AI ask the player rather than use a weak fallback?
- How much explanation is useful during play versus in a post-battle debugger?

## Rules and content extensibility

- Which effects can remain data and which require code hooks?
- Do effect hooks form an ordered stack, event subscriptions, or explicit resolution stages?
- How are content and replay schemas migrated?
- Can mods add deterministic code safely?
- How should conflicting replacement effects resolve?
- Is an ability definition declarative enough to preview accurately?

## Campaign-facing questions to defer

- party size and reserve roster;
- permanent death and replacement;
- rest cadence and attrition;
- procedural versus authored encounters;
- recruitment and personality;
- economy, loot, and crafting;
- progression ceiling and multiclassing;
- injury persistence.

These should not shape the first engine beyond stable character IDs, persistent loadout-ready definitions, and serializable post-encounter state.

## Poor literal imports to watch

- **Natural-language exception density:** expensive to validate, preview, and automate.
- **Death-save loops:** dramatic socially, potentially rote in repeated computer battles.
- **Rest-balanced resources:** meaningless until encounter cadence exists.
- **Bonus-action wording and spell restrictions:** may be legacy balance patches rather than intrinsically good action design.
- **Grid approximations built for miniatures:** computers can calculate geometry, but precision may reduce readability.
- **Unlimited conversational adjudication:** must become explicit rules, bounded choices, or authored exceptions.
- **Summon micromanagement:** automation makes larger groups possible, but turn duration and visual clarity still matter.

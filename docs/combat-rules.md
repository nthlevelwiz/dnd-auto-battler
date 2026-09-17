# Prototype Combat Rules

These are provisional rules designed to test hybrid control, not a commitment to reproduce a tabletop ruleset.

## Space and time

- Square grid; one tile is the basic spatial unit.
- Creatures occupy one tile in the first prototype.
- Diagonal movement uses a fixed, documented cost. Initial recommendation: every diagonal costs 1 tile for legibility; test the geometric distortion before considering alternating costs.
- Combat proceeds in rounds with rolled initiative and stable tie-breakers.
- A turn contains movement, one primary action, one quick action, and possible reactions outside the turn.
- Movement may be split around actions.

## State visible to controllers

Prototype combat uses perfect information except for line-of-sight occlusion. Hidden enemies, stealth, sound propagation, and fog-of-war are later experiments because they introduce a separate perception problem.

## Movement and positioning

- Movement follows a shortest legal path chosen or confirmed by the controller.
- Occupied and blocking tiles cannot be entered.
- Difficult terrain increases movement cost.
- Leaving a threatened tile without a safe-step/disengage effect opens an opportunity-reaction window.
- Forced movement does not trigger opportunity attacks by default.
- Forced movement can move a target into hazards if the effect and destination are legal.

## Attacks and defenses

- Attacks declare actor, target, source, and relevant mode.
- Range, line of sight, action budget, resources, and target validity are checked before resolution.
- Attack rolls compare against defense; saves compare against a difficulty value.
- Natural extremes may provide critical success/failure behavior, but only if playtesting shows the extra variance improves decisions.
- Cover is computed from geometry. Begin with none/partial/full rather than multiple stacking modifiers.
- Damage cannot be applied without a logged source and typed damage packet.

## Action economy

Each actor normally receives per turn:

- movement allowance;
- one primary action;
- one quick action;
- one reaction refreshed at the start of its turn.

An ability declares what budget it consumes. “Free” actions must specify a frequency limit to avoid unbounded command loops.

## Reactions

A reaction is an ability eligible during a declared trigger window. Examples:

- opportunity attack after threatened movement is declared;
- intercept when a nearby ally would take attack damage;
- counter-like response when an observed spell is committed.

Triggers occur before or after a specific event, never “whenever appropriate.” Manual controllers may pause for eligible reactions; AI controllers consult reaction policy. The log records offered, declined, invalidated, and taken reactions.

## Effects, conditions, and concentration

Effects have a source, targets, duration policy, stacking rule, tags, and lifecycle hooks. Durations expire at an explicit phase.

A character can maintain one concentration effect. Taking damage prompts a concentration save. Starting a new concentration effect ends the old one. Incapacitation ends concentration.

Prototype conditions: prone, hindered, guarded, burning, unconscious, and one control condition. Each is defined mechanically rather than by prose inheritance.

## HP, unconsciousness, and defeat

- At 0 HP, a player character becomes unconscious.
- Further damage and recovery use a deliberately simplified rule until lethality goals are chosen.
- Enemies may be removed at 0 HP unless an encounter needs surrender or revival.
- An encounter ends when a declared objective is satisfied, not necessarily when every opponent dies.

## Representative abilities

| Ability | Systems exercised |
|---|---|
| Strike | melee targeting, attack, damage |
| Bow shot | range, line of sight, cover |
| Shove | save, forced movement, hazard |
| Intercept | reaction window, damage modification |
| Hindering zone | area, concentration, persistent terrain effect |
| Burst spell | area targeting, friendly-fire policy |
| Short teleport | alternate movement, occupancy |
| Healing touch | resources, ally targeting, unconscious recovery |

## Explicitly deferred

- multiclass progression and full character creation;
- stealth and uncertain information;
- grappling beyond a single test ability;
- flying and verticality;
- ammunition, encumbrance, and detailed inventory actions;
- readying arbitrary actions;
- simultaneous turns;
- unrestricted nested reactions;
- long-rest/short-rest campaign tuning.

## Computer-native opportunities to evaluate later

- exact movement interruption and facing;
- sound and visibility fields;
- destructible and spreading environmental effects;
- morale and surrender;
- large summon groups controlled by compact policy templates;
- detailed injury and persistent-effect simulation;
- richer reactions without tabletop slowdown.

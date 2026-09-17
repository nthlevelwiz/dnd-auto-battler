# Character and Action Data Model

The model separates authored definitions from mutable encounter state. Names are illustrative; exact language and serialization format remain implementation choices.

## Identity and definitions

Every entity and definition has a stable ID. Commands and events refer to IDs, never display names.

### Character definition

```text
CharacterDefinition
  id
  name
  species/background presentation
  level/build metadata
  base attributes
  proficiencies/tags
  ability_definition_ids
  equipment_definition_ids
  base movement and defenses
```

The prototype may author four fixed characters while retaining this shape. Full classes, subclasses, feats, and multiclassing are deferred.

### Ability definition

```text
AbilityDefinition
  id
  name
  action_cost
  targeting_spec
  requirements[]
  resource_costs[]
  effects[]
  concentration
  trigger_spec?       // reactions only
  AI annotations      // intent tags, not privileged logic
```

Effects should compose from a deliberately small vocabulary: roll attack, roll save, deal/heal damage, add/remove condition, move entity, create/remove zone, spend/restore resource, and modify an event.

## Runtime state

```text
EncounterState
  schema_version
  rules_version
  seed_metadata
  round and turn cursor
  map_state
  entities_by_id
  zones_by_id
  pending_resolution
  reaction_stack
  objectives
  outcome?
```

```text
CharacterState
  definition_id
  faction
  position
  hp
  resources
  conditions/effects
  concentration_effect_id?
  action_budget
  controller_assignment
  alive/conscious status
```

Controller configuration is runtime state because switching control must be replayable. Policy definitions can be external assets referenced by versioned ID.

## Commands

Use a tagged union with a shared envelope:

```text
CommandEnvelope
  command_id
  actor_id
  expected_state_revision
  type
  payload
```

Prototype commands:

```text
MovePath(actor, path)
UseAbility(actor, ability_id, targets, placement?)
EndTurn(actor)
RespondToReaction(actor, reaction_id, choice, targets?)
SetController(character, controller_spec, effective_boundary)
```

Prefer `UseAbility` over separate hard-coded attack/spell/item commands inside the engine. Presentation may offer friendlier constructors such as `Attack` or `CastSpell`, but they compile into the same ability command.

The expected state revision prevents stale UI or AI choices from being silently applied after a reaction or state change.

## Validation result

```text
ValidationResult
  accepted
  errors[]             // stable code + human-readable context
  normalized_command? // canonical path/target ordering
  preview?             // costs and projected non-random effects
```

Validation is pure and reusable by the UI and AI, but only final submission is authoritative. Legal-action enumeration should use the same predicates to avoid drift.

## Events

Events are atomic facts, not prose log lines:

- `TurnStarted`
- `MovementSpent`
- `EntityMoved`
- `AbilityCommitted`
- `ResourceSpent`
- `AttackRolled`
- `SaveRolled`
- `DamageApplied`
- `ConditionAdded`
- `ReactionWindowOpened`
- `ReactionChosen`
- `ConcentrationEnded`
- `EntityDowned`
- `ObjectiveCompleted`
- `ControllerChanged`
- `TurnEnded`

Human-readable combat text is derived from events. This supports localization, replay inspection, tests, and alternate presentations.

## Observations and information boundaries

Controllers consume an `Observation`, not the raw state. Initially it can contain all non-occluded encounter information. Defining this boundary now prevents later AI from accidentally cheating when stealth or hidden information is introduced.

## Policy model

```text
Policy
  id and version
  rules[]              // ordered
  fallback
  tie_breaker

Rule
  label
  enabled
  when[]               // predicates over observation/candidate
  consider             // candidate generator
  score/priority
  limits               // resource and risk constraints
```

A policy selects only among commands produced by legal candidate generation. AI annotations on abilities may describe facts such as `damage`, `healing`, `mobility`, `area`, or `concentration`; they do not grant behavior or legality.

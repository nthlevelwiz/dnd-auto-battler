# Automation Design

## Goal

Automation should feel like programming a tactical doctrine, not toggling “play well.” A useful system supports novice presets and increasingly expressive policies without hiding the causal chain.

## Prototype policy language

Use ordered rules with explicit eligibility conditions, candidate generation, scoring, and resource constraints.

```text
WHEN <conditions>
CONSIDER <action family>
TARGET BY <scoring terms>
SUBJECT TO <limits>
```

Example:

```text
Rule: Safe area blast
WHEN enemies_in_area >= 3
CONSIDER abilities tagged area_damage
TARGET BY enemy_value_hit - 2 * ally_value_hit
SUBJECT TO ally_value_hit == 0
            reserve spell_slots >= 1
```

Ordered rules are easier to author and explain than an unrestricted behavior tree. Candidate scoring within a rule avoids brittle “first target” behavior. The two mechanisms should remain visibly distinct: priority chooses the intent; scoring chooses the execution.

## Evaluation pipeline

1. Query the engine for legal commands/candidate parameters.
2. Derive tactical facts from the current observation: threat, distance, expected targets, ally risk, objective value.
3. Evaluate enabled rules in priority order.
4. For the first rule with acceptable candidates, score candidates.
5. Apply stable tie-breaking.
6. Return the command plus a structured trace.
7. If no rule matches, execute the explicit fallback or request player input.

AI must never manufacture commands and ask validation to filter thousands of nonsense combinations. The engine should expose bounded candidate generators using the same legality predicates as manual UI queries.

## Explanation trace

Every choice records:

- observation/state revision;
- rules checked in order;
- why each rule failed or succeeded;
- candidates considered;
- important score components;
- constraints that rejected candidates;
- selected command and tie-break;
- random choice, if a policy intentionally uses one.

Example UI summary:

> Used **Hindering Zone** under “Protect backline”: 3 enemies could reach the archer; this placement reduced projected approaches by 2. Fire Burst was skipped because it would hit one protected ally.

The trace is diagnostic metadata, not part of authoritative resolution.

## Initial configurable controls

- rule order and enable/disable;
- protected allies;
- focus-target preference;
- HP thresholds for healing or retreat;
- minimum targets for area abilities;
- acceptable friendly-fire value;
- per-resource reserve;
- preferred distance band;
- reaction policies;
- concentration replacement threshold;
- risk stance: conservative, neutral, aggressive.

## Manual/AI handoff

- Controller assignment is checked at every decision and reaction boundary.
- A takeover during an action queues for the next boundary.
- The player can mark “pause before this character acts.”
- Returning control to AI uses the currently selected policy immediately at the next boundary.
- Manual commands do not rewrite the policy or cause the AI to infer new intent.
- Optional one-turn directives such as “focus this target” should be represented as explicit temporary policy overrides and logged.

## Reaction policies

Reactions need separate policy because their opportunity cost is time-sensitive:

```text
Counter dangerous spell if:
  estimated threat >= threshold
  and resource after use >= reserve
  and caster is observable

Use burst-on-critical if:
  target priority >= threshold
  and projected damage is not excessive overkill
```

A manual reaction prompt should include the same tactical facts used by automation, not only a yes/no question.

## What not to build yet

- natural-language policy authoring;
- arbitrary user code;
- machine-learned controllers;
- long-horizon planning across many turns;
- unrestricted behavior-tree editor;
- policies that inspect hidden authoritative state;
- a single opaque “AI difficulty” knob.

## Evaluation

Measure policy usefulness with authored tactical probes:

- avoids friendly fire;
- preserves a limited resource until its threshold is met;
- protects a marked ally;
- reacts correctly when the best target changes;
- handles no-valid-action cases;
- produces identical choices for identical state and policy;
- changes behavior after a documented policy change;
- explains each result in terms the player configured.

Batch simulation can reveal degenerate policies and balance outliers. Human playtesting determines whether configuring the policies is understandable and satisfying.

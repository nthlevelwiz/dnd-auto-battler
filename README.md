# D&D-Inspired Tactical Autobattler

A tactical party RPG in which **manual control and programmable automation use the same combat simulation**.

The project tests one central question:

> Is deep tabletop-style tactical combat compelling when the player can fluidly move between choosing every action and programming a party to fight autonomously?

## Run the Python prototype

Requires Python 3.11+ and Tkinter (usually included with Python; on Debian/Ubuntu install `python3-tk`).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
dnd-auto-battler --seed 7
```

The interface uses chat for commands, status, rules feedback, combat narration, and AI explanations. When the game asks a spatial question—where to move or who to attack—select the highlighted answer on the tactical grid.

Chat commands:

- `help`, `status`
- `manual <unit-id>`, `auto <unit-id>`
- `move`, `attack`, `end`

Run tests with `pytest`.

## Product pillars

1. **One authoritative simulation.** Human and AI controllers submit the same structured commands. The rules engine validates all commands.
2. **Manual control is complete.** A player can inspect and select the full legal action space for any player character.
3. **Automation is authored, not mysterious.** Players configure priorities, conditions, targets, and resource policies, and can inspect why an action was selected.
4. **Systemic interactions beat collection bonuses.** Party synergies emerge from positioning, conditions, terrain, timing, and abilities.
5. **Deterministic by default.** A seed plus an ordered command stream should reproduce a battle.
6. **Prototype the question, not the content catalog.** The first playable contains only enough rules and content to test hybrid control.

## First playable

A headless rules engine with a minimal tactical interface:

- square grid with blocking and hazardous terrain;
- 2–4 persistent player characters and 3–6 enemies;
- rolled initiative and discrete turns;
- movement, action, bonus-action-like quick action, and reaction;
- melee and ranged attacks, HP, defense, saves, unconsciousness, and victory;
- opportunity attacks, concentration, forced movement, and a few representative abilities;
- manual or configurable AI control per character;
- seamless control changes at safe decision boundaries;
- seeded randomness, structured combat log, replay, and AI decision explanations.

The current code is an intentionally narrower vertical slice: grid movement/pathing, initiative, melee/ranged attacks, HP/armor, obstacles, hazards, seeded rolls, manual/AI switching, a chat log, and explainable first-match AI. The remaining items above are milestone targets.

## Living documents

- [Concise design specification](docs/design-spec.md)
- [Architecture](docs/architecture.md)
- [Combat rules](docs/combat-rules.md)
- [Character and action data model](docs/data-model.md)
- [Automation design](docs/automation.md)
- [Decision log](docs/decisions.md)
- [Open questions](docs/open-questions.md)
- [Prototype milestones](docs/milestones.md)

## Immediate success criteria

The prototype succeeds when a player can run the same encounter in three ways—fully manual, hybrid, and fully automated—and each mode:

- exposes the same legal actions;
- produces a replayable event stream;
- permits useful, understandable automation;
- creates materially different tactical outcomes from different policies;
- makes taking over or returning control feel predictable.

## Non-goals

This is not an implementation of any licensed tabletop rules text. Familiar genre mechanics are starting hypotheses and should be retained only when they create useful computer-game decisions.

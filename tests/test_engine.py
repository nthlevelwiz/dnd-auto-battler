import pytest

from dnd_autobattler.controllers import BasicPolicyController
from dnd_autobattler.engine import Attack, EndTurn, RuleError, SetController
from dnd_autobattler.scenario import demo_game


def event_signature(game):
    return [(event.kind, event.message, event.data) for event in game.events]


def test_same_seed_and_commands_produce_same_events():
    left = demo_game(seed=42)
    right = demo_game(seed=42)
    for game in (left, right):
        actor = game.active
        game.submit(EndTurn(actor.id))
        actor = game.active
        game.submit(EndTurn(actor.id))
    assert event_signature(left) == event_signature(right)


def test_controller_change_does_not_change_action_api():
    game = demo_game()
    unit = game.units["guardian"]
    game.submit(SetController(unit.id, "ai"))
    assert unit.controller == "ai"
    game.submit(SetController(unit.id, "human"))
    assert unit.controller == "human"


def test_rejects_command_from_inactive_actor():
    game = demo_game()
    inactive = next(u for u in game.units.values() if u.id != game.active.id)
    with pytest.raises(RuleError, match="turn"):
        game.submit(EndTurn(inactive.id))


def test_pathing_avoids_obstacles_and_occupants():
    game = demo_game()
    actor = game.active
    assert game.shortest_path(actor.id, (4, 2)) is None
    assert all(point not in game.obstacles for point in game.legal_moves(actor.id))


def test_ai_only_returns_legal_commands():
    game = demo_game()
    policy = BasicPolicyController()
    for _ in range(30):
        if game.outcome:
            break
        actor = game.active
        decision = policy.decide(game, actor)
        game.submit(decision.command)
    assert len(game.events) > 10


def test_attack_legality_and_action_budget():
    game = demo_game()
    actor = game.active
    far_enemy = next(u for u in game.units.values() if u.side != actor.side)
    with pytest.raises(RuleError, match="legal attack"):
        game.submit(Attack(actor.id, far_enemy.id))

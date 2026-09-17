from __future__ import annotations

from .engine import Attack, Decision, EndTurn, Game, Move, Unit


class BasicPolicyController:
    """Readable first-match policy: attack, approach, otherwise end turn."""

    def decide(self, game: Game, actor: Unit) -> Decision:
        if actor.acted:
            return Decision(EndTurn(actor.id), "Rule 0: the primary action is spent; end turn.")

        targets = game.legal_targets(actor.id)
        if targets:
            target_id = min(targets, key=lambda uid: (game.units[uid].hp, uid))
            target = game.units[target_id]
            return Decision(
                Attack(actor.id, target_id),
                f"Rule 1: attack an enemy in range. Chose {target.name} because it has the lowest HP ({target.hp}).",
            )

        enemies = [u for u in game.units.values() if u.alive and u.side != actor.side]
        moves = game.legal_moves(actor.id)
        if enemies and moves:
            destination = min(
                moves,
                key=lambda p: (min(game.distance(p, enemy.position) for enemy in enemies), p[1], p[0]),
            )
            nearest = min(enemies, key=lambda enemy: (game.distance(destination, enemy.position), enemy.id))
            return Decision(
                Move(actor.id, destination),
                f"Rule 2: approach the nearest enemy. {destination} leaves distance "
                f"{game.distance(destination, nearest.position)} to {nearest.name}.",
            )

        return Decision(EndTurn(actor.id), "Fallback: no useful legal move or attack; end turn.")

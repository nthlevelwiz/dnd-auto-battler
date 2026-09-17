from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
import random
from typing import Literal, Protocol, TypeAlias

Point: TypeAlias = tuple[int, int]
Side = Literal["heroes", "enemies"]
ControllerKind = Literal["human", "ai"]


@dataclass(slots=True)
class Unit:
    id: str
    name: str
    side: Side
    position: Point
    hp: int
    max_hp: int
    armor: int
    move_speed: int = 5
    attack_range: int = 1
    attack_bonus: int = 4
    damage_bonus: int = 2
    controller: ControllerKind = "ai"
    moved: int = 0
    acted: bool = False

    @property
    def alive(self) -> bool:
        return self.hp > 0


@dataclass(frozen=True, slots=True)
class Move:
    actor_id: str
    destination: Point


@dataclass(frozen=True, slots=True)
class Attack:
    actor_id: str
    target_id: str


@dataclass(frozen=True, slots=True)
class EndTurn:
    actor_id: str


@dataclass(frozen=True, slots=True)
class SetController:
    actor_id: str
    controller: ControllerKind


Command: TypeAlias = Move | Attack | EndTurn | SetController


@dataclass(frozen=True, slots=True)
class Event:
    kind: str
    message: str
    data: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Decision:
    command: Command
    explanation: str


class Controller(Protocol):
    def decide(self, game: "Game", actor: Unit) -> Decision: ...


class RuleError(ValueError):
    """A rejected command with a player-readable reason."""


class Game:
    """Authoritative combat simulation. UI and AI only submit commands."""

    DIRECTIONS: tuple[Point, ...] = (
        (-1, -1), (0, -1), (1, -1),
        (-1, 0),            (1, 0),
        (-1, 1),  (0, 1),  (1, 1),
    )

    def __init__(
        self,
        width: int,
        height: int,
        units: list[Unit],
        obstacles: set[Point] | None = None,
        hazards: set[Point] | None = None,
        seed: int = 1,
    ) -> None:
        self.width = width
        self.height = height
        self.units = {unit.id: unit for unit in units}
        self.obstacles = obstacles or set()
        self.hazards = hazards or set()
        self.seed = seed
        self.rng = random.Random(seed)
        self.events: list[Event] = []
        self.round = 1
        self.revision = 0
        initiative = [(self._roll("initiative", unit.id, 20), unit.id) for unit in units]
        self.initiative = [uid for _, uid in sorted(initiative, key=lambda x: (-x[0], x[1]))]
        self.turn_index = 0
        self._skip_dead()
        self._emit("combat_started", f"Combat begins (seed {seed}).")
        self._emit("turn_started", f"{self.active.name}'s turn.", actor=self.active.id)

    @property
    def active(self) -> Unit:
        return self.units[self.initiative[self.turn_index]]

    @property
    def outcome(self) -> Side | None:
        living = {u.side for u in self.units.values() if u.alive}
        if living == {"heroes"}:
            return "heroes"
        if living == {"enemies"}:
            return "enemies"
        return None

    def _emit(self, kind: str, message: str, **data: object) -> None:
        self.events.append(Event(kind, message, data))

    def _roll(self, purpose: str, actor_id: str, sides: int) -> int:
        result = self.rng.randint(1, sides)
        self._emit(
            "random_roll",
            f"{actor_id} rolled {result} on d{sides} for {purpose}.",
            actor=actor_id,
            purpose=purpose,
            sides=sides,
            result=result,
        )
        return result

    def in_bounds(self, point: Point) -> bool:
        return 0 <= point[0] < self.width and 0 <= point[1] < self.height

    def occupied(self, ignore: str | None = None) -> set[Point]:
        return {u.position for u in self.units.values() if u.alive and u.id != ignore}

    @staticmethod
    def distance(a: Point, b: Point) -> int:
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))

    def shortest_path(self, actor_id: str, destination: Point) -> list[Point] | None:
        actor = self.units[actor_id]
        blocked = self.obstacles | self.occupied(ignore=actor_id)
        if not self.in_bounds(destination) or destination in blocked:
            return None
        queue: deque[tuple[Point, list[Point]]] = deque([(actor.position, [])])
        seen = {actor.position}
        while queue:
            point, path = queue.popleft()
            if point == destination:
                return path
            for dx, dy in self.DIRECTIONS:
                nxt = (point[0] + dx, point[1] + dy)
                if self.in_bounds(nxt) and nxt not in blocked and nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, [*path, nxt]))
        return None

    def legal_moves(self, actor_id: str) -> list[Point]:
        actor = self.units[actor_id]
        remaining = actor.move_speed - actor.moved
        result: list[Point] = []
        for y in range(self.height):
            for x in range(self.width):
                path = self.shortest_path(actor_id, (x, y))
                if path is not None and 0 < len(path) <= remaining:
                    result.append((x, y))
        return result

    def legal_targets(self, actor_id: str) -> list[str]:
        actor = self.units[actor_id]
        if actor.acted:
            return []
        return [
            unit.id
            for unit in self.units.values()
            if unit.alive
            and unit.side != actor.side
            and self.distance(actor.position, unit.position) <= actor.attack_range
        ]

    def submit(self, command: Command) -> list[Event]:
        before = len(self.events)
        if isinstance(command, SetController):
            unit = self._unit(command.actor_id)
            unit.controller = command.controller
            self._emit(
                "controller_changed",
                f"{unit.name} is now {command.controller}-controlled.",
                actor=unit.id,
                controller=command.controller,
            )
        else:
            actor = self._unit(command.actor_id)
            if actor.id != self.active.id:
                raise RuleError(f"It is {self.active.name}'s turn, not {actor.name}'s.")
            if isinstance(command, Move):
                self._move(actor, command.destination)
            elif isinstance(command, Attack):
                self._attack(actor, command.target_id)
            elif isinstance(command, EndTurn):
                self._end_turn(actor)
        self.revision += 1
        return self.events[before:]

    def _unit(self, unit_id: str) -> Unit:
        try:
            return self.units[unit_id]
        except KeyError as exc:
            raise RuleError(f"Unknown unit: {unit_id}") from exc

    def _move(self, actor: Unit, destination: Point) -> None:
        path = self.shortest_path(actor.id, destination)
        if path is None:
            raise RuleError("That tile is blocked or unreachable.")
        remaining = actor.move_speed - actor.moved
        if not path or len(path) > remaining:
            raise RuleError(f"Destination costs {len(path)} movement; {remaining} remains.")
        origin = actor.position
        actor.position = destination
        actor.moved += len(path)
        self._emit(
            "unit_moved",
            f"{actor.name} moves from {origin} to {destination}.",
            actor=actor.id,
            origin=origin,
            destination=destination,
            path=path,
        )
        if destination in self.hazards:
            actor.hp = max(0, actor.hp - 2)
            self._emit(
                "damage_applied",
                f"{actor.name} takes 2 hazard damage.",
                target=actor.id,
                amount=2,
                source="hazard",
            )

    def _attack(self, actor: Unit, target_id: str) -> None:
        if target_id not in self.legal_targets(actor.id):
            raise RuleError("Target is not a legal attack target.")
        target = self._unit(target_id)
        roll = self._roll("attack", actor.id, 20)
        total = roll + actor.attack_bonus
        actor.acted = True
        self._emit(
            "attack_rolled",
            f"{actor.name} attacks {target.name}: {roll} + {actor.attack_bonus} = {total}.",
            actor=actor.id,
            target=target.id,
            roll=roll,
            total=total,
        )
        if total >= target.armor:
            damage_roll = self._roll("damage", actor.id, 6)
            damage = damage_roll + actor.damage_bonus
            target.hp = max(0, target.hp - damage)
            self._emit(
                "damage_applied",
                f"Hit: {target.name} takes {damage} damage ({target.hp}/{target.max_hp} HP).",
                actor=actor.id,
                target=target.id,
                amount=damage,
            )
            if not target.alive:
                self._emit("unit_downed", f"{target.name} is down.", target=target.id)
        else:
            self._emit(
                "attack_missed",
                f"{actor.name} misses {target.name}.",
                actor=actor.id,
                target=target.id,
            )

    def _end_turn(self, actor: Unit) -> None:
        self._emit("turn_ended", f"{actor.name} ends their turn.", actor=actor.id)
        actor.moved = 0
        actor.acted = False
        self.turn_index += 1
        if self.turn_index >= len(self.initiative):
            self.turn_index = 0
            self.round += 1
            self._emit("round_started", f"Round {self.round} begins.", round=self.round)
        self._skip_dead()
        if self.outcome:
            self._emit("combat_ended", f"{self.outcome.title()} win.", winner=self.outcome)
        else:
            self._emit("turn_started", f"{self.active.name}'s turn.", actor=self.active.id)

    def _skip_dead(self) -> None:
        checked = 0
        while self.initiative and not self.active.alive and checked < len(self.initiative):
            self.turn_index = (self.turn_index + 1) % len(self.initiative)
            checked += 1

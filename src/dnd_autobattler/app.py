from __future__ import annotations

import argparse
import tkinter as tk
from tkinter import ttk

from .controllers import BasicPolicyController
from .engine import Attack, EndTurn, Game, Move, RuleError, SetController
from .scenario import demo_game


class TacticalApp:
    CELL = 64
    COLORS = {
        "floor": "#202632",
        "grid": "#465063",
        "obstacle": "#11151c",
        "hazard": "#9b4d20",
        "heroes": "#4ea1ff",
        "enemies": "#e15d68",
        "legal": "#4f784e",
        "selected": "#f0c75e",
    }

    def __init__(self, root: tk.Tk, game: Game) -> None:
        self.root = root
        self.game = game
        self.policy = BasicPolicyController()
        self.mode: str | None = None
        self.shown_events = 0
        root.title("Tactical Autobattler Prototype")
        root.geometry("1120x680")

        self.canvas = tk.Canvas(
            root,
            width=game.width * self.CELL,
            height=game.height * self.CELL,
            bg=self.COLORS["floor"],
            highlightthickness=0,
        )
        self.canvas.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.canvas.bind("<Button-1>", self.on_grid_click)

        side = ttk.Frame(root, padding=10)
        side.grid(row=0, column=1, sticky="nsew")
        self.status = ttk.Label(side, text="", justify="left")
        self.status.pack(fill="x")

        controls = ttk.Frame(side)
        controls.pack(fill="x", pady=8)
        ttk.Button(controls, text="Move", command=lambda: self.choose("move")).pack(side="left")
        ttk.Button(controls, text="Attack", command=lambda: self.choose("attack")).pack(side="left")
        ttk.Button(controls, text="End turn", command=self.end_turn).pack(side="left")
        ttk.Button(controls, text="AI this turn", command=self.ai_once).pack(side="left")

        self.chat = tk.Text(
            side,
            height=22,
            width=54,
            state="disabled",
            wrap="word",
            bg="#12161d",
            fg="#e8edf4",
            insertbackground="white",
        )
        self.chat.pack(fill="both", expand=True)

        entry_row = ttk.Frame(side)
        entry_row.pack(fill="x", pady=(8, 0))
        self.entry = ttk.Entry(entry_row)
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.on_chat_command)
        ttk.Button(entry_row, text="Send", command=self.on_chat_command).pack(side="left")

        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)
        self.say(
            "System",
            "Click Move or Attack, then answer spatial questions on the grid. "
            "Use chat for help, status, manual <unit>, auto <unit>, or end.",
        )
        self.refresh()
        self.root.after(250, self.advance_ai)

    def say(self, speaker: str, message: str) -> None:
        self.chat.configure(state="normal")
        self.chat.insert("end", f"{speaker}: {message}\n")
        self.chat.see("end")
        self.chat.configure(state="disabled")

    def refresh(self) -> None:
        self.draw_grid()
        active = self.game.active
        self.status.configure(
            text=(
                f"Round {self.game.round}  •  Active: {active.name}\n"
                f"HP {active.hp}/{active.max_hp}  •  Move {active.move_speed - active.moved}  "
                f"•  Action {'spent' if active.acted else 'ready'}  •  {active.controller.upper()}"
            )
        )
        while self.shown_events < len(self.game.events):
            event = self.game.events[self.shown_events]
            self.shown_events += 1
            if event.kind != "random_roll":
                self.say("Combat", event.message)

    def draw_grid(self) -> None:
        self.canvas.delete("all")
        legal: set[tuple[int, int]] = set()
        if self.mode == "move":
            legal = set(self.game.legal_moves(self.game.active.id))
        elif self.mode == "attack":
            legal = {
                self.game.units[uid].position
                for uid in self.game.legal_targets(self.game.active.id)
            }
        for y in range(self.game.height):
            for x in range(self.game.width):
                point = (x, y)
                fill = self.COLORS["floor"]
                if point in self.game.obstacles:
                    fill = self.COLORS["obstacle"]
                elif point in self.game.hazards:
                    fill = self.COLORS["hazard"]
                elif point in legal:
                    fill = self.COLORS["legal"]
                x0, y0 = x * self.CELL, y * self.CELL
                self.canvas.create_rectangle(
                    x0,
                    y0,
                    x0 + self.CELL,
                    y0 + self.CELL,
                    fill=fill,
                    outline=self.COLORS["grid"],
                )
        for unit in self.game.units.values():
            if not unit.alive:
                continue
            x, y = unit.position
            pad = 8
            color = self.COLORS[unit.side]
            outline = (
                self.COLORS["selected"]
                if unit.id == self.game.active.id
                else "#dbe4ef"
            )
            self.canvas.create_oval(
                x * self.CELL + pad,
                y * self.CELL + pad,
                (x + 1) * self.CELL - pad,
                (y + 1) * self.CELL - pad,
                fill=color,
                outline=outline,
                width=3,
            )
            self.canvas.create_text(
                x * self.CELL + self.CELL / 2,
                y * self.CELL + 24,
                text=unit.name.split()[0],
                fill="white",
            )
            self.canvas.create_text(
                x * self.CELL + self.CELL / 2,
                y * self.CELL + 43,
                text=f"{unit.hp}/{unit.max_hp}",
                fill="white",
            )

    def choose(self, mode: str) -> None:
        if self.game.active.controller != "human":
            self.say("System", "Take manual control first: manual <unit>.")
            return
        self.mode = mode
        if mode == "move":
            self.say(
                "System",
                f"Where should {self.game.active.name} move? Click a green tile.",
            )
        else:
            self.say(
                "System",
                f"Who should {self.game.active.name} attack? Click a green enemy.",
            )
        self.refresh()

    def on_grid_click(self, event: tk.Event) -> None:
        point = (event.x // self.CELL, event.y // self.CELL)
        try:
            if self.mode == "move":
                self.submit(Move(self.game.active.id, point))
            elif self.mode == "attack":
                target = next(
                    (
                        unit
                        for unit in self.game.units.values()
                        if unit.alive and unit.position == point
                    ),
                    None,
                )
                if target is None:
                    raise RuleError("No target occupies that tile.")
                self.submit(Attack(self.game.active.id, target.id))
            else:
                self.say("System", "Choose Move or Attack before selecting the grid.")
        except RuleError as exc:
            self.say("Rules", str(exc))

    def submit(self, command: object) -> None:
        self.game.submit(command)  # type: ignore[arg-type]
        self.mode = None
        self.refresh()
        self.root.after(250, self.advance_ai)

    def end_turn(self) -> None:
        try:
            self.submit(EndTurn(self.game.active.id))
        except RuleError as exc:
            self.say("Rules", str(exc))

    def ai_once(self) -> None:
        if self.game.outcome:
            return
        decision = self.policy.decide(self.game, self.game.active)
        self.say("AI", decision.explanation)
        self.submit(decision.command)

    def advance_ai(self) -> None:
        if self.game.outcome or self.game.active.controller == "human":
            return
        decision = self.policy.decide(self.game, self.game.active)
        self.say("AI", f"{self.game.active.name}: {decision.explanation}")
        self.game.submit(decision.command)
        self.refresh()
        self.root.after(400, self.advance_ai)

    def on_chat_command(self, _event: tk.Event | None = None) -> None:
        raw = self.entry.get().strip()
        self.entry.delete(0, "end")
        if not raw:
            return
        self.say("You", raw)
        parts = raw.lower().split()
        try:
            if parts[0] == "help":
                self.say(
                    "System",
                    "Commands: help, status, manual <unit>, auto <unit>, move, attack, end. "
                    "Unit IDs: " + ", ".join(self.game.units),
                )
            elif parts[0] == "status":
                summary = "; ".join(
                    f"{unit.id}: {unit.hp}/{unit.max_hp} HP, {unit.controller}"
                    for unit in self.game.units.values()
                )
                self.say("System", summary)
            elif parts[0] in {"manual", "auto"} and len(parts) == 2:
                kind = "human" if parts[0] == "manual" else "ai"
                self.game.submit(SetController(parts[1], kind))
                self.refresh()
                self.root.after(250, self.advance_ai)
            elif parts[0] in {"move", "attack"}:
                self.choose(parts[0])
            elif parts[0] in {"end", "pass"}:
                self.end_turn()
            else:
                self.say("System", "I did not understand that. Type help.")
        except RuleError as exc:
            self.say("Rules", str(exc))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()
    root = tk.Tk()
    TacticalApp(root, demo_game(args.seed))
    root.mainloop()


if __name__ == "__main__":
    main()

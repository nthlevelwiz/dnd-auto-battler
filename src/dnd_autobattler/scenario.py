from .engine import Game, Unit


def demo_game(seed: int = 7) -> Game:
    return Game(
        width=10,
        height=8,
        seed=seed,
        obstacles={(4, 1), (4, 2), (4, 3), (4, 5), (4, 6)},
        hazards={(5, 4), (6, 4)},
        units=[
            Unit("guardian", "Guardian", "heroes", (1, 2), 22, 22, 15, controller="human"),
            Unit("ranger", "Ranger", "heroes", (1, 5), 16, 16, 13, attack_range=5, controller="ai"),
            Unit("bruiser", "Bruiser", "enemies", (8, 2), 20, 20, 14),
            Unit("archer", "Enemy Archer", "enemies", (8, 5), 14, 14, 12, attack_range=5),
        ],
    )

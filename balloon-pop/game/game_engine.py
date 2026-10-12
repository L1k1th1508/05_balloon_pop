"""Game loop state for the balloon pop challenge."""

import random

from game.balloon import Balloon
from game.click_detection import check_pop
from game.renderer import WIDTH, HEIGHT

MAX_LIVES = 3
ROUND_TIME_SECONDS = 30.0

BALLOON_TYPES = {
    "normal": {"points": 10, "color": (84, 160, 230), "weight": 7},
    "bonus": {"points": 25, "color": (255, 204, 77), "weight": 2},
    "penalty": {"points": -20, "color": (238, 90, 90), "weight": 2},
}


class GameEngine:
    def __init__(self):
        self.balloons = []
        self.score = 0
        self.lives = MAX_LIVES
        self.time_left = ROUND_TIME_SECONDS
        self.spawn_cooldown = 0.0
        self.game_over = False
        self.round_active = True
        self.start_new_round()

    def start_new_round(self):
        self.balloons = []
        self.score = 0
        self.lives = MAX_LIVES
        self.time_left = ROUND_TIME_SECONDS
        self.spawn_cooldown = 0.0
        self.game_over = False
        self.round_active = True

    def _spawn_balloon(self):
        balloon_type = random.choices(
            population=list(BALLOON_TYPES.keys()),
            weights=[BALLOON_TYPES[name]["weight"] for name in BALLOON_TYPES],
            k=1,
        )[0]
        config = BALLOON_TYPES[balloon_type]

        radius = random.randint(16, 44)
        x = random.randint(radius + 10, WIDTH - radius - 10)
        speed = random.uniform(1.5, 3.0)
        self.balloons.append(
            Balloon(
                x=x,
                y=-radius,
                radius=radius,
                speed=speed,
                color=config["color"],
                kind=balloon_type,
                points=config["points"],
            )
        )

    def handle_click(self, pos):
        if self.game_over or not self.round_active:
            return False

        popped = check_pop(self.balloons, pos)
        if popped is None:
            return False

        self.balloons.remove(popped)
        self.score += popped.points
        return True

    def update(self, dt=1 / 60):
        if self.game_over or not self.round_active:
            return

        self.time_left = max(0.0, self.time_left - dt)
        self.spawn_cooldown -= dt

        if self.spawn_cooldown <= 0:
            self._spawn_balloon()
            self.spawn_cooldown = random.uniform(0.7, 1.25)

        for balloon in self.balloons:
            balloon.update(dt)

        missed = [b for b in self.balloons if b.is_past_bottom(HEIGHT)]
        if missed:
            self.lives -= len(missed)
            self.balloons = [b for b in self.balloons if not b.is_past_bottom(HEIGHT)]

        if self.time_left <= 0:
            self.round_active = False
            self.game_over = True
        elif self.lives <= 0:
            self.lives = 0
            self.round_active = False
            self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.balloons)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Lives: {self.lives}", (10, 35))
        renderer.draw_text(surface, font, f"Time: {max(0, self.time_left):.1f}s", (10, 60))

        if self.game_over:
            renderer.draw_banner(surface, font, "ROUND OVER")
            renderer.draw_text(
                surface,
                font,
                f"Final Score: {self.score}",
                (surface.get_width() // 2 - 90, surface.get_height() // 2 + 28),
                color=(20, 20, 20),
            )
            renderer.draw_text(
                surface,
                font,
                "Press SPACE or click to restart",
                (surface.get_width() // 2 - 170, surface.get_height() // 2 + 58),
                color=(20, 20, 20),
            )
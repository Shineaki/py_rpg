from client.room import Room
from client.player import Player
import pygame


class Game:
    TILE_SIZE = 16
    MOVE_TICKS = 16

    def __init__(self):
        pygame.init()
        # 1920 1080
        self.screen = pygame.display.set_mode(
            # (320, 180), pygame.SCALED, vsync=1
            (320, 180),
            pygame.FULLSCREEN | pygame.SCALED,
            vsync=1,
        )
        self.tile_position = pygame.Vector2(10, 5)
        self.map_group = pygame.sprite.Group()
        self.room = Room(1, self.map_group, base_offset=pygame.Vector2(0, 0))
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        self.tick = 0
        self.root_player_position = pygame.Vector2(160, 80)
        self.player = Player(self.root_player_position)
        self.moving = False
        self.target_position: pygame.Vector2 | None = None
        self.pending_direction: pygame.Vector2 | None = None
        self.move_step = pygame.Vector2(0, 0)
        self.move_ticks_left = 0

    def handle_movement_input(self) -> None:
        if self.pending_direction is not None:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.pending_direction = pygame.Vector2(0, -1)
            return
        if keys[pygame.K_s]:
            self.pending_direction = pygame.Vector2(0, 1)
            return
        if keys[pygame.K_a]:
            self.pending_direction = pygame.Vector2(-1, 0)
            return
        if keys[pygame.K_d]:
            self.pending_direction = pygame.Vector2(1, 0)
            return

    def _start_pending_move(self) -> None:
        if self.pending_direction is None:
            return

        start = pygame.Vector2(self.player.rect.topleft)
        self.target_position = start + (self.pending_direction * Game.TILE_SIZE)
        self.move_ticks_left = Game.MOVE_TICKS
        self.moving = True
        self.pending_direction = None

    def handle_movement(self) -> None:
        # While moving, start listening for next input only in the second half
        # of the move to avoid accidental double-queue from very short taps.
        if not self.moving or self.move_ticks_left <= 4:
            self.handle_movement_input()

        # Only start queued movement on tick boundary.
        if (
            (not self.moving)
            and (self.pending_direction is not None)
            and self.tick == 0
        ):
            self._start_pending_move()

        if not self.moving and self.pending_direction is None:
            if not self.moving:
                self.player.update_animation_state(moving=False)

        if self.moving and self.target_position:
            if self.player.rect.topleft[0] > self.target_position.x:
                self.player.facing_right = False
            elif self.player.rect.topleft[0] < self.target_position.x:
                self.player.facing_right = True
            self.player.update_animation_state(moving=True)

            # Move player towards target with dir * speed * dt
            direction = self.target_position - pygame.Vector2(self.player.rect.topleft)
            if direction.length() > 0:
                movement = direction.normalize() * 50 * self.dt
                new_pos = pygame.Vector2(self.player.rect.topleft) + movement
                self.player.rect.topleft = (round(new_pos.x), round(new_pos.y))

            self.move_ticks_left -= 1
            if self.move_ticks_left <= 0:
                self.player.rect.topleft = self.target_position
                self.moving = False
                self.target_position = None

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill((34, 34, 34))

            self.handle_movement()

            self.player.update(self.dt)
            self.map_group.update(self.dt, self.root_player_position - pygame.Vector2(self.player.rect.topleft))
            self.map_group.draw(self.screen)
            pygame.draw.rect(self.screen, (255, 0, 0), (self.tile_position.x * Game.TILE_SIZE, self.tile_position.y * Game.TILE_SIZE, Game.TILE_SIZE, Game.TILE_SIZE), 1)
            self.screen.blit(self.player.image, self.root_player_position)

            pygame.display.flip()

            self.dt = self.clock.tick(50) / 1000
            self.tick = (self.tick + 1) % 16

        pygame.quit()


def main():
    game = Game()
    game.run()

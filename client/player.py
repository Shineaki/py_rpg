from collections import defaultdict
import pygame


class Player(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.Rect

    def __init__(self, pos: pygame.Vector2):
        super().__init__()
        self.images = self.load_images()
        self.image: pygame.Surface = self.images["idle"][0]
        self.animation_timer = 0
        self.animation_index = 0
        self.animation_state = "idle"
        self.facing_right = True
        self.rect = self.image.get_rect(topleft=pos)

    def load_images(self) -> dict[str, list[pygame.Surface]]:
        # Load all images for the player sprite
        images = defaultdict(list)
        for anim in ["idle", "run"]:
            for i in range(4):
                img = pygame.image.load(
                    f"assets/dungeon/frames/elf_m_{anim}_anim_f{i}.png"
                )
                images[anim].append(img)
        return images

    def update_animation_state(self, moving: bool):
        if moving:
            if self.animation_state != "run":
                self.animation_index = 0  # Reset animation index when changing state
                self.animation_timer = 0  # Reset timer when changing state
            self.animation_state = "run"
        else:
            if self.animation_state != "idle":
                self.animation_index = 0  # Reset animation index when changing state
                self.animation_timer = 0  # Reset timer when changing state
            self.animation_state = "idle"

    def update(self, dt: float):
        if self.animation_timer == 4:  # Change frame every 0.8 seconds
            self.animation_timer = 0
            self.animation_index = (self.animation_index + 1) % len(
                self.images[self.animation_state]
            )
            if self.facing_right:
                self.image = self.images[self.animation_state][self.animation_index]
            else:
                self.image = pygame.transform.flip(
                    self.images[self.animation_state][self.animation_index], True, False
                )
        self.animation_timer += 1

import pygame
from pytmx.util_pygame import load_pygame
from pytmx import TiledTileLayer

class Room(pygame.sprite.Sprite):
    image: pygame.Surface
    rect: pygame.rect.Rect
    def __init__(self, room_id, group: pygame.sprite.Group, base_offset: pygame.Vector2 = pygame.Vector2(0, 0)):
        super().__init__(group)
        self.base_offset = base_offset
        self.image: pygame.Surface = pygame.Surface((320, 180), pygame.SRCALPHA)
        self.rect = pygame.rect.Rect(16, 0, 320, 180)
        self.raw_map = load_pygame(f"assets/maps/map_{room_id}.tmx")
        self.floor_layer: TiledTileLayer = self.raw_map.get_layer_by_name("floor")  # ty:ignore[invalid-assignment]
        self.wall_layer: TiledTileLayer = self.raw_map.get_layer_by_name("walls")  # ty:ignore[invalid-assignment]
        self.decoration_layer: TiledTileLayer = self.raw_map.get_layer_by_name("decorations")  # ty:ignore[invalid-assignment]
        self.animated_tiles = {}
        self.animated_decorations = []

        self.animation_timer = 0
        self.animation_idx = 0

        self.image.fill((34, 34, 34))
        for tile in self.floor_layer.tiles():
            x, y, surf = tile
            self.image.blit(surf, (x * 16, y * 16))
        for tile in self.wall_layer.tiles():
            x, y, surf = tile
            self.image.blit(surf, (x * 16, y * 16))
        # Animated Tiles
        for tile in self.raw_map.tile_properties:
            props = self.raw_map.tile_properties[tile]
            if "frames" in props:
                self.animated_tiles[tile] = [self.raw_map.get_tile_image_by_gid(af.gid) for af in props["frames"]]
        for tile in self.decoration_layer.tiles():
            x, y, surf = tile
            props = self.raw_map.get_tile_properties(x, y, self.raw_map.get_layer_by_name("decorations").id - 1)  # ty:ignore[unresolved-attribute]
            if props:
                c_tile_gid = self.raw_map.get_tile_gid(x, y, self.raw_map.get_layer_by_name("decorations").id - 1)  # ty:ignore[unresolved-attribute]
                if c_tile_gid in self.animated_tiles:
                    self.decoration_layer.data[y][x] = 0
                    self.animated_decorations.append((x, y, c_tile_gid))
            self.image.blit(surf, (x * 16, y * 16))


    def update(self, dt: float, offset: pygame.Vector2):
        self.rect.topleft = offset + self.base_offset
        self.animation_timer += dt
        if self.animation_timer >= 0.1:
            self.animation_timer = 0
            self.animation_idx = (self.animation_idx + 1) % 3
            for x, y, tile_gid in self.animated_decorations:
                self.image.blit(self.animated_tiles[tile_gid][self.animation_idx], (x * 16, y * 16))


    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, self.rect)
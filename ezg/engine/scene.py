import pygame

import logging

log = logging.getLogger(__name__)

class Renderer:
    def __init__(self, screen):
        self._screen = screen
        self._sprites = list()

    def update(self):
        self._screen.fill((0,0,0,))

        self._sprites.sort(key=lambda s: s.z)
        for s in self._sprites:
            surf, pos = s.paint()
            self._screen.blit(surf, pos)

    def register_sprite(self, sprite):
        self._sprites.append(sprite)

    def animate(self):
        for s in self._sprites:
            s.animate()

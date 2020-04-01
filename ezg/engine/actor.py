import os
import logging

from . import config

import pygame

log = logging.getLogger(__name__)

class Sprite:
    scale = 1.0
    start_frame_index = 1
    frame_period = 100

    def __init__(self, renderer):
        self._renderer = renderer
        self._animation = dict()
        self._state = None
        self._state_kwargs = dict()
        self._frame_index = 0
        self._frame_period = self.frame_period
        self._last_tick = pygame.time.get_ticks()

        self.x = 0
        self.y = 0
        self.z = 0

        self._renderer.register_sprite(self)
        self._load()
        self.set_state(self.init_state)

    def __getattr__(self, key):
        if key in self.actions:
            return lambda: self.set_state(key)
        return getattr(self, key)

    def is_collide_point(self, x, y):
        rect = self._frame_image.get_rect()
        rect.move_ip(self.x, self.y)
        return rect.collidepoint(x, y)
    
    def _load(self):
        for action, action_val in self.actions.items():
            images = list()
            i = self.start_frame_index
            while True:
                try:
                    img = pygame.image.load(
                        os.path.join(
                            config['ASSETS_DIR'],
                            self.assets_location,
                            action_val['assets_format'].format(i))
                    )
                except pygame.error as e:
                    break
                size = [int(s * self.scale) for s in img.get_size()]
                img = pygame.transform.scale(img, size)
                images.append(img)
                i += 1
            self._animation.update({action: images})

    def set_state(self, state, **kwargs):
        self._frame_index = 0
        self._state = state
        self._state_kwargs = kwargs
        self._animation_flag = True
        log.info(f'{self.__class__.__name__}.set_state: <{state}> with {kwargs}')

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.z = y

    def paint(self):
        return self._frame_image, (self.x, self.y, )
                
    def animate(self):
        if not self._animation_flag:
            return

        now = pygame.time.get_ticks()
        if now - self._last_tick < self._frame_period:
            return

        self._last_tick = now

        self._frame_index += 1
        if self._frame_index >= len(self._animation.get(self._state)):
            self._frame_index = 0         

            state_after = self._state_kwargs.get('state_after')
            call_after = self._state_kwargs.get('call_after')
            stop_after = self._state_kwargs.get('stop_after')

            if state_after and self._state != state_after:
                self.set_state(state_after)
            if call_after:
                call_after(self)
            if stop_after:
                self._animation_flag = False

        if self._animation_flag:
            images = self._animation.get(self._state)
            self._frame_image = images[self._frame_index]
            self._frame_period = self.actions.get(self._state, {}).get('frame_period', self.frame_period)


class Character(Sprite):
    life = 100
    selected = False

    def paint(self):
        margin = 0
        stroke = 8
        back, pos = super().paint()

        width, height = back.get_size()

        surf = pygame.Surface((width, height, ))
        surf.blit(back, (0, 0, ))

        x = int((width - 2 * margin) * self.life / 100.0 + margin)
        c =  int((255 * self.life) / 100.0)
        pygame.draw.lines(surf, (255 - c, c, 0, ), False, ((margin, margin + stroke/2, ), (x, margin + stroke/2, ),), stroke)
        
        if self.selected:
            rect = (0, 0, width, height, )
            pygame.draw.rect(surf, (0, 255, 0, ), rect, 1)

        return surf, pos

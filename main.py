import pygame
import os

import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

pygame.init()

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


class Sprite:
    scale = 1.0

    def __init__(self, renderer):
        self._renderer = renderer
        self._animation = dict()
        self._state = None
        self._state_kwargs = dict()
        self._frame_index = 0

        self.x = 0
        self.y = 0
        self.z = 0

        self._renderer.register_sprite(self)
        self._load()
        self.set_state(self.init_state)

    def __getattr__(self, key):
        if key in self.actions:
            return lambda: self.set_state(key)
        return self.get(key)

    def is_collide_point(self, x, y):
        rect = self._frame_image.get_rect()
        rect.move_ip(self.x, self.y)
        return rect.collidepoint(x, y)
    
    def _load(self):
        for action_name, action_value in self.actions.items():
            images = list()
            i = 1
            while True:
                try:
                    img = pygame.image.load(
                        os.path.join(self.assets_location, f'{action_name}_{i}.png')
                    )
                except pygame.error as e:
                    break
                img = pygame.transform.scale(img, (int(img.get_width() * self.scale), int(img.get_height() * self.scale), ))
                images.append(img)
                i += 1
            self._animation.update({action_name: images})

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


class Zombie(Character):
    scale = 0.3
    actions = {
        'attack': {},
        'dead': {},
        'idle': {},
        'walk': {},
    }
    init_state = 'idle'

    def attack(self):
        self.set_state('attack', state_after='idle')

    def dead(self):
        self.set_state('dead', stop_after=True)  

class ZombieMale(Zombie):
    assets_location = 'assets/zombie/male'

class ZombieFemale(Zombie):
    assets_location = 'assets/zombie/female'

class Human(Sprite):
    scale = 0.3
    actions = {
        'jump': {},
        'dead': {},
        'idle': {},
        'run': {},
        'walk': {},
    }
    init_state = 'idle'

    def jump(self):
        self.set_state('jump', state_after='idle')

    def dead(self):
        self.set_state('dead', stop_after=True)

class HumanGirl(Human):
    assets_location = 'assets/human/girl'

class HumanBoy(Human):
    assets_location = 'assets/human/boy'

screen = pygame.display.set_mode((1000, 800, ))

renderer = Renderer(screen)

clock = pygame.time.Clock()
done = False

pygame.time.set_timer(pygame.USEREVENT, 50)

man = ZombieMale(renderer)
man.set_position(100, 100)

woman = ZombieFemale(renderer)
woman.set_position(300, 100)

woman2 = ZombieFemale(renderer)
woman2.set_position(500, 100)

girl = HumanGirl(renderer)
girl.set_position(100, 400)

boy = HumanBoy(renderer)
boy.set_position(300, 400)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            man.attack()
            woman.attack()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            man.dead()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
            man.walk()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            man.idle()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            boy.idle()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            boy.run()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
            boy.walk()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
            boy.jump()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
            boy.dead()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
            girl.idle()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
            girl.run()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
            girl.walk()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            girl.jump()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
            girl.dead()
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if man.is_collide_point(x, y):
                
                if man.selected:
                    man.attack()
                else:
                    man.walk()
                man.selected = True
                woman.idle()
                woman.selected = False
            elif woman.is_collide_point(x, y):
                if woman.selected:
                    woman.attack()
                else:
                    woman.walk()
                woman.selected = True
                man.idle()
                man.selected = False
        if event.type == pygame.USEREVENT:
            man.life = (man.life + 1) % 100
            woman.life = (woman.life - 1) % 100
            renderer.animate()
    
    renderer.update()

    pygame.display.flip()
    clock.tick(60)
        
        


import os
import logging

import pygame

from ezg.engine.scene import Renderer
from ezg.game.figure import *

log = logging.getLogger(__name__)

def run():
    pygame.init()

    screen = pygame.display.set_mode((1000, 800, ))

    renderer = Renderer(screen)

    clock = pygame.time.Clock()
    done = False

    pygame.time.set_timer(pygame.USEREVENT, 50)

    man = ZombieMale(renderer)
    man.set_position(100, 100)

    woman = ZombieFemale(renderer)
    woman.set_position(300, 100)

    z1 = Zombie1(renderer)
    z1.set_position(100, 300)

    z2 = Zombie2(renderer)
    z2.set_position(300, 300)

    z3 = Zombie3(renderer)
    z3.set_position(500, 300)

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
                z1.idle()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                z1.run()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_t:
                z1.walk()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_y:
                z1.attack()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
                z1.dead()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_o:
                z1.hurt()
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

if __name__ == '__main__':
    run()
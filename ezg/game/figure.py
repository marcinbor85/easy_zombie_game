import os

from ezg.engine.actor import Character, Sprite

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
    assets_location = 'zombie/male'

class ZombieFemale(Zombie):
    assets_location = 'zombie/female'

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
    assets_location = 'human/girl'

class HumanBoy(Human):
    assets_location = 'human/boy'
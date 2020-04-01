import os

from ezg.engine.actor import Character, Sprite

class Zombie(Character):
    scale = 0.3
    init_state = 'idle'
    frame_period = 30
    actions = {
        'attack': {
            'assets_format': 'Attack ({}).png',
        },
        'dead': {
            'assets_format': 'Dead ({}).png',
        },
        'idle': {
            'assets_format': 'Idle ({}).png',
        },
        'walk': {
            'assets_format': 'Walk ({}).png',
        },
    }

    def attack(self):
        self.set_state('attack', state_after='idle')

    def dead(self):
        self.set_state('dead', stop_after=True)  

class ZombieMale(Zombie):
    assets_location = 'zombie/male'

class ZombieFemale(Zombie):
    assets_location = 'zombie/female'

class ZombieOther(Character):
    scale = 0.3
    init_state = 'idle'
    actions = {
        'attack': {
            'assets_format': 'Attack{}.png',
        },
        'dead': {
            'assets_format': 'Dead{}.png',
        },
        'idle': {
            'assets_format': 'Idle{}.png',
            'frame_period': 1000
        },
        'walk': {
            'assets_format': 'Walk{}.png',
        },
        'hurt': {
            'assets_format': 'Hurt{}.png',
        },
        'run': {
            'assets_format': 'Run{}.png',
        },
    }

    def attack(self):
        self.set_state('attack', state_after='idle')

    def hurt(self):
        self.set_state('hurt', state_after='idle')

    def dead(self):
        self.set_state('dead', stop_after=True)  

class Zombie1(ZombieOther):
    assets_location = 'zombie/Zombie1'

class Zombie2(ZombieOther):
    assets_location = 'zombie/Zombie2'

class Zombie3(ZombieOther):
    assets_location = 'zombie/Zombie3'

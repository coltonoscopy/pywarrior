from __future__ import division
from itertools import izip
import math, random, copy, sys
import pygame as pg
from .. import setup, observer
from .. import constants as c

# Python 2/3 compatibility
if sys.version_info[0] == 2:
    range = xrange


class Person(pg.sprite.Sprite):
    '''
    Base class for all world characters
    controlled by the computer.
    '''
    def __init__(self, sheet_key, x, y, direction='down', state='resting', index=0):
        super(Person, self).__init__()
        self.alpha = 255
        self.name = sheet_key
        self.get_image = setup.tools.get_image
        self.spritesheet_dict = self.create_spritesheet_dict(sheet_key)
        self.animation_dict = self.create_animation_dict()
        self.index = index
        self.direction = direction
        self.image_list = self.animation_dict[self.direction]
        self.image = self.image_list[self.index]
        self.rect = self.image.get_rect(left=x, top=y)
        self.origin_pos = self.rect.topleft
        self.state_dict = self.create_state_dict()
        self.vector_dict = self.create_vector_dict()
        self.x_vel = 0
        self.y_vel = 0
        self.timer = 0.0
        self.move_timer = 0.0
        self.current_time = 0.0
        self.state = state
        self.blockers = self.set_blockers()
        self.location = self.get_tile_location()
        self.dialogue = ['Location: ' + str(self.location)]
        self.default_direction = direction
        self.item = None
        self.wander_box = self.make_wander_box()
        self.observers = [observer.SoundEffects()]
        self.health = 0
        self.death_image = pg.transform.scale2x(self.image)
        self.battle = None

    def create_spritesheet_dict(self, sheet_key):
        '''
        Make a dictionary of images from sprite sheet.
        '''
        image_list = []
        image_dict = {}
        sheet = setup.GFX[sheet_key]

        image_keys = [
            'facing up 1', 'facing up 2',
            'facing down 1', 'facing down 2',
            'facing left 1', 'facing left 2',
            'facing right 1', 'facing right 2'
        ]

        for row in range(2):
            for column in range(4):
                image_list.append(self.get_image(column * 32, row * 32, 32, 32, sheet))

        for key, image in izip(image_keys, image_list):
            image_dict[key] = image

        return image_dict

    def create_animation_dict(self):
        '''
        Return a dictionary of image lists for animation.
        '''
        image_dict = self.spritesheet_dict

        left_list = [image_dict['facing left 1'], image_dict['facing left 2']]
        right_list = [image_dict['facing right 1'], image_dict['facing right 2']]
        up_list = [image_dict['facing up 1'], image_dict['facing up 2']]
        down_list = [image_dict['facing down 1'], image_dict['facing down 2']]

        direction_dict = {
            'left': left_list,
            'right': right_list,
            'up': up_list,
            'down': down_list
        }

        return direction_dict

    def create_state_dict(self):
        '''
        Return a dictionary of all state methods.
        '''
        state_dict = {
            'resting': self.resting,
            'moving': self.moving,
            'animated resting': self.animated_resting,
            'autoresting': self.auto_resting,
            'automoving': self.auto_moving,
            'battle resting': self.battle_resting,
            'attack': self.attack,
            'enemy attack': self.enemy_attack,
            c.RUN_AWAY: self.run_away,
            c.VICTORY_DANCE: self.victory_dance,
            c.KNOCK_BACK: self.knock_back,
            c.FADE_DEATH: self.fade_death
        }

        return state_dict

    def create_vector_dict(self):
        '''
        Return a dictionary of x and y velocities set to direction keys.
        '''
        vector_dict = {
            'up': (0, -1),
            'down': (0, 1),
            'left': (-1, 0),
            'right': (1, 0)
        }

        return vector_dict

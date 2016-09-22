'''
This is the state that handles battles against monsters
'''
import random, sys
from itertools import izip
import pygame as pg
from .. import tools, battlegui, observer, setup
from .. components import person, attack, attackitems
from .. import constants as c

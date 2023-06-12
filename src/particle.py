import ast
import json
import pygame
from constants import *

'''
    The particle class is a class that group the data related the
    the particles used during the simulation.
    The data is loaded based on the material_name in the constructor.
    The spread rules define how the material/particle should behave when
    in contact with other particles. The spread rules are made of two 
    elements:
    - "can_replace": tells if the particule can replace the elements in the
    array or stack above the particles. For instance water cannot replace 
    the sand. But sand can replace water.
    - "contact_colors": tells how the particle should be colored when in
    contact with another particle. For instance if lava meets sand it will
    turn darker.
'''
class particle:
    def __init__(self, material_name):
        self.material_name = material_name

        self.has_been_updated_this_frame = False

        # Set initial values before data loading
        self.material_type = ''
        self.life_time = -1
        self.color = (0, 0, 0)
        self.spread_rules = {}

        self.load_material()

    def load_material(self):
        ''' None -> None
        Loads or updates the material of the particle.
        '''
        with open(MATERIAL_FILE, 'r') as file:
            data = json.load(file)

        for material in data:
            if material['name'] == self.material_name:
                self.material_type = material['type']
                self.life_time = material['initial_life_time']
                self.color = ast.literal_eval(material['initial_color'])
                self.spread_rules = material['spread_rules']
                break

    def draw(self, window, rect):
        ''' pygame.Surface, pygame.Rect -> None
        Blits the particule to the window.
        '''
        pygame.draw.rect(window, self.color, rect)
import ast
import json
import pygame
from constants import *

def get_material(src_path, mat_name):
    ''' str, str -> {}
    Loads the material called mat_name from the file and
    return the data as a dictionary.
    '''
    with open(src_path, 'r') as file:
        data = json.load(file)

    for material in data:
        if material['name'] == mat_name:
            return material

    return {}

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
        self.spread_rules = []

    def load_material(self):
        ''' None -> None
        Loads or updates the material of the particle.
        '''
        mat_data = get_material(MATERIAL_FILE, self.material_name)

        self.material_type = mat_data['type']
        self.life_time     = mat_data['initial_life_time']
        self.color         = ast.literal_eval(mat_data['initial_color']),
        self.spread_rules  = mat_data['spread_rules']

    def draw(self, window, rect):
        ''' pygame.Surface, pygame.Rect -> None
        Blits the particule to the window.
        '''
        pygame.draw.rect(window, self.color, rect)
import math
import pygame
import random
from particle import *
from constants import *

class grid:
    def __init__(self, window, cell_size):
        '''
        pygame.Surface, int -> None
        Create a simulation grid.
        '''
        self.window = window
        self.cell_size = cell_size

        self.width = int(window.get_width() / cell_size)
        self.height = int(window.get_height() / cell_size)

        # This will hold our cells/particles
        self.cells = []

        self.create_grid()

    def create_grid(self):
        '''
        None -> None 
        Populates the cells in the grid with new empty particles.
        '''
        self.cells = [particle(MATERIAL_NAME_NONE) for _ in range(self.width * self.height)]

    def get_cell_index(self, x, y):
        '''
        int, int -> int
        Returns the index in the list of the cell located at x and y.
        '''
        return y * self.width + x

    def update_particle_simulation(self):
        '''
        None -> None
        Updates the particles motion.
        '''
        for y in range(self.height - 1, 0, -1):
            for x in range(0, self.width, 1):
                mat_type = self.get_particle_at(x, y).material_type
                if mat_type == MATERIAL_TYPE_SOLID:
                    self.update_solid(x, y)
                elif mat_type == MATERIAL_TYPE_LIQUID:
                    self.update_liquid(x, y)
                elif mat_type == MATERIAL_TYPE_GAS:
                    self.update_gas(x, y)

        for column_index in range(self.height):
            for row_index in range(self.width):
                current_particle = self.get_particle_at(row_index, column_index)
                rect = self.cell_to_rect(row_index, column_index)
                current_particle.draw(self.window, rect)

    def cell_is_empty(self, x, y):
        '''
        int, int -> bool
        Returns wether the cell located at x and y on the grid is
        empty or not.
        '''
        index = self.get_cell_index(x, y)
        return self.cells[index].material_name == MATERIAL_NAME_NONE
    
    def particle_is_empty(self, particle):
        '''
        particle -> bool
        Returns wether the cell located at x and y on the grid is
        empty or not.
        '''
        return particle.material_name == MATERIAL_NAME_NONE

    def swap_particles(self, p1, p2):
        '''
        particle, particle -> None
        p1 becomes p2 and p2 becomes p1.
        '''
        p1.material_name, p1.material_type, p1.color, p1.spread_rules,  \
        p2.material_name, p2.material_type, p2.color, p2.spread_rules = \
        p2.material_name, p2.material_type, p2.color, p2.spread_rules,  \
        p1.material_name, p1.material_type, p1.color, p1.spread_rules   \

    def update_solid(self, x, y):
        '''
        int, int -> None
        Updates the solid particle located at x and y on the grid.
        '''
        solid_particle = self.get_particle_at(x, y)

        # Get neighboring particles
        b_particle = self.get_particle_at(x, y + 1) # Below
        b_l_particle = self.get_particle_at(x - 1, y + 1) # Below left
        b_r_particle = self.get_particle_at(x + 1, y + 1) # Below right

        if b_particle and (b_particle.is_empty() or solid_particle.can_spread_to(b_particle.material_name)): # Move down
            solid_particle.color = solid_particle.get_contact_color(b_particle.material_name)
            self.swap_particles(b_particle, solid_particle)
        elif b_l_particle and b_l_particle.is_empty(): # Move down and left
            self.swap_particles(b_l_particle, solid_particle)
        elif b_r_particle and b_r_particle.is_empty(): # Move down and right
            self.swap_particles(b_r_particle, solid_particle)
        else:
            pass

    def update_liquid(self, x, y):
        '''
        int, int -> None
        Updates the liquid particle located at x and y on the grid.
        '''
        liquid_particle = self.get_particle_at(x, y)

        # Get neighbouring particles
        l_particle = self.get_particle_at(x - 1, y) # Left
        r_particle = self.get_particle_at(x + 1, y) # Right

        b_particle = self.get_particle_at(x, y + 1) # Below
        b_l_particle = self.get_particle_at(x - 1, y + 1) # Below left
        b_r_particle = self.get_particle_at(x + 1, y + 1) # Below right

        if b_particle and (b_particle.is_empty() or liquid_particle.can_spread_to(b_particle.material_name)): # Move down
            liquid_particle.color = liquid_particle.get_contact_color(b_particle.material_name)
            self.swap_particles(b_particle, liquid_particle)
        elif b_l_particle and b_l_particle.is_empty(): # Move down and left
            self.swap_particles(b_l_particle, liquid_particle)
        elif b_r_particle and b_r_particle.is_empty(): # Move down and right
            self.swap_particles(b_r_particle, liquid_particle)
        elif l_particle and l_particle.is_empty(): # Move left
            self.swap_particles(l_particle, liquid_particle)
        elif r_particle and r_particle.is_empty(): # Move right
            self.swap_particles(r_particle, liquid_particle)
        else:
            pass

    def update_gas(self, x, y):
        '''
        int, int -> None
        Updates the gas particle located at x and y on the grid.
        '''
        gas_particle = self.get_particle_at(x, y)

        # Get neighboring particles
        a_particle = self.get_particle_at(x, y - 1) # Above
        l_particle = self.get_particle_at(x - 1, y) # Left
        r_particle = self.get_particle_at(x + 1, y) # Right
        b_particle = self.get_particle_at(x, y + 1) # Below

        # Randomly select a direction to move
        directions = [a_particle, l_particle, r_particle, b_particle]
        random.shuffle(directions)

        for direction in directions:
            if direction and (direction.is_empty() or gas_particle.can_spread_to(direction.material_name)):
                gas_particle.color = gas_particle.get_contact_color(direction.material_name)
                self.swap_particles(direction, gas_particle)
                break

    def get_particle_at(self, x, y):
        '''
        int, int -> particle
        Returns the particle located at x and y in the grid.
        '''
        index = self.get_cell_index(x, y)
        if index >= 0 and index < len(self.cells):
            return self.cells[index]
        return None
        
    def cell_to_rect(self, x, y):
        '''
        int, int -> pygame.Rect
        Returns a rect based on the cell located at x and y on the grid.
        '''
        return pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def reveal_particle_at(self, x, y, material_name):
        '''
        int, int, str -> None
        Lights up a particle from the grid located at x and y.
        '''
        spawn_particle = self.get_particle_at(x, y)

        # Refresh material
        spawn_particle.material_name = material_name
        spawn_particle.load_material(MATERIAL_FILE)

    def reveal_particles_at(self, bounds, material_name):
        '''
        [int], str -> None
        Lights up particles from the grid located in the bounds.
        '''
        x_start, y_start, x_end, y_end = bounds

        total_particles = (x_end - x_start + 1) * (y_end - y_start + 1)

        # Percentage of particles to reveal in each iteration
        reveal_percentage = 0.2
        particles_to_reveal = int(total_particles * reveal_percentage)

        center_x = (x_start + x_end) // 2
        center_y = (y_start + y_end) // 2

        for _ in range(particles_to_reveal):
            angle = random.uniform(0, 2 * math.pi)
            radius = random.uniform(0, min(center_x - x_start, center_y - y_start))
            x = int(center_x + radius * math.cos(angle))
            y = int(center_y + radius * math.sin(angle))
            
            # Ensure the generated coordinates are within the bounds
            x = max(x_start, min(x, x_end))
            y = max(y_start, min(y, y_end))
            
            self.reveal_particle_at(x, y, material_name)

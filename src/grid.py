import pygame
from particle import *
from constants import *

class grid:
    def __init__(self, window, cell_size):
        ''' pygame.Surface, int -> None
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
        ''' None -> None 
        Populates the cells in the grid with new empty particles.
        '''
        for _ in range(self.width * self.height):
            # Create new empty particle
            new_particle = particle(MATERIAL_NONE)
            self.cells.append(new_particle)

    def get_cell_index(self, x, y):
        ''' int, int -> int
        Returns the index in the list of the cell located at x and y.
        '''
        return y * self.width + x

    def update_particle_simulation(self):
        ''' None -> None
        Updates the particles motion.
        '''
        for y in range(self.height - 1, 0, -1):
            for x in range(0, self.width, 1):
                material_name = self.get_particle_at(x, y).material_name
                if material_name == MATERIAL_NONE:    pass
                elif material_name == MATERIAL_SAND:  self.update_sand(x, y)
                elif material_name == MATERIAL_WATER: self.update_water(x, y)
                elif material_name == MATERIAL_LAVA:  self.update_lava(x, y)
                else:                                 pass

        for column_index in range(self.height):
            for row_index in range(self.width):
                current_particle = self.get_particle_at(row_index, column_index)
                rect = self.cell_to_rect(row_index, column_index)
                current_particle.draw(self.window, rect)

    def cell_is_empty(self, x, y):
        ''' int, int -> bool
        Returns wether the cell located at x and y on the grid is
        empty or not.
        '''
        index = self.get_cell_index(x, y)
        return self.cells[index].material_name == MATERIAL_NONE
    
    def particle_is_empty(self, particle):
        ''' particle -> bool
        Returns wether the cell located at x and y on the grid is
        empty or not.
        '''
        return particle.material_name == MATERIAL_NONE

    def swap_particles(self, p1, p2):
        ''' particle, particle -> None
        p1 becomes p2 and p2 becomes p1.
        '''
        p1.material_name, p1.color, p2.material_name, p2.color = p2.material_name, p2.color, p1.material_name, p1.color

    def update_sand(self, x, y):
        ''' int, int -> None
        Updates the sand particle located at x and y on the grid.
        '''
        sand_particle = self.get_particle_at(x, y)

        b_particle = self.get_particle_at(x, y + 1)
        b_l_particle = self.get_particle_at(x - 1, y + 1)
        b_r_particle = self.get_particle_at(x + 1, y + 1)

        if b_particle and (self.particle_is_empty(b_particle) or b_particle.material_name == MATERIAL_WATER):
            self.swap_particles(b_particle, sand_particle)
        elif b_l_particle and self.particle_is_empty(b_l_particle):
            self.swap_particles(b_l_particle, sand_particle)
        elif b_r_particle and self.particle_is_empty(b_r_particle):
            self.swap_particles(b_r_particle, sand_particle)
        else:
            pass

    def update_water(self, x, y):
        ''' int, int -> None
        Updates the water particle located at x and y on the grid.
        '''
        water_particle = self.get_particle_at(x, y)

        l_particle = self.get_particle_at(x - 1, y)
        r_particle = self.get_particle_at(x + 1, y)

        b_particle = self.get_particle_at(x, y + 1)
        b_l_particle = self.get_particle_at(x - 1, y + 1)
        b_r_particle = self.get_particle_at(x + 1, y + 1)

        if b_particle and self.particle_is_empty(b_particle):
            self.swap_particles(b_particle, water_particle)
        elif b_l_particle and self.particle_is_empty(b_l_particle):
            self.swap_particles(b_l_particle, water_particle)
        elif b_r_particle and self.particle_is_empty(b_r_particle):
            self.swap_particles(b_r_particle, water_particle)
        elif l_particle and self.particle_is_empty(l_particle):
            self.swap_particles(l_particle, water_particle)
        elif r_particle and self.particle_is_empty(r_particle):
            self.swap_particles(r_particle, water_particle)
        else:
            pass
    
    def update_lava(self, x, y):
        ''' int, int -> None
        Updates the lava particle located at x and y on the grid.
        '''
        lava_particle = self.get_particle_at(x, y)

        l_particle = self.get_particle_at(x - 1, y)
        r_particle = self.get_particle_at(x + 1, y)

        b_particle = self.get_particle_at(x, y + 1)
        b_l_particle = self.get_particle_at(x - 1, y + 1)
        b_r_particle = self.get_particle_at(x + 1, y + 1)

        if b_particle and (self.particle_is_empty(b_particle) or b_particle.material_name == MATERIAL_WATER or b_particle.material_name == MATERIAL_SAND):
            self.swap_particles(b_particle, lava_particle)
        elif b_l_particle and self.particle_is_empty(b_l_particle):
            self.swap_particles(b_l_particle, lava_particle)
        elif b_r_particle and self.particle_is_empty(b_r_particle):
            self.swap_particles(b_r_particle, lava_particle)
        elif l_particle and self.particle_is_empty(l_particle):
            self.swap_particles(l_particle, lava_particle)
        elif r_particle and self.particle_is_empty(r_particle):
            self.swap_particles(r_particle, lava_particle)
        else:
            pass

    def get_particle_at(self, x, y):
        ''' int, int -> particle
        Returns the particle located at x and y in the grid.
        '''
        index = self.get_cell_index(x, y)
        if index < len(self.cells) and index >= 0:
            return self.cells[index]
        return None
        
    def cell_to_rect(self, x, y):
        ''' int, int -> pygame.Rect
        Returns a rect based on the cell located at x and y on the grid.
        '''
        return pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def reveal_particle_at(self, x, y, material_name):
        ''' int, int, str -> None
        Lights up a particle from the grid located at x and y.
        '''
        spawn_particle = self.get_particle_at(x, y)

        # Refresh material
        spawn_particle.material_name = material_name
        spawn_particle.load_material()

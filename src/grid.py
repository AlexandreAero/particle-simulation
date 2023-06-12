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
        self.width = int(window.get_width() / self.cell_size)
        self.height = int(window.get_height() / self.cell_size)
        self.cells = [] # This will hold our cells/particles

        self.create_grid()

    def create_grid(self):
        ''' None -> None 
        Populates the cells in the grid with new empty particles.
        '''
        for _ in range(self.width * self.height):
            # Create new empty particle
            new_particle = particle(MATERIAL_NONE, 0.0, (0, 0, 0, 0))
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
                material_type = self.get_particle_at(x, y).material_type
                if material_type == MATERIAL_NONE:
                    pass
                elif material_type == MATERIAL_SAND:
                    self.update_sand(x, y)
                elif material_type == MATERIAL_WATER:
                    self.update_water(x, y)
                elif material_type == MATERIAL_LAVA:
                    pass
                else:
                    pass

        for column_index in range(self.height):
            for row_index in range(self.width):
                current_particle = self.get_particle_at(row_index, column_index)
                color = current_particle.color
                rect = self.cell_to_rect(row_index, column_index)
                pygame.draw.rect(self.window, color, rect)

    def cell_is_empty(self, x, y):
        ''' int, int -> bool
        Returns wether the cell located at x and y on the grid is
        empty or not.
        '''
        index = self.get_cell_index(x, y)
        return self.cells[index].material_type == MATERIAL_NONE
    
    def particle_is_empty(self, particle):
        ''' particle -> bool
        Returns wether the cell located at x and y on the grid is
        empty or not.
        '''
        return particle.material_type == MATERIAL_NONE

    def swap_particles_in_place(self, p1, p2):
        ''' particle, particle -> None
        p1 becomes p2 and p2 becomes p1.
        '''
        p1.material_type, p1.color, p2.material_type, p2.color = p2.material_type, p2.color, p1.material_type, p1.color

    def update_sand(self, x, y):
        ''' int, int -> None
        Updates the sand particle located at x and y on the grid.
        '''
        sand_particle = self.get_particle_at(x, y)

        b_down_particle = self.get_particle_at(x, y + 1)
        b_left_particle = self.get_particle_at(x - 1, y + 1)
        b_right_particle = self.get_particle_at(x + 1, y + 1)

        if b_down_particle is not None and self.particle_is_empty(b_down_particle):
            self.swap_particles_in_place(b_down_particle, sand_particle)
        elif b_left_particle is not None and self.particle_is_empty(b_left_particle):
            self.swap_particles_in_place(b_left_particle, sand_particle)
        elif b_right_particle is not None and self.particle_is_empty(b_right_particle):
            self.swap_particles_in_place(b_right_particle, sand_particle)
        else:
            pass

    def update_water(self, x, y):
        ''' int, int -> None
        Updates the water particle located at x and y on the grid.
        '''
        water_particle = self.get_particle_at(x, y)

        b_down_particle = self.get_particle_at(x, y + 1)
        b_left_particle = self.get_particle_at(x - 1, y + 1)
        b_right_particle = self.get_particle_at(x + 1, y + 1)
        
        left_particle = self.get_particle_at(x - 1, y)
        right_particle = self.get_particle_at(x + 1, y)

        if b_down_particle is not None and self.particle_is_empty(b_down_particle):
            self.swap_particles_in_place(b_down_particle, water_particle)
        elif b_left_particle is not None and self.particle_is_empty(b_left_particle):
            self.swap_particles_in_place(b_left_particle, water_particle)
        elif b_right_particle is not None and self.particle_is_empty(b_right_particle):
            self.swap_particles_in_place(b_right_particle, water_particle)
        elif left_particle is not None and self.particle_is_empty(left_particle):
            self.swap_particles_in_place(left_particle, water_particle)
        elif right_particle is not None and self.particle_is_empty(right_particle):
            self.swap_particles_in_place(right_particle, water_particle)
        else:
            pass

    def get_particle_at(self, x, y):
        ''' int, int -> particle
        Returns the particle located at x and y in the grid.
        '''
        index = self.get_cell_index(x, y)
        if index < len(self.cells):
            return self.cells[index]
        return None
        
    def cell_to_rect(self, x, y):
        ''' int, int -> pygame.Rect
        Returns a rect based on the cell located at x and y on the grid.
        '''
        return pygame.Rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size)

    def start_particle(self, x, y, material_type, color):
        ''' None -> None
        Lights up a particle from the grid located at x and y.
        '''
        spawn_particle = self.get_particle_at(x, y)
        spawn_particle.material_type = material_type
        spawn_particle.color = color

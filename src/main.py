import json
import pygame
from grid import *
from constants import *
from ast import literal_eval as make_tuple

# ----------+----------+----------+----------+----------+----------+----------+

pygame.init()
pygame.display.set_caption('Particle Simulation')

clock = pygame.time.Clock()
window = pygame.display.set_mode(SCREEN_SIZE)

shouldQuit = False
mouse_down = False

delta_time = 0

spawn_mat = 'none'

simulation_grid = grid(window, CELL_SIZE)

# ----------+----------+----------+----------+----------+----------+----------+

def get_material_data(file_path, mat_name):
    ''' str, str -> {}
    Returns the json data located at file_path for the 
    material named key.
    '''
    with open(file_path) as json_file:
        data = json.load(json_file)
        return data[mat_name]

def update_inputs():
    ''' None -> None
    Updates the user inputs.
    '''
    global mouse_down
    global spawn_mat

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            if event.button == pygame.BUTTON_LEFT:
                spawn_mat = MATERIAL_SAND
            elif event.button == pygame.BUTTON_MIDDLE:
                spawn_mat = MATERIAL_LAVA
            elif event.button == pygame.BUTTON_RIGHT:
                spawn_mat = MATERIAL_WATER
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

def update_spawn():
    ''' None -> None
    Checks if a new spawn is requested.
    '''
    global mouse_down
    global spawn_mat
    
    if mouse_down:
        mouse_pos = pygame.mouse.get_pos()
        cell_x = mouse_pos[0] // CELL_SIZE
        cell_y = mouse_pos[1] // CELL_SIZE

        mat_data = get_material_data(MATERIAL_FILE, spawn_mat)

        simulation_grid.start_particle(cell_x, cell_y, spawn_mat, make_tuple(mat_data['color']))

def run():
    ''' None -> None
    Updates the game loop.
    '''
    while not shouldQuit:
        update_inputs()
        window.fill(CLEAR_COLOR)
        update_spawn()
        simulation_grid.update_particle_simulation()
        pygame.display.update()
        delta_time = clock.tick(FPS) / 1000

if __name__ == '__main__':
    run()

pygame.quit()
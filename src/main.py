import pygame
from grid import *
from constants import *

# ----------+----------+----------+----------+----------+----------+----------+

pygame.init()
pygame.display.set_caption('Particle Simulation')

clock = pygame.time.Clock()
window = pygame.display.set_mode(SCREEN_SIZE)

shouldQuit = False
mouse_down = False

delta_time = 0

spawn_mat_name = MATERIAL_NONE

simulation_grid = grid(window, CELL_SIZE)

# ----------+----------+----------+----------+----------+----------+----------+

def update_inputs():
    ''' None -> None
    Updates the user inputs.
    '''
    global mouse_down
    global spawn_mat_name

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            if event.button == pygame.BUTTON_LEFT:
                spawn_mat_name = MATERIAL_SAND
            elif event.button == pygame.BUTTON_MIDDLE:
                spawn_mat_name = MATERIAL_LAVA
            elif event.button == pygame.BUTTON_RIGHT:
                spawn_mat_name = MATERIAL_WATER
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

def update_spawn():
    ''' None -> None
    Checks if a new spawn is requested.
    '''
    global mouse_down
    global spawn_mat_name
    
    if mouse_down:
        mouse_pos = pygame.mouse.get_pos()
        cell_x = mouse_pos[0] // CELL_SIZE
        cell_y = mouse_pos[1] // CELL_SIZE

        simulation_grid.reveal_particle_at(cell_x, cell_y, spawn_mat_name)

def run():
    ''' None -> None
    Updates the game loop.
    '''
    while not shouldQuit:
        window.fill(CLEAR_COLOR)
        
        update_inputs()
        update_spawn()
        
        simulation_grid.update_particle_simulation()
        
        pygame.display.update()
        
        delta_time = clock.tick(FPS) / 1000

if __name__ == '__main__':
    run()

pygame.quit()

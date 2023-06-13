import pygame
import pygame_gui
from grid import *
from constants import *

pygame.init()
pygame.display.set_caption('Particle Simulation')

clock = pygame.time.Clock()
window = pygame.display.set_mode(SCREEN_SIZE)
gui = pygame_gui.UIManager(SCREEN_SIZE)

selected_material = MATERIAL_NAME_NONE

shouldQuit = False
mouse_down = False

simulation_grid = grid(window, CELL_SIZE)

dropdown = pygame_gui.elements.UIDropDownMenu(
    [MATERIAL_NAME_NONE, MATERIAL_NAME_SAND, MATERIAL_NAME_WATER, MATERIAL_NAME_LAVA, MATERIAL_NAME_ACID], 
    MATERIAL_NAME_NONE,
    pygame.Rect((10, 10), (200, 20)),
    gui
)

def spawn_particle(grid, mouse_x, mouse_y, mat_name, cell_size):
    ''' 
    int, int, str -> None 
    Helper function that spawns a particle with the mouse coordinates
    and the material name.
    '''
    cell_x = mouse_x // cell_size
    cell_y = mouse_y // cell_size

    # Clamp the coordinates within the valid range
    cell_x = max(0, min(cell_x, grid.width - 1))
    cell_y = max(0, min(cell_y, grid.height - 1))

    grid.reveal_particle_at(cell_x, cell_y, mat_name)

def update_inputs(event):
    '''
    pygame.Event -> None
    Updates the inputs related the the material selection
    dropdown.
    '''
    global selected_material, mouse_down

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == pygame.BUTTON_LEFT:
            mouse_down = True
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == pygame.BUTTON_LEFT:
            mouse_down = False

    if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
        if event.ui_element == dropdown:
            selected_material = dropdown.selected_option

def run():
    '''
    None -> None
    Starts the game and update the game loop.
    '''
    delta_time = 0

    while not shouldQuit:
        for event in pygame.event.get():
            gui.process_events(event)
            update_inputs(event)

        window.fill(CLEAR_COLOR)

        if mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            spawn_particle(simulation_grid, 
                           mouse_pos[0], 
                           mouse_pos[1], 
                           selected_material, 
                           CELL_SIZE)

        simulation_grid.update_particle_simulation()
        
        gui.update(delta_time)
        gui.draw_ui(window)

        pygame.display.update()

        delta_time = clock.tick(FPS) / 1000
    
    pygame.quit()

if __name__ == '__main__':
    run()

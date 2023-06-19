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
selected_brush = BRUSH_SMALL

should_quit = False
mouse_down = False

simulation_grid = grid(window, CELL_SIZE)

material_dropdown = pygame_gui.elements.UIDropDownMenu(
    [MATERIAL_NAME_NONE, MATERIAL_NAME_SAND, MATERIAL_NAME_WATER, MATERIAL_NAME_LAVA, MATERIAL_NAME_ACID, MATERIAL_NAME_TOXICGAS], 
    MATERIAL_NAME_NONE,
    pygame.Rect((5, 5), (200, 20)),
    gui
)

brush_dropdown = pygame_gui.elements.UIDropDownMenu(
    [BRUSH_SMALL, BRUSH_BIG], 
    BRUSH_SMALL,
    pygame.Rect((210, 5), (150, 20)),
    gui
)

def update_inputs(event):
    '''
    pygame.Event -> None
    Updates the inputs related the the material selection
    dropdown.
    '''
    global selected_material, selected_brush, mouse_down

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == pygame.BUTTON_LEFT:
            mouse_down = True
    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == pygame.BUTTON_LEFT:
            mouse_down = False

    if event.type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED:
        if event.ui_element == material_dropdown:
            selected_material = material_dropdown.selected_option
        elif event.ui_element == brush_dropdown:
            selected_brush = brush_dropdown.selected_option

def mouse_coordinates_to_x_y(grid, mouse_x, mouse_y):
    '''
    grid, int, int -> (int, int)
    Transforms a mouse coordinates tuple to a row and column
    accordingly to the grid.
    '''
    x = mouse_x // grid.cell_size
    y = mouse_y // grid.cell_size

    # Clamp the coordinates within the valid range
    x = max(0, min(x, grid.width - 1))
    y = max(0, min(y, grid.height - 1))

    return (x, y)

def mouse_coordinates_to_bounds(grid, mouse_x, mouse_y, extent):
    '''
    grid, int, int, int -> [int]
    Transforms a mouse coordinates tuple to a rect bounds
    accordingly to the grid.
    '''
    cell_size = grid.cell_size

    # Convert mouse coordinates to cell coordinates
    cell_x = mouse_x // cell_size
    cell_y = mouse_y // cell_size

    # Calculate the rectangular bounds
    x_start = max(0, cell_x - extent)
    y_start = max(0, cell_y - extent)
    x_end = min(grid.width - 1, cell_x + extent)
    y_end = min(grid.height - 1, cell_y + extent)

    return [x_start, y_start, x_end, y_end]

def run():
    '''
    None -> None
    Starts the game and update the game loop.
    '''
    delta_time = 0

    while not should_quit:
        for event in pygame.event.get():
            gui.process_events(event)
            update_inputs(event)

        window.fill(CLEAR_COLOR)

        if mouse_down:
            mouse_pos = pygame.mouse.get_pos()
            if selected_brush == BRUSH_SMALL:
                coords = mouse_coordinates_to_x_y(simulation_grid, mouse_pos[0], mouse_pos[1])
                simulation_grid.reveal_particle_at(coords[0], coords[1], selected_material)
            elif selected_brush == BRUSH_BIG:
                bounds = mouse_coordinates_to_bounds(simulation_grid, mouse_pos[0], mouse_pos[1], 10)
                simulation_grid.reveal_particles_at(bounds, selected_material)

        simulation_grid.update_particle_simulation()
        
        gui.update(delta_time)
        gui.draw_ui(window)

        pygame.display.update()

        delta_time = clock.tick(FPS) / 1000
    
    pygame.quit()

if __name__ == '__main__':
    run()

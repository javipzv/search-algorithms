import pygame
from PIL import Image
import pickle
from utils.constants import MADRID_LIMITS, BARCELONA_LIMITS, SHIFT
from utils.helpers import cartesian_to_geo, geo_to_cartesian, get_nearest_node, transform_final_path
import numpy as np
from graph.algorithms.dijkstra import dijkstra
from graph.algorithms.a_star import a_star

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_BACKGROUND = (24, 24, 29)
DARK_GREEN = (65, 84, 85)
LIGHT_GREEN = (131, 179, 185)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
YELLOW = (255, 219, 77)

class BaseScreen:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 30)
        self.bigger_text_font = pygame.font.Font(None, 25)
        self.text_font = pygame.font.Font(None, 23)

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def draw_image(self, path, shape, pos):
        img = Image.open(path)
        img_redim = img.resize(shape, Image.Resampling.LANCZOS)
        img_redim_pg = pygame.image.fromstring(img_redim.tobytes(), img_redim.size, img_redim.mode)
        screen.blit(img_redim_pg, pos)

    def draw_text(self, text, font, color, pos):
        text_to_draw = font.render(text, True, color)
        screen.blit(text_to_draw, pos)

class InitialScreen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.selected_city = None

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] > 180 and mouse_pos[0] < 435 and mouse_pos[1] > 330 and mouse_pos[1] < 500:
                    self.selected_city = "Barcelona"
                    return "visualization"
                elif mouse_pos[0] > 580 and mouse_pos[0] < 835 and mouse_pos[1] > 330 and mouse_pos[1] < 500:
                    self.selected_city = "Madrid"
                    return "visualization"
        return None

    def draw(self, screen):
        screen.fill(GREEN_BACKGROUND)
        
        pygame.draw.rect(screen, DARK_GREEN, (0, 0, 1000, 150))
        self.draw_text(text="SEARCH ALGORITHMS", font=self.title_font, color=WHITE, pos=(180, 50))
        self.draw_text(text="Discover the most common search algorithms with a visualization!", font=self.subtitle_font, color=LIGHT_GREEN, pos=(165, 210))
        self.draw_text(text="Pick a city", font=self.subtitle_font, color=LIGHT_GREEN, pos=(450, 260))

        self.draw_image(path='static/BARCELONA.jpg', shape=(255, 170), pos=(180, 330))
        self.draw_image(path='static/MADRID.jpg', shape=(255, 170), pos=(580, 330))

        self.draw_text(text="Barcelona", font=self.text_font, color=LIGHT_GREEN, pos=(270, 510))
        self.draw_text(text="Madrid", font=self.text_font, color=LIGHT_GREEN, pos=(680, 510))

class VisualizationScreen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.algorithm = None
        self.mouse_pos_p1 = None
        self.mouse_pos_p2 = None
        self.p1 = None
        self.p2 = None
        self.selecting_p1 = False
        self.selecting_p2 = False
        self.selected_city = None
        self.selected_graph = None
        self.path_calculated = False
        self.trace = None
        self.p1_nearest = None
        self.p2_nearest = None
        self.index = 0
        self.visited_edges = []
        self.search_visualized = False
        self.path = None
        self.dist = None

    def set_selected_city(self, city):
        self.selected_city = city
        if city == "Madrid":
            with open('graphs_data/madrid_edges.pkl', 'rb') as file:
                self.madrid_edges = pickle.load(file)
            with open('graphs_data/madrid_graph.pkl', 'rb') as file:
                self.selected_graph = pickle.load(file)
        elif city == "Barcelona":
            with open('graphs_data/barcelona_edges.pkl', 'rb') as file:
                self.barcelona_edges = pickle.load(file)
            with open('graphs_data/barcelona_graph.pkl', 'rb') as file:
                self.selected_graph = pickle.load(file)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Selecting p1
                if self.selecting_p1 and mouse_pos[0] > 300 and mouse_pos[0] < 1000 and mouse_pos[1] > 0 and mouse_pos[1] < 600:
                    self.mouse_pos_p1 = mouse_pos
                    if self.selected_city == "Madrid":
                        self.p1 = cartesian_to_geo(mouse_pos[0] - SHIFT, mouse_pos[1],
                                                   MADRID_LIMITS[1][0], MADRID_LIMITS[1][1],
                                                   MADRID_LIMITS[0][0], MADRID_LIMITS[0][1])
                    elif self.selected_city == "Barcelona":
                        self.p1 = cartesian_to_geo(mouse_pos[0] - SHIFT, mouse_pos[1],
                                                   BARCELONA_LIMITS[1][0], BARCELONA_LIMITS[1][1],
                                                   BARCELONA_LIMITS[0][0], BARCELONA_LIMITS[0][1])
                    self.selecting_p2 = True
                    self.selecting_p1 = False

                # Selecting p2
                elif self.selecting_p2 and mouse_pos[0] > 300 and mouse_pos[0] < 1000 and mouse_pos[1] > 0 and mouse_pos[1] < 600:
                    self.mouse_pos_p2 = mouse_pos
                    if self.selected_city == "Madrid":
                        self.p2 = cartesian_to_geo(mouse_pos[0] - SHIFT, mouse_pos[1],
                                                   MADRID_LIMITS[1][0], MADRID_LIMITS[1][1],
                                                   MADRID_LIMITS[0][0], MADRID_LIMITS[0][1])
                    elif self.selected_city == "Barcelona":
                        self.p2 = cartesian_to_geo(mouse_pos[0] - SHIFT, mouse_pos[1],
                                                   BARCELONA_LIMITS[1][0], BARCELONA_LIMITS[1][1],
                                                   BARCELONA_LIMITS[0][0], BARCELONA_LIMITS[0][1])
                    self.selecting_p2 = False

                # Button to apply Dijkstra
                elif mouse_pos[0] > 24 and mouse_pos[0] < 270 and mouse_pos[1] > 247 and mouse_pos[1] < 287:
                    if self.p1 and self.p2:
                        self.algorithm = "Dijkstra"
                        dist, path, trace = self.calculate_path()
                        self.trace = trace
                        self.path = path
                        self.dist = dist
                        self.path_calculated = True

                # Button to apply A*
                elif mouse_pos[0] > 24 and mouse_pos[0] < 270 and mouse_pos[1] > 297 and mouse_pos[1] < 337:
                    if self.p1 and self.p2:
                        self.algorithm = "A*"
                        dist, path, trace = self.calculate_path()
                        self.trace = trace
                        self.path = path
                        self.dist = dist
                        self.path_calculated = True

                # Going back
                elif mouse_pos[0] > 27 and mouse_pos[0] < 267 and mouse_pos[1] > 530 and mouse_pos[1] < 565:
                    self.p1, self.p2, self.mouse_pos_p1, self.mouse_pos_p2, self.selected_city, self.selected_graph, self.index, self.visited_edges, self.path_calculated, self.search_visualized, self.dist = None, None, None, None, None, None, 0, [], False, None, None
                    return "initial"
                
                # Selecting points
                elif mouse_pos[0] > 27 and mouse_pos[0] < 267 and mouse_pos[1] > 51 and mouse_pos[1] < 85:
                    self.p1, self.p2, self.mouse_pos_p1, self.mouse_pos_p2, self.index, self.visited_edges, self.path_calculated, self.search_visualized, self.dist = None, None, None, None, 0, [], False, False, None
                    self.selecting_p1 = True

        return None

    def update(self):
        # Draw all the search
        if self.path_calculated:
            if self.selected_city == "Madrid":
                for tr in self.trace[self.index:self.index+10]:
                    t = [geo_to_cartesian(lon, lat, MADRID_LIMITS[1][0], MADRID_LIMITS[1][1], 
                                                      MADRID_LIMITS[0][0], MADRID_LIMITS[0][1]) for lon, lat in tr]
                    self.visited_edges.append(t)
                for edge in self.visited_edges:
                    pygame.draw.lines(screen, color=LIGHT_GREEN, closed=True, points=edge, width=2)

            elif self.selected_city == "Barcelona":
                for tr in self.trace[self.index:self.index+10]:
                    t = [geo_to_cartesian(lon, lat, BARCELONA_LIMITS[1][0], BARCELONA_LIMITS[1][1], 
                                                      BARCELONA_LIMITS[0][0], BARCELONA_LIMITS[0][1]) for lon, lat in tr]
                    self.visited_edges.append(t)
                for edge in self.visited_edges:
                    pygame.draw.lines(screen, color=LIGHT_GREEN, closed=True, points=edge, width=2)
        
            self.index += 10
            if self.index >= len(self.trace):
                self.index = 0
                self.path_calculated = False
                self.search_visualized = True

        # Draw final path
        if self.search_visualized:
            if self.selected_city == "Madrid":
                path_to_visualize: list[tuple] = transform_final_path(MADRID_LIMITS, self.selected_graph, self.path)
            else:
                path_to_visualize: list[tuple] = transform_final_path(BARCELONA_LIMITS, self.selected_graph, self.path)
            path_to_visualize = [self.mouse_pos_p1] + path_to_visualize + [self.mouse_pos_p2]
            pygame.draw.lines(screen, color=YELLOW, closed=False, points=path_to_visualize, width=2)

        # Draw source node
        if self.p1:
            pygame.draw.circle(screen, RED, self.mouse_pos_p1, 3)
            self.draw_text(text=str((np.round(self.p1[1], 3), np.round(self.p1[0], 3))), font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(100, 110))
        
        # Draw destination node
        if self.p2:
            pygame.draw.circle(screen, RED, self.mouse_pos_p2, 3)
            self.draw_text(text=str((np.round(self.p2[1], 3), np.round(self.p2[0], 3))), font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(100, 160))

    def draw_map(self):
        if self.selected_city == "Madrid":
            edges_to_draw = self.madrid_edges
        else:
            edges_to_draw = self.barcelona_edges

        for edges in edges_to_draw:
            pygame.draw.lines(screen, color=DARK_GREEN, closed=True, points=edges, width=1)

    def draw(self, screen):
        screen.fill(GREEN_BACKGROUND)

        self.draw_map()

        pygame.draw.rect(screen, DARK_GREEN, (0, 0, 300, 1000))

        pygame.draw.rect(screen, GRAY, (25, 48, 244, 39))
        pygame.draw.rect(screen, WHITE, (28, 51, 239, 34))
        self.draw_text(text="Select points", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(90, 60))

        pygame.draw.rect(screen, WHITE, (27, 100, 240, 35))
        self.draw_text(text="P1: ", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(40, 110))

        pygame.draw.rect(screen, WHITE, (27, 150, 240, 35))
        self.draw_text(text="P2: ", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(40, 160))

        pygame.draw.rect(screen, GRAY, (24, 247, 245, 40))
        pygame.draw.rect(screen, WHITE, (27, 250, 240, 35))
        self.draw_text(text="Apply Dijkstra", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(90, 260))

        pygame.draw.rect(screen, GRAY, (24, 297, 245, 40))
        pygame.draw.rect(screen, WHITE, (27, 300, 240, 35))
        self.draw_text(text="Apply A*", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(110, 310))

        pygame.draw.rect(screen, GRAY, (24, 527, 245, 40))
        pygame.draw.rect(screen, WHITE, (27, 530, 240, 35))
        self.draw_text(text="Back", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(127, 540))
    
    def calculate_path(self):
        source_node = get_nearest_node(self.selected_graph, self.p1[0], self.p1[1])

        destination_node = get_nearest_node(self.selected_graph, self.p2[0], self.p2[1])
        
        if self.algorithm == "Dijkstra":
            dist, path, trace = dijkstra(self.selected_graph, source_node, destination_node)
        elif self.algorithm == "A*":
            dist, path, trace = a_star(self.selected_graph, source_node, destination_node)
        return dist, path, trace

class ScreenController:
    def __init__(self):
        self.screens = {
            "initial": InitialScreen(),
            "visualization": VisualizationScreen()
        }
        self.current_screen = self.screens["initial"] 

    def change_screen(self, screen_name):
        """Change the current screen"""
        if screen_name in self.screens:
            if screen_name == "visualization":
                self.screens["visualization"].set_selected_city(self.screens["initial"].selected_city)
            self.current_screen = self.screens[screen_name]

    def handle_events(self, events):
        result = self.current_screen.handle_events(events)
        if result:
            self.change_screen(result)

    def update(self):
        self.current_screen.update()

    def draw(self, screen):
        self.current_screen.draw(screen)

pygame.init()

screen = pygame.display.set_mode((1000, 600))
screen_controller = ScreenController()

# Main loop
running = True
while running:
    # Handle events
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Handle events in the current screen
    screen_controller.handle_events(events)

    # Draw the current screen
    screen_controller.draw(screen)

    # Update the current screen
    screen_controller.update()

    # Update the display
    pygame.display.flip()

pygame.quit()
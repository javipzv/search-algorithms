import pygame
from PIL import Image
import pickle
from utils.constants import MADRID_LIMITS, BARCELONA_LIMITS, SHIFT
from utils.helpers import cartesian_to_geo, geo_to_cartesian, get_nearest_node, transform_final_path
import numpy as np
from graph.algorithms.dijkstra import dijkstra
from graph.algorithms.a_star import a_star
from graph.graph import Vertex

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_BACKGROUND = (24, 24, 29)
DARK_GREEN = (65, 84, 85)
LIGHT_GREEN = (131, 179, 185)
GRAY = (150, 150, 150)
RED = (255, 0, 0)
YELLOW = (255, 219, 77)

class BaseScreen:
    """
    This class represents a base screen with common methods and attributes
    """
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
        """
        Draw an image on the screen
        """
        img = Image.open(path)
        img_redim = img.resize(shape, Image.Resampling.LANCZOS)
        img_redim_pg = pygame.image.fromstring(img_redim.tobytes(), img_redim.size, img_redim.mode)
        screen.blit(img_redim_pg, pos)

    def draw_text(self, text, font, color, pos):
        """
        Draw text on the screen
        """
        text_to_draw = font.render(text, True, color)
        screen.blit(text_to_draw, pos)

class InitialScreen(BaseScreen):
    """
    This class represents the initial screen of the application
    """
    def __init__(self):
        super().__init__()
        self.selected_city = None

    def handle_events(self, events):
        """
        Handle the events of the screen
        """
        for event in events:

            # Check if the user clicked on a city
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # User clicks on Barcelona
                if mouse_pos[0] > 180 and mouse_pos[0] < 435 and mouse_pos[1] > 330 and mouse_pos[1] < 500:
                    self.selected_city = "Barcelona"
                    return "visualization"
                
                # User clicks on Madrid
                elif mouse_pos[0] > 580 and mouse_pos[0] < 835 and mouse_pos[1] > 330 and mouse_pos[1] < 500:
                    self.selected_city = "Madrid"
                    return "visualization"
        return None

    def draw(self, screen):
        """
        Draw the initial screen
        """
        screen.fill(GREEN_BACKGROUND)

        # Draw the title and subtitle
        pygame.draw.rect(screen, DARK_GREEN, (0, 0, 1000, 150))
        self.draw_text(text="SEARCH ALGORITHMS", font=self.title_font, color=WHITE, pos=(180, 50))
        self.draw_text(text="Discover the most common search algorithms with a visualization!", font=self.subtitle_font, color=LIGHT_GREEN, pos=(165, 210))
        self.draw_text(text="Pick a city", font=self.subtitle_font, color=LIGHT_GREEN, pos=(450, 260))

        # Draw the images of the cities
        self.draw_image(path='static/BARCELONA.jpg', shape=(255, 170), pos=(180, 330))
        self.draw_image(path='static/MADRID.jpg', shape=(255, 170), pos=(580, 330))

        # Draw the names of the cities
        self.draw_text(text="Barcelona", font=self.text_font, color=LIGHT_GREEN, pos=(270, 510))
        self.draw_text(text="Madrid", font=self.text_font, color=LIGHT_GREEN, pos=(680, 510))

class VisualizationScreen(BaseScreen):
    """
    This class represents the visualization screen of the application
    """
    def __init__(self):
        super().__init__()
        self.algorithm = None
        self.mouse_pos_P1 = None
        self.mouse_pos_P2 = None
        self.P1 = None
        self.P2 = None
        self.selecting_P1 = False
        self.selecting_P2 = False
        self.selected_city = None
        self.selected_graph = None
        self.path_calculated = False
        self.trace = None
        self.P1_nearest = None
        self.P2_nearest = None
        self.index = 0
        self.visited_edges = []
        self.search_visualized = False
        self.path = None
        self.dist = None
        self.limits = None

    def set_selected_city(self, city):
        """
        Set the selected city which is given by the user's election on the initial screen
        """
        self.selected_city = city

        # Load the selected city's graph and edges

        if city == "Madrid":
            self.limits = MADRID_LIMITS
            with open('graphs_data/madrid_edges.pkl', 'rb') as file:
                self.madrid_edges = pickle.load(file)
            with open('graphs_data/madrid_graph.pkl', 'rb') as file:
                self.selected_graph = pickle.load(file)

        elif city == "Barcelona":
            self.limits = BARCELONA_LIMITS
            with open('graphs_data/barcelona_edges.pkl', 'rb') as file:
                self.barcelona_edges = pickle.load(file)
            with open('graphs_data/barcelona_graph.pkl', 'rb') as file:
                self.selected_graph = pickle.load(file)

    def handle_events(self, events):
        """
        Handle the events of the screen
        """
        for event in events:
            # Check if the user clicked on the screen
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # User is selecting P1
                if self.selecting_P1 and mouse_pos[0] > 300 and mouse_pos[0] < 1000 and mouse_pos[1] > 0 and mouse_pos[1] < 600:
                    self.mouse_pos_P1 = mouse_pos
                    self.P1 = cartesian_to_geo(mouse_pos[0] - SHIFT, mouse_pos[1],
                                                   self.limits[0][0], self.limits[0][1],
                                                   self.limits[1][0], self.limits[1][1])
                    self.selecting_P2 = True
                    self.selecting_P1 = False

                # User is selecting P2
                elif self.selecting_P2 and mouse_pos[0] > 300 and mouse_pos[0] < 1000 and mouse_pos[1] > 0 and mouse_pos[1] < 600:
                    self.mouse_pos_P2 = mouse_pos
                    self.P2 = cartesian_to_geo(mouse_pos[0] - SHIFT, mouse_pos[1],
                                                   self.limits[0][0], self.limits[0][1],
                                                   self.limits[1][0], self.limits[1][1])
                    self.selecting_P2 = False

                # Button to apply Dijkstra
                elif mouse_pos[0] > 24 and mouse_pos[0] < 270 and mouse_pos[1] > 247 and mouse_pos[1] < 287 and not self.search_visualized:
                    if self.P1 and self.P2:
                        self.algorithm = "Dijkstra"
                        dist, path, trace = self.calculate_path()
                        self.trace = trace
                        self.path = path
                        self.dist = dist
                        self.path_calculated = True

                # Button to apply A*
                elif mouse_pos[0] > 24 and mouse_pos[0] < 270 and mouse_pos[1] > 297 and mouse_pos[1] < 337 and not self.search_visualized:
                    if self.P1 and self.P2:
                        self.algorithm = "A*"
                        dist, path, trace = self.calculate_path()
                        self.trace = trace
                        self.path = path
                        self.dist = dist
                        self.path_calculated = True

                # Going back to the initial screen
                elif mouse_pos[0] > 27 and mouse_pos[0] < 267 and mouse_pos[1] > 530 and mouse_pos[1] < 565:
                    self.reset_values()
                    return "initial"
                
                # User is going to select points
                elif mouse_pos[0] > 27 and mouse_pos[0] < 267 and mouse_pos[1] > 51 and mouse_pos[1] < 85:
                    self.reset_points()
                    self.selecting_P1 = True

        return None

    def update(self):
        """
        Update the screen
        """
        # Draw all the search that has been done by the algorithm
        if self.path_calculated:
            for trace_segment in self.trace[self.index:self.index+10]:
                cartesian_points = [geo_to_cartesian(lat, lon, self.limits[0][0], self.limits[0][1], 
                                                    self.limits[1][0], self.limits[1][1]) for lat, lon in trace_segment]
                self.visited_edges.append(cartesian_points)
            for edge in self.visited_edges:
                pygame.draw.lines(screen, color=LIGHT_GREEN, closed=True, points=edge, width=2)

            # Update the index to visualize the next 10 edges (faster visualization)
            self.index += 10
            if self.index >= len(self.trace):
                self.index = 0
                self.path_calculated = False
                self.search_visualized = True

        # Draw the final path after the search
        if self.search_visualized:
            path_to_visualize: list[tuple] = transform_final_path(self.limits, self.selected_graph, self.path)
            path_to_visualize = [self.mouse_pos_P1] + path_to_visualize + [self.mouse_pos_P2]
            pygame.draw.lines(screen, color=YELLOW, closed=False, points=path_to_visualize, width=2)
            self.draw_text(text=f"Distance: {np.round(self.dist, 3)} m", font=self.bigger_text_font, color=WHITE, pos=(65, 380))

        # Draw source node
        if self.P1:
            pygame.draw.circle(screen, RED, self.mouse_pos_P1, 3)
            self.draw_text(text=str((np.round(self.P1[0], 3), np.round(self.P1[1], 3))), font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(100, 110))
        
        # Draw destination node
        if self.P2:
            pygame.draw.circle(screen, RED, self.mouse_pos_P2, 3)
            self.draw_text(text=str((np.round(self.P2[0], 3), np.round(self.P2[1], 3))), font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(100, 160))

    def draw_map(self):
        """
        Draw the map of the selected city
        """
        if self.selected_city == "Madrid":
            edges_to_draw = self.madrid_edges
        else:
            edges_to_draw = self.barcelona_edges

        for edges in edges_to_draw:
            pygame.draw.lines(screen, color=DARK_GREEN, closed=True, points=edges, width=1)

    def draw(self, screen):
        """
        Draw the visualization screen
        """
        screen.fill(GREEN_BACKGROUND)

        self.draw_map()

        pygame.draw.rect(screen, DARK_GREEN, (0, 0, 300, 1000))

        # Draw the button to select points
        pygame.draw.rect(screen, GRAY, (25, 48, 244, 39))
        pygame.draw.rect(screen, WHITE, (28, 51, 239, 34))
        self.draw_text(text="Select points", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(90, 60))

        # Draw the show the coordinates of the selected points
        pygame.draw.rect(screen, WHITE, (27, 100, 240, 35))
        self.draw_text(text="P1: ", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(40, 110))

        pygame.draw.rect(screen, WHITE, (27, 150, 240, 35))
        self.draw_text(text="P2: ", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(40, 160))

        # Draw the buttons to apply the algorithms
        pygame.draw.rect(screen, GRAY, (24, 247, 245, 40))
        pygame.draw.rect(screen, WHITE, (27, 250, 240, 35))
        self.draw_text(text="Apply Dijkstra", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(90, 260))

        pygame.draw.rect(screen, GRAY, (24, 297, 245, 40))
        pygame.draw.rect(screen, WHITE, (27, 300, 240, 35))
        self.draw_text(text="Apply A*", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(110, 310))

        # Draw the button to go back
        pygame.draw.rect(screen, GRAY, (24, 527, 245, 40))
        pygame.draw.rect(screen, WHITE, (27, 530, 240, 35))
        self.draw_text(text="Back", font=self.bigger_text_font, color=GREEN_BACKGROUND, pos=(127, 540))
    
    def calculate_path(self):
        """
        Calculate the path using the selected algorithm
        """
        source_node: Vertex = get_nearest_node(self.selected_graph, self.P1[0], self.P1[1])

        destination_node: Vertex = get_nearest_node(self.selected_graph, self.P2[0], self.P2[1])
        
        if self.algorithm == "Dijkstra":
            dist, path, trace = dijkstra(self.selected_graph, source_node, destination_node)
        elif self.algorithm == "A*":
            dist, path, trace = a_star(self.selected_graph, source_node, destination_node)
        return dist, path, trace
    
    def reset_values(self):
        """
        Reset the values of the screen
        """
        self.P1, self.P2, self.mouse_pos_P1, self.mouse_pos_P2, self.selected_city, self.selected_graph, self.dist, self.limits = None, None, None, None, None, None, None, None
        self.visited_edges = []
        self.index = 0
        self.path_calculated, self.search_visualized = False, False

    def reset_points(self):
        """
        Reset the points selected by the user
        """
        self.P1, self.P2, self.mouse_pos_P1, self.mouse_pos_P2, self.dist = None, None, None, None, None
        self.visited_edges = []
        self.index = 0
        self.path_calculated, self.search_visualized = False, False

class ScreenController:
    def __init__(self):
        self.screens = {
            "initial": InitialScreen(),
            "visualization": VisualizationScreen()
        }
        self.current_screen = self.screens["initial"] 

    def change_screen(self, screen_name):
        """
        Change the current screen
        """
        if screen_name in self.screens:
            if screen_name == "visualization":
                self.screens["visualization"].set_selected_city(self.screens["initial"].selected_city)
            self.current_screen = self.screens[screen_name]

    def handle_events(self, events):
        """
        Handle the events of the current screen
        """
        result = self.current_screen.handle_events(events)
        if result:
            self.change_screen(result)

    def update(self):
        """
        Update the current screen
        """
        self.current_screen.update()

    def draw(self, screen):
        """
        Draw the current screen
        """
        self.current_screen.draw(screen)

# Initialize the screen and the screen controller
pygame.init()
pygame.display.set_caption("Search Algorithms Visualization")
pygame.display.set_icon(pygame.image.load('static/LOCATION.png'))
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
import pygame
from PIL import Image
import pickle
from constants import MADRID_LIMITS, CHICAGO_LIMITS, SHIFT
from functions import cartesian_to_geo, geo_to_cartesian, get_nearest_node
import numpy as np
from graph.algorithms.dijkstra import dijkstra
from graph.algorithms.a_star import a_star
import time

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
COLOR_FONDO = (24, 24, 29)
VERDE_OSCURO = (65, 84, 85)
VERDE_BRILLANTE = (131, 179, 185)
GRIS = (150, 150, 150)
ROJO = (255, 0, 0)

class PantallaBase:
    def __init__(self):
        self.title_font = pygame.font.Font(None, 80)
        self.subtitle_font = pygame.font.Font(None, 30)
        self.bigger_text_font = pygame.font.Font(None, 25)
        self.text_font = pygame.font.Font(None, 23)

    def manejar_eventos(self, eventos):
        """Manejar eventos como pulsaciones de teclas o clicks."""
        pass

    def actualizar(self):
        """Actualizar la lógica de la pantalla."""
        pass

    def dibujar(self, pantalla):
        """Dibujar los elementos de la pantalla."""
        pass

    def dibujar_imagen(self, path, shape, pos):
        img = Image.open(path)
        img_redim = img.resize(shape, Image.ANTIALIAS)
        img_redim_pg = pygame.image.fromstring(img_redim.tobytes(), img_redim.size, img_redim.mode)
        pantalla.blit(img_redim_pg, pos)

    def dibujar_texto(self, text, font, color, pos):
        text_to_draw = font.render(text, True, color)
        pantalla.blit(text_to_draw, pos)

class PantallaInicio(PantallaBase):
    def __init__(self):
        super().__init__()
        self.selected_city = None

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mouse_pos[0] > 180 and mouse_pos[0] < 435 and mouse_pos[1] > 330 and mouse_pos[1] < 500:
                    self.selected_city = "Chicago"
                    return "visualizacion"
                elif mouse_pos[0] > 580 and mouse_pos[0] < 835 and mouse_pos[1] > 330 and mouse_pos[1] < 500:
                    self.selected_city = "Madrid"
                    return "visualizacion"
        return None

    def dibujar(self, pantalla):
        pantalla.fill(COLOR_FONDO)
        
        pygame.draw.rect(pantalla, VERDE_OSCURO, (0, 0, 1000, 150))
        self.dibujar_texto(text="SEARCH ALGORITHMS", font=self.title_font, color=BLANCO, pos=(180, 50))
        self.dibujar_texto(text="Discover the most common search algorithms with a visualization!", font=self.subtitle_font, color=VERDE_BRILLANTE, pos=(165, 210))
        self.dibujar_texto(text="Pick a city", font=self.subtitle_font, color=VERDE_BRILLANTE, pos=(450, 260))

        self.dibujar_imagen(path='images/CHICAGO.jpg', shape=(255, 170), pos=(180, 330))
        self.dibujar_imagen(path='images/MADRID.jpg', shape=(255, 170), pos=(580, 330))

        self.dibujar_texto(text="Chicago", font=self.text_font, color=VERDE_BRILLANTE, pos=(280, 510))
        self.dibujar_texto(text="Madrid", font=self.text_font, color=VERDE_BRILLANTE, pos=(680, 510))

class PantallaVisualizacion(PantallaBase):
    def __init__(self):
        super().__init__()
        self.jugando = True
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

        with open('maps/madrid_edges.pkl', 'rb') as archivo:
            self.madrid_edges = pickle.load(archivo)
        with open('maps/chicago_edges.pkl', 'rb') as archivo:
            self.chicago_edges = pickle.load(archivo)
        with open('maps/madrid_graph.pkl', 'rb') as archivo:
            self.madrid_graph = pickle.load(archivo)
        with open('maps/chicago_graph.pkl', 'rb') as archivo:
            self.chicago_graph = pickle.load(archivo)

    def set_selected_city(self, city):
        self.selected_city = city
        if city == "Madrid":
            self.selected_graph = self.madrid_graph
        elif city == "Chicago":
            self.selected_graph = self.chicago_graph

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Selecting p1
                if self.selecting_p1 and mouse_pos[0] > 300 and mouse_pos[0] < 1000 and mouse_pos[1] > 0 and mouse_pos[1] < 600:
                    self.mouse_pos_p1 = mouse_pos
                    if self.selected_city == "Madrid":
                        self.p1 = cartesian_to_geo(mouse_pos[0] - SHIFT, mouse_pos[1],
                                                   MADRID_LIMITS[1][0], MADRID_LIMITS[1][1],
                                                   MADRID_LIMITS[0][0], MADRID_LIMITS[0][1])
                    elif self.selected_city == "Chicago":
                        self.p1 = cartesian_to_geo(mouse_pos[0], mouse_pos[1],
                                                   CHICAGO_LIMITS[1][0], CHICAGO_LIMITS[1][1],
                                                   CHICAGO_LIMITS[0][0], CHICAGO_LIMITS[0][1])
                    self.selecting_p2 = True
                    self.selecting_p1 = False

                # Selecting p2
                elif self.selecting_p2 and mouse_pos[0] > 300 and mouse_pos[0] < 1000 and mouse_pos[1] > 0 and mouse_pos[1] < 600:
                    self.mouse_pos_p2 = mouse_pos
                    if self.selected_city == "Madrid":
                        self.p2 = cartesian_to_geo(mouse_pos[0] - SHIFT, mouse_pos[1],
                                                   MADRID_LIMITS[1][0], MADRID_LIMITS[1][1],
                                                   MADRID_LIMITS[0][0], MADRID_LIMITS[0][1])
                    elif self.selected_city == "Chicago":
                        self.p2 = cartesian_to_geo(mouse_pos[0], mouse_pos[1],
                                                   CHICAGO_LIMITS[1][0], CHICAGO_LIMITS[1][1],
                                                   CHICAGO_LIMITS[0][0], CHICAGO_LIMITS[0][1])
                    self.selecting_p2 = False

                # Botón para aplicar Dijkstra
                elif mouse_pos[0] > 24 and mouse_pos[0] < 270 and mouse_pos[1] > 247 and mouse_pos[1] < 287:
                    if self.p1 and self.p2:
                        self.algorithm = "Dijkstra"
                        dist, path, trace = self.calcular_camino()
                        self.trace = trace
                        self.path_calculated = True

                # Botón para aplicar A*
                elif mouse_pos[0] > 24 and mouse_pos[0] < 270 and mouse_pos[1] > 297 and mouse_pos[1] < 337:
                    if self.p1 and self.p2:
                        self.algorithm = "A*"
                        dist, path, trace = self.calcular_camino()
                        self.trace = trace
                        self.path_calculated = True

                # Going back
                elif mouse_pos[0] > 27 and mouse_pos[0] < 267 and mouse_pos[1] > 530 and mouse_pos[1] < 565:
                    self.p1, self.p2, self.mouse_pos_p1, self.mouse_pos_p2, self.selected_city, self.selected_graph, self.index = None, None, None, None, None, None, 0
                    return "inicio"
                
                # Selecting points
                elif mouse_pos[0] > 27 and mouse_pos[0] < 267 and mouse_pos[1] > 51 and mouse_pos[1] < 85:
                    self.selecting_p1 = True
        return None

    def actualizar(self):
        if self.p1:
            pygame.draw.circle(pantalla, ROJO, self.mouse_pos_p1, 3)
            self.dibujar_texto(text=str((np.round(self.p1[0], 3), np.round(self.p1[1], 3))), font=self.bigger_text_font, color=COLOR_FONDO, pos=(100, 110))

        if self.p1_nearest:
            pygame.draw.circle(pantalla, BLANCO, self.p1_nearest, 3)
        
        if self.p2:
            pygame.draw.circle(pantalla, ROJO, self.mouse_pos_p2, 3)
            self.dibujar_texto(text=str((np.round(self.p2[0], 3), np.round(self.p2[1], 3))), font=self.bigger_text_font, color=COLOR_FONDO, pos=(100, 160))
        
        if self.p2_nearest:
            pygame.draw.circle(pantalla, BLANCO, self.p2_nearest, 3)

        if self.path_calculated:
            if self.selected_city == "Madrid":
                tr = [geo_to_cartesian(lon, lat, MADRID_LIMITS[1][0], MADRID_LIMITS[1][1], 
                                                      MADRID_LIMITS[0][0], MADRID_LIMITS[0][1]) for lon, lat in self.trace[self.index]]
                self.visited_edges.append(tr)
                for edge in self.visited_edges:
                    pygame.draw.lines(pantalla, color=VERDE_BRILLANTE, closed=True, points=edge, width=2)

            elif self.selected_city == "Chicago":
                for t in self.trace:
                    t_transformed = [geo_to_cartesian(lon, lat, CHICAGO_LIMITS[1][0], CHICAGO_LIMITS[1][1], 
                                                      CHICAGO_LIMITS[0][0], CHICAGO_LIMITS[0][1]) for lon, lat in t]
                    pygame.draw.lines(pantalla, color=VERDE_BRILLANTE, closed=True, points=t_transformed, width=2)
        
        self.index += 1

    def dibujar_mapa(self):
        if self.selected_city == "Madrid":
            edges_to_draw = self.madrid_edges
        else:
            edges_to_draw = self.chicago_edges

        for edges in edges_to_draw:
            pygame.draw.lines(pantalla, color=VERDE_OSCURO, closed=True, points=edges, width=1)

    def dibujar(self, pantalla):
        pantalla.fill(COLOR_FONDO)

        self.dibujar_mapa()

        pygame.draw.rect(pantalla, VERDE_OSCURO, (0, 0, 300, 1000))

        pygame.draw.rect(pantalla, GRIS, (25, 48, 244, 39))
        pygame.draw.rect(pantalla, BLANCO, (28, 51, 239, 34))
        self.dibujar_texto(text="Select points", font=self.bigger_text_font, color=COLOR_FONDO, pos=(90, 60))

        pygame.draw.rect(pantalla, BLANCO, (27, 100, 240, 35))
        self.dibujar_texto(text="P1: ", font=self.bigger_text_font, color=COLOR_FONDO, pos=(40, 110))

        pygame.draw.rect(pantalla, BLANCO, (27, 150, 240, 35))
        self.dibujar_texto(text="P2: ", font=self.bigger_text_font, color=COLOR_FONDO, pos=(40, 160))

        pygame.draw.rect(pantalla, GRIS, (24, 247, 245, 40))
        pygame.draw.rect(pantalla, BLANCO, (27, 250, 240, 35))
        self.dibujar_texto(text="Apply Dijkstra", font=self.bigger_text_font, color=COLOR_FONDO, pos=(90, 260))

        pygame.draw.rect(pantalla, GRIS, (24, 297, 245, 40))
        pygame.draw.rect(pantalla, BLANCO, (27, 300, 240, 35))
        self.dibujar_texto(text="Apply A*", font=self.bigger_text_font, color=COLOR_FONDO, pos=(110, 310))

        pygame.draw.rect(pantalla, GRIS, (24, 527, 245, 40))
        pygame.draw.rect(pantalla, BLANCO, (27, 530, 240, 35))
        self.dibujar_texto(text="Back", font=self.bigger_text_font, color=COLOR_FONDO, pos=(127, 540))
    
    def calcular_camino(self):
        source_node = get_nearest_node(self.selected_graph, self.p1[0], self.p1[1])
        # source_node_cart = geo_to_cartesian(source_node.longitude, source_node.latitude, MADRID_LIMITS[1][0], MADRID_LIMITS[1][1], 
        #                                     MADRID_LIMITS[0][0], MADRID_LIMITS[0][1])
        # self.p1_nearest = source_node_cart

        destination_node = get_nearest_node(self.selected_graph, self.p2[0], self.p2[1])
        # destination_node_cart = geo_to_cartesian(destination_node.longitude, destination_node.latitude, MADRID_LIMITS[1][0], MADRID_LIMITS[1][1], 
        #                                     MADRID_LIMITS[0][0], MADRID_LIMITS[0][1])
        # self.p2_nearest = destination_node_cart
        
        if self.algorithm == "Dijkstra":
            dist, path, trace = dijkstra(self.selected_graph, source_node, destination_node)
        elif self.algorithm == "A*":
            print(source_node, destination_node)
            dist, path, trace = a_star(self.selected_graph, source_node, destination_node)
        return dist, path, trace

class ControladorPantallas:
    def __init__(self):
        self.pantallas = {
            "inicio": PantallaInicio(),
            "visualizacion": PantallaVisualizacion()
        }
        self.pantalla_actual = self.pantallas["inicio"] 

    def cambiar_pantalla(self, nombre_pantalla):
        """Cambiar a una pantalla diferente por nombre."""
        if nombre_pantalla in self.pantallas:
            if nombre_pantalla == "visualizacion":
                self.pantallas["visualizacion"].set_selected_city(self.pantallas["inicio"].selected_city)
            self.pantalla_actual = self.pantallas[nombre_pantalla]

    def manejar_eventos(self, eventos):
        resultado = self.pantalla_actual.manejar_eventos(eventos)
        if resultado:
            self.cambiar_pantalla(resultado)

    def actualizar(self):
        self.pantalla_actual.actualizar()

    def dibujar(self, pantalla):
        self.pantalla_actual.dibujar(pantalla)

# Inicializar pygame
pygame.init()

# Crear la pantalla del juego
pantalla = pygame.display.set_mode((1000, 600))

# Inicializar el controlador de pantallas
controlador_pantallas = ControladorPantallas()

# Bucle principal
corriendo = True
while corriendo:
    # Manejar eventos
    eventos = pygame.event.get()
    for evento in eventos:
        if evento.type == pygame.QUIT:
            corriendo = False

    # Manejar eventos de la pantalla actual
    controlador_pantallas.manejar_eventos(eventos)

    # Dibujar la pantalla actual
    controlador_pantallas.dibujar(pantalla)

    # Actualizar lógica de la pantalla actual
    controlador_pantallas.actualizar()

    # Actualizar la pantalla
    pygame.display.flip()

# Finalizar pygame
pygame.quit()
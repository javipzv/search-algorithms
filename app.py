import pygame
from PIL import Image
import pickle

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
COLOR_FONDO = (24, 24, 29)
VERDE_OSCURO = (65, 84, 85)
VERDE_BRILLANTE = (131, 179, 185)
GRIS = (150, 150, 150)

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
        self.p1 = None
        self.p2 = None
        self.selecting_p1 = False
        self.selecting_p2 = False
        self.selected_city = None
        with open('maps/madrid_edges.pkl', 'rb') as archivo:
            self.madrid_edges = pickle.load(archivo)
        with open('maps/chicago_edges.pkl', 'rb') as archivo:
            self.chicago_edges = pickle.load(archivo)

    def set_selected_city(self, city):
        self.selected_city = city

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if self.selecting_p1 and mouse_pos[0] > 300 and mouse_pos[0] < 1000 and mouse_pos[1] > 0 and mouse_pos[1] < 600:
                    print(mouse_pos)
                    self.selecting_p2 = True
                    self.selecting_p1 = False

                elif self.selecting_p2 and mouse_pos[0] > 300 and mouse_pos[0] < 1000 and mouse_pos[1] > 0 and mouse_pos[1] < 600:
                    print(mouse_pos)
                    self.selecting_p2 = False

                elif mouse_pos[0] > 27 and mouse_pos[0] < 267 and mouse_pos[1] > 530 and mouse_pos[1] < 565:
                    return "inicio"
                
                elif mouse_pos[0] > 27 and mouse_pos[0] < 267 and mouse_pos[1] > 51 and mouse_pos[1] < 85:
                    self.selecting_p1 = True
        return None

    def actualizar(self):
        # Aquí va la lógica del juego
        pass

    def dibujar_mapa(self):
        if self.selected_city == "Madrid":
            edges_to_draw = self.madrid_edges
        else:
            edges_to_draw = self.chicago_edges

        for edges in edges_to_draw:
            pygame.draw.lines(pantalla, color=VERDE_BRILLANTE, closed=True, points=edges, width=1)

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

    # Actualizar lógica de la pantalla actual
    controlador_pantallas.actualizar()

    # Dibujar la pantalla actual
    controlador_pantallas.dibujar(pantalla)

    # Actualizar la pantalla
    pygame.display.flip()

# Finalizar pygame
pygame.quit()
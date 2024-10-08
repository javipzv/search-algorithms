import pygame
import sys
import regex as re

def latitude_to_screen(latitude):
    return (41.6445929 - latitude) * 600 / (41.6445929 - 42.0227242)

def longitude_to_screen(longitude):
    return (-87.5245786 - longitude) * 700 / (-87.5245786 + 87.8563351)

# Inicializar pygame
pygame.init()

# Definir dimensiones de la ventana
width, height = 700, 600
screen = pygame.display.set_mode((width, height))

# Definir color (RGB)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# Coordenada del punto (en el centro de la ventana)
point_position = (width // 2, height // 2)

with open('trace_astar.txt') as f:
    content = f.readlines()

i = 0

source_lat, source_lon = (41.8516426, -87.7233332)
x, y =  longitude_to_screen(source_lon), latitude_to_screen(source_lat)

dest_lat, dest_lon = (41.7461637, -87.7363158)
a, b = longitude_to_screen(dest_lon), latitude_to_screen(dest_lat) 

# Bucle principal
running = True
screen.fill(white)
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.circle(screen, red, (x, y), 5)
    pygame.draw.circle(screen, red, (a, b), 5)

    # Dibujar un nodo
    if i < len(content):
        node = re.findall("-?\d{1,2}\.\d*", content[i])
        latitude_source = latitude_to_screen(float(node[0]))
        longitude_source = longitude_to_screen(float(node[1]))
        latitude_destination = latitude_to_screen(float(node[2]))
        longitude_destination = longitude_to_screen(float(node[3]))

    # Dibujar el punto (grosor 5 píxeles)
    pygame.draw.circle(screen, black, (longitude_source, latitude_source), 1)
    pygame.draw.circle(screen, black, (longitude_destination, latitude_destination), 1)

    # Actualizar la pantalla
    pygame.display.flip()
    i += 1

# Salir de pygame
pygame.quit()
sys.exit()

import pygame
import sys
import regex as re
import time

def latitude_to_screen(latitude):
    return (40.36 - latitude) * 600 / (40.36 - 40.47)

def longitude_to_screen(longitude):
    return (-3.62 - longitude) * 700 / (-3.62 + 3.77)

# Inicializar pygame
pygame.init()

# Definir dimensiones de la ventana
width, height = 710, 610
screen = pygame.display.set_mode((width, height))

# Definir color (RGB)
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
red2 = (37, 0, 0)
fondo = (24, 24, 29)
calles = (65,84,85)
calles_pintadas = (101,179,185)

# Coordenada del punto (en el centro de la ventana)
point_position = (width // 2, height // 2)

with open('traces/trace_dijkstra.txt') as f:
    content = f.readlines()

i = 0

source_lat, source_lon = (40.4506315, -3.6877832)
x, y =  longitude_to_screen(source_lon), latitude_to_screen(source_lat)

dest_lat, dest_lon = (40.3981148, -3.6595603)
a, b = longitude_to_screen(dest_lon), latitude_to_screen(dest_lat) 

# Bucle principal
running = True
screen.fill(fondo)
while running:
    # Manejar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.draw.circle(screen, red, (x, y), 5)
    pygame.draw.circle(screen, red, (a, b), 5)

    # Dibujar un nodo
    if i < len(content):
        nodes = re.findall("-?\d{1,2}\.\d*", content[i])
        latitude_source = latitude_to_screen(float(nodes[0]))
        longitude_source = longitude_to_screen(float(nodes[1]))
        latitude_destination = latitude_to_screen(float(nodes[2]))
        longitude_destination = longitude_to_screen(float(nodes[3]))
        path = [(longitude_source, latitude_source)]
        for j in range(4, len(nodes), 2):
            path.append((longitude_to_screen(float(nodes[j])), latitude_to_screen(float(nodes[j+1]))))
        path.append((longitude_destination, latitude_destination))
    
    # Dibujar el path (grosor 5 píxeles)
    pygame.draw.lines(screen, color=calles_pintadas, closed=True, points=path, width=1)

    # Actualizar la pantalla
    pygame.display.flip()
    i += 1

# Salir de pygame
pygame.quit()
sys.exit()
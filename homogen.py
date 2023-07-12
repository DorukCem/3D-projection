import pygame
import numpy as np
from math import sin, cos


WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WIDTH, HEIGHT = 800, 600

pygame.init()
screen = pygame.display.set_mode((WIDTH ,  HEIGHT))
clock = pygame.time.Clock()

scale = 100
position = [WIDTH/2, HEIGHT/2, 5]  # x, y
angle = 0
camera_dist = 20

cube_vertices= [
    np.array([-1,-1,-1]),
    np.array([ 1,-1,-1]),
    np.array([ 1, 1,-1]),
    np.array([-1, 1,-1]),
    np.array([-1,-1, 1]),
    np.array([ 1,-1, 1]),
    np.array([ 1, 1, 1]),
    np.array([-1, 1, 1])
   ]

projection_matrix = np.array([ 
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
])

# One dimension stays the same, since we are rotating around that axis
def rot_mat_x(a):
    return np.array([
        [1, 0, 0, 0],
        [0, cos(a), -sin(a), 0], 
        [0, sin(a), cos(a), 0],
        [0, 0, 0, 1]
    ])

def rot_mat_y(a):
    return np.array([
        [cos(a), 0, sin(a), 0],
        [0, 1, 0, 0],
        [-sin(a), 0, cos(a), 0],
        [0, 0, 0, 1]
        ])

def rot_mat_z(a):
    return np.array([
        [cos(a), 0, -sin(a), 0],
        [sin(a), 0, cos(a), 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
        ])

def translate_mat(p):
    x,y,z = p
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])


def draw_edges(vertices):
    edges = [
        (0, 1),
        (0, 3),
        (0, 4),
        (1, 2),
        (1, 5),
        (2, 6),
        (2, 3),
        (3, 7),
        (4, 5),
        (4, 7),
        (6, 5),
        (6, 7)
    ]

    for edge in edges:
        a, b = edge
        pygame.draw.line(screen, WHITE, vertices[a], vertices[b], 1)



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill( BLACK )

    angle += 0.03
    

    projected_points = []
    for v in cube_vertices:
        print(v)
        scaled = v * 100
        exp = np.array([*scaled, 1]) #(-100, 100, 0, 1)
        trans = np.dot(translate_mat(position), exp) #(300, 500, 5, 1)
        print(trans)
        print("----")
        rot_x = np.dot(rot_mat_x(angle), trans) 
        rot_y = np.dot(rot_mat_y(angle), rot_x)
        point4d = np.dot(rot_mat_z(angle), rot_y)

        point4d /= point4d[3]
        projection_matrix = point4d 
        x, y, z, w = projection_matrix
        
       

        projected_points.append((x,y))

        #draw points
        pygame.draw.circle(screen, WHITE, (x, y), 5 )
    
    draw_edges(projected_points)

    pygame.display.update()
    clock.tick(60)

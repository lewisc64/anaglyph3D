import math
import pygame

def rotate(x, y, angle):
    mag = math.sqrt(x ** 2 + y ** 2)
    p_angle = math.atan2(y, x)
    x2 = mag * math.cos(p_angle + angle)
    y2 = mag * math.sin(p_angle + angle)
    return x2, y2

def transform_point(p, camera):
    x = p[0] - camera.x
    y = p[1] - camera.y
    z = p[2] - camera.z
    
    x, z = rotate(x, z, camera.yaw)
    y, z = rotate(y, z, camera.pitch)
    
    return x, y, z

def get_screen_point(p, surface):
    x, y, z = p
    f = 500 / z
    width, height = surface.get_size()
    
    x *= f
    y *= f
    
    return x + width // 2, y + height // 2
    
def get_screen_points(p, channels, intensity=10):
    x, y, z = p
    x, y = get_screen_point(p, channels[0])
    
    seperation = intensity * z
    
    return [(x - seperation / 2, y), (x + seperation / 2, y)]

def draw(surface, camera, color, shape):
    lines = []
    for line in shape.get_lines():
        transformed = [transform_point(p, camera) for p in line]
        if transformed[0][2] < 0 or transformed[1][2] < 0:
            continue
        lines.append([get_screen_point(p, surface) for p in transformed])
    for line in lines:
        try:
            pygame.draw.line(surface, color, line[0], line[1])
        except TypeError:
            pass

def draw3d(channels, camera, colors, shape, intensity=5):
    lines = []
    for line in shape.get_lines():
        transformed = [transform_point(p, camera) for p in line]
        if transformed[0][2] < 0 or transformed[1][2] < 0:
            continue
        lines.append([get_screen_points(p, channels, intensity) for p in transformed])
    for line in lines:
        try:
            pygame.draw.line(channels[0], colors[0], line[0][0], line[1][0])
            pygame.draw.line(channels[1], colors[1], line[0][1], line[1][1])
        except TypeError:
            print(line[0], line[1])

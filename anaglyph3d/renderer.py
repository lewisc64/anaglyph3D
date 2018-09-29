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
    side = max(surface.get_size())
    
    x *= f
    y *= f
    
    return x + side // 2, y + side // 2

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
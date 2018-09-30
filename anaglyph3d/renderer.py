import math
import pygame

channel_colors = [(255, 0, 0), (0, 255, 255)]

def get_channels(width, height):
    return pygame.Surface((width, height)), pygame.Surface((width, height))

def apply_channels(surface, channels):
    apply = pygame.Surface(surface.get_size())
    apply.blit(channels[0], (0, 0), special_flags=pygame.BLEND_ADD)
    apply.blit(channels[1], (0, 0), special_flags=pygame.BLEND_ADD)
    channels[0].fill((0, 0, 0))
    channels[1].fill((0, 0, 0))
    surface.blit(apply, (0, 0))

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

def draw3d(channels, camera, shape, intensity=5):
    lines = []
    for line in shape.get_lines():
        transformed = [transform_point(p, camera) for p in line]
        if transformed[0][2] < 0 or transformed[1][2] < 0:
            continue
        lines.append([get_screen_points(p, channels, intensity) for p in transformed])
    for line in lines:
        try:
            pygame.draw.line(channels[0], channel_colors[0], line[0][0], line[1][0])
            pygame.draw.line(channels[1], channel_colors[1], line[0][1], line[1][1])
        except TypeError:
            print(line[0], line[1])

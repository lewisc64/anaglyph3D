from .renderer import *

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

def draw_anaglyph(channels, camera, shape, intensity=5):
    draw3d(channels, camera, channel_colors, shape, intensity)
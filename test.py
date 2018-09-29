import pygame
import anaglyph3d
pygame.init()

WIDTH, HEIGHT = 800, 800
FPS = 60

channels = anaglyph3d.get_channels(WIDTH, HEIGHT)
display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

camera = anaglyph3d.Camera(0, 0, 0, 0, 0)

shapes = [
    anaglyph3d.Cube(-0.5, -0.5, 5, 1, 1, 1),
    anaglyph3d.Cube(-0.5, 5, -0.5, 1, 1, 1),
]

camera.capture()

while True:
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            quit()
        camera.handle_event(e)
    
    camera.update(display)
    
    display.fill((0, 0, 0))
    for shape in shapes:
        anaglyph3d.draw3d(channels, camera, shape)
        
    anaglyph3d.apply_channels(display, channels)
    
    pygame.display.update()
    clock.tick(FPS)
import pygame
import math

class Camera:
    def __init__(self, x, y, z, pitch, yaw):
        self.x = x
        self.y = y
        self.z = z
        self.pitch = pitch
        self.yaw = yaw
        self.sensitivity = 100
        self.speed = 0.1
        
        self.first_capture = True
        self.capture_mouse = False
        self.held_keys = []
        self.controls = {
            "forward":pygame.K_w,
            "back":pygame.K_s,
            "left":pygame.K_a,
            "right":pygame.K_d,
            "up":pygame.K_SPACE,
            "down":pygame.K_LSHIFT
        }
    
    def capture(self):
        self.first_capture = True
        pygame.event.set_grab(True)
        pygame.mouse.set_visible(False)
        self.capture_mouse = True
    
    def release(self):
        pygame.event.set_grab(False)
        pygame.mouse.set_visible(True)
        self.capture_mouse = False
    
    def handle_event(self, e):
        if e.type == pygame.KEYDOWN:
            if e.key not in self.held_keys:
                self.held_keys.append(e.key)
        elif e.type == pygame.KEYUP:
            while e.key in self.held_keys:
                self.held_keys.remove(e.key)
    
    def move_rel_flat(self, rx, ry, rz):
        if rz != 0:
            self.x += rz * math.sin(self.yaw)
            self.z += rz * math.cos(self.yaw)
        if rx != 0:
            self.x += rx * math.sin(self.yaw + math.pi / 2)
            self.z += rx * math.cos(self.yaw + math.pi / 2)
    
    def update(self, surface):
        width, height = surface.get_size()
        
        if self.capture_mouse:
            x, y = pygame.mouse.get_pos()
            x -= width // 2
            y -= height // 2
            pygame.mouse.set_pos((width // 2, height // 2))
            if self.first_capture:
                self.first_capture = False
            else:
                self.yaw = (self.yaw + x / self.sensitivity) % (math.pi * 2)
                self.pitch = max(min(self.pitch + y / self.sensitivity, math.pi / 2), -math.pi / 2)
        
        if self.controls["up"] in self.held_keys:
            self.y -= self.speed
        if self.controls["down"] in self.held_keys:
            self.y += self.speed
        if self.controls["forward"] in self.held_keys:
            self.move_rel_flat(0, 0, self.speed)
        if self.controls["back"] in self.held_keys:
            self.move_rel_flat(0, 0, -self.speed)
        if self.controls["left"] in self.held_keys:
            self.move_rel_flat(-self.speed, 0, 0)
        if self.controls["right"] in self.held_keys:
            self.move_rel_flat(self.speed, 0, 0)
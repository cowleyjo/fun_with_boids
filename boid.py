import math
import pygame

class Boid:
    def __init__(self, x, y, angle, size):
        self.pos = pygame.math.Vector2(x, y)
        self.angle = angle
        self.size = size

    def triangle_points(self):
        rad = math.radians(self.angle)
        p1 = (self.pos.x + math.sin(rad) * self.size, self.pos.y - math.cos(rad) * self.size)

        # Left Corner (120 degree offset)
        rad_left = math.radians(self.angle + 120)
        p2 = (self.pos.x + math.sin(rad_left) * self.size, self.pos.y - math.cos(rad_left) * self.size)

        # Right Corner (240 degree offset)
        rad_right = math.radians(self.angle + 240)
        p3 = (self.pos.x + math.sin(rad_right) * self.size, self.pos.y - math.cos(rad_right) * self.size)

        return [p1, p2, p3]
    
    def update(self):
        rad = math.radians(self.angle)
        self.pos += pygame.math.Vector2(math.sin(rad), -math.cos(rad)) * 2

    


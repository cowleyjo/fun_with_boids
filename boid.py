import math
import pygame

from config import WIDTH, HEIGHT, EDGE_GAP, ALIGNMENT_FACTOR, COHESION_FACTOR, SEPARATION_FACTOR, VIS_RANGE

class Boid:
    def __init__(self, x, y, angle, size, speed):
        self.pos = pygame.math.Vector2(x, y)
        self.angle = angle
        self.size = size
        self.speed = speed
        self.vis_range = VIS_RANGE

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
    
    def update(self, boids):
        rad = math.radians(self.angle)
        self.pos += pygame.math.Vector2(math.sin(rad), -math.cos(rad)) * self.speed

         # Edge Teleport for X Direction
        if self.pos.x < -EDGE_GAP:
            self.pos.x = WIDTH
        if self.pos.x > WIDTH + EDGE_GAP:
            self.pos.x = 0
        
        # Edge Teleport for Y Direction
        if self.pos.y < -EDGE_GAP:
            self.pos.y = HEIGHT
        if self.pos.y > HEIGHT + EDGE_GAP:
            self.pos.y = 0

        neighbors = self.get_neighbors(boids)

        # for neighbor in neighbors
        #   apply alignment, cohesion, and separation
        #   make sure to use the factors!!!!
        # if neighbors:
        #     print(f"Boid at ({self.pos.x:.1f}, {self.pos.y:.1f}) sees {len(neighbors)} neighbors")


    def get_neighbors(self, boids):
        neighbors = []
        for other in boids:
            if other is self:
                continue

            dx = other.pos.x - self.pos.x
            dy = other.pos.y - self.pos.y
            dist = math.sqrt(dx*dx + dy*dy)

            if dist < self.vis_range:
                neighbors.append(other)
                # print("neighbor added!")
        return neighbors


    def cohesion(self):
        pass

    


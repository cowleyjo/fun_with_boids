import math
import pygame
import random

import config
from config import WIDTH, HEIGHT, EDGE_GAP, ALIGNMENT_FACTOR, COHESION_FACTOR, SEPARATION_FACTOR, VIS_RANGE, PROTECT_RANGE, MAX_SPEED

class Boid:
    def __init__(self, x, y, angle, size):
        self.pos = pygame.math.Vector2(x, y)
        dir_vec = pygame.math.Vector2(math.cos(math.radians(angle)),
                                      math.sin(math.radians(angle)))
        self.velocity = dir_vec.normalize() * random.uniform(2, MAX_SPEED)
        self.angle = angle
        self.size = size
        self.vis_range = VIS_RANGE
        self.protect_range = PROTECT_RANGE
        self.alignment_factor = ALIGNMENT_FACTOR
        self.cohesion_factor = COHESION_FACTOR
        self.separation_factor = SEPARATION_FACTOR

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
        
        speed = self.velocity.length()
        if speed > MAX_SPEED:
            self.velocity = self.velocity.normalize() * MAX_SPEED
        elif speed < 3:
            self.velocity.scale_to_length(3)
        
        self.pos += self.velocity

        if self.velocity.length_squared() > 0:
            self.angle = math.degrees(math.atan2(self.velocity.y, self.velocity.x)) + 90
    

        neighbors = self.get_neighbors(boids)
        if neighbors:
            self.cohesion(neighbors)
            self.separation(self.get_dangerous_neighbors(neighbors))
            self.alignment(neighbors)
        
        self.player_interaction(config.PLAYER_X, config.PLAYER_Y)

        # Edge Teleport for X Direction
        if self.pos.x < -EDGE_GAP:
            self.pos.x = config.WIDTH
        if self.pos.x > config.WIDTH + EDGE_GAP:
            self.pos.x = 0
        
        # Edge Teleport for Y Direction
        if self.pos.y < -EDGE_GAP:
            self.pos.y = config.HEIGHT
        if self.pos.y > config.HEIGHT + EDGE_GAP:
            self.pos.y = 0

    # Returns a list of all boids within the visibility range
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
    
    # Returns a list of all boids within the protected range (Calls get_neighbors)
    def get_dangerous_neighbors(self, neighbors):
        dangerous_neighbors = []
    
        for neighbor in neighbors:
            dx = neighbor.pos.x - self.pos.x
            dy = neighbor.pos.y - self.pos.y
            dist = math.sqrt(dx*dx + dy*dy)

            if dist < self.protect_range:
                dangerous_neighbors.append(neighbor)
        
        return dangerous_neighbors


    def alignment(self, neighbors):
        xvel_avg = 0
        yvel_avg = 0
        
        for neighbor in neighbors:
            xvel_avg += neighbor.velocity.x
            yvel_avg += neighbor.velocity.y
        
        xvel_avg = xvel_avg / len(neighbors)
        yvel_avg = yvel_avg / len(neighbors)

        self.velocity.x += (xvel_avg - self.velocity.x) * self.alignment_factor
        self.velocity.y += (yvel_avg - self.velocity.y) * self.alignment_factor
        
    def separation(self, dang_neighbors):
        for boid in dang_neighbors:
            offset = self.pos - boid.pos
            dist = offset.length()
            if dist > 0:
                self.velocity += (offset / dist) * self.separation_factor
    
    def cohesion(self, neighbors):
        xpos_avg = 0
        ypos_avg = 0

        for boid in neighbors:
            xpos_avg += boid.pos.x
            ypos_avg += boid.pos.y

        xpos_avg = xpos_avg / len(neighbors)
        ypos_avg = ypos_avg / len(neighbors)

        self.velocity.x += (xpos_avg - self.pos.x) * self.cohesion_factor
        self.velocity.y += (ypos_avg - self.pos.y) * self.cohesion_factor

    def player_interaction(self, x, y):
        dx = x - self.pos.x
        dy = y - self.pos.y
        dist = math.sqrt(dx*dx + dy*dy)

        if dist < self.vis_range:
            if config.PLAYER_ATTRACT > 0:
                self.velocity.x += (config.PLAYER_X - self.pos.x) * (self.cohesion_factor * config.PLAYER_COHESION)
                self.velocity.y += (config.PLAYER_Y - self.pos.y) * (self.cohesion_factor * config.PLAYER_COHESION)
            elif config.PLAYER_ATTRACT < 0:
                player_pos = pygame.math.Vector2(config.PLAYER_X, config.PLAYER_Y)
                offset = self.pos - player_pos
                self.velocity += (offset / dist) * (self.separation_factor * 2)
            elif config.PLAYER_ATTRACT < 0:
                player_pos = pygame.math.Vector2(config.PLAYER_X, config.PLAYER_Y)
                offset = self.pos - player_pos
                new_dist = offset.length()
                if new_dist > 0:
                    self.velocity += (offset / new_dist) * (self.separation_factor * config.PLAYER_SEPARATION)
    


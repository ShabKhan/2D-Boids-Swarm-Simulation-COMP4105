import pygame
import random
import math

MAX_SPEED = 2
MAX_FORCE = 0.05

class Boid:
    def __init__(self, width, height):
        self.position = pygame.Vector2(
            random.uniform(width / 3, 2 * width / 3),
            random.uniform(height / 3, 2 * height / 3)
        )
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.width = width
        self.height = height

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > MAX_SPEED:
            self.velocity.scale_to_length(MAX_SPEED)
        self.position += self.velocity
        self.acceleration *= 0
        self.wrap_around()

    def apply_behavior(self, boids, sep_weight=1.0, ali_weight=1.0, coh_weight=1.0):
        from utils import separation, alignment, cohesion
        sep = separation(self, boids) * sep_weight
        ali = alignment(self, boids, neighbor_dist=100) * ali_weight
        coh = cohesion(self, boids, neighbor_dist=100) * coh_weight
        self.acceleration += sep + ali + coh

    def draw(self, screen):
        angle = self.velocity.angle_to(pygame.Vector2(1, 0))
        points = [
            (self.position.x + 10 * math.cos(math.radians(angle)),
             self.position.y - 10 * math.sin(math.radians(angle))),
            (self.position.x + 5 * math.cos(math.radians(angle + 135)),
             self.position.y - 5 * math.sin(math.radians(angle + 135))),
            (self.position.x,
             self.position.y),
            (self.position.x + 5 * math.cos(math.radians(angle - 135)),
             self.position.y - 5 * math.sin(math.radians(angle - 135)))
        ]
        pygame.draw.polygon(screen, (0, 255, 255), points)

    def wrap_around(self):
        if self.position.x > self.width: self.position.x = 0
        if self.position.x < 0: self.position.x = self.width
        if self.position.y > self.height: self.position.y = 0
        if self.position.y < 0: self.position.y = self.height

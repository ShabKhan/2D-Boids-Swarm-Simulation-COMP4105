import pygame
import csv
import os
import math
from boid import Boid

class Obstacle:
    def __init__(self, x, y, size, shape="circle"):
        self.position = pygame.Vector2(x, y)
        self.size = size
        self.shape = shape

    def draw(self, screen):
        if self.shape == "circle":
            pygame.draw.circle(screen, (255, 0, 0), (int(self.position.x), int(self.position.y)), self.size, width=2)
        elif self.shape == "square":
            rect = pygame.Rect(self.position.x - self.size/2, self.position.y - self.size/2, self.size, self.size)
            pygame.draw.rect(screen, (255, 165, 0), rect, width=2)
        elif self.shape == "triangle":
            points = [
                (self.position.x, self.position.y - self.size),
                (self.position.x - self.size, self.position.y + self.size),
                (self.position.x + self.size, self.position.y + self.size)
            ]
            pygame.draw.polygon(screen, (255, 255, 0), points, width=2)

class Environment:
    def __init__(self, width, height, num_boids,
                 separation_strength=1.0, alignment_strength=1.0, cohesion_strength=1.0,with_predator=False, include_predator_column=False, log_file=None):
        self.width = width
        self.height = height
        self.include_predator_column = include_predator_column
        self.with_predator = with_predator
        self.boids = [Boid(width, height) for _ in range(num_boids)]
        self.obstacles = [
            Obstacle(width / 3, height / 3, 30, shape="circle"),
            Obstacle(2 * width / 3, 2 * height / 3, 40, shape="square"),
            Obstacle(width / 2, height / 4, 25, shape="triangle"),
            Obstacle(width / 2, 3 * height / 4, 35, shape="circle")
        ]

        self.step = 0
        self.collisions = 0
        self.leader = self.boids[0] if self.boids else None
        # Initialize predator if enabled
        if self.with_predator:
            self.predator = Boid(width, height)
            self.predator.color = (255, 0, 0)
            self.predator.is_predator = True
            self.predator.position = pygame.Vector2(0, height // 2)
            self.predator.velocity = pygame.Vector2(2, 1.5)

        self.separation_strength = separation_strength
        self.alignment_strength = alignment_strength
        self.cohesion_strength = cohesion_strength

        if log_file is None:
            self.log_file = os.path.join(os.path.dirname(__file__), "results", "simulation_log_temp.csv")
        else:
            self.log_file = log_file

    def handle_manual_leader_control(self, keys_pressed):
        if self.leader:
            speed = 2.5
            if keys_pressed[pygame.K_UP]:
                self.leader.position.y -= speed
            if keys_pressed[pygame.K_DOWN]:
                self.leader.position.y += speed
            if keys_pressed[pygame.K_LEFT]:
                self.leader.position.x -= speed
            if keys_pressed[pygame.K_RIGHT]:
                self.leader.position.x += speed

            if self.leader.position.x > self.width: self.leader.position.x = 0
            if self.leader.position.x < 0: self.leader.position.x = self.width
            if self.leader.position.y > self.height: self.leader.position.y = 0
            if self.leader.position.y < 0: self.leader.position.y = self.height

    def update(self, keys_pressed):
        self.handle_manual_leader_control(keys_pressed)
        if self.log_file is None:
            return

        
        # Write header only once at step 0
        if self.step == 0:
            headers = ["Step", "Avg Distance to Center", "Collisions"]
            if self.include_predator_column:
                headers.append("With Predator")
            with open(self.log_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                self.handle_manual_leader_control(keys_pressed)

        if not self.boids:
            return

        center = pygame.Vector2(
            sum(b.position.x for b in self.boids) / len(self.boids),
            sum(b.position.y for b in self.boids) / len(self.boids)
        )
        avg_dist = sum(b.position.distance_to(center) for b in self.boids) / len(self.boids)

        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            row = [self.step, avg_dist, self.collisions]
            if self.include_predator_column:
                row.append(int(self.with_predator))
            writer.writerow(row)

        self.step += 1
        # Update predator movement
        if self.with_predator and hasattr(self, "predator"):
            self.predator.position += self.predator.velocity
            if self.predator.position.x <= 0 or self.predator.position.x >= self.width:
                self.predator.velocity.x *= -1
            if self.predator.position.y <= 0 or self.predator.position.y >= self.height:
                self.predator.velocity.y *= -1
            if self.predator.position.x > self.width:
                self.predator.position.x = 0
        self.collisions = 0

        for i, boid in enumerate(self.boids):
            boid.apply_behavior(self.boids,
                                sep_weight=self.separation_strength,
                                ali_weight=self.alignment_strength,
                                coh_weight=self.cohesion_strength)
            if self.with_predator and hasattr(self, "predator"):
                distance = boid.position.distance_to(self.predator.position)
                if distance < 100:
                    away = boid.position - self.predator.position
                    if away.length_squared() > 0:
                        away = away.normalize()
                        strength = (100 - distance) / 100
                        boid.acceleration += away * strength * 2.0
                        sep_weight=self.separation_strength,
                        ali_weight=self.alignment_strength,
                        coh_weight=self.cohesion_strength

            for other_boid in self.boids[i+1:]:
                if boid.position.distance_to(other_boid.position) < 5:
                    self.collisions += 1

            for obs in self.obstacles:
                distance = boid.position.distance_to(obs.position)
                safe_distance = obs.size + 30
                if distance < safe_distance:
                    away = boid.position - obs.position
                    if away.length_squared() > 0:
                        away = away.normalize()
                        strength = (safe_distance - distance) / safe_distance
                        boid.acceleration += away * strength * 1.5

            if self.leader and boid != self.leader:
                target = self.leader.position
                desired = target - boid.position
                if desired.length() > 0:
                    desired.scale_to_length(4)
                    steer = desired - boid.velocity
                    if steer.length() > 0.05:
                        steer.scale_to_length(0.05)
                    boid.acceleration += steer * 0.05

            boid.update()

    def draw(self, screen):
        for obs in self.obstacles:
            obs.draw(screen)

        for boid in self.boids:
            if self.leader and boid == self.leader:
                pulse = 6 + 2 * math.sin(pygame.time.get_ticks() * 0.005)
                pygame.draw.circle(screen, (255, 0, 255), (int(boid.position.x), int(boid.position.y)), int(pulse))
            else:
                boid.draw(screen)

        # Draw predator as red circle
        if self.with_predator and hasattr(self, "predator"):
            pygame.draw.circle(screen, (255, 0, 0), (int(self.predator.position.x), int(self.predator.position.y)), 8)

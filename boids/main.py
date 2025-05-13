import pygame
import random
import math
from boid import Boid
from environment import Environment

WIDTH, HEIGHT = 800, 600
NUM_BOIDS = 30
FPS = 60

pygame.init()
#screen resolution for fullscreen
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)

# Hide mouse
pygame.mouse.set_visible(False)

# Create simulation environment
env = Environment(width, height, num_boids=30, with_predator=True)
env.include_predator_column = True
# Clock for frame control
clock = pygame.time.Clock()
running = True

while running:
    screen.fill((0, 0, 0))
    font = pygame.font.SysFont(None, 20)
    info_lines = [
        "Simulation Mode: Manual Demo",
        f"Boid Count: {len(env.boids)}",
        "Leader Control: Arrow Keys",
        f"Predator: {'On' if env.with_predator else 'Off'}",
        f"Logging: {env.log_file.split('/')[-1]}"
    ]

    for i, line in enumerate(info_lines):
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (10, 10 + i * 20))

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            running = False

    env.update(keys)
    env.draw(screen)
    pygame.display.flip()
    clock.tick(60)  # 60 FPS for smoother video

pygame.quit()
import pygame
import time
from environment import Environment
import os
import csv

WIDTH, HEIGHT = 800, 600
FPS = 60
RUN_TIME = 20  # seconds

# Parameter grid
BOID_COUNTS = [30, 60]
PREDATOR_STATES = [False, True]
WEIGHT_SETS = [
    (1.0, 1.0, 1.0),
    (2.0, 0.5, 0.5),
    (0.5, 2.0, 1.5)
]

def run_experiment(num_boids, sep, ali, coh, with_predator):
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    env = Environment(WIDTH, HEIGHT, num_boids,
                      separation_strength=sep,
                      alignment_strength=ali,
                      cohesion_strength=coh,
                      with_predator=with_predator,
                      include_predator_column=True
                      )
    
    # Customize output file name
    label = f"{num_boids}boids_sep{sep}_ali{ali}_coh{coh}{'_pred' if with_predator else ''}"
    env.log_file = os.path.join(os.path.dirname(__file__), "results", f"simulation_log_{label}.csv")

    with open(env.log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Step", "Avg Distance to Center", "Collisions", "With Predator"])

    start_time = time.time()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        screen.fill((30, 30, 30))
        env.update(keys)
        env.draw(screen)

        # Draw experiment configuration overlay
        font = pygame.font.SysFont(None, 28)
        config_text = f"{num_boids}b sep={sep} ali={ali} coh={coh} pred={'ON' if with_predator else 'OFF'}"
        overlay = font.render(config_text, True, (255, 255, 255))
        screen.blit(overlay, (20, 20))
        pygame.display.flip()
        clock.tick(FPS)

        if time.time() - start_time > RUN_TIME:
            running = False

    pygame.quit()

if __name__ == "__main__":
    for num_boids in BOID_COUNTS:
        for sep, ali, coh in WEIGHT_SETS:
            for pred in PREDATOR_STATES:
                print(f"Running: {num_boids} boids, sep={sep}, ali={ali}, coh={coh}, predator={pred}")
                run_experiment(num_boids, sep, ali, coh, pred)

    print("All experiments complete. Check 'results/' folder.")
    



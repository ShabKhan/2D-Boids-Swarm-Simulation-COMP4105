import pygame
from pygame.math import Vector2

MAX_SPEED = 4
NEIGHBOR_RADIUS = 50

def separation(boid, boids, desired_distance=20):
    steer = Vector2()
    count = 0
    for other in boids:
        distance = boid.position.distance_to(other.position)
        if 0 < distance < desired_distance:
            diff = boid.position - other.position
            if diff.length_squared() > 0:
                diff = diff.normalize() / distance
                steer += diff
                count += 1
    if count > 0:
        steer /= count
    if steer.length_squared() > 0:
        steer.scale_to_length(MAX_SPEED)
        steer -= boid.velocity
        if steer.length() > 0.05:
            steer.scale_to_length(0.05)
    return steer

def alignment(boid, boids, neighbor_dist=NEIGHBOR_RADIUS):
    avg_velocity = Vector2()
    count = 0
    for other in boids:
        distance = boid.position.distance_to(other.position)
        if 0 < distance < neighbor_dist:
            avg_velocity += other.velocity
            count += 1
    if count > 0:
        avg_velocity /= count
        if avg_velocity.length_squared() > 0:
            avg_velocity.scale_to_length(MAX_SPEED)
            steer = avg_velocity - boid.velocity
            if steer.length() > 0.05:
                steer.scale_to_length(0.05)
            return steer
    return Vector2()

def cohesion(boid, boids, neighbor_dist=NEIGHBOR_RADIUS):
    center_mass = Vector2()
    count = 0
    for other in boids:
        distance = boid.position.distance_to(other.position)
        if 0 < distance < neighbor_dist:
            center_mass += other.position
            count += 1
    if count > 0:
        center_mass /= count
        return seek(boid, center_mass)
    return Vector2()

def seek(boid, target):
    desired = target - boid.position
    if desired.length_squared() > 0:
        desired.scale_to_length(MAX_SPEED)
        steer = desired - boid.velocity
        if steer.length() > 0.05:
            steer.scale_to_length(0.05)
        return steer
    return Vector2()

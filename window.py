import pygame
import math
import random
from boid import Boid

TWEAK_WINDOW = True


# --------- Pygame Setup ---------
WIDTH, HEIGHT = 800, 600

WHITE = (255, 255, 255)
BLUE = (50, 100, 255)
triangle_pos = pygame.math.Vector2(WIDTH // 2, HEIGHT // 2)
triangle_points = [pygame.math.Vector2(0, -20), pygame.math.Vector2(20, 20), pygame.math.Vector2(-20, 20)]
angle = 0

# Variables to be tweaked via GUI
rotation_speed = 3
speed = 5
running = True


# --------- TEST BOID INIT ---------
boid_count = 10
boids: list[Boid] = []
for i in range(boid_count):
    boids.append(Boid(random.randint(0, 500), random.randint(0, 500), random.randint(0, 360), random.randint(10, 20)))

# --------- Game Loop Function ---------

def game_loop():
    global triangle_pos, angle, speed, rotation_speed, running
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Basic Game Window")

    # Clock for controlling FPS
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))

        for boid in boids:
            boid.update()
            pygame.draw.polygon(screen, BLUE, boid.triangle_points())

        # pygame.draw.circle(screen, "red", player_pos, 40)

        # pygame.draw.polygon(screen, "red", [(250, 100), (150, 400), (350, 400)], 0)

        # --- Test Triangle ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            angle -= rotation_speed
        if keys[pygame.K_RIGHT]:
            angle += rotation_speed
        if keys[pygame.K_UP]:
            rad = math.radians(angle)
            movement = pygame.math.Vector2(math.sin(rad), -math.cos(rad)) * speed
            triangle_pos += movement
        if keys[pygame.K_DOWN]:
            rad = math.radians(angle)
            movement = pygame.math.Vector2(-math.sin(rad), math.cos(rad)) * speed
            triangle_pos += movement

        moved_points = [triangle_pos + point.rotate(angle) for point in triangle_points]
        pygame.draw.polygon(screen, BLUE, moved_points)
        # ---------------------

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# --------- Tkinter GUI Setup ---------

if TWEAK_WINDOW:
    import tkinter
    from tkinter import ttk

    def update_speed(val):
        global speed
        speed = float(val)
    
    def update_rotation_speed(val):
        global rotation_speed
        rotation_speed = float(val)

    root = tkinter.Tk()
    root.title("Game Tweaker")
    root.geometry("400x200")

    tkinter.Label(root, text="Speed").pack()
    speed_slider = ttk.Scale(root, from_=1, to=20, orient="horizontal", command=update_speed)
    speed_slider.set(speed)
    speed_slider.pack()

    tkinter.Label(root, text="Rotation Speed").pack()
    rotation_slider = ttk.Scale(root, from_=1, to=10, orient="horizontal", command=update_rotation_speed)
    rotation_slider.set(rotation_speed)
    rotation_slider.pack()

    # Run the GUI in a separate thread
    import threading
    pygame_thread = threading.Thread(target=game_loop)
    pygame_thread.start()

    root.mainloop()

    running = False
    pygame_thread.join()
else:
    game_loop()
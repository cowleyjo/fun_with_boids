import pygame
import math
import random
from boid import Boid

TWEAK_WINDOW = True


# --------- Pygame Setup ---------
WIDTH, HEIGHT = 800, 600

EDGE_GAP = 70

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

        # for boid in boids:
        #     boid.update()
        #     pygame.draw.polygon(screen, BLUE, boid.triangle_points())

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


        # Edge Teleport for X Direction
        if triangle_pos.x < -EDGE_GAP:
            triangle_pos.x = WIDTH
        if triangle_pos.x > WIDTH + EDGE_GAP:
            triangle_pos.x = 0
        
        # Edge Teleport for Y Direction
        if triangle_pos.y < -EDGE_GAP:
            triangle_pos.y = HEIGHT
        if triangle_pos.y > HEIGHT + EDGE_GAP:
            triangle_pos.y = 0


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

    speed_var = tkinter.DoubleVar(value=speed)

    def update_speed():
        global speed
        speed = speed_var
        print(f"Speed: {val}")
    
    def update_rotation_speed(val):
        global rotation_speed
        rotation_speed = float(val)
        print(f"Rotation Speed: {val}")

    def update_edge_gap(val):
        global EDGE_GAP
        EDGE_GAP = float(val)
        print(f"Edge Gap: {val}")

    root = tkinter.Tk()
    root.title("Game Tweaker")
    root.geometry("400x200")


    tkinter.Label(root, text="Speed").pack()
    speed_input = tkinter.Spinbox(root, from_=0, to=50, increment=0.5, textvariable=speed, command=update_speed)
    speed_input.pack()

    speed_slider = ttk.Scale(root, from_=1, to=20, orient="horizontal", command=update_speed)
    speed_slider.set(speed)
    speed_slider.pack()

    tkinter.Label(root, text="Rotation Speed").pack()
    rotation_slider = ttk.Scale(root, from_=1, to=10, orient="horizontal", command=update_rotation_speed)
    rotation_slider.set(rotation_speed)
    rotation_slider.pack()

    tkinter.Label(root, text="Edge Gap").pack()
    edge_slider = ttk.Scale(root, from_=1, to=100, orient="horizontal", command=update_edge_gap)
    edge_slider.set(EDGE_GAP)
    edge_slider.pack()

    # Run the GUI in a separate thread
    import threading
    pygame_thread = threading.Thread(target=game_loop)
    pygame_thread.start()

    root.mainloop()

    running = False
    pygame_thread.join()
else:
    game_loop()


import pygame
import math
import random
from boid import Boid

from config import WIDTH, HEIGHT, EDGE_GAP, ALIGNMENT_FACTOR, COHESION_FACTOR, SEPARATION_FACTOR, VIS_RANGE, PROTECT_RANGE, MAX_SPEED

CONTROL_PANEL = True
VIS_DEBUG = False


# --------- Pygame Setup ---------
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

def update_boid_attribute(boids: list[Boid], var_name: str, var: float):
    for boid in boids:
        match var_name:
            case "VIS_RANGE":
                boid.vis_range = var
            case "PROTECT_RANGE":
                boid.protect_range = var
            case "ALIGNMENT_FACTOR":
                boid.alignment_factor = var
            case "COHESION_FACTOR":
                boid.cohesion_factor = var
            case "SEPARATION_FACTOR":
                boid.separation_factor = var

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
            boid.update(boids)
            pygame.draw.polygon(screen, BLUE, boid.triangle_points())
            if VIS_DEBUG: 
                pygame.draw.circle(screen, (0, 255, 0), (boid.pos), boid.vis_range, width=1)
                pygame.draw.circle(screen, (255, 0, 0), (boid.pos), boid.protect_range, width=1)


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

if CONTROL_PANEL:
    import tkinter
    from tkinter import ttk
    
    root = tkinter.Tk()
    root.title("Control Panel")
    root.geometry("400x400")

    def update_value(var_name, entry: tkinter.Entry, event=None):
        global speed, rotation_speed, EDGE_GAP, ALIGNMENT_FACTOR, COHESION_FACTOR, SEPARATION_FACTOR, VIS_RANGE, PROTECT_RANGE, MAX_SPEED
        try:
            value = float(entry.get())
            print(f"{var_name} Updated: {value}")

            match var_name:
                case "speed":
                    MAX_SPEED = value
                case "rotation_speed":
                    rotation_speed = value
                case "EDGE_GAP":
                    EDGE_GAP = value
                case "ALIGNMENT_FACTOR":
                    ALIGNMENT_FACTOR = value
                case "COHESION_FACTOR":
                    COHESION_FACTOR = value
                case "SEPARATION_FACTOR":
                    SEPARATION_FACTOR = value
                case "VIS_RANGE":
                    VIS_RANGE = value
                case "PROTECT_RANGE":
                    PROTECT_RANGE = value
            update_boid_attribute(boids, var_name, value)
        except ValueError:
            print("Invalid Number")


    tkinter.Label(root, text="Speed").pack()
    speed_entry = ttk.Entry(root)
    speed_entry.insert(0, str(speed))
    speed_entry.bind("<Return>", lambda event: update_value("speed", speed_entry, event))
    speed_entry.pack()

    tkinter.Label(root, text="Rotation Speed").pack()
    rotation_entry = ttk.Entry(root)
    rotation_entry.insert(0, str(rotation_speed))
    rotation_entry.bind("<Return>", lambda event: update_value("rotation_speed", rotation_entry, event))
    rotation_entry.pack()

    tkinter.Label(root, text="Edge Gap").pack()
    edge_entry = ttk.Entry(root)
    edge_entry.insert(0, str(EDGE_GAP))
    edge_entry.bind("<Return>", lambda event: update_value("EDGE_GAP", edge_entry, event))
    edge_entry.pack()

    tkinter.Label(root, text="VIS_RANGE").pack()
    vis_entry = ttk.Entry(root)
    vis_entry.insert(0, str(VIS_RANGE))
    vis_entry.bind("<Return>", lambda event: update_value("VIS_RANGE", vis_entry, event))
    vis_entry.pack()

    tkinter.Label(root, text="PROTECT_RANGE").pack()
    protect_entry = ttk.Entry(root)
    protect_entry.insert(0, str(PROTECT_RANGE))
    protect_entry.bind("<Return>", lambda event: update_value("PROTECT_RANGE", protect_entry, event))
    protect_entry.pack()

    tkinter.Label(root, text="ALIGNMENT FACTOR").pack()
    alignment_entry = ttk.Entry(root)
    alignment_entry.insert(0, str(ALIGNMENT_FACTOR))
    alignment_entry.bind("<Return>", lambda event: update_value("ALIGNMENT_FACTOR", alignment_entry, event))
    alignment_entry.pack()

    tkinter.Label(root, text="COHESION FACTOR").pack()
    cohesion_entry = ttk.Entry(root)
    cohesion_entry.insert(0, str(COHESION_FACTOR))
    cohesion_entry.bind("<Return>", lambda event: update_value("COHESION_FACTOR", cohesion_entry, event))
    cohesion_entry.pack()

    tkinter.Label(root, text="SEPARATION FACTOR").pack()
    separation_entry = ttk.Entry(root)
    separation_entry.insert(0, str(SEPARATION_FACTOR))
    separation_entry.bind("<Return>", lambda event: update_value("SEPARATION_FACTOR", separation_entry, event))
    separation_entry.pack()

    # Run the GUI in a separate thread
    import threading
    pygame_thread = threading.Thread(target=game_loop)
    pygame_thread.start()

    root.mainloop()

    running = False
    pygame_thread.join()
else:
    game_loop()


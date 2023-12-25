import pygame as pg
import numpy as np
from scipy.optimize import curve_fit

pg.init()
screen = pg.display.set_mode((640, 480))
clock = pg.time.Clock()
running = True
drawing = False
draw_coordinates = []
surface = pg.Surface((640, 480), pg.SRCALPHA)
font = pg.font.Font(None, 36)
text = font.render(f"Accuracy: 0", True, (255, 255, 255))
base_rmsd = 100.0


def circle_equation(xy, cx, cy, r):
    x, y = xy
    return (x - cx) ** 2 + (y - cy) ** 2 - r ** 2


def fit_circle_scipy(points):
    x, y = zip(*points)
    initial_guess = 320, 240, 320 + 240
    try:
        params, _ = curve_fit(circle_equation, (x, y), np.zeros_like(x), p0=initial_guess)
        center_x, center_y, radius = params
        return (center_x, center_y), radius
    except:
        return (0, 0), 0


def calculate_rmsd(points, center, radius):
    x, y = zip(*points)
    distances = np.sqrt((np.array(x) - center[0]) ** 2 + (np.array(y) - center[1]) ** 2)
    rmsd = np.sqrt(np.mean((distances - radius) ** 2))
    return rmsd


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            surface.fill((0, 0, 0))
            draw_coordinates = []
            drawing = True
        elif event.type == pg.MOUSEBUTTONUP:
            drawing = False

    screen.fill((0, 0, 0))
    pg.draw.circle(surface, (255, 0, 0),
                   (320, 240), 5)
    if drawing:
        if len(draw_coordinates) > 10:
            center, radius = fit_circle_scipy(draw_coordinates)
            rmsd = calculate_rmsd(draw_coordinates, (320, 240), radius)
            if rmsd > 100:
                percent_deviation = 0
            else:
                percent_deviation = 100 - rmsd
            text = font.render(f"Accuracy: {percent_deviation:.2f}", True, (255, 255, 255))
        mouse_coord = pg.mouse.get_pos()
        draw_coordinates.append(mouse_coord)
        pg.draw.circle(surface, (len(draw_coordinates) % 255, 255 - len(draw_coordinates) % 255, 255),
                       (mouse_coord[0], mouse_coord[1]), 3)
    screen.blit(surface, (0, 0))
    screen.blit(text, (10, 10))

    pg.display.flip()
    clock.tick(360)

pg.quit()

from PIL import Image, ImageOps, ImageDraw
import pygame
import sys
import os
from copy import copy

args = sys.argv
if len(args) == 1:
    image = Image.new("RGB", (1000, 700))
    for i in range(image.width):
        for j in range(image.height):
            image.putpixel((i, j), (255, 255, 255))
    filepath = "Untitled.png"
    image.save(filepath)
else:
    filepath = args[1]
    image = Image.open(filepath)

pygame.init()
font = pygame.font.Font("freesansbold.ttf", 16)
msptw = font.render(f"x: {image.width}  y: {image.height}  color: (R:  255  G:  255  B:  255)", True, "white").get_width()
res = width, height = max(image.width, msptw), image.height + 50
screen = pygame.display.set_mode(res)
pygame.display.set_caption(f"Paint.py - {filepath}")
pg_img = pygame.image.load(filepath)

img2 = copy(image)
for i in range(img2.width):
    for j in range(img2.height):
        r, g, b = img2.getpixel((i, j))
        avg = int((r + g + b) / 3)
        img2.putpixel((i, j), (avg, avg, avg))

img3 = copy(image)
img3 = ImageOps.invert(img3)
try: os.mkdir(".Paint.py_temp")
except: pass
img2.save(f".Paint.py_temp/{filepath}.grayscale.png")
img3.save(f".Paint.py_temp/{filepath}.invert.png")

gspg_img = pygame.image.load(f".Paint.py_temp/{filepath}.grayscale.png")
invpg_img = pygame.image.load(f".Paint.py_temp/{filepath}.invert.png")
current_img = pg_img

def exit_norm():
    os.remove(f".Paint.py_temp/{filepath}.grayscale.png")
    os.remove(f".Paint.py_temp/{filepath}.invert.png")
    os.rmdir(".Paint.py_temp")
    sys.exit(0)

clock = pygame.time.Clock()
fps = 60

points_chunks = []
removed_points_chunks = []
ri = 0
i = 0

while True:
    screen.fill((0, 0, 0))
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit_norm()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_c:
                for points in points_chunks:
                    removed_points_chunks.append(points)
                    ri += 1
                points_chunks = []
                i = 0
            
            elif e.key == pygame.K_z:
                if points_chunks != []:
                    removed_points_chunks.append(points_chunks[-1])
                    ri += 1
                    points_chunks.remove(points_chunks[-1])
                    i -= 1
                
            elif e.key == pygame.K_y:
                if removed_points_chunks != []:
                    removed = removed_points_chunks[-ri]
                    removed_points_chunks.remove(removed)
                    points_chunks.append(removed)
                    i += 1
                    ri -= 1

            elif e.key == pygame.K_s:
                draw = ImageDraw.Draw(image)
                for points in points_chunks:
                    for point in points:
                        if points.index(point) != 0:
                            draw.line((point[0], point[1], points[points.index(point) - 1][0], points[points.index(point) - 1][1]), (255, 0, 0), 2)
                image.save(f"{filepath}.edited.png")

        if e.type == pygame.MOUSEBUTTONDOWN:
            points_chunks.append([])

        if e.type == pygame.MOUSEBUTTONUP:
            i += 1

    screen.blit(current_img, (0, 0))
    if pygame.key.get_pressed()[pygame.K_g]:
        current_img = gspg_img
        mx, my = pygame.mouse.get_pos()
        if my <= image.height - 1 and mx <= image.width - 1:
            c = img2.getpixel((mx, my))
            text = font.render(f"x: {mx}  y: {my}  color: (R: {c[0]}  G: {c[1]}  B: {c[2]})", True, "white")
        else:
            text = font.render(f"x: {mx}  y: {my}  color: (R: 0  G: 0  B: 0)", True, "white")
    elif pygame.key.get_pressed()[pygame.K_i]:
        current_img = invpg_img
        mx, my = pygame.mouse.get_pos()
        if my <= image.height - 1 and mx <= image.width - 1:
            c = img3.getpixel((mx, my))
            text = font.render(f"x: {mx}  y: {my}  color: (R: {c[0]}  G: {c[1]}  B: {c[2]})", True, "white")
        else:
            text = font.render(f"x: {mx}  y: {my}  color: (R: 0  G: 0  B: 0)", True, "white")
    else:
        current_img = pg_img
        mx, my = pygame.mouse.get_pos()
        if my <= image.height - 1 and mx <= image.width - 1:
            c = image.getpixel((mx, my))
            text = font.render(f"x: {mx}  y: {my}  color: (R: {c[0]}  G: {c[1]}  B: {c[2]})", True, "white")
        else:
            text = font.render(f"x: {mx}  y: {my}  color: (R: 0  G: 0  B: 0)", True, "white")

    if pygame.mouse.get_pressed()[0]:
        mx, my = pygame.mouse.get_pos()
        if mx < image.width and my < image.width:
            if (mx, my) not in points_chunks[i]:
                points_chunks[i].append((mx, my))
        
    for points in points_chunks:
        for idx, point in enumerate(points):
            if idx != 0:
                pygame.draw.line(screen, (255, 0, 0), points[idx - 1], point, 3)

    screen.blit(text, (0, height - text.get_height()))

    pygame.display.update()
    clock.tick(fps)
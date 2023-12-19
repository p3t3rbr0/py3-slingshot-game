import os.path
from math import sqrt

import pygame
from pygame.locals import *

from .settings import Settings


def load_image(name, colorkey=None):
    fullname = os.path.join(Settings.DATA_PATH, name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print("Cannot load image:", fullname)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
            image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def get_intersect(center, r, pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos2[1] - pos1[1]
    px = pos1[0]
    py = pos1[1]
    cx = center[0]
    cy = center[1]
    a = dx ** 2 + dy ** 2
    b = 2 * (dx * px - dx * cx + dy * py - dy * cy)
    c = -2 * cx * px - 2 * cy * py + px ** 2 + py ** 2 + cx ** 2 + cy ** 2 - r ** 2
    D = b ** 2 - 4 * a * c
    if D < 0:
        return (4000.0, 3000.0)
    alpha = (-b + sqrt(D)) / (2 * a)
    if alpha > 1:
        alpha = (-b - sqrt(D)) / (2 * a)
        alpha = alpha - 0.05
        pos = (px + alpha * dx, py + alpha * dy)
    return pos


def get_data_path(file):
    print(Settings.DATA_PATH)
    return os.path.join(Settings.DATA_PATH, file)


def prep_text(text, antialias, font, linespacing, color):
    """
    Let's make it easy to draw text.

    Input:
      text: a list of lines to print.
      antialias: Bool that controls antialiasing
      font: An initialized pygames.font.Font object
      linespacing: the number of pixels between lines
      color: (R, G, B)
    Output:
      A list of tuples in the format:
      (surface, (line width, distance between the top of the first line
      and the top of this line))
    """
    text_surfaces = []
    text_height = 0
    for line in text:
        rendered_text = font.render(line, antialias, color)
        text_surfaces.append((rendered_text, (rendered_text.get_width(), text_height)))
        # So that we place the next line directly under this one:
        text_height += rendered_text.get_height()
        text_height += linespacing
    return text_surfaces

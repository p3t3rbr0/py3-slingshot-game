import string

import pygame
from pygame.locals import *

from .settings import *


class Inputbox:
    def __init__(self, screen, question):
        self.screen = screen
        self.question = question
        self.new_str = []
        self.input_box(question + ": " + string.join(self.new_str, ""))

    def input_box(self, msg):
        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            (
                (self.screen.get_width() / 2) - 200,
                (self.screen.get_height() / 2) - 20,
                400,
                40,
            ),
            0,
        )
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            (
                (self.screen.get_width() / 2) - 204,
                (self.screen.get_height() / 2) - 24,
                408,
                48,
            ),
            1,
        )

        if len(msg) != 0:
            self.screen.blit(
                Settings.menu_font.render(msg, 1, (255, 255, 255)),
                (
                    (self.screen.get_width() / 2) - 200,
                    (self.screen.get_height() / 2) - 12,
                ),
            )
            pygame.display.flip()

    def ask(self):
        while 1:
            key = self.get_key()
            if key == K_BACKSPACE:
                self.new_str = self.new_str[0:-1]
            elif key == K_RETURN:
                break
            elif key == K_ESCAPE:
                return False
            elif key <= 127 and len(self.new_str) < 19:
                self.new_str.append(chr(key))
            self.input_box(self.question + ": " + string.join(self.new_str, ""))
        return string.join(self.new_str, "")

    def get_key(self):
        while 1:
            event = pygame.event.poll()
            if event.type == KEYDOWN:
                return event.key

from random import randint
import pygame


class Pipe:
    GAP = 200

    def __init__(self, x, screen_size, vel, img):
        self.screen_size = screen_size
        self.x = x
        self.create_new()

        self.width = 100
        self.vel = vel
        self.img = img

    def create_new(self):
        self.y = randint(self.GAP, self.screen_size[1] - self.GAP)

    def collide(self, rect):
        if rect.colliderect(pygame.Rect(self.x, self.y, self.width, self.screen_size[1])):
            return True

        if rect.colliderect(pygame.Rect(self.x, self.y - self.screen_size[1] - self.GAP, self.width, self.screen_size[1])):
            return True

        return False

    def move(self):
        self.x -= self.vel*5

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
        surface.blit(pygame.transform.flip(self.img, False, True), (self.x, self.y - self.screen_size[1] - 40))

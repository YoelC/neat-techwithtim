import pygame


class Bird:
    # 0.6
    # 8
    gravity = 0.6
    jump_force = 8

    def __init__(self, y, screen_size, imgs):
        self.width = 65
        self.height = 50
        self.imgs = imgs
        self.screen_size = screen_size
        self.x = screen_size[0] - screen_size[0]/1.25 - self.width/2
        self.y = y - self.height/2
        self.y_vel = 0
        self.x_vel = 0
        self.img_count = 0
        self.img = self.imgs[0]
        self.angle = 180

    def move(self):
        self.y_vel -= self.gravity
        self.y -= self.y_vel
        self.x += self.x_vel

        if self.y_vel > -3:
            self.angle = 15

        elif self.y_vel < -3:
            self.angle -= 3

        if self.angle < -90:
            self.angle = -90

    def jump(self):
        self.y_vel = self.jump_force

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, stop=False):
        if not stop:
            self.img_count += 1

        if self.img_count < 5:
            self.img = self.imgs[0]
        elif self.img_count < 10:
            self.img = self.imgs[1]
        elif self.img_count < 15:
            self.img = self.imgs[2]
        elif self.img_count < 20:
            self.img = self.imgs[1]
        elif self.img_count <= 21:
            self.img = self.imgs[0]
            self.img_count = 0

        img = pygame.transform.rotate(self.img, self.angle)
        new_rect = img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        surface.blit(img, new_rect)

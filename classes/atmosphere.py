class Background:
    def __init__(self, x, vel, img):
        self.x = x
        self.y = 0
        self.vel = vel
        self.img = img

    def move(self):
        self.x -= self.vel

    def draw(self, surface):

        surface.blit(self.img, (self.x, self.y))


class Floor:
    def __init__(self, screen_size, vel, img):
        self.x = 0
        self.y = screen_size[1] - 55
        self.vel = vel
        self.img = img

    def move(self):
        self.x -= self.vel*5
        if self.x < -90:
            self.x = 0

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))
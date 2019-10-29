import pygame
import pygame.freetype
from random import randint
import os
import neat

pygame.init()

LINES = True
max_birds = 0
LINE_WIDTH = 2
GAP = 200
GAP_TWO_PIPES = 525
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 800
FPS = 0

VEL_DECORATION = 1
GRAVITY = 0.6
JUMP_FORCE = 8

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Where')


class Background:
    def __init__(self, x):
        self.x = x
        self.y = 0

    def draw(self, surface, stop=False):
        if not stop:
            self.x -= VEL_DECORATION

        surface.blit(BG_IMG, (self.x, self.y))


class Floor:
    def __init__(self):
        self.x = 0
        self.y = WINDOW_HEIGHT - 55

    def draw(self, surface, stop=False):
        if not stop:
            self.x -= VEL_DECORATION*5
            if self.x < -90:
                self.x = 0

        surface.blit(BASE_IMG, (self.x, self.y))


class Text:
    def __init__(self, color, pos, font_size):
        self.win = win
        self.color = color
        self.x = pos[0]
        self.y = pos[1]
        self.font = pygame.freetype.Font('slkscrb.ttf', font_size)

    def draw(self, win, text):
        self.font.render_to(win, (self.x, self.y), text, self.color)


class Bird:
    def __init__(self, y, color):
        self.width = 65
        self.height = 50
        self.color = color
        self.x = WINDOW_WIDTH - WINDOW_WIDTH/1.25 - self.width/2
        self.y = y - self.height/2
        self.y_vel = 0
        self.x_vel = 0
        self.img_count = 0
        self.img = BIRD_IMGS[0]

        self.angle = 180

    def move(self):
        self.y_vel -= GRAVITY
        self.y -= self.y_vel
        self.x += self.x_vel

    def jump(self):
        self.y_vel = JUMP_FORCE

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, stop=False):
        if not stop:
            self.img_count += 1

        if self.img_count < 5:
            self.img = BIRD_IMGS[0]
        elif self.img_count < 10:
            self.img = BIRD_IMGS[1]
        elif self.img_count < 15:
            self.img = BIRD_IMGS[2]
        elif self.img_count < 20:
            self.img = BIRD_IMGS[1]
        elif self.img_count <= 21:
            self.img = BIRD_IMGS[0]
            self.img_count = 0

        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        #pygame.draw.rect(win, self.color, rect, 1)

        if self.y_vel > -3:
            self.angle = 15

        elif self.y_vel < -3:
            self.angle -= 3

        if self.angle < -90:
            self.angle = -90

        img = pygame.transform.rotate(self.img, self.angle)
        new_rect = img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        surface.blit(img, new_rect)


class Pipe:
    def __init__(self, x, color):
        self.x = x
        self.create_new()

        self.color = color
        self.width = 100

    def create_new(self):
        self.y = randint(GAP, WINDOW_HEIGHT - GAP)

    def collide(self, rect):
        if rect.colliderect(pygame.Rect(self.x, self.y, self.width, WINDOW_HEIGHT)):
            return True

        if rect.colliderect(pygame.Rect(self.x, self.y - WINDOW_HEIGHT - GAP, self.width, WINDOW_HEIGHT)):
            return True

        return False

    def draw(self, surface, stop=False):
        if not stop:
            self.x -= VEL_DECORATION*5

        surface.blit(PIPE_IMG, (self.x, self.y))
        surface.blit(pygame.transform.flip(PIPE_IMG, False, True), (self.x, self.y - WINDOW_HEIGHT - 40))


def render_screen(backgrounds, pipes, birds, score_text, score_text_background, floor, score, bird_draw, pipe_bottom_draw, pipe_top_draw, generation_text, generation_text_background):
    global max_birds
    birds_original = birds.copy()

    for background in backgrounds:
        background.draw(win)

    for pipe in pipes:
        pipe.draw(win)

    score_text_background.draw(win, f'{score}')
    score_text.draw(win, f'{score}')

    if len(birds_original) > max_birds:
        max_birds = len(birds_original)

    generation_text_background.draw(win, f'Population: {len(birds_original)}/{max_birds}')
    generation_text.draw(win, f'Population: {len(birds_original)}/{max_birds}')

    if LINES:
        for x, bird in enumerate(birds):
            for bird_pos, pipe_pos in zip([bird_draw[x]], [pipe_bottom_draw[x]]):
                pygame.draw.line(win, (255, 0, 0), (bird_pos[0]+birds[0].width/2, bird_pos[1]+birds[0].height/2), pipe_pos, LINE_WIDTH)

            for bird_pos, pipe_pos in zip([bird_draw[x]], [pipe_top_draw[x]]):
                pygame.draw.line(win, (0, 255, 0), (bird_pos[0]+birds[0].width/2, bird_pos[1]+birds[0].height/2), (pipe_pos[0], pipe_pos[1]), LINE_WIDTH)

            for bird_pos in [bird_draw[x]]:
                pygame.draw.line(win, (0, 0, 255), (bird_pos[0]+birds[0].width/2, bird_pos[1]+birds[0].height/2), (bird_pos[0]+ birds[0].width/2, WINDOW_HEIGHT), LINE_WIDTH)

    for bird in birds:
        bird.draw(win)

    floor.draw(win)

    pygame.display.flip()


def main(genomes, config):
    global LINES
    score = 0
    run = True

    lines_delay = 0

    nets = []
    birds = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        ge.append(genome)

    floor = Floor()
    bird = Bird(WINDOW_HEIGHT/2, (255, 0, 0))

    pipe1 = Pipe(700, (255, 0, 0))
    pipe2 = Pipe(pipe1.x*1.5 + pipe1.width/2, (255, 0, 0))

    score_text = Text((255, 255, 255), (WINDOW_WIDTH/2 - 12, 25), 60)
    score_text_background = Text((0, 0, 0), (WINDOW_WIDTH/2 - 12 - 2, 25 + 2), 60)

    generation_text = Text((255, 255, 255), (WINDOW_WIDTH/2 - 20, 2), 20)
    generation_text_background = Text((0, 0, 0), (WINDOW_WIDTH/2 - 20 - 2, 2+2), 20)

    background1 = Background(0)
    background2 = Background(BG_IMG.get_rect().width)

    backgrounds = [background1, background2]

    pipes = [pipe1, pipe2]
    score = 0

    passed_pipe1 = False
    passed_pipe2 = False

    while run:
        try:
            pygame.time.delay(int(1000/FPS))
        except ZeroDivisionError:
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if pygame.key.get_pressed()[pygame.K_z] and LINES and lines_delay == 0:
            LINES = False
            lines_delay += 3

        elif pygame.key.get_pressed()[pygame.K_z] and not LINES and lines_delay == 0:
            LINES = True
            lines_delay += 3

        elif not pygame.key.get_pressed()[pygame.K_z]:
            if lines_delay > 0:
                lines_delay -= 1

        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird.get_rect()):
                    ge[x].fitness -= 1
                    nets.pop(x)
                    ge.pop(x)
                    birds.pop(x)

            if pipe.x + pipe.width < 0:
                pipe.x = 700
                pipe.create_new()

        if pipe1.x < 0 and not passed_pipe1:
            score += 1
            passed_pipe1 = True

        if not pipe1.x < 0 and passed_pipe1:
            passed_pipe1 = False

        if pipe2.x < 0 and not passed_pipe2:
            score += 1
            passed_pipe2 = True

        if not pipe2.x < 0 and passed_pipe2:
            passed_pipe2 = False

        for background in backgrounds:
            if background.x + BG_IMG.get_rect().width < 0:
                background.x = BG_IMG.get_rect().width

        for x, bird in enumerate(birds):
            if bird.y + bird.height > WINDOW_HEIGHT - 55 or bird.y < 0:
                ge[x].fitness -= 5
                nets.pop(x)
                ge.pop(x)
                birds.pop(x)

        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            bird.move()

        pipe = None
        two_chosen = False
        if pipe1.x + pipe1.width > bird.x:
            pipe = pipe1

        if pipe2.x + pipe2.width > bird.x:
            if pipe == pipe1:
                two_chosen = True
            pipe = pipe2

        if two_chosen:
            if pipe1.x > pipe2.x:
                pipe = pipe2
            else:
                pipe = pipe1

        bird_draw = []
        pipe_bottom_draw = []
        pipe_top_draw = []
        for x, bird in enumerate(birds):
            output = nets[x].activate((bird.y, pipe.y, pipe.y - 200))

            bird_draw.append((bird.x, bird.y))
            pipe_bottom_draw.append((pipe.x, pipe.y))
            pipe_top_draw.append((pipe.x, pipe.y - 200))

            if output[0] > 0.5:
                bird.jump()

        if len(birds) == 0:
            break

        render_screen(backgrounds, pipes, birds, score_text, score_text_background, floor, score, bird_draw, pipe_bottom_draw, pipe_top_draw, generation_text, generation_text_background)


def run(config_file):
    global winner
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)

    print(f'\nBest genome:\n{winner}')


run(config_file='config-feedforward.txt')

import pygame
import pygame.freetype
import os
import neat
from classes.data import Generations, Key
from classes.atmosphere import Background, Floor
from classes.pipe import Pipe
from classes.bird import Bird
import sys

pygame.init()

LINES = True
max_birds = 0
LINE_WIDTH = 3
GAP_TWO_PIPES = 525
WINDOW_WIDTH = 550
WINDOW_HEIGHT = 800
FPS = 0
FONT = pygame.freetype.Font('slkscrb.ttf')

VEL_DECORATION = 1

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

win = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE)
clock = pygame.time.Clock()


def render_screen(backgrounds, pipes, birds, floor, score, bird_draw, pipe_bottom_draw, pipe_top_draw):
    global max_birds
    birds_original = birds.copy()

    for background in backgrounds:
        background.draw(win)

    for pipe in pipes:
        pipe.draw(win)

    if len(birds_original) > max_birds:
        max_birds = len(birds_original)

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

    font_surface, font_pos = FONT.render(f'{score}', (0, 0, 0), size=80)
    win.blit(font_surface, (WINDOW_WIDTH / 2 - font_pos.width / 2 + 5, 55 + 5))
    font_surface, font_pos = FONT.render(f'{score}', (225, 225, 225), size=80)
    win.blit(font_surface, (WINDOW_WIDTH / 2 - font_pos.width / 2, 55))

    font_surface, font_pos = FONT.render(f'Generations: {generations.generations}', (0, 0, 0), size=25)
    win.blit(font_surface, (WINDOW_WIDTH - font_pos.width - 15 + 2.5, 10 + 2.5))
    font_surface, font_pos = FONT.render(f'Generations: {generations.generations}', (225, 225, 225), size=25)
    win.blit(font_surface, (WINDOW_WIDTH - font_pos.width - 15, 10))

    font_surface, font_pos = FONT.render(f'Alive {len(birds_original)} of {max_birds}', (0, 0, 0), size=25)
    win.blit(font_surface, (WINDOW_WIDTH - font_pos.width - 15 + 2.5, 30 + 2.5))
    font_surface, font_pos = FONT.render(f'Alive {len(birds_original)} of {max_birds}', (225, 225, 225), size=25)
    win.blit(font_surface, (WINDOW_WIDTH - font_pos.width - 15, 30))

    font_surface, font_pos = FONT.render(f'Speed {generations.speed}x', (0, 0, 0), size=25)
    win.blit(font_surface, (15 + 2.5, WINDOW_HEIGHT - 40 + 2.5))
    font_surface, font_pos = FONT.render(f'Speed {generations.speed}x', (225, 225, 225), size=25)
    win.blit(font_surface, (15, WINDOW_HEIGHT - 40))

    pygame.display.flip()


def main(genomes, config):
    tick = 0
    global LINES
    run = True

    lines_delay = 0

    nets = []
    birds = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230, (WINDOW_WIDTH, WINDOW_HEIGHT), BIRD_IMGS))
        ge.append(genome)

    floor = Floor((WINDOW_WIDTH, WINDOW_HEIGHT), VEL_DECORATION, BASE_IMG)

    pipe1 = Pipe(700, (WINDOW_WIDTH, WINDOW_HEIGHT), VEL_DECORATION, PIPE_IMG)
    pipe2 = Pipe(pipe1.x*1.5 + pipe1.width/2, (WINDOW_WIDTH, WINDOW_HEIGHT), VEL_DECORATION, PIPE_IMG)

    background1 = Background(0, VEL_DECORATION, BG_IMG)
    background2 = Background(BG_IMG.get_rect().width, VEL_DECORATION, BG_IMG)

    backgrounds = [background1, background2]

    pipes = [pipe1, pipe2]
    score = 0

    passed_pipe1 = False
    passed_pipe2 = False

    while run:
        pygame.display.set_caption(f'{round(clock.get_fps()/generations.speed, 2)} fps')
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        if pygame.key.get_pressed()[pygame.K_RIGHT] and not key_right.holding:
            key_right.holding = True
            key_right.clicked = True
        elif pygame.key.get_pressed()[pygame.K_RIGHT] and key_right.holding:
            key_right.clicked = False
        elif not pygame.key.get_pressed()[pygame.K_RIGHT]:
            key_right.holding = False
            key_right.clicked = False

        if pygame.key.get_pressed()[pygame.K_LEFT] and not key_left.holding:
            key_left.holding = True
            key_left.clicked = True
        elif pygame.key.get_pressed()[pygame.K_LEFT] and key_left.holding:
            key_left.clicked = False
        elif not pygame.key.get_pressed()[pygame.K_LEFT]:
            key_left.holding = False
            key_left.clicked = False

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

        pipe1.move()
        pipe2.move()
        floor.move()
        background1.move()
        background2.move()

        if generations.speed < 100000:

            if key_right.clicked and generations.speed >= 10000:
                generations.speed += 10000
            elif key_right.clicked and generations.speed >= 1000:
                generations.speed += 1000
            elif key_right.clicked and generations.speed >= 100:
                generations.speed += 100
            elif key_right.clicked and generations.speed >= 10:
                generations.speed += 10
            elif key_right.clicked:
                generations.speed += 1

        if key_left.clicked and generations.speed > 10000:
            generations.speed -= 10000
        elif key_left.clicked and generations.speed > 1000:
            generations.speed -= 1000
        elif key_left.clicked and generations.speed > 100:
            generations.speed -= 100
        elif key_left.clicked and generations.speed > 10:
            generations.speed -= 10
        elif key_left.clicked and generations.speed > 1:
            generations.speed -= 1

        if tick % generations.speed == 0:
            render_screen(backgrounds, pipes, birds, floor, score, bird_draw, pipe_bottom_draw, pipe_top_draw)

        tick += 1

    generations.add()


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

    winner = p.run(main, 50000)

    print(f'\nBest genome:\n{winner}')


key_left = Key()
key_right = Key()
generations = Generations()
run(config_file='config-feedforward.txt')

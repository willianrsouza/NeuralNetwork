import os.path

import neat.config
import pygame

from game.objects.bird import Bird
from game.env import window_config, font_score
from game.objects.screen import window
from game.objects.base import Base
from game.objects.pipe import Pipe

global_score = 0
global_game_over = False
global_state = True

global_ge = []
global_nets = []
global_birds = []


def main(genomes, config):
    global global_state
    global global_game_over

    global global_ge
    global global_nets
    global global_birds

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        global_nets.append(net)
        global_birds.append(Bird(230, 350))
        g.fitness = 0
        global_ge.append(g)

    pygame.init()
    screen = window_config()

    base = Base(700)
    pipes = [Pipe(600)]

    while global_state:

        capture_events(pygame, global_birds)

        pipe_ind = 0
        if len(global_birds) > 0:
            if len(pipes) > 1 and global_birds[0].x > pipes[0].x + pipes[0].pipe_top.get_width():
                pipe_ind = 1
        else:
            global_state = False
            break

        for x, bird in enumerate(global_birds):
            bird.move()
            global_ge[x].fitness += 0.1

            output = global_nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height),
                                              abs(bird.y - pipes[pipe_ind].bottom)))

            if output[0] > 0.5:
                bird.jump()

        render_scene(screen, base, global_birds, pipes)


def capture_events(py, bird):
    global global_game_over
    global global_score
    global global_state

    for event in py.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                bird.jump()


def render_scene(screen, base, birds, pipes):
    window(screen)

    render_base(screen, base)
    render_pipe(screen, pipes, birds)
    render_score(screen)
    render_bird(screen, birds)

    pygame.display.update()


def render_base(win, base):
    base.draw(win)
    base.move()


def render_score(win):
    score_text = font_score().render(str(global_score), 1, (255, 255, 255))
    win.blit(score_text, (300 - 10 - score_text.get_width(), 10))


def render_pipe(screen, pipes, birds):
    global global_game_over

    global global_ge
    global global_nets
    global global_birds

    for pipe in pipes:
        pipe.draw(screen)

    add_pipe = False
    rem = []

    for pipe in pipes:
        pipe.move()

        for bird in birds:
            if pipe.collide(bird):
                global_ge[birds.index(bird)].fitness -= 1
                global_nets.pop(birds.index(bird))
                global_ge.pop(birds.index(bird))
                global_birds.pop(birds.index(bird))

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if pipe.x + pipe.pipe_top.get_width() < 0:
            rem.append(pipe)

    if add_pipe:
        add_score()

        for g in global_ge:
            g.fitness += 5
        pipes.append(Pipe(600))

    for r in rem:
        pipes.remove(r)

    for bird in birds:
        if bird.y + bird.img.get_height() - 10 >= 730 or bird.y < -50:
            global_nets.pop(birds.index(bird))
            global_ge.pop(birds.index(bird))
            birds.pop(birds.index(bird))


def add_score():
    global global_score
    global_score = global_score + 1


def render_bird(win, birds):
    global global_game_over

    for bird in birds:
        bird.draw(win)
        bird.move()


def run(path_config):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                path_config)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    winner = p.run(main, 3000)

    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = "/Users/willian/Documents/FlappyIA/config-feedforward.txt"
    run(config_path)

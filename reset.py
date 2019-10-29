def reset():
    global score
    score = 0
    bird.y_vel = 0
    bird.y = WINDOW_HEIGHT / 2 - bird.height / 2
    pipe1.x = 700
    pipe2.x = pipe1.x * 1.5 + pipe1.width / 2

    pipe1.create_new()
    pipe2.create_new()
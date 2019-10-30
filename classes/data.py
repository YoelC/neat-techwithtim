class Generations:
    def __init__(self):
        self.generations = 0
        self.speed = 1

    def add(self):
        self.generations += 1


class Key:
    def __init__(self):
        self.holding = False
        self.clicked = False

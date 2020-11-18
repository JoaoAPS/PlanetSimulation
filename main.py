import pygame

from src.Planet import Planet
from src.Universe import Universe
from src.View import View
from src.vecN import Vec3


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
FPS = 60
TIMESTEP = 0.05


def main():
    clock = pygame.time.Clock()
    v = View(SCREEN_WIDTH, SCREEN_HEIGHT)

    planets = [
        Planet(100, Vec3(), Vec3(0, -1), (200, 200, 200)),
        Planet(100, Vec3(40, -10), Vec3(0, 1), (200, 0, 200)),
        Planet(100, Vec3(100, 40), Vec3(), (0, 200, 200)),
    ]

    # # Stable circular orbit
    # m = 1000
    # r = 10
    # planets = [
    #     Planet(m, Vec3(-r), Vec3(0, 5), (200, 200, 200)),
    #     Planet(m, Vec3(r), Vec3(0, -5), (200, 0, 200)),
    # ]

    universe = Universe(planets, TIMESTEP, gravConst=1)

    while v.running:
        clock.tick(FPS)
        v.drawUniverse(universe)
        universe.stepTime()
        v.handleEvents()


if __name__ == '__main__':
    main()

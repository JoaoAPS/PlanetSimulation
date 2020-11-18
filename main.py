from src.Planet import Planet
from src.vecN import Vec3

from src.App import App


def main():
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

    app = App()
    app.universe.setPlanets(planets)
    app.run()


if __name__ == '__main__':
    main()

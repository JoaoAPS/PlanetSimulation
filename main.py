from src.App import App

from src.Planet import Planet
from src.vecN import Vec3


def main():

    # 8 loop
    # pos = 10 * Vec3(-0.97000436, 0.24308753)
    # vel2 = 10 * Vec3(-0.93240737, -0.86473146)
    # vel13 = 10 * Vec3(0.4662036850, 0.4323657300)
    # planets = [
    #     Planet(1000, pos, vel13, (200, 20, 20)),
    #     Planet(1000, Vec3(), vel2, (20, 200, 20)),
    #     Planet(1000, -pos, vel13, (20, 20, 200))
    # ]

    planets = [
        Planet(1000, Vec3(50), Vec3(-10, 5), (200, 20, 20)),
        Planet(1000, Vec3(5, -15), Vec3(7, 0), (20, 200, 20)),
        Planet(1000, Vec3(0, 30), Vec3(1, -5), (20, 20, 200)),
    ]

    planets = [
        Planet(5000, Vec3(20), Vec3(-5, -5), (200, 20, 20)),
        Planet(5000, Vec3(-20), Vec3(5, 5), (20, 200, 20)),
    ]

    app = App()

    app.universe.setPlanets(planets)

    app.run()


if __name__ == '__main__':
    main()

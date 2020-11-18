import pygame
import copy

from .Planet import Planet
from .Universe import Universe
from .View import View
from .vecN import Vec3


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TIMESTEP = 0.01


class App:

    def __init__(self):
        self.view = View(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.planets = []
        self.universe = Universe(TIMESTEP, 1)
        self.fps = FPS
        self.clock = pygame.time.Clock()
        self.runSimulation = False
        self.selectedPlanet = None
        self.initialUniverse = None

    def run(self):
        """Run the application"""
        while self.view.running:
            self._playUniverseContruction()

            if self.runSimulation:
                self.pause = False
                self._playSimulation()

            if self.initialUniverse:
                self.universe = copy.copy(self.initialUniverse)

    def _playSimulation(self):
        """Simulate the orbits and show them on the screen"""
        self.view.constructionMode = False
        self.initialUniverse = copy.deepcopy(self.universe)

        while self.view.running:
            self.clock.tick(self.fps)
            self.view.drawUniverse(self.universe)

            if not self.pause:
                self.universe.stepTime()

            action = self.view.handleEvents(self.universe.planets)

            if action:
                if action.type == 'PAUSE':
                    self.pause = not self.pause
                if action.type == 'STOP':
                    self.runSimulation = False
                    return

                if action.type == 'FPS_UP':
                    self.fps += 1
                if action.type == 'FPS_DOWN':
                    self.fps -= 1

    def _playUniverseContruction(self):
        """Show the universe construction screen"""
        current_color = 0
        color_list = [
            (250, 250, 250),
            (10, 10, 250),
            (255, 10, 10),
            (10, 250, 10),
            (250, 250, 10),
            (10, 250, 250),
            (250, 250, 10)
        ]

        self.view.constructionMode = True

        while self.view.running and not self.runSimulation:
            self.clock.tick(self.fps)
            self.view.drawUniverse(self.universe)

            action = self.view.handleEvents(self.universe.planets)

            if action:
                if action.type == 'ADD_PLANET':
                    self.universe.addPlanet(Planet(
                        100,
                        action.payload['pos'],
                        action.payload['vel'],
                        color_list[current_color]
                    ))

                    current_color += 1
                    if current_color == len(color_list):
                        current_color = 0

                    self.selectedPlanet = None

                if action.type == 'SELECT_PLANET':
                    self.selectedPlanet = action.payload

                if action.type == 'SET_VEL' and \
                        self.selectedPlanet is not None:
                    planets = self.universe.planets
                    drag = action.payload - planets[self.selectedPlanet].pos

                    if abs(drag) > 1.2 * planets[self.selectedPlanet].radius:
                        planets[self.selectedPlanet].vel = 0.667 * Vec3(drag)
                        self.universe.setPlanets(planets)

                        self.selectedPlanet = None

                if action.type == 'REMOVE_PLANET':
                    self.universe.removePlanet(action.payload)

                if action.type == 'START_SIMULATION' or action.type == 'STOP' \
                        or action.type == 'PAUSE':
                    self.runSimulation = True

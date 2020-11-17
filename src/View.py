import pygame

from .vecN import Vec2


WINDOW_TITLE = 'Planet Simmulation'
MIN_CAM_SIZE = 50
PLANET_RADIUS = 10


class View():
    """Manages the GUI"""

    def __init__(self, screen_width, screen_height):
        self.planetRadius = PLANET_RADIUS
        self.screenSize = (screen_width, screen_height)

        self.running = True
        self.camCenter = None
        self.camSize = None

        # Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)

    def quit(self):
        """Terminate the GUI and close window"""
        self.running = False
        pygame.quit()

    def handleEvents(self):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return

    def drawUniverse(self, universe):
        """Draw the current state of a universe"""
        if not self.camCenter:
            self._setUpCamera(universe.planets)

        # Background
        self.screen.fill((0, 0, 0))

        self._drawOrigin()

        self._drawCenterOfMass(universe.planets)

        # Draw all planets
        sorted_planets = sorted(universe.planets, key=lambda p: p.pos.z)
        for planet in sorted_planets:
            self._drawPlanet(planet)

        pygame.display.update()

    def _drawPlanet(self, planet):
        """Draw a planet to the screen"""
        screen_x, screen_y = self._posToScreenCoords(planet.pos)
        radius = self.planetRadius

        if not self._isInScreen((screen_x, screen_y)):
            radius /= 2

        screen_x = max(screen_x, 0)
        screen_x = min(screen_x, self.screenSize[0])
        screen_y = max(screen_y, 0)
        screen_y = min(screen_y, self.screenSize[1])

        pygame.draw.circle(
            self.screen,
            planet.color,
            (screen_x, screen_y),
            radius
        )

    def _drawOrigin(self):
        """Draw a cross on the origin of the coordinate system"""
        screen_coords = self._posToScreenCoords(Vec2())

        if not self._isInScreen(screen_coords):
            return

        pygame.draw.line(
            self.screen,
            (150, 150, 150),
            (screen_coords[0] - 3, screen_coords[1]),
            (screen_coords[0] + 3, screen_coords[1]),
        )
        pygame.draw.line(
            self.screen,
            (150, 150, 150),
            (screen_coords[0], screen_coords[1] - 3),
            (screen_coords[0], screen_coords[1] + 3),
        )

    def _drawCenterOfMass(self, planets):
        """Draw a cross on the center of mass of the planets"""
        center_of_mass = planets[0].mass * planets[0].pos
        for p in planets[1:]:
            center_of_mass += p.mass * p.pos
        center_of_mass /= sum([p.mass for p in planets])

        screen_coords = self._posToScreenCoords(center_of_mass)

        if not self._isInScreen(screen_coords):
            return

        pygame.draw.line(
            self.screen,
            (200, 100, 100),
            (screen_coords[0] - 3, screen_coords[1]),
            (screen_coords[0] + 3, screen_coords[1]),
        )
        pygame.draw.line(
            self.screen,
            (200, 100, 100),
            (screen_coords[0], screen_coords[1] - 3),
            (screen_coords[0], screen_coords[1] + 3),
        )

    def _setUpCamera(self, planets):
        """Set the starting position of the camera"""

        # Find most extreme points
        min_x = min([p.pos.x for p in planets])
        max_x = max([p.pos.x for p in planets])
        min_y = min([p.pos.y for p in planets])
        max_y = max([p.pos.y for p in planets])

        self.camCenter = Vec2((max_x + min_x) / 2, (max_y + min_y) / 2)
        self.camSize = max(max_x - min_x, max_y - min_y, MIN_CAM_SIZE)

    def _posToScreenCoords(self, pos):
        """Translate the space position into the screen drawing coordinates"""
        camLim_x = self.camCenter.x - self.camSize / 2
        camLim_y = self.camCenter.y - self.camSize / 2

        x = (self.screenSize[0] / self.camSize) * (pos.x - camLim_x)
        y = (self.screenSize[1] / self.camSize) * (pos.y - camLim_y)

        # Invert orientation of y
        y = self.screenSize[1] - y

        return int(x), int(y)

    def _isInScreen(self, pos):
        """Return True if coordinate is in  the bounds of the screen"""
        if type(pos) is Vec2:
            return pos.x >= 0 and pos.x <= self.screenSize[0] and \
                pos.y >= 0 and pos.y <= self.screenSize[1]

        return pos[0] >= 0 and pos[0] <= self.screenSize[0] and \
            pos[1] >= 0 and pos[1] <= self.screenSize[1]

    def _isInCamera(self, pos):
        """Return True if position is inside camera field of view"""
        return self._isInScreen(self._posToScreenCoords(pos))

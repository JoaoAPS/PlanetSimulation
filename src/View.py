import pygame

from .vecN import Vec2


WINDOW_TITLE = 'Planet Simmulation'
MIN_SPACE = 50
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

        # Draw origin
        if self._isInCamera(Vec2()):
            self._drawOrigin()

        # Draw all planets
        for planet in universe.planets:
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
        origin_screen = self._posToScreenCoords(Vec2())

        pygame.draw.line(
            self.screen,
            (150, 150, 150),
            (origin_screen[0] - 3, origin_screen[1]),
            (origin_screen[0] + 3, origin_screen[1]),
        )
        pygame.draw.line(
            self.screen,
            (150, 150, 150),
            (origin_screen[0], origin_screen[1] - 3),
            (origin_screen[0], origin_screen[1] + 3),
        )

    def _setUpCamera(self, planets):
        """Set the starting position of the camera"""

        # Find most extreme points
        min_x = min([p.pos.x for p in planets])
        max_x = max([p.pos.x for p in planets])
        min_y = min([p.pos.y for p in planets])
        max_y = max([p.pos.y for p in planets])

        self.camCenter = Vec2((max_x + min_x) / 2, (max_y + min_y) / 2)
        self.camSize = (1.1 * (max_x - min_x), 1.1 * (max_y - min_y))

    def _posToScreenCoords(self, pos):
        """Translate the space position into the screen drawing coordinates"""
        camLim_x = self.camCenter.x - self.camSize[0] / 2
        camLim_y = self.camCenter.y - self.camSize[1] / 2

        x = (self.screenSize[0] / self.camSize[0]) * (pos.x - camLim_x)
        y = (self.screenSize[1] / self.camSize[1]) * (pos.y - camLim_y)

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

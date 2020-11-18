import pygame

from .vecN import Vec2, Vec3


WINDOW_TITLE = 'Planet Simmulation'
MIN_CAM_SIZE = 50
CONTROL_BAR_WIDTH = 150


class Action:
    """An action the View handleEvents method can pass up to the parent App"""

    def __init__(self, actionType, payload=None):
        self.type = actionType
        self.payload = payload


class View():
    """Manages the GUI"""

    def __init__(self, screen_width, screen_height):
        self.screenSize = (screen_width, screen_height)

        self.running = True
        self.camCenter = None
        self.camSize = None
        self.constructionMode = True

        # Init pygame
        pygame.init()
        self.screen = pygame.display.set_mode(self.screenSize)
        pygame.display.set_caption(WINDOW_TITLE)

    def quit(self):
        """Terminate the GUI and close window"""
        self.running = False
        pygame.quit()

    def handleEvents(self, planets):
        """Handle input events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
                return

            if event.type == pygame.KEYDOWN:
                # Stop control
                if event.key == pygame.K_SPACE:
                    return Action('PAUSE')
                if event.key == pygame.K_RETURN:
                    return Action('STOP')

            if self.constructionMode:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    space_pos = self._screenCoordsToPos(pos)

                    # Click on a planet
                    for i, p in enumerate(planets):
                        if abs(space_pos - p.pos) < 1.1 * p.radius:
                            return Action('SELECT_PLANET', i)

                    # Add new planet
                    if self._isInScreen(pos):
                        return Action('ADD_PLANET', {
                            'pos': Vec3(space_pos),
                            'vel': Vec3()
                        })

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    space_pos = self._screenCoordsToPos(pos)

                    if self._isInScreen(pos):
                        return Action('SET_VEL', space_pos)

        keys = pygame.key.get_pressed()

        # Camera movement controls
        if keys[pygame.K_a] or keys[pygame.K_LEFT] or keys[pygame.K_h]:
            self._moveCamera(Vec2(-0.01 * self.camSize))
        if keys[pygame.K_d] or keys[pygame.K_RIGHT] or keys[pygame.K_l]:
            self._moveCamera(Vec2(0.01 * self.camSize))
        if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_k]:
            self._moveCamera(Vec2(0, 0.01 * self.camSize))
        if keys[pygame.K_s] or keys[pygame.K_DOWN] or keys[pygame.K_j]:
            self._moveCamera(Vec2(0, -0.01 * self.camSize))

        # Camera zoom controls
        if keys[pygame.K_q] or keys[pygame.K_i]:
            self._zoomCamera(0.01 * self.camSize)
        if keys[pygame.K_e] or keys[pygame.K_u]:
            self._zoomCamera(-0.01 * self.camSize)

        # Speed control
        if keys[pygame.K_COMMA]:
            return Action('FPS_DOWN')
        if keys[pygame.K_PERIOD]:
            return Action('FPS_UP')

    def drawUniverse(self, universe):
        """Draw the universe simulation GUI"""
        self.screenSize = self.screen.get_size()

        # Background
        self.screen.fill((0, 0, 0))

        self._drawUniverse(universe)

        pygame.display.update()

    def _drawUniverse(self, universe):
        """Draw the current state of a universe"""
        if not self.camCenter:
            self._setUpCamera(universe.planets)

        self._drawOrigin()

        self._drawCenterOfMass(universe.planets)

        # Draw all planets
        for planet in universe.planets:
            self._drawPlanet(planet)

    def _drawPlanet(self, planet):
        """Draw a planet to the screen"""
        screen_x, screen_y = self._posToScreenCoords(planet.pos)
        radius = (self.screenSize[0] / self.camSize) * planet.radius

        if not self._isInScreen((screen_x, screen_y)):
            radius /= 2

        screen_x = max(screen_x, 0)
        screen_x = min(screen_x, self.screenSize[0])
        screen_y = max(screen_y, 0)
        screen_y = min(screen_y, self.screenSize[1])

        # Draw trajectory
        if len(planet.trajectory) > 1:
            pygame.draw.lines(
                self.screen,
                (*planet.color, 10),
                False,
                [self._posToScreenCoords(point) for point in planet.trajectory]
            )

        # Draw planet
        pygame.draw.circle(
            self.screen,
            planet.color,
            (screen_x, screen_y),
            radius
        )

        # Draw velocity
        end_screen_pos = self._posToScreenCoords(planet.pos + 1.5 * planet.vel)
        pygame.draw.line(
            self.screen,
            (255, 255, 255),
            (screen_x, screen_y),
            (end_screen_pos[0], end_screen_pos[1])
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
        if not planets:
            return Vec2()

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

        if not planets:
            self.camCenter = Vec2()
            self.camSize = MIN_CAM_SIZE
            return

        # Find most extreme points
        min_x = min([p.pos.x for p in planets])
        max_x = max([p.pos.x for p in planets])
        min_y = min([p.pos.y for p in planets])
        max_y = max([p.pos.y for p in planets])

        self.camCenter = Vec2((max_x + min_x) / 2, (max_y + min_y) / 2)
        self.camSize = max(max_x - min_x, max_y - min_y, MIN_CAM_SIZE)

    def _moveCamera(self, displacement):
        """Change the position of the camera"""
        if type(displacement) is not Vec2:
            displacement = Vec2(displacement)

        self.camCenter += displacement

    def _zoomCamera(self, sizeChange):
        """Change the zoom level of the camera"""
        self.camSize -= sizeChange

    def _posToScreenCoords(self, pos):
        """Translate the space position into the screen drawing coordinates"""
        camLim_x = self.camCenter.x - self.camSize / 2
        camLim_y = self.camCenter.y - self.camSize / 2

        x = (self.screenSize[0] / self.camSize) * (pos.x - camLim_x)
        y = (self.screenSize[1] / self.camSize) * (pos.y - camLim_y)

        # Invert orientation of y
        y = self.screenSize[1] - y

        return int(x), int(y)

    def _screenCoordsToPos(self, coords):
        # Invert orientation of y
        coord_y = self.screenSize[1] - coords[1]

        camLim_x = self.camCenter.x - self.camSize / 2
        camLim_y = self.camCenter.y - self.camSize / 2

        x = camLim_x + (self.camSize / self.screenSize[0]) * coords[0]
        y = camLim_y + (self.camSize / self.screenSize[1]) * coord_y

        return Vec2(x, y)

    def _isInScreen(self, pos):
        """Return True if coordinate is in  the bounds of the screen"""
        if type(pos) is Vec2:
            return pos.y >= 0 and pos.y <= self.screenSize[1] and pos.x >= 0 \
                and pos.x <= self.screenSize[0]

        return pos[1] >= 0 and pos[1] <= self.screenSize[1] and pos[0] >= 0 \
            and pos[0] <= self.screenSize[0]

    def _isInCamera(self, pos):
        """Return True if position is inside camera field of view"""
        return self._isInScreen(self._posToScreenCoords(pos))

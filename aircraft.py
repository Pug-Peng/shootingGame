
import math
from pathlib import Path

import pygame

pygame.init()

screenHigh = 760
screenWidth = 1000
playground = [screenWidth, screenHigh]
screen = pygame.display.set_mode((screenWidth, screenHigh))
parent_path = Path(__file__).parents[1]
print(parent_path)
image_path = parent_path / 'res'
print(image_path)
icon_path = image_path / 'airplaneIcon.png'
print(icon_path)

pygame.display.set_caption("1942偽")
icon = pygame.image.load(icon_path)
pygame.display.set_icon(icon)
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((50, 50, 50))


class airGameObject:
    def __init__(self, playground=None):
        if playground is None:
            self._playground = [1200, 900]
        else:
            self._playground = playground

        self._objectBound = (0, self._playground[0], 0, self._playground[1])
        self._changeX = 0
        self._changeY = 0
        self._x = 0
        self._y = 0
        self._moveScale = 1
        self._hp = 1
        self._image = None
        self._available = True
        self._center = None
        self._radius = None
        self._collided = False

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def xy(self):
        return [self._x, self._y]

    @xy.setter
    def xy(self, xy):
        try:
            self._x, self._y = xy
            if self.x > self._objectBound[1]:
                self.x = self._objectBound[1]
            if self.x < self._objectBound[0]:
                self.x = self._objectBound[0]
            if self.y > self._objectBound[3]:
                self.y = self._objectBound[3]
            if self.y < self._objectBound[2]:
                self.y = self._objectBound[2]

        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            pass

    def to_the_left(self):
        self._changeX = -self._moveScale

    def to_the_right(self):
        self._changeX = self._moveScale

    def to_the_bottom(self):
        self._changeY = self._moveScale

    def to_the_top(self):
        self._changeY = -self._moveScale

    def stop_x(self):
        self._changeX = 0

    def stop_y(self):
        self._changeY = 0

    def update(self):
        self.x += self._changeX
        self.y += self._changeY
        if self.x > self._objectBound[1]:
            self.x = self._objectBound[1]
        if self.x < self._objectBound[0]:
            self.x = self._objectBound[0]
        if self.y > self._objectBound[3]:
            self.y = self._objectBound[3]
        if self.y < self._objectBound[2]:
            self.y = self._objectBound[2]

    def _collided_(self, it):
        distance = math.hypot(self._center[0] - it.center[0], self._center[1] - it.center[1])
        if distance < self._radius + it.radius:
            return True
        else:
            return False


class Player(airGameObject):

    def __init__(self, playground, xy=None, sensitivity=1):
        airGameObject.__init__(self, playground)
        self._moveScale = 0.5 * sensitivity
        __parent_path = Path(__file__).parents[1]
        self.__player_path = __parent_path / 'res' / 'airforce.png'
        self._image = pygame.image.load(self.__player_path)
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2
        self._radius = 0.3 * math.hypot(self._image.get_rect().w, self._image.get_rect().h)

        if xy is None:
            self._x = (self._playground[0] - self._image.get_rect().w) / 2
            self._y = 3 * self._playground[1] / 4
        else:
            self._x = xy[0]
            self._y = xy[1]

        self._objectBound = (10, self._playground[0] - (self._image.get_rect().w + 10),
                             10, self._playground[1] - (self._image.get_rect().h + 10))

    def update(self):
        airGameObject.update(self)
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().h / 2

    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):
                self._hp -= 10
                self._collided = True
                m.hp = -1
                m.collided = True
                m.available = False


class MyMissile(airGameObject):

    def __init__(self, playground, xy, sensitivity=1):
        airGameObject.__init__(self, playground)
        __parent_path = Path(__file__).parents[1]
        self.__missile_path = __parent_path / 'res' / 'missile2.png'
        self._image = pygame.image.load(self.__missile_path)
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().w / 2
        self._radius = self._image.get_rect().w / 2
        self._x = xy[0]
        self._y = xy[1]
        self._objectBound = (0, self._playground[0], -self._image.get_rect().h - 10, self._playground[1])
        self._moveScale = 0.7 * sensitivity
        self.to_the_top()

    def update(self):
        self._y += self._changeY
        if self._y < self._objectBound[2]:
            self._available = False
        self._center = self._x + self._image.get_rect().w / 2, self._y + self._image.get_rect().w / 2

    def collision_detect(self, enemies):
        for m in enemies:
            if self._collided_(m):
                self._hp -= 10
                self._collided = True
                self._available = False
                m.hp = -1
                m.collided = True
                m.available = False






Missiles = []
keyCountX = 0
keyCountY = 0

running = True
fps = 120
movingScale = 600 / fps
player = Player(playground=playground, sensitivity=movingScale)

clock = pygame.time.Clock()

while running:
    launchMissile = pygame.USEREVENT + 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == launchMissile:
            m_x = player.xy[0] + 20
            m_y = player.xy[1]
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
            m_x = player.xy[0] + 80
            Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                keyCountX += 1
                player.to_the_left()
            if event.key == pygame.K_d:
                keyCountX += 1
                player.to_the_right()
            if event.key == pygame.K_s:
                keyCountY += 1
                player.to_the_bottom()
            if event.key == pygame.K_w:
                keyCountY += 1
                player.to_the_top()
            if event.key == pygame.K_SPACE:
                m_x = player.x + 20
                m_y = player.y
                Missiles.append(MyMissile(xy=(m_x, m_y), playground=playground, sensitivity=movingScale))
                m_x = player.x + 80
                Missiles.append(MyMissile(playground, (m_x, m_y), movingScale))
                pygame.time.set_timer(launchMissile, 400)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                if keyCountX == 1:
                    keyCountX = 0
                    player.stop_x()
                else:
                    keyCountX -= 1
            if event.key == pygame.K_s:
                if keyCountY == 1:
                    keyCountY = 0
                    player.stop_y()
                else:
                    keyCountY -= 1
            if event.key == pygame.K_SPACE:
                pygame.time.set_timer(launchMissile, 0)

    screen.blit(background, (0, 0))
    Missiles = [item for item in Missiles if item._available]
    for m in Missiles:
        m.update()
        screen.blit(m.image, m.xy)

    pygame.display.update()
    player.update()
    screen.blit(player.image, player.xy)
    pygame.display.update()
    dt = clock.tick(fps)

pygame.quit()
import os
import sys
import random
import pygame


class Board:
    # создание поля1
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # значения по умолчанию
        self.left = 50
        self.top = 25
        self.cell_size = 50

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (255, 255, 255), (self.left + i * self.cell_size,
                                                           self.top + j * self.cell_size,
                                                           self.cell_size,
                                                           self.cell_size), 1)
        pygame.draw.rect(screen, (0, 0, 0), (0, 0, self.width, 25))
        pygame.draw.rect(screen, (0, 0, 0), (0, self.height - 25, self.width, 25))


class Shape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.shape = random.randint(1, 5)
        self.image = load_image(f"{self.shape}.png", colorkey=(255, 255, 255))
        # if self.shape == 1:
        #     self.image = pygame.transform.scale(self.image, (48, 198))
        # elif self.shape == 2:
        #     self.image = pygame.transform.scale(self.image, (98, 98))
        # else:
        #     self.image = pygame.transform.scale(self.image, (98, 148))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = random.randint(1, 7) * 50
        self.rect.y = 10
        self.filled = []

    def move(self, key):  # Фигура налезает на фигуру!!!!
        t = True
        if self.rect.y != 625 - self.rect.size[1]:
            if key == pygame.K_LEFT:
                if 50 != self.rect.x:
                    for i in calm_shapes:
                        if self.rect.y + self.rect.size[1] in [_ for _ in range(i.rect.y, i.rect.y + i.rect.size[1])] \
                                and self.rect.x - i.rect.x - i.rect.size[0] <= 50:
                            t = False
                    if t:
                        self.rect = self.rect.move(-50, 0)
            else:
                if self.rect.x + self.rect.size[0] < 400:
                    for i in calm_shapes:
                        # print(self.rect.x - i.rect.x - i.rect.size[0])
                        if self.rect.y + self.rect.size[1] in [_ for _ in range(i.rect.y, i.rect.y + i.rect.size[1])] \
                                and i.rect.x - self.rect.x - self.rect.size[0] <= 50:
                            t = False
                    if t:
                        self.rect = self.rect.move(50, 0)

    def update_last_row(self):
        # x = [i.rect.x for i in calm_shapes]
        # y = [i.rect.y for i in calm_shapes]
        # size = [i.rect.size for i in calm_shapes]
        # check_line = []
        # for i in range(len(y)):
        #     if y[i] + size[i][1] > 575:
        #         for j in range(x[i], x[i] + size[i][0]):
        #             check_line.append(j)
        # # print(check_line)
        # full = len(set([_ for _ in range(50, 451)]) - set(check_line))
        # # print(full)
        # if full < 50:
        #     for shape in calm_shapes:
        #         shape.rect.y += 50
        test = 0
        for i in range(50, 451):
            if screen.get_at((i, 620)) != (0, 0, 0, 255):
                test += 1
        if test > 350:
            for shape in calm_shapes:
                shape.rect.y += 50


    def turn(self):
        t = True
        if self.rect.x + self.rect.size[1] <= 475 and self.rect.y + self.rect.size[0] <= 600:
            # for i in calm_shapes:
            #     if self.rect.x + self.rect.size[1] >= i.rect.x and self.rect.y - i.rect.y < 50:
            #         t = False
            # if t:
            current_x = self.rect.x
            current_y = self.rect.y
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect()
            self.rect.y = current_y
            self.rect.x = current_x
            self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global main_shape
        if self.rect.y < 625 - self.rect.size[1] and \
                not any([pygame.sprite.collide_mask(self, shape) for shape in calm_shapes]):
            self.rect = self.rect.move(0, 1)

        elif self.rect.y == 625 - self.rect.size[1] or \
                any([pygame.sprite.collide_mask(self, shape) for shape in calm_shapes]):
            self.add(calm_shapes)
            if self.rect.y == 625 - self.rect.size[1]:
                self.update_last_row()
            main_shape = Shape()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('')
    size = width, height = 500, 650
    all_sprites = pygame.sprite.Group()
    calm_shapes = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()

    Border(5, 5, width - 5, 5) #вепхняя граница
    Border(50, height - 25, width - 50, height - 25)
    Border(49, 25, 50, height - 25) # левая граница
    Border(width - 50, 25, width - 50, height - 25) # правая граница

    board = Board(8, 12)
    running = True

    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 1000)
    clock = pygame.time.Clock()

    main_shape = Shape()

    while running:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 625, 500, 650))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    main_shape.move(event.key)
                if event.key == pygame.K_UP:
                    main_shape.turn()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        main_shape.update()
        board.render(screen)
        clock.tick(200)

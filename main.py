import os
import sys
import random
import pygame


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 50
        self.top = 25
        self.cell_size = 50

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (255, 255, 255), (self.left + i * self.cell_size,
                                                           self.top + j * self.cell_size,
                                                           self.cell_size,
                                                           self.cell_size), 1)

class Shape:
    def __init__(self, color):
        self.color = color
        shapes_type = {
            1: [[0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]],

            2: [[0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0]],

            3: [[0, 0, 0, 0],
                [0, 1, 1, 0],
                [0, 1, 0, 0],
                [0, 1, 0, 0]],

            4: [[0, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 1, 0, 0]],

            5: [[0, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0]]

        }

    def new_shape(self):
        self.color = random.randint(0, 255)
        self.shape = random.randint(1, 5)
        sprite = pygame.sprite.Sprite()
        sprite.image = load_image(f"{self.shape}.jpg")
        if self.shape == 1:
            sprite.image = pygame.transform.scale(sprite.image, (50, 200))
        elif self.shape == 2:
            sprite.image = pygame.transform.scale(sprite.image, (100, 100))
        else:
            sprite.image = pygame.transform.scale(sprite.image, (100, 150))
        sprite.rect = sprite.image.get_rect()
        sprite.mask = pygame.mask.from_surface(sprite.image)
        all_sprites.add(sprite)
        sprite.rect.x = 150
        sprite.rect.y = 25
        return sprite

    def update(self):
        if self.rect.y < 625 - self.rect.size[1] and not pygame.sprite.collide_mask(self, shape):
            self.rect = self.rect.move(0, 1)


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
    screen = pygame.display.set_mode(size)
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    Border(1, height - 1, width - 1, height - 1)
    Border(1, 1, 1, height - 1)
    Border(width - 1, 1, width - 1, height - 1)
    board = Board(8, 12)
    running = True


    MYEVENTTYPE = pygame.USEREVENT + 1
    pygame.time.set_timer(MYEVENTTYPE, 1000)
    clock = pygame.time.Clock()

    shape = Shape.new_shape(Shape)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.draw(screen)
        all_sprites.update()
        board.render(screen)
        pygame.display.flip()
        clock.tick(90)
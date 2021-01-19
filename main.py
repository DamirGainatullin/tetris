import os
import sys
import random
import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.left = 50
        self.top = 25
        self.cell_size = 50

    def render(self, screen):  # Вывод клетчатого поля на экран
        pygame.draw.rect(screen, (0, 0, 0), (50, 0, self.width * self.cell_size, 25))
        pygame.draw.rect(screen, (0, 0, 0), (50, (self.height * self.cell_size) + 25, self.width * self.cell_size, 25))
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, (255, 255, 255), (self.left + i * self.cell_size,
                                                           self.top + j * self.cell_size,
                                                           self.cell_size,
                                                           self.cell_size), 1)


class Shape(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        global next_shape
        self.shape = next_shape
        next_shape = random.randint(1, 5)
        self.image = load_image(f"{self.shape}.png", colorkey=(255, 255, 255))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = (random.randint(1, 7) * 50) + 2
        self.rect.y = 10
        self.filled = []

    def move(self, key):
        if self.rect.y != 625 - self.rect.size[1]:
            if key == pygame.K_LEFT:
                if 52 != self.rect.x:
                    self.rect.x -= 50
                    if any([pygame.sprite.collide_mask(self, shape) for shape in
                            calm_shapes]):  # Если есть касание с какой либо упавшей фигурой то возвращает фигуру на место
                        self.rect.x += 50
            elif key == pygame.K_RIGHT:
                if self.rect.x + self.rect.size[0] < 403:
                    self.rect.x += 50
                    if any([pygame.sprite.collide_mask(self, shape) for shape in
                            calm_shapes]):  # Если есть касание с какой либо упавшей фигурой то возвращает фигуру на место
                        self.rect.x -= 50

    def update_last_row(self):  # Проверка заполнености нижних рядов
        global score
        for j in range(4):
            test = 0
            for i in range(50, 451):
                if screen.get_at((i, 620 - j * 50)) != (0, 0, 0, 255):
                    test += 1
            if test > 370:
                score += 1
                for shape in calm_shapes:  # При заполнении ряда все фигуры спускаются на 1 клетку вниз
                    shape.rect.y += 50
            else:
                break

    def turn(self):
        if self.rect.x + self.rect.size[1] <= 475 and self.rect.y + self.rect.size[0] <= 600:
            current_x = self.rect.x
            current_y = self.rect.y
            self.image = pygame.transform.rotate(self.image, 90)
            self.rect = self.image.get_rect()
            self.rect.y = current_y
            self.rect.x = current_x
            self.mask = pygame.mask.from_surface(self.image)
            if any([pygame.sprite.collide_mask(self, shape) for shape in
                    calm_shapes]):  # Если есть касание с какой либо упавшей фигурой то возвращает фигуру на место
                self.image = pygame.transform.rotate(self.image, -90)
                self.rect = self.image.get_rect()
                self.rect.y = current_y
                self.rect.x = current_x
                self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global new_record
        global record
        global main_shape
        global end_game
        if any([pygame.sprite.collide_mask(self, border) for border in horizontal_borders]) \
                and any([pygame.sprite.collide_mask(self, shape) for shape in calm_shapes]):
            if score > record:
                record = score
                f = open("data/record.txt", 'w')
                f.write(f"{score}")
                f.close()
                new_record = True
            end_game = True
        else:
            if self.rect.y < 625 - self.rect.size[1] and \
                    not any([pygame.sprite.collide_mask(self, shape) for shape in calm_shapes]):
                self.rect = self.rect.move(0, 1)


            elif self.rect.y == 625 - self.rect.size[1] or \
                    any([pygame.sprite.collide_mask(self, shape) for shape in calm_shapes]):
                self.add(calm_shapes)
                self.update_last_row()
                main_shape = Shape()


class Particle(pygame.sprite.Sprite):  # Класс звездочек при установлении нового реокрда
    def __init__(self, pos, dx, dy):
        super().__init__(stars)
        self.fire = [load_image("star.png")]
        for scale in (5, 10, 20):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))

        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 0
        while self.gravity == 0:
            self.gravity = random.randint(-2, 2)

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


class Border(pygame.sprite.Sprite):
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


def terminate():
    pygame.quit()
    sys.exit()


def next_shape_view():
    next_img = load_image(f"{next_shape}.png", colorkey=(255, 255, 255))
    next_rect = next_img.get_rect()
    next_rect.x = 465
    next_rect.y = 400
    next_img = pygame.transform.scale(next_img, (next_rect.size[0] // 2, next_rect.size[1] // 2))
    screen.blit(next_img, next_rect)


def create_particles(position):
    particle_count = 10
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


def end_screen():
    # Экран окончания игры
    global screen
    fon = pygame.transform.scale(load_image('end.jpg'), (600, 650))
    rec = pygame.font.Font(None, 50)
    rec = rec.render(f'Record: {record}', True, (180, 0, 0))
    new_rec = pygame.font.Font(None, 90)
    new_rec = new_rec.render(f'New Record', True, (180, 0, 0))
    res = pygame.font.Font(None, 40)
    res = res.render(f'Score: {score}', True,
                     (180, 0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if new_record:
            create_particles((90, 450))
            create_particles((510, 450))
            screen.blit(new_rec, (140, 420))
        stars.update()
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        screen.blit(res, (250, 330))
        screen.blit(rec, (230, 360))
        stars.draw(screen)
        pygame.display.flip()
        clock.tick(100)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('тетрис')
    size = width, height = 600, 650
    all_sprites = pygame.sprite.Group()
    stars = pygame.sprite.Group()
    calm_shapes = pygame.sprite.Group()
    screen = pygame.display.set_mode(size)
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()
    score = 0
    end_game = False
    screen_rect = (0, 0, width, height)
    Border(5, 25, width - 5, 5)  # верхняя граница
    Border(50, height - 25, width - 50, height - 25)
    Border(49, 25, 50, height - 25)  # левая граница
    Border(width - 250, 25, width - 250, height - 25)  # правая граница

    board = Board(8, 12)
    running = True

    clock = pygame.time.Clock()
    fps = 100
    counter = 10
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    next_shape = random.randint(1, 5)
    next_img = load_image(f"{next_shape}.png", colorkey=(255, 255, 255))
    next_rect = next_img.get_rect()
    next_rect.x = 465
    next_rect.y = 400
    f = open("data/record.txt", encoding="utf8")
    record = int(f.read(3))
    f.close()
    new_record = False
    main_shape = Shape()

    while running:
        if end_game:
            end_screen()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                        main_shape.move(event.key)
                    if event.key == pygame.K_UP:
                        main_shape.turn()
                if event.type == pygame.USEREVENT:
                    counter -= 1
                    if counter == 0:
                        fps += 20
                        counter = 10
            screen.fill((0, 0, 0))
            pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 625, 500, 650))
            # Прямоугольник который закрывает фигуры упавшие на клетку вниз при заполнении ряда
            f1 = pygame.font.Font(None, 36)
            text1 = f1.render(f'Score: {score}', True,
                              (180, 0, 0))
            text2 = f1.render(f'Next shape:', True, (180, 0, 0))
            screen.blit(text1, (475, 525))
            screen.blit(text2, (455, 375))
            next_shape_view()
            all_sprites.draw(screen)
            main_shape.update()
            board.render(screen)
        pygame.display.flip()
        clock.tick(fps)

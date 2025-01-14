import pygame
import os
import sys
import random

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


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


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image_boom = load_image("boom.png")

    def __init__(self, *group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно!!!
        super().__init__(*group)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        im_w = self.image.get_width()
        im_h = self.image.get_height()
        self.rect.x = random.randrange(width - im_w)
        self.rect.y = random.randrange(height - im_h)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom
        # self.rect = self.rect.move(random.randrange(3) - 1,
        #                            random.randrange(3) - 1)


if __name__ == '__main__':
    fps = 50  # количество кадров в секунду
    clock = pygame.time.Clock()
    running = True

    all_sprites = pygame.sprite.Group()
    for _ in range(20):
        Bomb(all_sprites)

    while running:  # главный игровой цикл

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            all_sprites.update(event)

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()

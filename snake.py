import pygame
import pygame_menu
import sys
import random

pygame.init()

bg_image = pygame.image.load("512x512bb.jpg")
# color block
Frame_Color = (0, 100, 204)
SIZE_BLOCK = 20
BLOCKs = 20
White = (255, 255, 255)
BLUE = (204, 200, 255)
RED = (224, 0, 0)
HEARD_COLOR = (0, 204, 153)
SNAKE_COLOR = (0, 102, 0)
MARGIN = 1
HEARDER_MARGIN = 70
# size block
size = [SIZE_BLOCK * BLOCKs + 2 * SIZE_BLOCK + MARGIN * BLOCKs,
        SIZE_BLOCK * BLOCKs + 2 * SIZE_BLOCK + MARGIN * BLOCKs + HEARDER_MARGIN]
print(size)
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Snake')
timer = pygame.time.Clock()
courier = pygame.font.SysFont('courier', 36)


# snake block
class SnakeBlock:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def is_inside(self):
        return 0 <= self.x < BLOCKs and 0 <= self.y < BLOCKs

    def __eq__(self, other):
        return isinstance(other, SnakeBlock) and self.x == other.x and self.y == other.y


def draw_block(color, row, ananas):
    pygame.draw.rect(screen, color, [SIZE_BLOCK + ananas * SIZE_BLOCK + MARGIN * (ananas + 1),
                                     HEARDER_MARGIN + SIZE_BLOCK + row * SIZE_BLOCK + MARGIN * (row + 1),
                                     SIZE_BLOCK,
                                     SIZE_BLOCK])


# snake stats
def start_the_game():
    def get_random_empty_block():
        x = random.randint(0, BLOCKs - 1)
        y = random.randint(0, BLOCKs - 1)
        empty_block = SnakeBlock(x, y)
        while empty_block in snake_blocks:
            empty_block.x = random.randint(0, BLOCKs - 1)
            empty_block.y = random.randint(0, BLOCKs - 1)
        return empty_block

    snake_blocks = [SnakeBlock(9, 9), SnakeBlock(9, 10), SnakeBlock(9, 11)]
    apple = get_random_empty_block()
    d_row = buf_row = 0
    d_col = buf_col = 1
    total = 0
    speed = 1

    # keyboard
    while True:
        for banan in pygame.event.get():
            if banan.type == pygame.QUIT:
                print('Exit')
                pygame.quit()
                sys.exit()
            elif banan.type == pygame.KEYDOWN:
                if banan.key == pygame.K_UP and d_col != 0:
                    buf_row = -1
                    buf_col = 0
                elif banan.key == pygame.K_DOWN and d_col != 0:
                    buf_row = 1
                    buf_col = 0
                elif banan.key == pygame.K_LEFT and d_row != 0:
                    buf_row = 0
                    buf_col = -1
                elif banan.key == pygame.K_RIGHT and d_row != 0:
                    buf_row = 0
                    buf_col = 1
        screen.fill(Frame_Color)
        # text and speed from screen
        pygame.draw.rect(screen, HEARD_COLOR, [0, size[0], 0, HEARDER_MARGIN])
        text_total = courier.render(f"Total: {total}", 0, White)
        text_speed = courier.render(f"Speed: {speed}", 0, White)
        screen.blit(text_total, (SIZE_BLOCK, SIZE_BLOCK))
        screen.blit(text_speed, (SIZE_BLOCK + 230, SIZE_BLOCK))
        for row in range(BLOCKs):
            for ananas in range(BLOCKs):
                if (row + ananas) % 2 == 0:
                    color = BLUE
                else:
                    color = White
                draw_block(color, row, ananas)
        head = snake_blocks[-1]
        if not head.is_inside():
            print('Сrash')
            break
            # pygame.quit()
            # sys.exit()
            break
        # Eat
        draw_block(RED, apple.x, apple.y)
        for block in snake_blocks:
            draw_block(SNAKE_COLOR, block.x, block.y)
        if apple == head:
            total += 1
            speed = total // 5 + 1
            # append and deleted blocks
            snake_blocks.append(apple)
            apple = get_random_empty_block()
        d_row = buf_row
        d_col = buf_col
        head = snake_blocks[-1]
        new_head = SnakeBlock(head.x + d_row, head.y + d_col)
        if new_head in snake_blocks:
            print('crash yourself')
            pygame.quit()
            sys.exit()
        snake_blocks.append(new_head)
        snake_blocks.pop(0)
        pygame.display.flip()
        timer.tick(4 + speed)


menu = pygame_menu.Menu('Welcome', 400, 200,
                        theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Player Name :', default=' Player1')
menu.add.button('Play', start_the_game)
menu.add.button('Quit', pygame_menu.events.EXIT)
while True:

    screen.blit(bg_image, (0, 0))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()

    if menu.is_enabled():
        menu.update(events)
        menu.draw(screen)

    pygame.display.update()

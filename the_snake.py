# Заводим нужные импорты.
from random import choice, randint

import pygame as pg

# Заводим константы (дефолт из практикума).
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
MIDDLE = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
SPEED = 10
# Настройка игрового окна.
# Даем заголовок.
# Настройка времени.
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Snake Game')
clock = pg.time.Clock()


class GameObject:
    """Объявляем базовый класс.
    маг метод инит.
    - определяем центр экрана для базового класса,
    - и заглушку цвета.
    """

    def __init__(self, position=MIDDLE, length=None, body_color=None):
        self.position = position
        self.body_color = body_color
        self.length = length

    def draw(self):
        """Объявляем метод-заглушку рисования."""
        pass


class Apple(GameObject):
    """Создаем дочерний Яблоко.
    маг метод инит.
    - присваиваем цвет яблоку
    - вызываем рандомайзер яблока на игровом поле.
    """

    def __init__(self, occupied_points=None):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_points or [])

    def randomize_position(self, occupied_points):
        """
        Рандомайзер определяет
        случайное положение клетки GRID_SIZE на поле.
        """
        while True:
            self.position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_points:
                break

    def draw(self):
        """
        Переопределяем заглушку рисования
        из базового класса и отрисовываем яблоко.
        """
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Создаем дочерний Змею.
    маг метод инит.
    - присваиваем атрибуты дочернему классу.
    """

    def __init__(self):
        super().__init__(position=MIDDLE, length=1, body_color=SNAKE_COLOR)
        self.reset()
        self.direction = RIGHT  # Предусмотрено ТЗ.
        self.next_direction = None
        self.last = None

    def reset(self):
        """
        Метод класса змейки отвечающий за
        сброс характеристик змейки.
        """
        self.length = 1
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))

    def draw(self):
        """
        Метод отрисовки
        - тела змейки
        - головы змейки
        - затирания хвоста змейки.
        """
        for position in self.positions[:-1]:
            rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pg.Rect(
            Snake.get_head_position(self),
            (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращающий позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions
        и удаляя последний элемент, если длина змейки не увеличилась.
        """
        d_head_x, d_head_y = self.get_head_position()
        s_dir_x, s_dir_y = self.direction
        self.positions.insert(0, (
            (d_head_x + s_dir_x * GRID_SIZE) % SCREEN_WIDTH,
            (d_head_y + s_dir_y * GRID_SIZE) % SCREEN_HEIGHT
        ))
        if self.length < len(self.positions):
            self.last = self.positions.pop()
        else:
            self.last = None


def handle_keys(game_object):
    """Функция отвечающая за взаимодействие игрока с клавиатурой.
    и ожидающая прерывания программы посредством ESC.
    """
    for event in pg.event.get():
        if (event.type == pg.QUIT
                or (event.type == pg.KEYDOWN
                    and event.key == pg.K_ESCAPE)):
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инит pygame.
    Экземпляр класса змейка.
    Экземпляр класса яблоко.
    """
    pg.init()
    snake = Snake()
    apple = Apple(occupied_points=snake.positions)
    while True:
        # Помещаем в бесконечный цикл:
        # скорость движения змейки
        # функцию управления змейкой
        # отрисовку яблока
        # отрисовку змейки
        # функцию апдейта направления змейки
        # функцию движения змейки
        # ------------блок if elif----------------------
        # подруб обновления игрового поля согласно ФПС.
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        # Если змейка съела яблоко - добавляем к змейке ячейку
        # и добавляем новое яблоко на поле
        # исключая занимания змейки и яблока одной клетки.
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Если змейка врезалась в себя - скидываем змейку.
        # в дефолт и заливаем поле в черный цвет (визуально готовим
        # игрока к новой игре)
        # исключая занимания змейки и яблока одной клетки.
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()

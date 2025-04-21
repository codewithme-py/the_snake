"""Заводим нужные импорты."""

from random import choice, randint

import pygame

"""Заводим константы (дефолт из практикума)."""
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
SPEED = 10

"""
- Настройка игрового окна
- Даем заголовок
- Настройка времени
"""
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()


class GameObject:
    """Объявляем базовый класс,
    маг метод инит,
    - определяем центр экрана для базового класса,
    - и заглушку цвета.
    """

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    """Объявляем метод-заглушку рисования."""

    def draw(self):
        pass


class Apple(GameObject):
    """Создаем дочерний Яблоко,
    маг метод инит,
    - присваиваем цвет яблоку
    - вызываем рандомайзер яблока на игровом поле.
    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    """Рандомайзер определяет случайное положение клетки GRID_SIZE на поле."""

    def randomize_position(self):
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    """Переопределяем заглушку рисования из базового класса и отрисовываем яблоко"""

    def draw(self):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Создаем дочерний Змею
    маг метод инит
    - присваиваем цвет змейке
    - устанавливаем дефолт длину тела
    - согласно ТЗ и практике удобства устанавливаем дефолт атрибут позиции змейки как список кортежей
    - устанавливаем дефолт направление с первого запуска игры - RIGHT
    - устанавливаем атрибут следущего направления змейки как заглушку для будущего переопределния
    - устанавливаем атрибут хвоста змейки как заглушку для будущего переопределния.
    """

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    """Метод класса змейки отвечающий за сброс характеристик змейки в дефолт в случае если змейка укусит себя."""

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))

    """Метод отрисовки
    - тела змейки
    - головы змейки
    - затирания хвоста змейки."""

    def draw(self):
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    """Метод возвращающий позицию головы змейки."""

    def get_head_position(self):
        return self.positions[0]

    """Метод обновления направления после нажатия на кнопку."""

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    """Обновляет позицию змейки (координаты каждой секции), добавляя новую голову в начало списка positions 
    и удаляя последний элемент, если длина змейки не увеличилась.
    """

    def move(self):
        d_head_x, d_head_y = self.get_head_position()
        self.positions.insert(0, (
            (d_head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (d_head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        ))
        if self.length < len(self.positions):
            self.last = self.positions.pop()
        else:
            self.last = []


"""Функция отвечающая за взаимодействие игрока с клавиатурой."""


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """- Инит pygame
    - экземпляр класса яблоко
    - экземпляр класса змейка
    """
    pygame.init()
    apple = Apple()
    snake = Snake()
    while True:
        """Помещаем в бесконечный цикл:
        - скорость движения змейки
        - функцию управления змейкой
        - отрисовку яблока
        - отрисовку змейки
        - функцию апдейта направления змейки
        - функцию движения змейки
        -----------------------------------------------
        - подруб обновления игрового поля согласно ФПС.
        """
        clock.tick(SPEED)
        handle_keys(snake)
        apple.draw()
        snake.draw()
        snake.update_direction()
        snake.move()

        """Если змейка съела яблоко - добавляем к змейке ячейку и добавляем новое яблоко на поле.
        ---------------------
        Если змейка врезалась в себя - скидываем змейку в дефолт и заливаем поле в черный цвет (визуально готовим
        игрока к новой игре).
        """

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        pygame.display.update()


if __name__ == '__main__':
    main()

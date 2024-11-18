import pygame
from random import randint

# Константы
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = 20
FPS = 10


class GameObject:
    """
    Базовый класс для игровых объектов.

    Атрибуты:
        position (tuple): Позиция объекта на игровом поле.
        body_color (tuple): Цвет объекта (RGB).
    """
    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self, surface):
        """
        Метод для отрисовки объекта на экране.
        Переопределяется в дочерних классах.
        """
        pass


class Apple(GameObject):
    """
    Класс яблока, наследуется от GameObject.

    Атрибуты:
        body_color (tuple): Цвет яблока (красный).
    """
    def __init__(self):
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Генерирует случайную позицию яблока в пределах игрового поля."""
        self.position = (
            randint(0, (SCREEN_WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            randint(0, (SCREEN_HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовывает яблоко на экране."""
        pygame.draw.rect(
            surface, self.body_color,
            (*self.position, GRID_SIZE, GRID_SIZE)
        )


class Snake(GameObject):
    """
    Класс змейки, наследуется от GameObject.

    Атрибуты:
        length (int): Длина змейки.
        positions (list): Позиции всех сегментов тела змейки.
        direction (tuple): Текущее направление движения змейки.
        next_direction (tuple): Следующее направление движения змейки.
        body_color (tuple): Цвет змейки (зелёный).
    """
    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = (GRID_SIZE, 0)
        self.next_direction = None
        self.body_color = (0, 255, 0)

    def update_direction(self, new_direction):
        """
        Обновляет направление движения змейки.

        Аргументы:
            new_direction (tuple): Новое направление движения.
        """
        if (
            new_direction[0] * -1 != self.direction[0] or
            new_direction[1] * -1 != self.direction[1]
        ):
            self.next_direction = new_direction

    def move(self):
        """Перемещает змейку, обновляя позиции сегментов."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        new_head = (
            self.positions[0][0] + self.direction[0],
            self.positions[0][1] + self.direction[1]
        )

        if (
            new_head[0] < 0 or new_head[0] >= SCREEN_WIDTH or
            new_head[1] < 0 or new_head[1] >= SCREEN_HEIGHT
        ):
            self.reset()
            return

        self.positions.insert(0, new_head)

        if len(self.positions) > self.length:
            self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.__init__()

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for segment in self.positions:
            pygame.draw.rect(
                surface, self.body_color,
                (*segment, GRID_SIZE, GRID_SIZE)
            )


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для управления змейкой.

    Аргументы:
        snake (Snake): Объект змейки.
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.update_direction((0, -GRID_SIZE))
    elif keys[pygame.K_DOWN]:
        snake.update_direction((0, GRID_SIZE))
    elif keys[pygame.K_LEFT]:
        snake.update_direction((-GRID_SIZE, 0))
    elif keys[pygame.K_RIGHT]:
        snake.update_direction((GRID_SIZE, 0))


def main():
    """Главная функция игры."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        if len(snake.positions) != len(set(snake.positions)):
            snake.reset()

        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()

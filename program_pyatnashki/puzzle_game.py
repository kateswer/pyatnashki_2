"""
Этот файл содержит класс PuzzleGame, который управляет всей логикой и интерфейсом игры.

Используемые компоненты внутри класса:
- pygame: библиотека для графики и управления событиями.
- random: для случайной генерации конфигураций плиток.
- time: для отслеживания времени в игре.

"""
import pygame
import random
import time
import functools

TILE_SIZE = 100
WINDOW_SIZE = TILE_SIZE * 4
RESULT_WINDOW_SIZE = (WINDOW_SIZE + 100, WINDOW_SIZE // 2)
WHITE = (255, 255, 255)
LIGHT_BLUE = (173, 216, 230)
BLACK = (0, 0, 0)
from dataclasses import dataclass, field
from exceptions import InvalidGridSizeError, TileSwapError, AdjacentIndexError
from decorators import log_method_calls

@dataclass
class PuzzleGame:
    """Класс, содержащий основную концепцию игры."""
    grid_size: int
    tile_size: int = TILE_SIZE
    window_size: int = field(init=False)#Размер окна игры.
    window: pygame.Surface = field(init=False)#Объект, представляющий окно игры.
    clock: pygame.time.Clock = field(init=False)#Часы для контроля времени игры.
    font: pygame.font.Font = field(init=False)#Шрифт, используемый в игре.
    tiles: list = field(init=False)
    blank_pos: int = field(init=False)
    start_time: float = None
    move_count: int = 0

    def __post_init__(self):
        """Настройка игры и создание окна."""
        if self.grid_size not in [3, 4]:
            raise InvalidGridSizeError# Исключение для недопустимого размера сетки.
        self.window_size = self.tile_size * self.grid_size# Размер окна = произведению размера плитки и размера сетки.
        self.window = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Пятнашки")
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.tiles = self.create_random_tiles()
        self.blank_pos = self.tiles.index(0)


    def create_random_tiles(self):
        """Создает случайную конфигурацию плиток."""
        tiles = list(range(1, self.grid_size * self.grid_size)) + [0] # Генерация списка плиток от 1 до N, где N = grid_size * grid_size - 1.
        random.shuffle(tiles)
        while not self.is_solvable(tiles):# Перемешивание до получения решаемой конфигурации.
            random.shuffle(tiles)
        return tiles

    def is_solvable(self, tiles):
        """Проверяет, является ли текущая конфигурация решаемой."""
        tiles_without_blank = [tile for tile in tiles if tile != 0]
        inversions = 0
        for i in range(len(tiles_without_blank)):
            for j in range(i + 1, len(tiles_without_blank)):
                if tiles_without_blank[i] > tiles_without_blank[j]:
                    inversions += 1
        return inversions % 2 == 0

    @log_method_calls# Декоратор для логирования вызовов метода.
    def swap_tiles(self, index1, index2):
        """Обмен плиток по указанным индексам.
                   index1 (int): Первый индекс.
                   index2 (int): Второй индекс."""
        if index1 < 0 or index1 >= len(self.tiles) or index2 < 0 or index2 >= len(self.tiles):
            raise IndexError()# Исключение, если один из индексов вне границ списка плиток.
        self.tiles[index1], self.tiles[index2] = self.tiles[index2], self.tiles[index1]
        self.blank_pos = index1

    def is_adjacent(self, index1, index2):
        """Проверяет, являются ли две плитки смежными."""
        if index1 < 0 or index1 >= len(self.tiles) or index2 < 0 or index2 >= len(self.tiles):
            raise IndexError()
        row1, col1 = divmod(index1, self.grid_size)
        row2, col2 = divmod(index2, self.grid_size)
        return (row1 == row2 and abs(col1 - col2) == 1) or (col1 == col2 and abs(row1 - row2) == 1)# Проверка смежности плиток (горизонтально или вертикально).

    def is_solved(self):
        """Проверяет, решена ли головоломка."""
        return self.tiles == list(range(1, self.grid_size * self.grid_size)) + [0]


    def draw_tiles(self):
        """Формирует плитки, фон, таймер и счетчик ходов на игровом экране."""
        self.window.fill(WHITE)
        for index, tile in enumerate(self.tiles):
            if tile != 0:
                # Определение позиции плитки на экране.
                x = (index % self.grid_size) * self.tile_size
                y = (index // self.grid_size) * self.tile_size
                # Прорисовка плитки с фоновым цветом и черной рамкой.
                pygame.draw.rect(self.window, LIGHT_BLUE, (x, y, self.tile_size, self.tile_size), 0)
                pygame.draw.rect(self.window, BLACK, (x, y, self.tile_size, self.tile_size), 3)
                text_surf = self.font.render(str(tile), True, (0, 0, 0))
                self.window.blit(text_surf, (x + self.tile_size // 4, y + self.tile_size // 4))
        if self.start_time:# Если игра началась, запуск отображения таймера и счетчика ходов.
            elapsed_time = int(time.time() - self.start_time)# Вычисление времени, прошедшего с начала игры.
            timer_text = self.font.render(f"Время: {elapsed_time} сек", True, (0, 0, 0))
            self.window.blit(timer_text, (10, self.window_size - 30))
            move_text = self.font.render(f"Ходы: {self.move_count}", True, (0, 0, 0))
            self.window.blit(move_text, (10, self.window_size - 60))
        pygame.display.flip()# Обновление экрана для отображения изменений.

    def run(self):
        """Запускает основной цикл игры."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:# Если пользователь закрыл окно.
                    running = False# Завершение игры.
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    clicked_index = (y // self.tile_size) * self.grid_size + (x // self.tile_size) # Вычисление индекса плитки, на которую пользователь щелкнул.
                    if self.is_adjacent(clicked_index, self.blank_pos):  # Проверка, смежна ли щелкнутая плитка с пустой.
                        self.swap_tiles(clicked_index, self.blank_pos)
                        self.move_count += 1
                        if not self.start_time:
                            self.start_time = time.time()
                        if self.is_solved():
                            self.on_game_won()
            self.draw_tiles()
            self.clock.tick(30)# Ограничение частоты кадров до 30 FPS.


    def on_game_won(self):
        """Обрабатывает событие победы в игре."""
        elapsed_time = int(time.time() - self.start_time)
        win_text = f"Победа! Время: {elapsed_time} сек, Ходы: {self.move_count}"
        self.show_result_window(win_text)


    def show_result_window(self, win_text):
        """Отображает окно с результатами игры."""
        result_window = pygame.display.set_mode(RESULT_WINDOW_SIZE)
        result_window.fill(WHITE)
        lines = win_text.split(',')# Разделение текста на строки.
        for i, line in enumerate(lines):
            text_surf = self.font.render(line, True, (0, 0, 0))
            result_window.blit(text_surf, (10, 10 + i * 40))
        pygame.display.flip()
        time.sleep(3)
        pygame.quit()

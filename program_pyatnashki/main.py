"""Основной файл для запуска игры """
import pygame
from Class_puzzle_game import PuzzleGame

if __name__ == "__main__":
    try:
        grid_size = int(input("Выберите уровень игры (3 или 4): "))# Запрос уровня игры у пользователя.
    except KeyboardInterrupt:
        print("\nВвод прерван. Завершение программы.")
        exit()# Завершение программы при прерывании.

    # Создание игры с выбранным размером сетки.
    game = PuzzleGame(grid_size)
    game.run()
    pygame.quit()

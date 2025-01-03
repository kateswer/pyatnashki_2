"""Файл, содержащий определение пользовательских исключений для игры."""

class InvalidGridSizeError(Exception):
    """Исключение, возникающее при недопустимом размере игрового поля."""
    def __init__(self, message="Размер игрового поля должен быть 3 или 4."):
        super().__init__(message)

class TileSwapError(Exception):
    """Исключение, возникающее при ошибке обмена плиток."""
    def __init__(self, message="Индексы должны быть в пределах допустимого диапазона."):
        super().__init__(message)

class AdjacentIndexError(Exception):
    """Исключение, возникающее при несовпадении индексов для смежных плиток."""
    def __init__(self, message="Индексы должны быть в пределах допустимого диапазона."):
        super().__init__(message)

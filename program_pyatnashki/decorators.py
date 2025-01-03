"""Файл, содержащий декоратор для логирования вызовов методов."""
import functools

def log_method_calls(method):
    """Декоратор, который логирует вызовы методов."""
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs):
        print(f"Вызван метод: {method.__name__}, аргументы: {args}, {kwargs}")
        result = method(self, *args, **kwargs)
        print(f"Результат: {result}")
        return result
    return wrapper

import math

class Calc:

    def add(self, a, b):
        # Возвращает сумму двух чисел
        self._validate_input(a, b)
        return a + b

    def subtract(self, a, b):
        # Возвращает разницу двух чисел
        self._validate_input(a, b)
        return a - b

    def multiply(self, a, b):
        # Возвращает умножение двух чисел
        self._validate_input(a, b)
        return a * b

    def divide(self, a, b):
        # Возвращает деление чисел
        self._validate_input(a, b)
        if b == 0:
            raise ZeroDivisionError("Oops, cannot divide by zero!")
        return a / b

    def sqrt(self, a):
        # Возвращает корень числа
        """Returns the square root of a number. Raises ValueError if the number is negative."""
        if not isinstance(a, (int, float)):
            raise TypeError("Oops,input must be int or float!")
        if a < 0:
            raise ValueError("Oops, cannot calculate the square root of a negative number!")
        return math.sqrt(a)

    @staticmethod
    def _validate_input(a, b):
        # Проверка корректности типа данных
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError("Oops, inputs must be int or float!")

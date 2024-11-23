import pytest
from LR5 import Calc
from unittest.mock import Mock

@pytest.fixture
def calculator():
    return Calc()

# Тест на сложение
def test_add(calculator):
    assert calculator.add(7, 2) == 9
    assert calculator.add(-2, 2) == 0

# Тест на вычитание
def test_subtract(calculator):
    assert calculator.subtract(8, 3) == 5
    assert calculator.subtract(4, 7) == -3

# Тест на умножение
def test_multiply(calculator):
    assert calculator.multiply(2, 9) == 18
    assert calculator.multiply(-2, 9) == -18

# Тест на деление
def test_divide(calculator):
    assert calculator.divide(12, 4) == 3
    assert calculator.divide(7, 2) == 3.5

# Тест на деление на ноль
def test_divide_by_zero(calculator):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(4, 0)

# Тест на некорректные типы входных данных
@pytest.mark.parametrize("a, b", [("4", 5), (6, "7"), (None, 8), (9, None)])
def test_invalid_input(calculator, a, b):
    with pytest.raises(TypeError):
        calculator.add(a, b)

# Тест на параметризованное деление
@pytest.mark.parametrize("a, b, result", [(8, 2, 4), (4, 2, 2), (6, 0.5, 12)])
def test_divide_parametrized(calculator, a, b, result):
    assert calculator.divide(a, b) == result

# Тест с моком для проверки вызова метода _validate_input
def test_validate_input_call():
    mock_calculator = Calc()
    mock_calculator._validate_input = Mock()
    mock_calculator.add(2, 3)
    mock_calculator._validate_input.assert_called_once_with(2, 3)

# Тест на нахождение квадратного корня положительного числа
def test_sqrt_positive(calculator):
    assert calculator.sqrt(4) == 2
    assert calculator.sqrt(25) == 5
    assert calculator.sqrt(0) == 0

# Тест на отрицательное число
def test_sqrt_negative(calculator):
    with pytest.raises(ValueError):
        calculator.sqrt(-9)

# Тест на некорректный тип входного значения
def test_sqrt_invalid_type(calculator):
    with pytest.raises(TypeError):
        calculator.sqrt("9")

# Параметризованный тест для sqrt с разными входными значениями
@pytest.mark.parametrize("input_value, expected_output", [
    (16, 4),
    (0.25, 0.5),
    (1, 1),
    (100, 10)
])
def test_sqrt_parametrized(calculator, input_value, expected_output):
    assert calculator.sqrt(input_value) == expected_output

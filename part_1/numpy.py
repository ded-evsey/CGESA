import numpy as np


def fibonacci(last):
    """
    Построить последовательность Фибоначчи
    методом цикла
    """
    fib = np.array([0, 1], dtype=np.int64)
    if last in [0, 1]:
        return fib
    for _ in np.arange(2, last):
        fib = np.append(fib, fib[-2] + fib[-1])
    return fib


def file_numerical_sequence(file_name):
    """
     В файле хранятся числовые данные,
     перечисленные через разделитель пробела.
     Загрузить данные в одномерный массив.
     Вычислить минимальный элемент,
     максимальный элемент,
     среднее значение,
     медианное значение
     и стандартное отклонение
     для этой числовой последовательности
    :param file_name:
    :return: dict_results
    """
    try:
        array = np.loadtxt(file_name, delimiter=' ', dtype=int)
    except FileNotFoundError:
        return

    return {
        'array': array,
        'max': np.max(array),
        'min': np.min(array),
        'mean value': np.mean(array),
        'median value': np.median(array),
        'standard deviation': np.std(array)
    }


if __name__ == '__main__':
    FILE_NAME = 'input_files/numerical_sequence.txt'
    print(
        f'fibonacci numbers:{fibonacci(9)}'
        .replace(
            '[', ''
        ).replace(
            ']', ''
        )
    )
    for key, value in file_numerical_sequence(FILE_NAME).items():
        print(f'{key}: {value}')

    x = np.array([[1, 2], [4, 3]])
    print(f'Sum of array: {x.sum()}')

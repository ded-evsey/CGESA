import numpy as np
from matplotlib import pyplot as plt
from matplotlib import patches
from random import choices, randint
import math


#  Вписанная фигура случайная и с выбранным количество углов. Начало
def on_circle(center, point, r):
    calc_x = (center[0] - point[0]) ** 2 / r ** 2
    calc_y = (center[1] - point[1]) ** 2 / r ** 2
    return calc_x + calc_y == 1.0


def get_points(center, r, n=None):
    step = 10**-r
    point_round = [
        np.arange(center[i] - r - step, center[i] + r + step, step)
        for i in range(len(center))
    ]

    clear_points = []
    for i, x in enumerate(point_round[0]):
        for j, y in enumerate(point_round[1]):
            point = (round(x, r), round(y, r))
            if on_circle(center, point, r):
                clear_points.append(point)
    points = []
    if not n:
        n = randint(3, len(clear_points))
    if len(clear_points) < n:
        raise ValueError(
            'Не возможно построить фигуру с таким количеством уголов,'
            f' максимальное колчиество углов = {len(clear_points)},'
            f' при радусе = {r} .'
        )
    print(f'Всего точек на окружности {len(clear_points)}, при шаге {step}.\n'
          f'Фигура будет построена из {n}.')
    while 1:
        if len(points) == n:
            return points
        point = choices(clear_points).pop()
        if point not in points:
            points.append(point)
            print(f'Точка {point} добавленна в фигуру.')


def polygon_in_round():
    """
    https://github.com/ded-evsey/CGESA/projects/14#card-34256262
    Для заданного n>2 построить правильный n угольник,
    вписанный в окружность с данным центром и радиусом
    """
    # ввод от пользователя
    x, y = input('Введите центр в формате x,y ').split(',')
    r = 0
    while not r:
        r = int(input('Введите радиус: '))
    n = 0
    flag = bool(input(
        'Выберите одно из: '
        '\n\t 0)Случайный N-угольник'
        '\n\t 1)Задать количество углов'
    ))
    if flag:
        while n <= 2:
            n = int(input('Введите количество углов: '))
    else:
        n = None
    # получение точек
    center = (float(x), float(y))

    points = get_points(center, int(r), n)
    points_sort = sorted(
        points,
        key=lambda point: np.arctan2(
            point[1] - center[1],
            point[0] - center[0]
        )
    )
    # отрисовка
    fig, ax = plt.subplots()
    ax.add_patch(plt.Circle(center, int(r), color='b', fill=False))

    ax.add_patch(
        patches.Polygon(
            points_sort,
            closed=True,
            fill=False,
            color='r'
        )
    )
    plt.xlabel("ось Х")
    plt.ylabel("ось Y")
    ax.set_aspect('equal', adjustable='datalim')
    ax.plot()
    plt.show()
#  Описаная фигура. Конец


# Заданная функция и различные отметки на графике. Начало
# https://github.com/ded-evsey/CGESA/projects/14#card-34256210
# https://github.com/ded-evsey/CGESA/projects/14#card-34256309
def many_graf():
    max_x = int(input('Введите макисмальный X '))
    x_list = np.arange(-max_x, max_x, 0.1)
    arr_sin = [math.sin(x) for x in x_list]
    arr_cos = [math.cos(x) for x in x_list]
    arr_sinh = [math.sinh(x) for x in x_list]
    arr_cosh = [math.cosh(x) for x in x_list]
    plt.plot(x_list, arr_sin, '-', label='Синус')
    plt.plot(x_list, arr_cos, '--', label='Косинус')
    plt.plot(x_list, arr_sinh, '-.', label='Синус гиперболический')
    plt.plot(x_list, arr_cosh, ':', label='Косинус гиперболический')
    plt.xlabel('Ось X')
    plt.ylabel('Ось Y')
    plt.legend()
    plt.show()
# Заданная функция и различные отметки на графике. Конец


if __name__ == '__main__':
    # polygon_in_round()
    # many_graf()

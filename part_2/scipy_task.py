import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import (
    Voronoi,
    voronoi_plot_2d,
    Delaunay
)


def get_rand_point(x_start=-10, x_finish=10, y_f_start=None, y_f_finish=None):
    x_rand = np.random.uniform(x_start, x_finish)
    if not y_f_start and not y_f_finish:
        y_rand = np.random.uniform(x_start, x_finish)
    else:
        y_start = y_f_start(x_rand)
        y_finish = y_f_finish(x_rand)
        if y_finish < y_start:
            y_start, y_finish = y_finish, y_start
        y_rand = np.random.uniform(y_start, y_finish)
    return x_rand, y_rand


# https://github.com/ded-evsey/CGESA/projects/16#card-34257286 start
def make_voronov():
    points = [get_rand_point() for _ in range(np.random.randint(50, 100))]
    voronov = Voronoi(points)
    voronoi_plot_2d(voronov)
    plt.show()
# https://github.com/ded-evsey/CGESA/projects/16#card-34257286 finish


# https://github.com/ded-evsey/CGESA/projects/16#card-34257286 start
def make_delaunay():
    points = np.array([get_rand_point(0, 1, np.exp, np.sin) for _ in range(np.random.randint(10, 15))])
    delaunay = Delaunay(points)
    plt.triplot(points[:, 0], points[:, 1], delaunay.simplices)
    plt.plot(points[:, 0], points[:, 1])
    plt.show()
# https://github.com/ded-evsey/CGESA/projects/16#card-34257286 finish


if __name__ == '__main__':
    k = 1
    array_funcs = ['', make_voronov, make_delaunay]
    while 0 < k < 3:
        print('1) Voronov\n2)Delaunay\n another num)Exit')
        try:
            k = int(input('select ones: '))
        except ValueError:
            print("Enter num!")
            continue
        if not 0 < k < 3:
            print('exiting...')
            continue
        array_funcs[k]()

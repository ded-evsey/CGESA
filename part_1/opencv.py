import cv2
import numpy as np
import os

# Input images
FILE_NAME_KITTEN = 'kitten'
FILE_NAME_BOOK = 'book'
FILE_NAME_GEOMETRY = 'geometry'

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Support variables
CLEAR_IMG = lambda w, h: np.zeros(shape=[w, h, 3], dtype=np.uint8)
KERNEL = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
HSV_MIN = np.array((2, 28, 65), np.uint8)
HSV_MAX = np.array((26, 238, 255), np.uint8)


def read_write_file(func_name, grey, file_name):
    """
    Декоратор, создающий объект изображения в памяти
    и сохраняющий изображение после выполнения функции.
    Так же, при необходимости переводит изображение в серый
    :param func_name: str
    :param grey: bool
    :param file_name: str
    """
    def args_wrapper(func):
        img = cv2.imread(f'input_files/{file_name}.jpg')
        if grey:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        def wrapper(image=img):
            return_img = func(image)
            cv2.imwrite(f'output_files/{file_name}/{func_name}.jpg', return_img)
            print(f'{func_name} complete')
        return wrapper
    return args_wrapper


def laplacian(img):
    """
    https://github.com/ded-evsey/CGESA/projects/4#card-33180662
    Загрузить заданное изображение из файла.
    Преобразовать в оттенки серого.
    Применить фильтр вычисления лапласиана.
    Результат сохранить в файл.
    :param img obj cv2
    :return img obj cv2
    """
    return cv2.Laplacian(img, cv2.CV_16S)


def blur_gaussian(img):
    """
    https://github.com/ded-evsey/CGESA/projects/4#card-33180658
    Загрузить изображение из файла.
    Применить сглаживающий фильтр Гаусса.
    Результат сохранить в файл.
    :param img obj cv2
    :return img obj cv2
    """
    return cv2.GaussianBlur(img, (5, 5), cv2.BORDER_DEFAULT)


def median(img):
    """
    https://github.com/ded-evsey/CGESA/projects/4#card-33180648
    Загрузить изображение из файла.
    Применить медианный сглаживающий фильтр.
    Результат сохранить в файл.
    :param img obj cv2
    :return: img obj cv2
    """
    return cv2.medianBlur(img, 1)


def morph(img, type_morph, kernel=KERNEL):
    """
    Функция, для сокращения вызова записи морфологического преобразования
    :param img: объект изображения
    :param type_morph: тип преобразования
    :param kernel: кернел
    :return img: obj cv2
    """
    return cv2.morphologyEx(img, type_morph, kernel)


def top_hat(img):
    """
    https://github.com/ded-evsey/CGESA/projects/7#card-33180940
    Загрузить изображение из файла.
    Привести к оттенкам серого.
    Выполнить морфологическое преобразование
    «top hat» с различными параметрами.
    Результат сохранить в файл
    :param img: obj cv2
    :return img: obj cv2
    """
    return morph(img, cv2.MORPH_TOPHAT)


def gradient(img):
    """
    https://github.com/ded-evsey/CGESA/projects/7#card-33180946
    Загрузить изображение из файла.
    Привести к оттенкам серого.
    Выполнить морфологическое преобразование
    градиента с различными параметрами.
    Результат сохранить в файл
    :param img: obj cv2
    :return img:obj cv2
    """
    return morph(img, cv2.MORPH_GRADIENT)


def closing(img):
    """
    https://github.com/ded-evsey/CGESA/projects/7#card-33180943
    Загрузить изображение из файла.
    Привести к оттенкам серого.
    Выполнить морфологическое преобразование замыкания
    с различными параметрами.
    Результат сохранить в файл
    :param img:obj cv2
    :return img:obj cv2
    """
    return morph(img, cv2.MORPH_CLOSE)


def erosion(img):
    """
    Загрузить изображение из файла.
    Привести к оттенкам серого.
    Выполнить морфологическое преобразование
    эрозии с различными параметрами.
    Результат сохранить в файл #36
    :param img: obj cv2
    :return img: obj cv2
    """
    return cv2.erode(img, KERNEL)


def rotate(img):
    """
    https://github.com/ded-evsey/CGESA/projects/9#card-33180972
    Загрузить изображение из файла.
    Выполнить поворот на заданный угол.
    Результат сохранить в файл
    :param img: obj cv2
    :return img: obj cv2
    """
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 42, 0.7)
    return cv2.warpAffine(img, M, (w, h))


def move(img):
    """
    https://github.com/ded-evsey/CGESA/projects/9#card-33180970
    Загрузить изображение из файла.
    Выполнить сдвиг изображения на заданный вектор.
    Результат сохранить в файл
    :param img:obj cv2
    :return img:obj cv2
    """
    rows, cols = img.shape[:2]
    M = np.float32([[1, 0, 100], [0, 1, 50]])
    return cv2.warpAffine(img, M, (cols, rows))


def canny(img):
    """
    https://github.com/ded-evsey/CGESA/projects/10#card-33183941
    Загрузить изображение из файла и преобразовать
    к оттенкам серого.
    Преобразовать изображение фильтром Канни.
    Результат сохранить в файл
    :param img: obj cv2
    :return img: obj cv2
    """
    return cv2.Canny(img, 10, 250)


def contour(img):
    """
    https://github.com/ded-evsey/CGESA/projects/10#card-33183940
    Загрузить изображение из файла.
    Определить контуры.
    Сохранить их изображения в отдельный файл
    :param img: obj cv2
    :return img: obj cv2
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # меняем цветовую модель с BGR на HSV
    thresh = cv2.inRange(hsv, HSV_MIN, HSV_MAX)  # применяем цветовой фильтр
    contours, hierarchy = cv2.findContours(
        thresh.copy(),
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_TC89_KCOS
    )
    (h, w) = img.shape[:2]
    return cv2.drawContours(
        CLEAR_IMG(h, w),
        contours,
        -1,
        BLACK
    )


def search_geometry(img):
    """
    https://github.com/ded-evsey/CGESA/projects/11#card-33183908
    https://github.com/ded-evsey/CGESA/projects/11#card-33183909
    Предполагая наличие на
    фотоснимке обложки книги
    обвести соответствующую
    часть изображения прямоугольником.
    Результат вывести на экран.
    :param img: obj cv2
    :return img: obj cv2
    """
    blur = blur_gaussian(img)
    dirt_contour = canny(blur)
    closing_contour = closing(dirt_contour)
    cntr, hier = cv2.findContours(closing_contour.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    for cont in cntr:
        peri = cv2.arcLength(cont, True)
        approx = cv2.approxPolyDP(cont, 0.045 * peri, True)
        if len(approx) == 4:
            img = cv2.drawContours(img, [approx], -1, GREEN, 4)
        if len(approx) == 3:
            img = cv2.drawContours(img, [approx], -1, RED, 3)
    return img


def equalize_hist(img):
    """
    https://github.com/ded-evsey/CGESA/projects/12#card-33183872
    Для заданного изображения выполнить
    операцию выравнивания гистограммы.
    Вывести на экран исходное
    и результирующие изображения #59
    :param img: obj cv2
    :return: obj cv2
    """
    equ = cv2.equalizeHist(img)
    return np.hstack((img, equ))


if __name__ == '__main__':
    for FILE_NAME in [FILE_NAME_KITTEN, FILE_NAME_BOOK, FILE_NAME_GEOMETRY]:
        if not os.path.exists(f'output_files/{FILE_NAME}'):
            os.mkdir(f'output_files/{FILE_NAME}')
    functions = [
        {
            'func': canny,
            'grey': True,
            'file_name': FILE_NAME_KITTEN,
            'func_name': canny.__name__
        },
        {
            'func': erosion,
            'grey': True,
            'file_name': FILE_NAME_KITTEN,
            'func_name': erosion.__name__
        },
        {
            'func': laplacian,
            'grey': True,
            'file_name': FILE_NAME_KITTEN,
            'func_name': laplacian.__name__
        },
        {
            'func': closing,
            'grey': True,
            'file_name': FILE_NAME_KITTEN,
            'func_name': closing.__name__
        },
        {
            'func': top_hat,
            'grey': True,
            'file_name': FILE_NAME_KITTEN,
            'func_name': top_hat.__name__
        },
        {
            'func': gradient,
            'grey': True,
            'file_name': FILE_NAME_KITTEN,
            'func_name': gradient.__name__
        },
        {
            'func': blur_gaussian,
            'grey': False,
            'file_name': FILE_NAME_KITTEN,
            'func_name': blur_gaussian.__name__
        },
        {
            'func': median,
            'grey': False,
            'file_name': FILE_NAME_KITTEN,
            'func_name': median.__name__
        },
        {
            'func': rotate,
            'grey': False,
            'file_name': FILE_NAME_KITTEN,
            'func_name': rotate.__name__
        },
        {
            'func': move,
            'grey': False,
            'file_name': FILE_NAME_KITTEN,
            'func_name': move.__name__
        },
        {
            'func': contour,
            'grey': False,
            'file_name': FILE_NAME_KITTEN,
            'func_name': contour.__name__
        },
        {
            'func': search_geometry,
            'grey': True,
            'file_name': FILE_NAME_GEOMETRY,
            'func_name': search_geometry.__name__
        },
        {
            'func': equalize_hist,
            'grey': True,
            'file_name': FILE_NAME_KITTEN,
            'func_name': equalize_hist.__name__
        },
    ]
    for func in functions:
        @read_write_file(
            func_name=func['func_name'],
            grey=func['grey'],
            file_name=func['file_name']
        )
        def call_func(img):
            f = func['func']
            return f(img)
        call_func()


import cv2
import numpy as np
import os

FILE_NAME = 'kitten'
KERNEL = np.ones((5, 5), np.uint8)


def read_write_file(grey=False, file_name=FILE_NAME):
    """
    Декоратор, создающий объект изображения в памяти
    и сохраняющий изображение после выполнения функции.
    Так же, при необходимости переводит изображение в серый
    :param grey: bool
    :param file_name: str
    """
    def args_wrapper(func):
        img = cv2.imread(f'input_files/{file_name}.jpg')
        if grey:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        def wrapper(image=img):
            return_img = func(image)
            cv2.imwrite(f'output_files/{file_name}/{func.__name__}.jpg', return_img)
            print(f'{func.__name__} complete')
        return wrapper
    return args_wrapper


@read_write_file(grey=True)
def laplacian(img):
    """
    Загрузить заданное изображение из файла.
    Преобразовать в оттенки серого.
    Применить фильтр вычисления лапласиана.
    Результат сохранить в файл.
    :param img obj
    :return img obj post correct
    """
    return cv2.Laplacian(img, cv2.CV_16S)


@read_write_file()
def blur_gaussian(img):
    """
    Загрузить изображение из файла.
    Применить сглаживающий фильтр Гаусса.
    Результат сохранить в файл.
    :param img obj
    :return img obj post correct
    """
    return cv2.GaussianBlur(img, (5, 5), cv2.BORDER_DEFAULT)


@read_write_file()
def median(img):
    """
    Загрузить изображение из файла.
    Применить сглаживающий фильтр Гаусса.
    Результат сохранить в файл.
    :param img obj
    :return: img obj post correct
    """
    return cv2.medianBlur(img, 1)


def morph(img, type_morph, kernel=KERNEL, iterations=1):
    return cv2.morphologyEx(img, type_morph, kernel, iterations=iterations)


@read_write_file(grey=True)
def top_hat(img):
    """
    Загрузить изображение из файла.
    Привести к оттенкам серого.
    Выполнить морфологическое преобразование
    «top hat» с различными параметрами.
    Результат сохранить в файл
    :param img:
    :return:
    """
    return morph(img, cv2.MORPH_TOPHAT)


@read_write_file(grey=True)
def gradient(img):
    """
    Загрузить изображение из файла.
    Привести к оттенкам серого.
    Выполнить морфологическое преобразование
    градиента с различными параметрами.
    Результат сохранить в файл
    :param img:
    :return:
    """
    return morph(img, cv2.MORPH_GRADIENT)


@read_write_file(grey=True)
def closing(img):
    """
    Загрузить изображение из файла.
    Привести к оттенкам серого.
    Выполнить морфологическое преобразование замыкания
    с различными параметрами.
    Результат сохранить в файл
    :param img:
    :return:
    """
    return morph(img, cv2.MORPH_CLOSE)


@read_write_file(grey=True)
def erosion(img):
    """
    Загрузить изображение из файла.
    Привести к оттенкам серого.
    Выполнить морфологическое преобразование
    эрозии с различными параметрами.
    Результат сохранить в файл #36
    :param img:
    :return:
    """
    return cv2.erode(img, KERNEL)


@read_write_file()
def rotate(img):
    """
    Загрузить изображение из файла.
    Выполнить поворот на заданный угол.
    Результат сохранить в файл
    :param img:
    :return:
    """
    (h, w) = img.shape[:2]
    center = (w / 2, h / 2)
    M = cv2.getRotationMatrix2D(center, 42, 0.7)
    return cv2.warpAffine(img, M, (w, h))


@read_write_file()
def move(img):
    """
    Загрузить изображение из файла.
    Выполнить сдвиг изображения на заданный вектор.
    Результат сохранить в файл
    :param img:
    :return:
    """
    rows, cols = img.shape[:2]
    M = np.float32([[1, 0, 100], [0, 1, 50]])
    return cv2.warpAffine(img, M, (cols, rows))


if __name__ == '__main__':
    if not os.path.exists(f'output_files/{FILE_NAME}'):
        os.mkdir(f'output_files/{FILE_NAME}')
    # filters
    laplacian()
    blur_gaussian()
    median()
    # morphology
    top_hat()
    gradient()
    closing()
    erosion()
    # geometric
    rotate()
    move()

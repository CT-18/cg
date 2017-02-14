import numpy as np


def convert_demo(convert, plt):
    # Зафиксируем seed
    np.random.seed(239)

    # Количество точек
    point_n = 500
    # Сгенерируем координаты точек в старой СК
    old_x = np.random.uniform(0, 1, point_n)
    old_y = np.random.uniform(0, 1, point_n)
    # Точки - столбцы матрицы
    olds = np.array([old_x, old_y])
    # Координаты центра и вектора базиса новой СК в старой
    new_c = np.array([0.5, 0.5])
    new_e = np.array([[1, 0.5], [0.5, 1]])
    news = convert(olds, new_c, new_e)

    # Рисуем точки
    f, axes = plt.subplots(1, 2, figsize=(11, 5))
    max_coord = 1.5
    for axis, points, c, (e1, e2) in zip(axes,
                                         [olds, news],
                                         [new_c, [0, 0]],
                                         [new_e, ([0, 1], [1, 0])]):
        axis.scatter(points[0,], points[1,], c='r', zorder=10)
        axis.axis([-max_coord, max_coord, -max_coord, max_coord])
        axis.quiver(c, c, e1, e2, angles='xy', scale_units='xy', scale=1, zorder=20)
    plt.show()


def affine_demo(convert, plt):
    # Зафиксируем seed
    np.random.seed(239)

    # Количество точек на прямой
    point_n = 50

    # Максимальное абсолютное значение координат точек в исходной СК
    max_coord = 4

    # Точки-ориентиры
    base_landmarks = np.array([[1, 0], [0, 1]]).T
    # Положения начал СК
    base_centers = np.array([[0, 0], [2, 1]])
    # Точки прямой в первой СК
    base_x = np.random.uniform(-max_coord + 1, max_coord, point_n)
    base_y = 1 - base_x
    base_points = np.array([base_x, base_y])
    # Точки не на прямой
    base_other_points = np.array([np.random.uniform(-max_coord, max_coord, point_n),
                                  np.random.uniform(-max_coord, max_coord, point_n)])

    # То же, только во второй СК
    base_to_new = lambda points: convert(points,
                                         base_centers[1],
                                         base_landmarks - base_centers[1])
    new_points = base_to_new(base_points)
    new_centers = base_to_new(base_centers.T)
    new_landmarks = base_to_new(base_landmarks)
    new_other_points = base_to_new(base_other_points)

    # Нарисуем точки в двух СК
    f, axes = plt.subplots(1, 2, figsize=(11, 5))
    for title, axis, points, other_points, centers, landmarks in zip(["0", "p"],
                                                                     axes,
                                                                     [base_points, new_points],
                                                                     [base_other_points, new_other_points],
                                                                     [base_centers.T, new_centers],
                                                                     [base_landmarks, new_landmarks]):
        axis.scatter(points[0,], points[1,], c='r', zorder=10)
        axis.scatter(other_points[0,], other_points[1,], c='y', zorder=10)
        axis.scatter(centers[0,:1], centers[1,:1], c='b', s=50, zorder=10)
        axis.scatter(centers[0,1:], centers[1,1:], c='cyan', s=50, zorder=10)
        axis.scatter(landmarks[0,], landmarks[1,], c='g', s=50, zorder=10)
        axis.axis([-max_coord, max_coord, -max_coord, max_coord])
        axis.set_title("Relative to {}".format(title))
    plt.show()

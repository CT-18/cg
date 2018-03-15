import numpy as np

from test_utils import generate_segments


def draw_segment(plt, segments):
    for segment in segments:
        plot_segment(plt, segment, "b")


def draw_points(plt, segments, col="ro"):
    plt.plot([point[0] for point in segments], [point[1] for point in segments], col)


def plot_segment(plt, segment, col):
    plt.plot([segment[0][0], segment[1][0]],
             [segment[0][1], segment[1][1]], col)


def draw(plt):
    max_val = 9
    segments = generate_segments(max_val, 10)
    draw_segment(plt, segments)
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')
    plt.show()


def colors(val):
    if val > 0:
        return "r"
    if val < 0:
        return "b"
    return "g"


def draw_figure(plt, turn, width, step):
    plt.title('Turn predicate values (turn([0, 0], [1, 1], [x, y])')
    plt.xlabel('x-coordinate')
    plt.ylabel('y-coordinate')

    plt.axis([-width, width, -width, width])
    x = np.array([-width, -width])
    y = np.array([width, width])
    for x_i in np.arange(-width + step, width, step):
        for y_i in np.arange(-width + step, width, step):
            color = colors(turn([x, y], np.array([x_i, y_i])))
            plt.scatter(x_i, y_i, color=color, s=20)
    plt.show()

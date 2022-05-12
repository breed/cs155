import click
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
from matplotlib.widgets import Button


poly_points = [
    [(41, -6), (-24, -74), (-51, -6), (73, 17), (-30, -34)],
    [(3, 1), (6, 3), (9, 2), (8, 4), (9, 6), (9, 9), (8, 9), (6, 5), (5, 8), (4, 4), (3, 5), (1, 3)],
    [(0, 0), (10, 0), (0, 10)],
]
points = [
    [(-12, -26), (39, -8)],
    [(3, 3)],
    [(4, 5), (5, 5), (6, 5)],
]

current_plot = 0
fig = None
sub = None
maxdim = 0


def do_plot():
    global fig, sub, maxdim
    if sub:
        sub.clear()
    else:
        fig = plt.figure()
        sub = fig.subplots()
        sub.grid(which='both')

    maxdim = 0
    xs = []
    ys = []
    for (x, y) in poly_points[current_plot]:
        if x >= maxdim:
            maxdim = x + 1
        if y >= maxdim:
            maxdim = y + 1
        xs.append(x)
        ys.append(y)

    xs.append(poly_points[current_plot][0][0])
    ys.append(poly_points[current_plot][0][1])

    sub.plot(xs, ys)
    sub.xaxis.set_minor_locator(AutoMinorLocator())
    sub.yaxis.set_minor_locator(AutoMinorLocator())
    global plotted_points
    global plotted_lines
    plotted_points = []
    plotted_lines = []
    plt.draw()


def do_back(_):
    global current_plot
    current_plot -= 1
    if current_plot < 0:
        current_plot = len(poly_points) - 1
    do_plot()


def do_forward(_):
    global current_plot
    current_plot += 1
    if current_plot == len(poly_points):
        current_plot = 0
    do_plot()


plotted_points = []


def do_points(_):
    global plotted_points
    global sub
    if plotted_points:
        for point in plotted_points:
            point.remove()
        plotted_points = []
    else:
        for (x, y) in points[current_plot]:
            plotted_points.extend(sub.plot(x, y, marker="o"))
    plt.draw()


plotted_lines = []


def do_lines(_):
    global plotted_lines
    if plotted_lines:
        for line in plotted_lines:
            line.remove()
        plotted_lines = []
        plt.draw()
        return
    plotted_lines = []
    for (x, y) in points[current_plot]:
        xs = [maxdim, x]
        ys = [maxdim, y]
        plotted_lines.extend(sub.plot(xs, ys))
        plt.draw()


def polyplot():
    """
    Plot a ploygon and points to help with visualizing https://open.kattis.com/problems/pointinpolygon
    solution using intersecting line segments.
    """
    do_plot()

    bpoints_axes = plt.axes([.1, 0, 0.1, 0.05])
    bpoints = Button(bpoints_axes, "Points")
    bpoints.on_clicked(do_points)

    blines_axes = plt.axes([.2, 0, 0.1, 0.05])
    blines = Button(blines_axes, "Lines")
    blines.on_clicked(do_lines)

    bback_axes = plt.axes([.3, 0, 0.05, 0.05])
    bback = Button(bback_axes, "<")
    bback.on_clicked(do_back)

    bforward_axes = plt.axes([.35, 0, 0.05, 0.05])
    bforward = Button(bforward_axes, ">")
    bforward.on_clicked(do_forward)

    plt.show()

if __name__ == "__main__":
    polyplot()
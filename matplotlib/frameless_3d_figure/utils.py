"""Many parts are from

https://github.com/nschloe/tikzplotlib/blob/f5c5ee784694029d9caf540a5ac83119b809cd13/tikzplotlib/_cleanfigure.py#L1153
"""

from matplotlib import pyplot as plt
import numpy as np

def subplots_3D(nrows=1, ncols=1, projection="ortho"):
    """TODO: actually implement n_rows and n_cols support"""

    fig = plt.figure()
    axes = []
    i = 1
    for i_row in range(1, nrows + 1):
        for i_col in range(1, ncols + 1):
            plot_id = (nrows, ncols, i)
            ax = fig.add_subplot(*plot_id, projection="3d")
            axes.append(ax)
            i += 1
    for ax in axes:
        ax.set_proj_type(projection)
    if len(axes) == 1:
        axes = axes.pop(0)

    return fig, axes


def set_axes_3D_equal(ax):
    """Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.


    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().

    References:
        https://stackoverflow.com/questions/13685386/matplotlib-equal-unit-length-with-equal-aspect-ratio-z-axis-is-not-equal-to # noqa
    """

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5 * max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])



def get_rc_params(ncols, nrows, size_per_plot=(7, 7)):
    """Size per plot: (width, height)
    # TODO: write function which calculates RC params based on subplot layout
    # for example, scale figsize appropriately with number of RC params
    # scale fontsize appropriately with figsize
    """
    figsize = (size_per_plot[0] * ncols, size_per_plot[1] * nrows)
    RC_PARAMS = {
        "figure.figsize": figsize,
        "figure.dpi": 250,
        "figure.autolayout": True,
        "figure.titlesize": "xx-large",
        "legend.frameon": True,
        "axes.titlesize": "xx-large",
        "axes.labelsize": "x-large",
        "xtick.labelsize": "x-large",
        "ytick.labelsize": "x-large",
        "legend.fontsize": "large",
        "axes.grid": True,
    }
    return RC_PARAMS


def cube_3D_data():
    data = np.array([
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1],
    ])
    return data

def plot_cube_3D(ax):
    plot_line(ax, [0, 0, 0], [0, 1, 0])  # A -- B
    plot_line(ax, [0, 1, 0], [1, 1, 0])  # B -- D
    plot_line(ax, [1, 1, 0], [1, 0, 0])  # D -- C
    plot_line(ax, [1, 0, 0], [0, 0, 0])  # C -- A
    # ---
    plot_line(ax, [0, 0, 1], [0, 1, 1])  # E -- F
    plot_line(ax, [0, 1, 1], [1, 1, 1])  # F -- H
    plot_line(ax, [1, 1, 1], [1, 0, 1])  # H -- G
    plot_line(ax, [1, 0, 1], [0, 0, 1])  # G -- E
    # ---
    plot_line(ax, [0, 0, 0], [0, 0, 1])  # E -- F
    plot_line(ax, [0, 1, 0], [0, 1, 1])  # F -- H
    plot_line(ax, [1, 1, 0], [1, 1, 1])  # H -- G
    plot_line(ax, [1, 0, 0], [1, 0, 1])  # G -- E
    for p in cube_3D_data():
        ax.scatter(*p)

def plot_line(ax, start, end):
    ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]])


def get_data_3D(ax):
    line_data = []
    for line in ax.lines:
        d = get_line_data(line)
        line_data.append(d)
    line_data = np.concatenate(line_data, axis=0)

    collection_data = []
    for collection in ax.collections:
        d = get_collection_data(collection)
        collection_data.append(d)
    collection_data = np.concatenate(collection_data, axis=0)
    data = np.concatenate([line_data, collection_data], axis=0)
    return data


def calculate_limits(data):
    xlim = [np.min(data[:, 0]), np.max(data[:, 0])]
    ylim = [np.min(data[:, 1]), np.max(data[:, 1])]
    zlim = [np.min(data[:, 2]), np.max(data[:, 2])]
    return xlim, ylim, zlim


def get_line_data(linehandle):
    """Retrieve 2D or 3D data from line object.
    :param linehandle: matplotlib linehandle object
    :returns : (data, is3D)

    From https://github.com/nschloe/tikzplotlib/blob/f5c5ee784694029d9caf540a5ac83119b809cd13/tikzplotlib/_cleanfigure.py#L560
    """
    xData, yData, zData = linehandle.get_data_3d()
    data = _stack_data_3D(xData, yData, zData).astype(np.float32)
    return data


def _stack_data_3D(xData, yData, zData) -> np.ndarray:
    """ xData, yData, zData --> data """
    data = np.stack([xData, yData, zData], axis=1)
    return data


def get_collection_data(collection):
    """From https://github.com/nschloe/tikzplotlib/blob/f5c5ee784694029d9caf540a5ac83119b809cd13/tikzplotlib/_cleanfigure.py#L582"""
    # https://stackoverflow.com/questions/51716696/extracting-data-from-a-3d-scatter-plot-in-matplotlib
    offsets = collection._offsets3d
    xData, yData, zData = [o.data for o in offsets]
    data = _stack_data_3D(xData, yData, zData)
    return data


def corners3D(xLim, yLim, zLim):
    """Determine the corners of the 3D axes as defined by xLim, yLim and zLim.
    :param xLim: x-axis limits
    :type xLim: list or np.array
    :param yLim: y-axis limits
    :type yLim: list or np.array
    :param zLim: z-axis limits
    :type zLim: list or np.array
    """

    # Lower square of the cube
    lowerBottomLeft = np.array([xLim[0], yLim[0], zLim[0]])
    lowerTopLeft = np.array([xLim[0], yLim[1], zLim[0]])
    lowerBottomRight = np.array([xLim[1], yLim[0], zLim[0]])
    lowerTopRight = np.array([xLim[1], yLim[1], zLim[0]])

    # Upper square of the cube
    upperBottomLeft = np.array([xLim[0], yLim[0], zLim[1]])
    upperTopLeft = np.array([xLim[0], yLim[1], zLim[1]])
    upperBottomRight = np.array([xLim[1], yLim[0], zLim[1]])
    upperTopRight = np.array([xLim[1], yLim[1], zLim[1]])

    corners = np.array(
        [
            lowerBottomLeft,
            lowerTopLeft,
            lowerBottomRight,
            lowerTopRight,
            upperBottomLeft,
            upperTopLeft,
            upperBottomRight,
            upperTopRight,
        ]
    )
    return corners
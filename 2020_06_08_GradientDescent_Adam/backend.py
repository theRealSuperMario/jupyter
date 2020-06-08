import numpy as np




def rosenbrock_function(x_k, deriv=0):
    if deriv == 0:
        return 100 * (x_k[1, :] - x_k[0, :]**2)**2 + (1 - x_k[0, :])**2
    if deriv == 1:
        dx0 = 200 * (x_k[1, :] - x_k[0, :]**2) * (-2) * x_k[0, :] - 2 * (1 - x_k[0, :])
        dx1 = 200 * (x_k[1, :] - x_k[0, :]**2)
        return np.stack([dx0, dx1], axis=0)


def sgd_iteration(f, df, x_k, learning_rate):
    """single iteration of gradient descent 
    
    f :  callable x_k --> scalar
    df : callable x_k --> [N, 1] array
    x_k : [N, 1] array
    """
    p_k = - learning_rate * df(x_k)
    x_kpp = x_k + p_k

    iteration_values = {
        "p_k" : p_k,
        "x_k" : x_k,
        "x_k++" : x_kpp,
    }
    yield iteration_values

from supermariopy import plotting
from matplotlib import pyplot as plt



def gradient_descent(f, df, x_0, N, max_k=30, lims=[-3, 3], learning_rate=0.0001):
    plotting.set_style()
    x_k = x_0

    colors = plotting.get_palette("custom6")
    c1, c2, c3, c4, c5, c6 = np.split(colors, 6, 0)
    colors = plt.cm.viridis(np.linspace(0, 1, max_k))

    N = 20 # sampling density for objective function

    x = np.linspace(lims[0], lims[1], N)
    y = x.copy()
    x_meshgrid, y_meshgrid = np.meshgrid(x, y)
    xy = np.stack([x_meshgrid.ravel(), y_meshgrid.ravel()], axis=0)
    z = f(xy).reshape(N, N)

    k = 0

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.contour(x, y, np.log(z), cmap=plt.cm.viridis)
    ax.set_xlabel(r"x")
    ax.set_ylabel(r"y")
    ax.scatter(*x_k, label=r"$x_0$", marker="x", color=c1)

    while not (max_k == k):
        iteration_values = next(sgd_iteration(f, df, x_k, learning_rate))
        x_k = iteration_values["x_k"]
        x_kpp = iteration_values["x_k++"]
        p_k = iteration_values["p_k"]
        # p_k_norm = p_k / np.linalg.norm(p_k)
        # ax.scatter(*x_k, label=r"$x_k$", marker="x", color=c1)
        # ax.scatter(*x_kpp, label=r"$x_{k+1}$", marker="x", color=c2)
        head_width = 0.5 * np.linalg.norm(p_k)
        ax.arrow(x_k[0].squeeze(), x_k[1].squeeze(), p_k[0].squeeze(), p_k[1].squeeze(), label=r"$p_{k}$", head_width=head_width, color=colors[k])
        x_k = x_kpp
        k += 1
    # ax.legend()
    ax.scatter(*x_k, label=r"$x_{30}$", marker="x", color=c2)
    ax.legend()
    return fig, ax, x_k


def adam_sgd_iteration_biased(f, df, x_k, m_k, v_k, learning_rate, beta_1=0.9, beta_2=0.999, epsilon=1.0e-6):
    """single iteration of ADAM from x_k 
    
    f :  callable x_k --> scalar
    df : callable x_k --> [N, 1] array
    x_k : [N, 1] array
    """

    m_kpp = beta_1 * m_k + (1 - beta_1)*(df(x_k))
    v_kpp = beta_2 * v_k + (1 - beta_2)*(df(x_k) ** 2)


    p_k = - learning_rate / (np.sqrt(v_kpp) + epsilon) * m_kpp
    x_kpp = x_k + p_k

    iteration_values = {
        "p_k" : p_k,
        "x_k" : x_k,
        "x_k++": x_kpp,
        "m_kpp": m_kpp,
        "v_kpp": v_kpp,
        "m_k": m_k,
        "v_k" : v_k
    }
    yield iteration_values


def adam_gradient_descent(f, df, x_0, N, max_k=30, lims=[-3, 3], learning_rate=0.0001):
    plotting.set_style()
    m_0 = np.array([0.0, 0.0]).reshape((2, 1))
    v_0 = np.array([0.0, 0.0]).reshape((2, 1))
    x_k = x_0
    m_k = m_0
    v_k = v_0

    colors = plotting.get_palette("custom6")
    c1, c2, c3, c4, c5, c6 = np.split(colors, 6, 0)
    colors = plt.cm.viridis(np.linspace(0, 1, max_k))

    N = 20 # sampling density for objective function

    x = np.linspace(lims[0], lims[1], N)
    y = x.copy()
    x_meshgrid, y_meshgrid = np.meshgrid(x, y)
    xy = np.stack([x_meshgrid.ravel(), y_meshgrid.ravel()], axis=0)
    z = f(xy).reshape(N, N)

    k = 0

    fig, ax = plt.subplots(1, 1, figsize=(5, 5))
    ax.contour(x, y, np.log(z), cmap=plt.cm.viridis)
    ax.set_xlabel(r"x")
    ax.set_ylabel(r"y")
    ax.scatter(*x_k, label=r"$x_0$", marker="x", color=c1)

    while not (max_k == k):
        iteration_values = next(adam_sgd_iteration_biased(f, df, x_k, m_k, v_k, learning_rate))
        x_k = iteration_values["x_k"]
        x_kpp = iteration_values["x_k++"]
        p_k = iteration_values["p_k"]
        # p_k_norm = p_k / np.linalg.norm(p_k)
        # ax.scatter(*x_k, label=r"$x_k$", marker="x", color=c1)
        # ax.scatter(*x_kpp, label=r"$x_{k+1}$", marker="x", color=c2)
        head_width = 0.5 * np.linalg.norm(p_k)
        ax.arrow(x_k[0].squeeze(), x_k[1].squeeze(), p_k[0].squeeze(), p_k[1].squeeze(), label=r"$p_{k}$", head_width=head_width, color=colors[k])
        x_k = x_kpp
        m_k = iteration_values["m_kpp"]
        v_k = iteration_values["v_kpp"]
        k += 1
    # ax.legend()
    ax.scatter(*x_k, label=r"$x_{30}$", marker="x", color=c2)
    ax.legend()
    return fig, ax, x_k
import numpy as np


"""Code for Superellipses
Equal-Distance Sampling of Supercllipse Models, 1995
"""


def ownpow(a, b):
    """
    Workaround to allow powers of negative numbers in numpy arrays
    https://stackoverflow.com/questions/49029019/in-python-3-6-why-does-a-negative-number-to-the-power-of-a-fraction-return-nan
    """
    out = np.zeros_like(a)
    out = np.where(a >= 0, a ** b, -((-a) ** b))
    out = out.real
    return out


def contour_function(omega, epsilon=1, alpha_vec=np.array([1.0, 1.0])):
    """
    Omega in range [-\pi, \pi], eta in range [-\pi / 2, \pi / 2]
    """
    a1, a2 = alpha_vec
    v = np.array(
        [a1 * ownpow(np.cos(omega), epsilon), a2 * ownpow(np.sin(omega), epsilon)]
    )
    return v


def model_A(theta, a1, a2, epsilon, K=0.025):
    a = np.cos(theta) ** 2 * np.sin(theta) ** 2
    b = a1 ** 2 * ownpow(np.cos(theta), epsilon) ** 2 * ownpow(np.sin(theta), 4)
    c = a2 ** 2 * ownpow(np.sin(theta), epsilon) ** 2 * ownpow(np.cos(theta), 4)
    delta_theta = K / epsilon * np.sqrt(a / (b + c))
    delta_theta = np.abs(delta_theta)
    return delta_theta


def model_theta_towards_zero(theta, a1, a2, epsilon, K=0.025):
    # delta_theta = ownpow(K / a2 - ownpow(theta, epsilon), 1 / epsilon) - theta
    delta_theta = (K / a2 - theta ** epsilon) ** (1 / epsilon) - theta
    delta_theta = delta_theta.real
    delta_theta = np.abs(delta_theta)
    return delta_theta


def model_theta_towards_90(theta, a1, a2, epsilon, K=0.025):
    delta_theta = ownpow(K / a1 - ownpow(np.pi / 2 - theta, epsilon), 1 / epsilon) - (
        np.pi / 2 - theta
    )
    delta_theta = np.abs(delta_theta)
    return delta_theta


def adaptive_sampling_v1(
    a1, a2, epsilon, K=0.025, theta_threshold=0.02, N=100, theta_max=np.pi / 2
):
    """Sampling model from Section 4.3. ONLY FOR FIRST QUADRANT
    * Use `model_theta_towards_zero` when theta below certain threshold
    * Use `model_theta_towards_90`when pi/2 - theta below certain threshold.
    * Use `model_A` otherwise

    Working set of parameters:
        a1 = a2 = 20
        epsilon = 0.2
        K = 1
        theta_threshold = 0.02
    """
    theta_0 = 0
    theta_i = theta_0
    theta_threshold = 1.0e-2  # for epsilon = 0.2, a1 = a2 = 1.0e-2
    thetas = [theta_i]
    deltas = []
    # while theta_i < theta_max :
    for i in range(N):
        t = theta_i
        if t < theta_threshold:
            """ use model for theta -> 0"""
            delta_theta = model_theta_towards_zero(t, a1, a2, epsilon, K)
        elif (np.pi - t) < theta_threshold:
            delta_theta = model_theta_towards_90(t, a1, a2, epsilon, K)
        else:
            delta_theta = model_A(t, a1, a2, epsilon, K)
        theta_i = theta_i + delta_theta
        if theta_i >= theta_max:
            break
        thetas.append(theta_i)
        deltas.append(delta_theta)
    return np.array(thetas), np.array(deltas)


def adaptive_sampling_v2(a1, a2, epsilon, K=0.025, theta_threshold=0.02, N=100):
    """Sampling model from Section 4.3. ONLY FOR FIRST QUADRANT
    * Use `model_theta_towards_zero` when theta or (pi / 2 - theta) below certain threshold
    * Use `model_A` otherwise
    * swap axis at pi / 4

    Working set of parameters:
        a1 = a2 = 20
        epsilon = 0.2
        K = 1
        theta_threshold = 0.02
    """
    theta_0 = 0
    theta_i = theta_0
    theta_max = np.pi / 2
    theta_threshold = 1.0e-2  # for epsilon = 0.2, a1 = a2 = 1.0e-2
    theta_forward_i = theta_i
    theta_backward_i = theta_i
    theta_forwards = [theta_i]
    theta_backwards = [theta_i]

    theta_forwards, delta_forwards = adaptive_sampling_v1(
        a1, a2, epsilon, K, theta_threshold, N, theta_max=np.pi / 4
    )
    theta_backwards, delta_backwards = adaptive_sampling_v1(
        a2, a1, epsilon, K, theta_threshold, N, theta_max=np.pi / 4
    )
    theta = np.concatenate([theta_forwards, np.pi / 2 - theta_backwards[::-1]], axis=0)
    deltas = np.concatenate([delta_forwards, delta_backwards[::-1]], axis=0)
    return theta, deltas


def adaptive_sampling_full_circle(
    a1, a2, epsilon, K=0.025, theta_threshold=0.02, N=100
):
    theta_Q1, deltas_Q1 = adaptive_sampling_v2(a1, a2, epsilon, K, theta_threshold, N)
    theta_Q2 = theta_Q1 + np.pi / 2
    theta_Q4 = -theta_Q1[::-1]
    theta_Q3 = -theta_Q2[::-1]
    theta_Q1Q2 = np.concatenate([theta_Q1, theta_Q2], axis=0)
    theta_Q3Q4 = np.concatenate([theta_Q3, theta_Q4], axis=0)
    final_theta = np.concatenate([theta_Q3Q4, theta_Q1Q2], axis=0)
    return final_theta

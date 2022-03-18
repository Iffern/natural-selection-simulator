import random


def get_gauss_in_range(min_val, max_val):
    mu = (max_val + min_val) / 2
    # TODO: sigma calculated empirically (check during real simulation if correct)
    sigma = (max_val - min_val) / 8

    num = random.gauss(mu, sigma)
    while num < min_val or num > max_val:
        num = random.gauss(mu, sigma)

    return round(num, 2)

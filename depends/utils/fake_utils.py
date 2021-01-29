import numpy as np
import pandas as pd
from faker.providers.person.en import Provider


def random_names(name_type, size):
    names = getattr(Provider, name_type)
    return np.random.choice(names, size=size)


def random_genders(size, p=None):
    if not p:
        p = (0.49, 0.49, 0.01, 0.01)
    gender = ("M", "F", "O", "")
    return np.random.choice(gender, size=size, p=p)


def random_dates(start, end, size):
    divide_by = 24 * 60 * 60 * 10 ** 9
    start_u = start.value // divide_by
    end_u = end.value // divide_by
    return pd.to_datetime(np.random.randint(start_u, end_u, size), unit="D")

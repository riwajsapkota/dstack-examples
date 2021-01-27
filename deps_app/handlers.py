import pandas as pd
import dstack.controls as ctrl

from utils.fake_utils import random_names, random_genders, random_dates


def fake_handler(self: ctrl.Output):
    size = 100
    df = pd.DataFrame(columns=['First', 'Last', 'Gender', 'Birthdate'])
    df['First'] = random_names('first_names', size)
    df['Last'] = random_names('last_names', size)
    df['Gender'] = random_genders(size)
    df['Birthdate'] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2008-01-01'), size=size)
    self.data = df

## How do I use this tutorial?

1. Make sure `dstack` is [installed and started](https://docs.dstack.ai/quickstart#installation)
2. Run `app.py` from this folder to push the application. Click the URL from the output.
3. Read this tutorial for more details on how the application works.
4. Check out other tutorials in this repo.
5. Still have questions? Ask in our [Discord channel](https://discord.gg/8xfhEYa).

**IMPORTANT**: Run `app.py` from the `deps_app` folder (and not the `dstack-examples` folder).

## Simple Application with Dependencies

A `dstack` application may contain own packages and modules as well have dependencies to third party libraries.

In order to push such an application, one must provide the information on these packages, modules, and libraries within
the call of the `dstack.app()` function.

Imagine, we have a folder with the following structure:

```
utils
    __init__.py
    fake_utils.py
app.py
requirements.txt
handlers.py
```

Here's `app.py`:

```python
import dstack as ds

from handlers import fake_handler

app = ds.app(fake_handler, depends=["handlers", "utils"], requirements="requirements.txt")

url = ds.push("deps_app", app)
print(url)
```

As you see, we use `depends` and `requirements` arguments to specify what modules, packages, and libraries our
application depends on. In this case, the application depends on the module `handlers`, the package `utils`, and on all
libraries specified in the `requirements.txt`.

The `depends` argument may list either local modules and packages or PiPy packages. An alternative equivalent of the
line above would be the following:

```python
app = ds.app(fake_handler, depends=["numpy", "pandas", "faker==5.5.0", "handlers", "utils"])
```

**IMPORTANT**: Note, it's important that when you run `app.py` the root directory is `deps_app` where `handlers`
and `utils` are located. If the directory is different, `dstack` may not find them. 

Here's `handlers.py`:

```python
import pandas as pd

from utils.fake_utils import random_names, random_genders, random_dates


def fake_handler():
    size = 100
    df = pd.DataFrame(columns=['First', 'Last', 'Gender', 'Birthdate'])
    df['First'] = random_names('first_names', size)
    df['Last'] = random_names('last_names', size)
    df['Gender'] = random_genders(size)
    df['Birthdate'] = random_dates(start=pd.to_datetime('1940-01-01'), end=pd.to_datetime('2008-01-01'), size=size)
    return df
```

Here's `utils/fake_utils.py`:

```python
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
```

Here's `requirements.txt`:

```
pandas
numpy
faker==5.5.0
```
 
Now if you run `app.py` and click the URL, you'll see a very simple application that on every run generates a new 
list of fake personal data.

![](https://gblobscdn.gitbook.com/assets%2F-LyOZaAwuBdBTEPqqlZy%2F-MQupXFHCj2xq_Tkm99P%2F-MQurPmRIyfhDscuKc9n%2FScreenshot%202021-01-13%20at%2009.21.36.png?alt=media&token=1023f46c-6d29-4f96-91d8-cfbad9fcd3a5)

When you run the application the first time, it makes sure all dependencies are installed.
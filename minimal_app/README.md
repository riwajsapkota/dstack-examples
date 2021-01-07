## How do I use this tutorial?

1. Make sure `dstack` is [installed and started](https://docs.dstack.ai/quickstart#installation)
2. Run `app.py` from this folder to push the application. Click the URL from the output.
3. Read this tutorial for more details on how the application works.
4. Check out other tutorials in this repo.
5. Still have questions? Ask in our [Discord channel](https://discord.gg/8xfhEYa).

## Minimal Application

Here's an elementary example of using `dstack`. The application takes real-time stock exchange data from Yahoo Finance
for the FAANG companies and renders it for a selected symbol. Here's the Python code that you have to run to make such
an application:

```python
from datetime import datetime, timedelta

import dstack.controls as ctrl
import dstack as ds
import plotly.graph_objects as go
import pandas_datareader.data as web


def get_chart(symbols: ctrl.ComboBox):
    start = datetime.today() - timedelta(days=30)
    end = datetime.today()
    df = web.DataReader(symbols.value(), 'yahoo', start, end)
    fig = go.Figure(
        data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    return fig


app = ds.app(get_chart, symbols=ctrl.ComboBox(["FB", "AMZN", "AAPL", "NFLX", "GOOG"]))

result = ds.push("minimal_app", app)
print(result.url)
```

If you run it and click the provided URL, you'll see the application:

![](https://gblobscdn.gitbook.com/assets%2F-LyOZaAwuBdBTEPqqlZy%2F-MOewQku261UjWNNtZlD%2F-MOf161glUdXH5cSOiX0%2FScreenshot%202020-12-16%20at%2011.09.52.png?alt=media&token=114fd3f4-cdd6-451d-b886-d47f34d1a639)

The user is prompted to choose one of the companies to view its latest market data in form of a candlestick chart. Let's
take a closer look at this code and describe every step.

### Application output

First, we define the function get_chart that takes the argument symbols of the type ctrl.ComboBox. The argument
represents a combo box in which the user selects a stock symbol (e.g. "FB", "AMZN", etc). Based on the selected symbol (
see symbols.value()), the function fetches the market data for the corresponding stock (from the Yahoo Financial
Services – using the pandas_datareader package), makes a Candlestick chart (using the plotly package), and returns the
resulting figure.

```python
def get_chart(symbols: ctrl.ComboBox):
    start = datetime.today() - timedelta(days=30)
    end = datetime.today()
    df = web.DataReader(symbols.value(), 'yahoo', start, end)
    fig = go.Figure(
        data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    return fig
```

### User controls and application

Once the function is defined, we call the function `dstack.app` where we pass our function that produces the output and
assigns an instance of `dstack.controls.ComboBox` into the argument named `symbols`. This call creates an instance of an
application. The application contains information on the function that produces the visualizations and binds an instance
`dstack.controls.ComboBox` to the name of the argument of the function (`symbols`).

```python
app = ds.app(get_chart, symbols=ctrl.ComboBox(["FB", "AMZN", "AAPL", "NFLX", "GOOG"]))
```

### Deploy application

Finally, we deploy our application to the `dstack` server by using the function `dstack.push()`. The arguments of the call
are `"minimal_app"` – the name of the application, and `app` – the instance of our application. If successful, this call
returns a push result that has an attribute `url`. This is the URL of the deployed application.

```python
result = ds.push("minimal_app", app)
print(result.url)
```

If we click the URL, we'll see the application.
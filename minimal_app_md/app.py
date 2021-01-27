from datetime import datetime, timedelta

import dstack.controls as ctrl
import dstack as ds
import plotly.graph_objects as go
import pandas_datareader.data as web


def output_handler(self: ctrl.Output, symbols: ctrl.ComboBox):
    start = datetime.today() - timedelta(days=30)
    end = datetime.today()
    df = web.DataReader(symbols.value(), 'yahoo', start, end)
    fig = go.Figure(
        data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    self.data = fig


symbols = ctrl.ComboBox(data=["FB", "AMZN", "AAPL", "NFLX", "GOOG"])

app = ds.app(controls=[symbols],
             outputs=[ctrl.Output(data=ds.md("Here's a simple application with **Markdown** and a chart.")),
                      ctrl.Output(handler=output_handler, depends=[symbols])])

result = ds.push("minimal_app_with_md", app)
print(result.url)
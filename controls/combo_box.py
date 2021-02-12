from datetime import datetime, timedelta

import dstack as ds
import plotly.express as px
import pandas_datareader as pdr

app = ds.app()


def ticker_handler(self: ds.Select):
    self.items = []


def output_handler(self: ds.Output, ticker: ds.Select):
    if ticker.selected is not None:
        symbol = ticker.value()
        start = datetime.today() - timedelta(days=30)
        end = datetime.today()
        df = pdr.data.DataReader(symbol, 'yahoo', start, end)
        self.label = symbol
        self.data = px.line(df, x=df.index, y=df['High'])
    else:
        self.label = "No ticker selected"
        self.data = None


ticker = app.select(label="Select ticker", handler=ticker_handler)
output = app.output(handler=output_handler, depends=[ticker])

result = app.deploy("controls/combo_box")
print(result.url)

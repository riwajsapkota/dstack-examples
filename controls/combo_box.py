from datetime import datetime, timedelta

import dstack.controls as ctrl
import dstack as ds
import plotly.express as px
import pandas_datareader as pdr


def ticker_handler(self: ctrl.ComboBox):
    self.items = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOG']


def output_handler(self: ctrl.Output, ticker: ctrl.ComboBox):
    if ticker.selected > -1:
        start = datetime.today() - timedelta(days=30)
        end = datetime.today()
        df = pdr.data.DataReader(ticker.items[ticker.selected], 'yahoo', start, end)
        self.data = px.line(df, x=df.index, y=df['High'])
    else:
        self.data = ds.md("No ticker selected")


app = ds.app(controls=[ctrl.ComboBox(label="Select ticker", handler=ticker_handler)],
             outputs=[ctrl.Output(handler=output_handler)])

result = ds.push('controls/combo_box', app)
print(result.url)

from datetime import datetime, timedelta

import dstack.controls as ctrl
import dstack as ds
import plotly.graph_objects as go
import pandas_datareader.data as web


def symbols_handler(self: ctrl.ComboBox):
    print("Calling symbols_handler")
    self.data = ['FB', 'AMZN', 'AAPL', 'NFLX', 'GOOG']


def output_handler(self: ctrl.Output, symbols: ctrl.ComboBox):
    print("Calling output_handler")
    start = datetime.today() - timedelta(days=30)
    end = datetime.today()
    df = web.DataReader(symbols.value(), 'yahoo', start, end)
    fig = go.Figure(
        data=[go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])])
    self.data = fig


app = ds.app(controls=[ctrl.ComboBox(handler=symbols_handler)],
             outputs=[ctrl.Output(handler=output_handler)])

result = ds.push('minimal_app_logs', app)
print(result.url)

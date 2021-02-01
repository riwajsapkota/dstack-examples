from datetime import datetime, timedelta

import dstack.controls as ctrl
import dstack as ds
import plotly.express as px
import pandas_datareader as pdr


def output_handler(self: ctrl.Output, ticker: ctrl.TextField):
    if len(ticker.text) > 0:
        start = datetime.today() - timedelta(days=30)
        end = datetime.today()
        df = pdr.data.DataReader(ticker.text, 'yahoo', start, end)
        self.data = px.line(df, x=df.index, y=df['High'])
    else:
        self.data = ds.md("No ticker selected")


app = ds.app(controls=[ctrl.TextField(label="Select ticker")],
             outputs=[ctrl.Output(handler=output_handler)])

result = ds.push('controls/text_field', app)
print(result.url)
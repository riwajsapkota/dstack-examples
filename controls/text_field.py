from datetime import datetime, timedelta

import dstack as ds
import plotly.express as px
import pandas_datareader as pdr


def output_handler(self: ds.Output, ticker: ds.Input):
    if len(ticker.text) > 0:
        start = datetime.today() - timedelta(days=30)
        end = datetime.today()
        df = pdr.data.DataReader(ticker.text, "yahoo", start, end)
        self.label = ticker.text
        self.data = px.line(df, x=df.index, y=df["High"])
    else:
        self.label = "No ticker selected"
        self.data = None


app = ds.app()

ticker = app.input(label="Select ticker")
_ = app.output(handler=output_handler)

result = app.deploy("controls/text_field")
print(result.url)

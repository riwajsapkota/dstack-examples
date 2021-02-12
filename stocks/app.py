import dstack as ds
import plotly.express as px


@ds.cache()
def get_data():
    return px.data.stocks()


def output_handler(self, ticker: ds.Select):
    self.data = px.line(get_data(), x='date', y=ticker.value())


app = ds.app()

ticker = app.select(items=get_data().columns[1:].tolist())
output = app.output(handler=output_handler, depends=[ticker])

result = app.deploy("stocks")
print(result.url)
import dstack as ds
import plotly.express as px


@ds.cache()
def get_data():
    return px.data.stocks()


def symbols_handler(self: ds.Select):
    print("Calling symbols_handler")
    self.items = get_data().columns[1:].tolist()


def output_handler(self, ticker: ds.Select):
    print("Calling output_handler")
    self.data = px.line(get_data(), x='date', y=ticker.value())


app = ds.app()

ticker = app.select(handler=symbols_handler)
_ = app.output(handler=output_handler)

result = app.deploy("logs")
print(result.url)

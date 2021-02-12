import dstack as ds
import plotly.express as px


@ds.cache()
def get_data():
    return px.data.stocks()


def ticker_handler(self: ds.Select):
    self.items = get_data().columns[1:].tolist()


def output_handler(self, ticker: ds.Select):
    self.data = px.line(get_data(), x='date', y=ticker.value())


app = ds.app()

ticker = app.select(handler=ticker_handler)

_ = app.markdown(text="Here's a simple application"
                      " with **Markdown** and a chart.")
_ = app.output(handler=output_handler)

result = ds.push("markdown", app)
print(result.url)

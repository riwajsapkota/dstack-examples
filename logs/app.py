import dstack.controls as ctrl
import dstack as ds
import plotly.express as px


@ds.cache()
def get_data():
    return px.data.stocks()


def symbols_handler(self: ctrl.ComboBox):
    print("Calling symbols_handler")
    self.items = get_data().columns[1:].tolist()


def output_handler(self, ticker):
    print("Calling output_handler")
    self.data = px.line(get_data(), x='date', y=ticker.value())


app = ds.app(controls=[(ctrl.ComboBox(handler=symbols_handler))],
             outputs=[(ctrl.Output(handler=output_handler))])

result = ds.push("logs", app)
print(result.url)

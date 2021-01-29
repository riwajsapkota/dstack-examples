import dstack.controls as ctrl
import dstack as ds
import plotly.express as px


@ds.cache()
def get_data():
    return px.data.stocks()


def output_handler(self, ticker):
    self.data = px.line(get_data(), x='date', y=ticker.value())


app = ds.app(controls=[(ctrl.ComboBox(items=get_data().columns[1:].tolist()))],
             outputs=[ctrl.Output(data=ds.md("Here's a simple application with **Markdown** and a chart.")),
                      ctrl.Output(handler=output_handler)])

result = ds.push("markdown", app)
print(result.url)

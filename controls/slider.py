import dstack.controls as ctrl
import dstack as ds
import plotly.express as px


@ds.cache()
def get_data():
    return px.data.gapminder()


def output_handler(self: ctrl.Output, year: ctrl.Slider):
    year = year.values[year.selected]
    self.data = px.scatter(get_data().query("year==" + str(year)), x="gdpPercap", y="lifeExp",
                           size="pop", color="country", hover_name="country", log_x=True, size_max=60)


app = ds.app(controls=[ctrl.Slider(values=get_data()["year"].unique().tolist(), require_apply=False)],
             outputs=[ctrl.Output(handler=output_handler)])

result = ds.push('controls/slider', app)
print(result.url)

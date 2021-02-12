import dstack as ds
import plotly.express as px


@ds.cache()
def get_data():
    return px.data.gapminder()


def output_handler(self: ds.Output, year: ds.Slider):
    year = year.values[year.selected]
    self.data = px.scatter(get_data().query("year==" + str(year)), x="gdpPercap", y="lifeExp",
                           size="pop", color="country", hover_name="country", log_x=True, size_max=60)


app = ds.app()

slider = app.slider(values=get_data()["year"].unique().tolist())
_ = app.output(handler=output_handler, depends=[slider])

result = app.deploy("controls/slider")
print(result.url)

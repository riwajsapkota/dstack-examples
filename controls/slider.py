import dstack as ds
import plotly.express as px

app = ds.app()  # create an instance of the application


# an utility function that loads the data
def get_data():
    return px.data.gapminder()


# a handler that updates the plot output based on the selected year
def output_handler(self, year):
    value = year.value()  # the selected year
    self.data = px.scatter(get_data().query("year==" + str(value)), x="gdpPercap", y="lifeExp",
                           size="pop", color="country", hover_name="country", log_x=True, size_max=60)


# a slider control that prompts to select a year
slider = app.slider(values=get_data()["year"].unique().tolist())

# an output control that shows the chart
app.output(handler=output_handler, depends=[slider])

# deploy the application with the name "controls/" and print its URL
url = app.deploy("controls/slider")
print(url)

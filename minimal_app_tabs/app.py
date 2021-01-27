import dstack as ds
import dstack.controls as ctrl
import plotly.express as px


def scatter_handler(self: ctrl.Output):
    df = px.data.iris()
    self.data = px.scatter(df, x="sepal_width", y="sepal_length", color="species")


def bar_handler(self: ctrl.Output):
    df = px.data.tips()
    self.data = px.bar(df, x="sex", y="total_bill", color="smoker", barmode="group")


frame = ds.frame("minimal_app_tabs")

frame.add(ds.app(outputs=[ds.Output(handler=scatter_handler)]), params={"Scatter Chart": ds.tab()})
frame.add(ds.app(outputs=[ds.Output(handler=bar_handler)]), params={"Bar Chart": ds.tab()})

url = frame.push()
print(url)
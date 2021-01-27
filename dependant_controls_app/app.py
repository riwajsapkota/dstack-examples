import dstack.controls as ctrl
import dstack as ds
import pandas as pd


@ds.cache()
def get_data():
    return pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)


def get_regions():
    df = get_data()
    return df["Region"].unique().tolist()


def countries_handler(self: ctrl.ComboBox, regions: ctrl.ComboBox):
    df = get_data()
    self.data = df[df["Region"] == regions.value()]["Country"].unique().tolist()


regions = ctrl.ComboBox(data=get_regions, label="Region")
countries = ctrl.ComboBox(handler=countries_handler, label="Country", depends=[regions])


def output_handler(self: ctrl.Output, countries: ctrl.ComboBox):
    df = get_data()
    self.data = df[df["Country"] == countries.value()]


app = ds.app(controls=[regions, countries, ctrl.Apply()],
             outputs=[ds.Output(handler=output_handler, depends=[countries])])

result = ds.push('dependant_controls_app', app)
print(result.url)

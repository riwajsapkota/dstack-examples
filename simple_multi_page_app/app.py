import dstack.controls as ctrl
import dstack as ds
import pandas as pd
import plotly.express as px


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


def country_output_handler(self: ctrl.Output, countries: ctrl.ComboBox):
    df = get_data()
    self.data = df[df["Country"] == countries.value()]


data_by_country_app = ds.app(controls=[regions, countries],
                             outputs=[ctrl.Output(handler=country_output_handler, depends=[countries])])


def get_companies():
    df = get_data()
    return df["Company"].unique().tolist()


companies = ctrl.ComboBox(data=get_companies, label="Company")


def company_output_handler(self: ctrl.Output, companies: ctrl.ComboBox):
    df = get_data()
    row = df[df["Company"] == companies.value()].filter(["y2015", "y2016", "y2017", "y2018", "y2019"], axis=1)
    row.rename(columns={"y2015": "2015", "y2016": "2016", "y2017": "2017", "y2018": "2018", "y2019": "2019"},
               inplace=True)
    col = row.transpose()
    col.rename(columns={col.columns[0]: "Licenses"}, inplace=True)
    fig = px.bar(col.reset_index(), x="index", y="Licenses", labels={"index": "Year"})
    fig.update(layout_showlegend=False)
    self.data = fig


data_by_company_app = ds.app(controls=[companies],
                             outputs=[ctrl.Output(handler=company_output_handler)])

frame = ds.frame("simple_multi_page_app")
frame.add(data_by_country_app, params={"Companies": ds.tab()})
frame.add(data_by_company_app, params={"Licenses": ds.tab()})
result = frame.push()
print(result.url)

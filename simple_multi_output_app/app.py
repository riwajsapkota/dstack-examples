import dstack.controls as ctrl
import dstack as ds
import pandas as pd
import plotly.express as px


@ds.cache()
def get_data():
    return pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)


@ds.cache()
def get_regions():
    df = get_data()
    return df["Region"].unique().tolist()


regions = ctrl.ComboBox(data=get_regions, label="Region")


def countries_handler(self: ctrl.ComboBox, regions: ctrl.ComboBox):
    df = get_data()
    self.data = df[df["Region"] == regions.value()]["Country"].unique().tolist()


def get_companies_by_country(self: ctrl.ComboBox, countries: ctrl.ComboBox):
    df = get_data()
    self.data = df[df["Country"] == countries.value()]["Company"].unique().tolist()


@ds.cache()
def country_output_handler(self: ds.Output, countries: ctrl.ComboBox):
    df = get_data()
    self.data = df[df["Country"] == countries.value()]


@ds.cache()
def company_output_handler(self: ds.Output, companies: ctrl.ComboBox):
    company = companies.value()
    df = get_data()
    row = df[df["Company"] == company].filter(["y2015", "y2016", "y2017", "y2018", "y2019"], axis=1)
    row.rename(columns={"y2015": "2015", "y2016": "2016", "y2017": "2017", "y2018": "2018", "y2019": "2019"},
               inplace=True)
    col = row.transpose()
    col.rename(columns={col.columns[0]: "Licenses"}, inplace=True)
    fig = px.bar(col.reset_index(), x="index", y="Licenses", labels={"index": "Year"})
    fig.update(layout_showlegend=False)
    self.data = fig
    self.label = company


countries = ctrl.ComboBox(handler=countries_handler, label="Country", depends=[regions])
companies = ctrl.ComboBox(handler=get_companies_by_country, label="Company", depends=[countries])
md_output = ds.Output(data=ds.md("This is an example of a `dstack` application with multiple controls and outputs."))
countries_output = ds.Output(handler=country_output_handler, label="Companies", depends=[countries])
company_chart = ds.Output(handler=company_output_handler, depends=[companies])

app = ds.app(controls=[regions, countries, companies],
             outputs=[md_output, countries_output, company_chart])

url = ds.push("simple_multi_output_app", app)
print(url)

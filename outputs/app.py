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


app = ds.app()

sidebar = app.sidebar()

regions = sidebar.select(items=get_regions, label="Region")


def countries_handler(self: ds.Select, regions: ds.Select):
    df = get_data()
    self.items = df[df["Region"] == regions.value()]["Country"].unique().tolist()


def get_companies_by_country(self: ds.Select, countries: ds.Select):
    df = get_data()
    self.items = df[df["Country"] == countries.value()]["Company"].unique().tolist()


def country_output_handler(self: ds.Output, countries: ds.Select):
    df = get_data()
    self.data = df[df["Country"] == countries.value()]


def company_output_handler(self: ds.Output, companies: ds.Select):
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


countries = sidebar.select(handler=countries_handler, label="Country", depends=[regions])
companies = sidebar.select(handler=get_companies_by_country, label="Company", depends=[countries])
_ = app.markdown(text="This is an example of a `dstack` application with multiple controls and outputs.",
                 columns=12)
countries_output = app.output(handler=country_output_handler, label="Companies", depends=[countries],
                              columns=6, rows=6)
company_chart = app.output(handler=company_output_handler, depends=[companies],
                           columns=6, rows=6)

url = app.deploy("outputs")
print(url)

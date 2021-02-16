import dstack as ds
import pandas as pd
import plotly.express as px


@ds.cache()
def get_data():
    return pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)


app = ds.app()


def get_regions():
    df = get_data()
    return df["Region"].unique().tolist()


def countries_handler(self: ds.Select, regions: ds.Select):
    df = get_data()
    self.items = df[df["Region"] == regions.value()]["Country"].unique().tolist()


companies_tab = app.tab("Companies")

sidebar = companies_tab.sidebar()

regions = sidebar.select(items=get_regions, label="Region")
countries = sidebar.select(handler=countries_handler, label="Country", depends=[regions])


def country_output_handler(self: ds.Output, countries: ds.Select):
    df = get_data()
    self.data = df[df["Country"] == countries.value()]


_ = companies_tab.output(handler=country_output_handler, depends=[countries])


def get_companies():
    df = get_data()
    return df["Company"].unique().tolist()


def company_output_handler(self: ds.Output, companies: ds.Select):
    df = get_data()
    row = df[df["Company"] == companies.value()].filter(["y2015", "y2016", "y2017", "y2018", "y2019"], axis=1)
    row.rename(columns={"y2015": "2015", "y2016": "2016", "y2017": "2017", "y2018": "2018", "y2019": "2019"},
               inplace=True)
    col = row.transpose()
    col.rename(columns={col.columns[0]: "Licenses"}, inplace=True)
    fig = px.bar(col.reset_index(), x="index", y="Licenses", labels={"index": "Year"})
    fig.update(layout_showlegend=False)
    self.data = fig


licenses_tab = app.tab("Licenses")

companies = licenses_tab.select(items=get_companies, label="Company")
_ = licenses_tab.output(handler=company_output_handler, depends=[companies])

result = app.deploy("tabs")
print(result.url)

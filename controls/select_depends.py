import dstack as ds
import pandas as pd

app = ds.app()  # create an instance of the application


# an utility function that loads the data
def get_data():
    return pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)


# an utility function that returns regions
def get_regions():
    df = get_data()
    return df["Region"].unique().tolist()


# a drop-down control that shows regions
regions = app.select(items=get_regions, label="Region")


# a handler that updates the drop-down with counties based on the selected region
def countries_handler(self, regions):
    region = regions.value()  # the selected region
    df = get_data()
    self.items = df[df["Region"] == region]["Country"].unique().tolist()


# a drop-down control that shows countries
countries = app.select(handler=countries_handler, label="Country", depends=[regions])


# a handler that updates the table output based on the selected country
def output_handler(self, countries):
    country = countries.value()  # the selected country
    df = get_data()
    self.data = df[df["Country"] == country]  # we assign a pandas dataframe here to self.data


# an output that shows companies based on the selected country
app.output(handler=output_handler, depends=[countries])

# deploy the application with the name "controls/select_depends" and print its URL
url = app.deploy("controls/select_depends.py")
print(url)

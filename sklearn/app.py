import dstack as ds
import numpy as np
import pandas as pd


# Retrieve the latest version of the model
def get_model():
    return ds.pull("tutorials/sklearn_model")


# An utility function that loads the data
@ds.cache()  # caching the result
def get_data():
    df = pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)
    df = df[df["Churn"].isnull()].drop(["Churn"], axis=1)
    return df


# An utility function that loads data, invokes the model to predict churn, and drops unnecessary columns
@ds.cache()
def get_predicted_data():
    df = get_data().copy()

    predicted_churn = get_model().predict(df)  # Predict churn

    # Replace 1.0 with "Yes" and 0.0 with "No"
    df["Predicted Churn"] = np.array(list(map(lambda x: "Yes" if x == 1.0 else "No", predicted_churn)))

    # Replace the numbers of months with the names of the months
    df["RenewalMonth"] = df["RenewalMonth"].apply(
        lambda x: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][x - 1])

    # Drop unnecessary columns
    return df.drop(["y2015", "y2016", "y2017", "y2018", "y2019"], axis=1)


# Create an application
app = ds.app()

# A drop-down control with the list of regions
regions_select = app.select(get_data()["Region"].unique().tolist(), label="Region")
# A drop drown controls with the list of months
months_select = app.select(['Oct', 'Nov', 'Dec'], label="Month")


# A handler that updates the state of the output with the predicted data
def app_handler(self, regions_select, months_select):
    df = get_predicted_data().copy()

    df = df[df["Predicted Churn"] == "Yes"]
    df = df[(df["Region"] == regions_select.value())]
    df = df[(df["RenewalMonth"] == months_select.value())]
    self.data = df


# A table output that shows the predicted data based on the selected region and month
app.output(handler=app_handler, depends=[regions_select, months_select])

# deploy the application with the name "sklearn" and print its URL
url = app.deploy("sklearn")
print(url)

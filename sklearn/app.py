import dstack as ds
import numpy as np
import pandas as pd


def get_model():
    return ds.pull("tutorials/sklearn_model")


@ds.cache()
def get_data():
    df = pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)
    df = df[df["Churn"].isnull()].drop(["Churn"], axis=1)
    return df


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']


@ds.cache()
def get_predicted_data():
    df = get_data().copy()

    predicted_churn = get_model().predict(df)

    df["Predicted Churn"] = np.array(list(map(lambda x: "Yes" if x == 1.0 else "No", predicted_churn)))
    df["RenewalMonth"] = df["RenewalMonth"].apply(lambda x: months[x - 1])

    return df.drop(["y2015", "y2016", "y2017", "y2018", "y2019"], axis=1)


app = ds.app()

regions_ctrl = app.select(get_data()["Region"].unique().tolist(), label="Region")
months_ctrl = app.select(['Oct', 'Nov', 'Dec'], label="Month")
churn_ctrl = app.checkbox(label="Churn", selected=True)


def app_handler(self, regions_ctrl, months_ctrl, churn_ctrl):
    df = get_predicted_data().copy()

    df = df[(df["Predicted Churn"] == ("Yes" if churn_ctrl.selected else "No"))]
    df = df[(df["Region"] == regions_ctrl.value())]
    df = df[(df["RenewalMonth"] == months_ctrl.value())]
    self.data = df


app.output(handler=app_handler, depends=[regions_ctrl, months_ctrl, churn_ctrl])

url = app.deploy("sklearn")
print(url)

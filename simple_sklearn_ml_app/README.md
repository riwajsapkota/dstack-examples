## How do I use this tutorial?

1. Make sure `dstack` is [installed and started](https://docs.dstack.ai/quickstart#installation)
2. Run `model.py` and `app.py` from this folder to push the application. Click the URLs from the output.
3. Read this tutorial for more details on how the application works.
4. Check out other tutorials in this repo.
5. Still have questions? Ask in our [Discord channel](https://discord.gg/8xfhEYa).

## Simple Application with a Scikit-learn ML Model

Let's start by training a very simple model:

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import dstack as ds


def transform(X, countries, sectors):
    def n_years(row):
        l = [row["y2019"], row["y2018"], row["y2017"], row["y2016"], row["y2015"]]
        return len([x for x in l if x != 0])

    X = X.copy()
    X["nyears"] = X.apply(n_years, axis=1)

    X = X.drop(["Company", "Region", "Manager", "Churn", "RenewalMonth", "RenewalDate"], axis=1)

    year_col = ["y2015", "y2016", "y2017", "y2018", "y2019"]
    for col in year_col:
        X[col] = X[col] / X[col].max()
    for c in countries:
        X[c] = X["Country"].apply(lambda x: 1 if x == c else 0)
    for s in sectors:
        if s:
            X[s] = X["Sector"].apply(lambda x: 1 if x == s else 0)

    X = X.drop(["Country", "Sector"], axis=1)
    return X


df = pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)

countries = df["Country"].unique()
sectors = df["Sector"].unique()

X = df[df["RenewalMonth"] < 10].copy()
y = X["Churn"]
X = transform(X, countries, sectors)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=99)

model = LogisticRegression()
model.fit(X_train, y_train)

url = ds.push("simple_sklearn_ml_model", model)
print(url)
```

If we run this code, it will train the model and push it to dstack. In the output, you'll see its URL which you can use
to view the model via the interface. If you click it, you'll see the following:

![](https://gblobscdn.gitbook.com/assets%2F-LyOZaAwuBdBTEPqqlZy%2F-MPsKmT-BDVNt5W2a40K%2F-MPsRM8MWXa8ral7YRRJ%2FScreenshot%202020-12-31%20at%2011.56.26.png?alt=media&token=85a741a2-d7ae-4330-b1f9-c7124016ec7b)

Now, this model is stored with `dstack`'s registry and can be pulled from any application. Let's look at an example of
an application that uses this model:

```python
import dstack as ds
import dstack.controls as ctrl
import pandas as pd


def get_model():
    return ds.pull("churn_demo/lr_model")


def transform(X, countries, sectors):
    def n_years(row):
        l = [row["y2019"], row["y2018"], row["y2017"], row["y2016"], row["y2015"]]
        return len([x for x in l if x != 0])

    X = X.copy()
    X["nyears"] = X.apply(n_years, axis=1)

    X = X.drop(["Company", "Region", "Manager", "Churn", "RenewalMonth", "RenewalDate"], axis=1)

    year_col = ["y2015", "y2016", "y2017", "y2018", "y2019"]

    for col in year_col:
        X[col] = X[col] / X[col].max()

    for c in countries:
        X[c] = X["Country"].apply(lambda x: 1 if x == c else 0)

    for s in sectors:
        if s:
            X[s] = X["Sector"].apply(lambda x: 1 if x == s else 0)

    X = X.drop(["Country", "Sector"], axis=1)
    return X


@ds.cache()
def get_data():
    df = pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)

    countries = df["Country"].unique()
    sectors = df["Sector"].unique()

    x1 = df[df["RenewalMonth"] >= 10].copy()
    x1a = transform(x1, countries, sectors)
    return x1, x1a


x1, x1a = get_data()

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

regions_ctrl = ctrl.ComboBox(x1["Region"].unique().tolist(), label="Region")
months_ctrl = ctrl.ComboBox(['Oct', 'Nov', 'Dec'], label="Month")
churn_ctrl = ctrl.CheckBox(label="Churn", selected=True, require_apply=False)


def app_handler(regions_ctrl: ctrl.ComboBox, months_ctrl: ctrl.ComboBox, churn_ctrl: ctrl.CheckBox):
    x1, x1a = get_data()
    y1_pred = get_model().predict(x1a)
    data = x1.copy()
    data["Predicted Churn"] = y1_pred
    data["Predicted Churn"] = data["Predicted Churn"].apply(lambda x: "Yes" if x == 1.0 else "No")
    data["RenewalMonth"] = data["RenewalMonth"].apply(lambda x: months[x - 1])
    data = data.drop(["y2015", "y2016", "y2017", "y2018", "y2019", "Churn"], axis=1)

    data = data[(data["Predicted Churn"] == ("Yes" if churn_ctrl.selected else "No"))]
    data = data[(data["Region"] == regions_ctrl.value())]
    data = data[(data["RenewalMonth"] == months_ctrl.value())]
    return data


app = ds.app(app_handler, regions_ctrl=regions_ctrl, months_ctrl=months_ctrl, churn_ctrl=churn_ctrl)

url = ds.push("simple_sklearn_ml_app", app)
print(url)
```

Now, if we run this code, and open the URL from the output, we'll see the following:

![](https://gblobscdn.gitbook.com/assets%2F-LyOZaAwuBdBTEPqqlZy%2F-MPsRNaSLV_cIawC-uG-%2F-MPs_V1bx18-fR9SDOm4%2FScreenshot%202020-12-31%20at%2012.36.11.png?alt=media&token=3035ec62-9e0a-41e9-b7b7-474915cec203)

Now, if you push another model, the application will immediately use the new version.
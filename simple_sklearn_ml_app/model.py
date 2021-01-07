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
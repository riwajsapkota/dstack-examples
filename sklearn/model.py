import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
import dstack as ds


class PrepareData(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def transform(self, X, **transform_params):
        X_copy = X.copy()

        def n_years(row):
            l = [row["y2019"], row["y2018"], row["y2017"], row["y2016"], row["y2015"]]
            return len([x for x in l if x != 0])

        X_copy["Years"] = X_copy.apply(n_years, axis=1)

        X_copy = X_copy.drop(["Company", "Region", "Manager", "RenewalMonth", "RenewalDate"], axis=1)

        for col in ["y2015", "y2016", "y2017", "y2018", "y2019"]:
            X_copy[col] = X_copy[col] / X_copy[col].max()

        for c in X["Country"].unique():
            X_copy[c] = X_copy["Country"].apply(lambda x: 1 if x == c else 0)

        for s in X["Sector"].unique():
            if s:
                X_copy[s] = X_copy["Sector"].apply(lambda x: 1 if x == s else 0)

        X_copy = X_copy.drop(["Country", "Sector"], axis=1)
        return X_copy

    def fit(self, X, y=None, **fit_params):
        return self


class ReindexColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def transform(self, X, **transform_params):
        return X.reindex(columns=self.columns, fill_value=0)

    def fit(self, X, y=None, **fit_params):
        return self


df = pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0).dropna()
X = df.drop(["Churn"], axis=1)
y = df["Churn"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=99)

X_train_columns = PrepareData().transform(X_train)

pipeline = Pipeline([
    ('prepare', PrepareData()),
    ('dummies', ReindexColumns(X_train_columns.columns)),
    ('lr', LogisticRegression())
])
pipeline.fit(X_train, y_train)

url = ds.push("tutorials/sklearn_model", pipeline)
print(url)

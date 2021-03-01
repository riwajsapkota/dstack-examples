#!/usr/bin/env python
# coding: utf-8

# # Simple Application with a Scikit-learn ML Model
# 
# One of the simplest yet typical problem that Machine Learning can help with in business is churn prediction. In this tutorial, we'll go through simple steps of solving this problem. We'll start with a problem definition, we'll do data exploratory analysis, prototype a model, and in the end, building an application that uses that model against the live data to help the sales department to plan their activities based on the predictions.
# 
# ### Disclaimers
# 
# Note, in this tutorial there a lot of things, that in a real case are quite complicated, are simplified for the education purposes. Here's what is important:
# 
# 1. In real life, data often resides in multiple data sources (including databases and datalakes) and needs additional cleanups and processing (often done using ETL solutions). In this tutorial, we'll use an already prepared dataset that emulates to a certain extent the data that is close to a real scenario.
# 2. When it comes to using ML model in a real situation, one of the most critical facts in the end is the acccuracy, reliability, and explainability of the model. In this tutorial, those questions will be only touched upon and will require from you additional dedicated work.
# 3. The target audience of this tutorials includes beginner data scientists that are only starting their data science careers interested in not just building an ML model but also putting it into production to drive day-to-day business decisions.
# 
# In this tutorial, we'll use `pandas` to work with data, `scikit-learn` to transform and train the model, and `dstack` to deploy the model and build the business application.
# 
# 
# ### Problem definition
# 
# 
# 
# ### Exploring data

# In[1]:


import pandas as pd


# In[213]:


df = pd.read_csv("https://www.dropbox.com/s/cat8vm6lchlu5tp/data.csv?dl=1", index_col=0)
df


# In[214]:


df.info()


# In[161]:


df.describe()


# In[163]:


train_df_1 = df[df["Churn"].notnull()]


# In[164]:


train_df_1.groupby(["Country"])["Churn"].mean().sort_values(ascending=False)


# In[165]:


train_df_1.groupby(["Country", "Sector"]).agg({'Company': 'size', 'Churn': 'mean'}).sort_values(ascending=False,
                                                                                                by='Churn')


# ### Feature engineering

# In[166]:


def n_years(row):
    l = [row["y2019"], row["y2018"], row["y2017"], row["y2016"], row["y2015"]]
    return len([x for x in l if x != 0])


train_df_2 = train_df_1.copy()
train_df_2["Years"] = train_df_2.apply(n_years, axis=1)
train_df_2


# In[167]:


train_df_2.groupby(["Years"])["Churn"].mean().sort_values(ascending=False)


# In[168]:


train_df_2.groupby(["Years", "Sector"]).agg({'Company': 'size', 'Churn': 'mean'}).sort_values(ascending=False,
                                                                                              by='Churn')


# In[169]:


train_df_2 = train_df_1.copy()
train_df_2 = train_df_2.drop(["Company", "Region", "Manager", "RenewalMonth", "RenewalDate"], axis=1)
train_df_2


# ### Data normalization

# In[170]:


train_df = train_df_2.copy()
for col in ["y2015", "y2016", "y2017", "y2018", "y2019"]:
    train_df[col] = train_df[col] / train_df[col].max()

for c in train_df_2["Country"].unique():
    train_df[c] = train_df["Country"].apply(lambda x: 1 if x == c else 0)

for s in train_df_2["Sector"].unique():
    if s:
        train_df[s] = train_df["Sector"].apply(lambda x: 1 if x == s else 0)

train_df = train_df.drop(["Country", "Sector"], axis=1)

train_df


# ### Training model

# In[198]:


from sklearn.model_selection import train_test_split


# In[199]:


X = train_df.drop(["Churn"], axis=1)
y = train_df["Churn"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=99)
X_train.info()


# In[200]:


from sklearn.linear_model import LogisticRegression


# In[202]:


model = LogisticRegression()
model.fit(X_train, y_train)
accuracy = model.score(X_test, y_test)
print(accuracy * 100, '%')
# summarize feature importance
for i, v in enumerate(model.coef_[0]):
    if v > 0.5:
        print('Feature: %0s, Score: %.5f' % (X_train.columns[i], v))


# ### Making the model re-usable

# In[203]:


live_df = df[df["Churn"].isnull()]
live_df = live_df.drop(["Churn"], axis=1)
live_df.info()


# In[204]:


from sklearn.base import BaseEstimator, TransformerMixin


# In[205]:


class PrepareData(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass

    def transform(self, X, **transform_params):
        X_prepared = X.copy()

        def n_years(row):
            l = [row["y2019"], row["y2018"], row["y2017"], row["y2016"], row["y2015"]]
            return len([x for x in l if x != 0])

        X_prepared["Years"] = X_prepared.apply(n_years, axis=1)

        X_prepared = X_prepared.drop(["Company", "Region", "Manager", "RenewalMonth", "RenewalDate"], axis=1)

        for col in ["y2015", "y2016", "y2017", "y2018", "y2019"]:
            X_prepared[col] = X_prepared[col] / X_prepared[col].max()

        for c in X["Country"].unique():
            X_prepared[c] = X_prepared["Country"].apply(lambda x: 1 if x == c else 0)

        for s in X["Sector"].unique():
            if s:
                X_prepared[s] = X_prepared["Sector"].apply(lambda x: 1 if x == s else 0)

        X_prepared = X_prepared.drop(["Country", "Sector"], axis=1)
        return X_prepared

    def fit(self, X, y=None, **fit_params):
        return self


# In[206]:


prepared_df = PrepareData().transform(live_df)
prepared_df.info()


# In[185]:


# predicted_churn = model.predict(prepared_df)  # ValueError: X has 70 features per sample; expecting 74


# In[207]:


class ReindexColumns(BaseEstimator, TransformerMixin):
    def __init__(self, columns):
        self.columns = columns

    def transform(self, X, **transform_params):
        return X.reindex(columns=self.columns, fill_value=0)

    def fit(self, X, y=None, **fit_params):
        return self


# In[208]:


reindexed_df = ReindexColumns(X.columns).transform(prepared_df)
reindexed_df.info()


# In[209]:


from scipy.stats import describe


# In[210]:


predicted_churn = model.predict(reindexed_df)
describe(predicted_churn)


# In[211]:


from sklearn.pipeline import Pipeline


# In[212]:


pipeline = Pipeline([
    ('prepare', PrepareData()),
    ('reindex', ReindexColumns(X.columns)),
    ('regression', LogisticRegression())
])
X_1 = df[df["Churn"].notnull()]
y_1 = X_1["Churn"]
X_1 = X_1.drop(["Churn"], axis=1)
pipeline.fit(X_1, y_1)
predicted_churn = pipeline.predict(live_df)
describe(predicted_churn)


# ### Intro to dstack
# 
# 
# ### Deploying the model to dstack

# ### Building the application

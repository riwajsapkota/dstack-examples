import dstack as ds
import seaborn as sns


def my_handler(self: ds.Output):
    tips = sns.load_dataset("tips")
    ax = sns.boxplot(x=tips["total_bill"])
    self.data = ax.figure


app = ds.app()

app.output(handler=my_handler)

url = app.deploy("seaborn")
print(url)

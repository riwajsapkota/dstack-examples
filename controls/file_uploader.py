import dstack as ds
import pandas as pd


def app_handler(self: ds.Output, uploader: ds.Uploader):
    if len(uploader.uploads) > 0:
        with uploader.uploads[0].open() as f:
            self.label = uploader.uploads[0].file_name
            self.data = pd.read_csv(f).head(100)
    else:
        self.label = "No file selected"
        self.data = None


app = ds.app()

controls = app.uploader(label="Select a CSV file")
outputs = app.output(handler=app_handler)

url = app.deploy("controls/file_uploader")
print(url)

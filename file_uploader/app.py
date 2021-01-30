import dstack as ds
import dstack.controls as ctrl
import pandas as pd


def app_handler(self: ctrl.Output, uploader: ctrl.FileUploader):
    if len(uploader.uploads) > 0:
        u = uploader.uploads[0]
        self.data = pd.read_csv(u.open()).head(100)
    else:
        self.data = ds.md("No file selected")


app = ds.app(controls=[ctrl.FileUploader(label="Select a CSV file")],
             outputs=[ctrl.Output(handler=app_handler)])

url = ds.push("file_uploader", app)
print(url)

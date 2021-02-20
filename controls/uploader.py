import dstack as ds
import pandas as pd

app = ds.app()  # create an instance of the application


# a handler that loads a dataframe from the content of the uploaded CSV file and passes it to the output
def app_handler(self, uploader):
    if len(uploader.uploads) > 0:
        with uploader.uploads[0].open() as f:
            self.label = uploader.uploads[0].file_name
            self.data = pd.read_csv(f).head(100)
    else:
        self.label = "No file selected"
        self.data = None


# a file uploader control
uploader = app.uploader(label="Select a CSV file")

# an output control that shows the content of the uploaded file
app.output(handler=app_handler, depends=[uploader])

# deploy the application with the name "controls/select" and print its URL
url = app.deploy("controls/file_uploader")
print(url)

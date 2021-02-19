import dstack as ds

app = ds.app()  # create an instance of the application


# a handler that updates the label of the checkbox based on wether it's selected or not
def checkbox_handler(self):
    if self.selected:
        self.label = "Selected"
    else:
        self.label = "Not selected"


# a checkbox control
name = app.checkbox(handler=checkbox_handler)

# deploy the application with the name "controls/checkbox" and print its URL
url = app.deploy("controls/checkbox")
print(url)

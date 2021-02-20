import dstack as ds

app = ds.app()  # create an instance of the application

# a markdown output
app.markdown(text="Hello, **World!**")

# deploy the application with the name "markdown" and print its URL
url = app.deploy("markdown")
print(url)

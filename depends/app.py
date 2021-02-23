import dstack as ds

from handlers import fake_handler

# create an instance of an application an pass over
# dependencies to local modules "handlers" and "utils" and third-party packages
app = ds.app(depends=["handlers", "utils"], requirements="requirements.txt")

# The line above is equal to the line below
# app = ds.app(depends=["numpy", "pandas", "faker==5.5.0", "handlers", "utils"])

# an output with a handler from one of the modules the application depends on
app.output(handler=fake_handler)

# deploy the application with the name "stocks" and print its URL
url = app.deploy("faker")
print(url)

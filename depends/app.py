import dstack as ds

from handlers import fake_handler

app = ds.app(depends=["handlers", "utils"], requirements="requirements.txt")

# An equal alternative to this is the following:
# app = ds.app(depends=["numpy", "pandas", "faker==5.5.0", "handlers", "utils"])

_ = app.output(handler=fake_handler)

url = app.deploy("depends")
print(url)

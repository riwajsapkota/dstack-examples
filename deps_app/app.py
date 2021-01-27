import dstack as ds
import dstack.controls as ctrl

from handlers import fake_handler

app = ds.app(outputs=[ctrl.Output(handler=fake_handler)], depends=["handlers", "utils"],
             requirements="requirements.txt")

# An equal alternative to this is the following:
# ds.app(outputs=[ctrl.Output(handler=fake_handler)], depends=["numpy", "pandas", "faker==5.5.0", "handlers", "utils"])

url = ds.push("deps_app", app)
print(url)

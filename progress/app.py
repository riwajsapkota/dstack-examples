from time import sleep
import dstack as ds


def markdown_handler(self: ds.Markdown):
    for _ in ds.trange(100):
        sleep(0.5)
    self.text = "Finished"


app = ds.app()

app.markdown(handler=markdown_handler)

result = app.deploy("tqdm")
print(result.url)

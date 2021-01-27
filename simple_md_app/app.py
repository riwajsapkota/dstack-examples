import dstack as ds


def handler():
    return ds.md("Hello, this is *Markdown*!")


app = ds.app(handler)

result = ds.push("simple_md_app", app)
print(result)

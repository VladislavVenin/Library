import os
import json

from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


def on_reload():
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("template.html")

    with open("meta_data.json", "r", encoding=("UTF-8")) as file:
        meta_data_json = file.read()

    meta_data = json.loads(meta_data_json)
    books_on_page = 10
    pages = list(chunked(meta_data, books_on_page))
    book_cols = 2

    for index, page in enumerate(pages, start=1):
        rendered_page = template.render(
            books=list(chunked(page, book_cols)),
            current_page=index,
            page_count=len(pages)
        )

        with open(f"pages/index{index}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    os.makedirs("pages", exist_ok=True)
    on_reload()

    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".", default_filename="pages/index1.html")


if __name__ == "__main__":
    main()

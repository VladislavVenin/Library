import os
import json
import argparse

from livereload import Server
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


def remove_old_htmls():
    for filename in os.listdir("./pages"):
        file_path = os.path.join("./pages", filename)
        extension = os.path.splitext(file_path)[1]
        if extension == ".html":
            os.remove(file_path)


def on_reload(meta_data_path, cards_count):
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html", "xml"])
    )

    template = env.get_template("template.html")

    with open(meta_data_path, "r", encoding=("UTF-8")) as file:
        meta_data_json = file.read()

    meta_data = json.loads(meta_data_json)
    cards_on_page = cards_count
    pages = list(chunked(meta_data, cards_on_page))
    cards_cols = 2

    remove_old_htmls()

    for index, page in enumerate(pages, start=1):
        rendered_page = template.render(
            books=list(chunked(page, cards_cols)),
            current_page=index,
            page_count=len(pages)
        )

        with open(f"pages/index{index}.html", "w", encoding="utf8") as file:
            file.write(rendered_page)


def reload_with_args():
    on_reload(args.path, args.cards)


def main():
    global args

    parser = argparse.ArgumentParser(
        description="Скрипт для рендера страниц по html шаблону и запуска сервера"
    )
    parser.add_argument(
        "-p", "--path",
        help="Путь к файлу с данными для карточек на сайте, по стандарту 'meta_data.json'",
        default="meta_data.json"
    )
    parser.add_argument(
        "-c", "--cards",
        type=int,
        help="Кол-во карточек на странице",
        default=10
    )
    args = parser.parse_args()

    os.makedirs("pages", exist_ok=True)

    reload_with_args()
    server = Server()
    server.watch("template.html", reload_with_args)
    server.watch(args.path, reload_with_args)
    server.serve(root=".", default_filename="pages/index1.html")


if __name__ == "__main__":
    main()

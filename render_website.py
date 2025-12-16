import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def on_reload():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    with open("meta_data.json", "r", encoding=("UTF-8")) as file:
        meta_data_json = file.read()

    meta_data = json.loads(meta_data_json)

    rendered_page = template.render(
        books=list(chunked(meta_data, 2))
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def main():
    on_reload()

    server = Server()
    server.watch('template.html', on_reload)
    server.serve(root='.')


if __name__ == '__main__':
    main()

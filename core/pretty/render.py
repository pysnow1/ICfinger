import os
from jinja2 import Environment, FileSystemLoader


def render_to_html(results):
    # 设置Jinja2环境
    env = Environment(loader=FileSystemLoader(r'D:\pythonProject\ICfinger\db\templates'))
    template = env.get_template('output.html')

    # 渲染HTML
    html_content = template.render(results=results)

    return html_content

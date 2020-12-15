from flask import render_template

def render_page(name, title, **context):
  return render_template(
    "page.html",
    title=title,
    content=render_template(name, **context)
  )
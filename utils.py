from flask import render_template

def render_page(name, title, authenticated=False, **context):
  return render_template(
    "page.html",
    title=title,
    content=render_template(name, **context),
    authenticated=authenticated
  )
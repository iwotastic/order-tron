from flask import render_template
from datetime import datetime, timezone
import json
import html

def render_page(name, title, authenticated=False, **context):
  return render_template(
    "page.html",
    title=title,
    content=render_template(name, **context),
    authenticated=authenticated
  )

class MetaStr:
  """Wraps strings with optional metadata, which allows html_str to make nice
  user-facing output.
  """

  def __init__(self, string, meta_repr=None):
    self.string = string
    self.meta_repr = meta_repr

  def __str__(self):
    return self.string

  def json_repr(self):
    return self.meta_repr

def tsz_to_date(tsz):
  if isinstance(tsz, int):
    date = datetime.fromtimestamp(tsz, timezone.utc)
    
    return date

def tsz_to_meta_str(tsz, action=None):
  if isinstance(tsz, int):
    date = datetime.fromtimestamp(tsz, timezone.utc)
    date_meta_str = MetaStr(
      date.strftime("%x %I:%M %p"),
      date.isoformat()
    )
    return date_meta_str
  else:
    if action == None:
      return MetaStr("No Date", None)
    else:
      return MetaStr("Not " + action, None)

def html_str(value):
  if isinstance(value, bool):
    return "Yes" if value else "No"
  elif isinstance(value, str):
    return html.escape(value)
  elif isinstance(value, int):
    return str(value)
  elif isinstance(value, float):
    return str(value)
  elif value == None:
    return "&nbsp;"
  else:
    return str(value)
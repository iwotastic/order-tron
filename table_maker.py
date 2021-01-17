import json
from utils import html_str, MetaStr
from session_manager import sessions
from flask import abort, Blueprint, make_response, request

class TableMaker:
  def __init__(self, headings, create_func):
    self.create_func = create_func
    self.headings = headings
    self.session = None

  @staticmethod
  def create(headings):
    def wrapper(func):
      return TableMaker(headings, func)

    return wrapper

  def get_page_data(self, session, page):
    data = []
    def add_row(*col_data):        
      data.append(col_data)

    self.create_func(add_row, session, page)
    return data

  def html(self, session, keys=[], page=0):
    result = "<table><thead><tr>"
    
    indicies_to_render = []
    for index, data in enumerate(self.headings):
      heading, key = data
      if len(keys) == 0 or key in keys:
        indicies_to_render.append(index)
        result += "<th>" + html_str(heading) + "</th>"

    result += "</tr></thead><tbody>"

    for row in self.get_page_data(session, page):
      result += "<tr>"

      for col_index in indicies_to_render:
        result += "<td>" + html_str(row[col_index]) + "</td>"

    result += "</tbody></table>"
    return result

  def json(self, session, keys=[], page=0):
    result = {"headings": [], "data": []}

    indicies_to_render = []
    for index, data in enumerate(self.headings):
      heading, key = data
      if len(keys) == 0 or key in keys:
        indicies_to_render.append(index)
        result["headings"].append([heading, key])

    for row in self.get_page_data(session, page):
      result["data"].append([row[index] for index in indicies_to_render])

    def default(obj):
      if isinstance(obj, MetaStr):
        return obj.json_repr()

    return json.dumps(result, default=default)

  def csv(self, session, keys=[], page=0):
    result = ""
    
    indicies_to_render = []
    for index, data in enumerate(self.headings):
      heading, key = data
      if len(keys) == 0 or key in keys:
        indicies_to_render.append(index)
        result += key + ","

    for row in self.get_page_data(session, page):
      result += "\r\n"

      for col_index in indicies_to_render:
        result += (str(row[col_index].json_repr()) if isinstance(row[col_index], MetaStr) else str(row[col_index])) + ","

    return result

  def bp(self, bpname):
    bp = Blueprint(bpname, __name__, url_prefix="/" + bpname)

    @bp.route("/html/<keys>/get")
    def get_html(keys):
      session_id = request.cookies["session_id"]
      if session_id in sessions:
        page = int(request.args["page"]) if "page" in request.args else 0
        return self.html(sessions[session_id], keys.split("+") if keys != "_" else [], page)
      else:
        abort(401)

    @bp.route("/json/<keys>/data.json")
    def get_json(keys):
      session_id = request.cookies["session_id"]
      if session_id in sessions:
        page = int(request.args["page"]) if "page" in request.args else 0
        return self.json(sessions[session_id], keys.split("+") if keys != "_" else [], page)
      else:
        abort(401)

    @bp.route("/csv/<keys>/data")
    def get_csv(keys):
      session_id = request.cookies["session_id"]
      if session_id in sessions:
        page = int(request.args["page"]) if "page" in request.args else 0
        resp = make_response(self.csv(sessions[session_id], keys.split("+") if keys != "_" else [], page))
        resp.headers["Content-Type"] = "application/octet-stream"
        resp.headers["Content-Disposition"] = f"attachment; filename=\"{bpname}_page_{page}.csv\""
        return resp
      else:
        abort(401)

    return bp

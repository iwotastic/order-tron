from flask import abort, Blueprint, g, redirect, request, url_for
from session_manager import sessions
from utils import render_page

bp = Blueprint("authenticated", __name__, url_prefix="/app")

@bp.before_request
def before_request():
  session_id = request.cookies["session_id"]
  if session_id in sessions:
    g.session = sessions[session_id]
  else:
    g.session = None

class SessionRequiredException(Exception):
  pass

def require_session():
  if not g.session:
    raise SessionRequiredException()

  return g.session

@bp.errorhandler(SessionRequiredException)
def no_session(err):
  return render_page(
    "no_session.html", "Order-tron - Authentication Required"
  )

@bp.route("/")
def home():
  session = require_session()
  return render_page(
    "user_home.html", "Order-tron - Home",
    authenticated=True,
    user_data=session.user_profile()
  )

@bp.route("/log-out")
def log_out():
  session = require_session()
  sessions.delete(session)
  return redirect(url_for("index"))
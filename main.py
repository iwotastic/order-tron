from flask import abort, Flask, make_response, render_template, request, url_for
from session_manager import sessions
from utils import render_page
import authenticated

app = Flask(__name__)

@app.route("/")
def index():
  return render_page("index.html", "Order-tron")

@app.route("/get-started")
def get_started():
  new_session = sessions.create()
  resp = make_response(
    render_page(
      "get_started.html",
      "Get Started With Order-tron",
      login_url=new_session.get_login_url()
    )
  )
  resp.set_cookie("session_id", str(new_session.id))
  return resp

@app.route("/callback")
def callback():
  session_id = request.cookies["session_id"]
  if session_id not in sessions:
    abort(400)

  sessions[session_id].finish_authorization(
    request.args["oauth_token"],
    request.args["oauth_verifier"]
  )

  return render_template("callback_redirect.html", redir_url=url_for("authenticated.home"))

app.register_blueprint(authenticated.bp)

if __name__ == "__main__":
  app.run()
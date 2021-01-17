from flask import abort, Flask, make_response, render_template, request, redirect, url_for
from session_manager import sessions
from utils import render_page
import authenticated
import tables

app = Flask(__name__)

@app.route("/")
def index():
  return render_page("index.html", "Order-tron")

@app.route("/get-started")
def get_started():
  """This route prepares a new OAuth session with Etsy, this is basically the
  closest thing to a log-in screen Order-tron has.
  """
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
  """This route is the OAuth callback, it finalizes the "link" with the new
  user. It then redirects to the authenticated user homepage.
  """
  session_id = request.cookies["session_id"]
  if session_id not in sessions:
    abort(400)

  sessions[session_id].finish_authorization(
    request.args["oauth_token"],
    request.args["oauth_verifier"]
  )

  return redirect(url_for("authenticated.home"))

app.register_blueprint(authenticated.bp)
app.register_blueprint(tables.order_overview.bp("order_overview"))

if __name__ == "__main__":
  app.run(debug=True)
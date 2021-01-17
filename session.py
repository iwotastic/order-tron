from requests_oauthlib import OAuth1Session
from config import config
import urllib.parse
from uuid import uuid4

callback_uri = "http://127.0.0.1:5000/callback"
scopes = ["email_r", "transactions_r"]

scopes_str = urllib.parse.quote(" ".join(scopes))

class Session:
  def __init__(self):
    self._oauth_session = OAuth1Session(
      config["api_key"],
      client_secret=config["api_secret"],
      callback_uri=callback_uri
    )
    self._login_url = None
    self._user_secret = None
    self._user_data = None

    self.authorized = False
    self.id = uuid4()
  
  def get_login_url(self):
    if self._login_url == None:
      request_token = self._oauth_session.fetch_request_token(
        f"https://openapi.etsy.com/v2/oauth/request_token?scope={scopes_str}"
      )
      self._user_secret = request_token["oauth_token_secret"]
      self._login_url = request_token["login_url"]

    return self._login_url

  def finish_authorization(self, user_token, verifier):
    self._oauth_session = OAuth1Session(
      config["api_key"],
      client_secret=config["api_secret"],
      resource_owner_key=user_token,
      resource_owner_secret=self._user_secret,
      verifier=verifier
    )
    self._oauth_session.fetch_access_token(
      "https://openapi.etsy.com/v2/oauth/access_token"
    )
    self.authorized = True

  def user_profile(self):
    if self._user_data == None:
      resp = self._oauth_session.get(
        "https://openapi.etsy.com/v2/users/__SELF__/profile"
      )
      self._user_data = resp.json()["results"][0]

    return self._user_data

  def transactions(self, page=0):
    return self._oauth_session.get(
      f"https://openapi.etsy.com/v2/shops/__SELF__/transactions?limit=40&offset={page * 40}"
    ).json()["results"]

  def receipts(self, page=0):
    return self._oauth_session.get(
      f"https://openapi.etsy.com/v2/shops/__SELF__/receipts?limit=40&offset={page * 40}"
    ).json()["results"]
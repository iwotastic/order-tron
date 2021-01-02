from requests.sessions import session
from session import Session
from uuid import UUID

class SessionManager:
  def __init__(self):
    self._sessions = {}

  def create(self):
    new_session = Session()
    self._sessions[new_session.id] = new_session
    return new_session

  def delete(self, session):
    del self._sessions[session.id]

  def __getitem__(self, session_id):
    return self._sessions[UUID(session_id)]

  def __contains__(self, session_id):
    return UUID(session_id) in self._sessions.keys()

sessions = SessionManager()
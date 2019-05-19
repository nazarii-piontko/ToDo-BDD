from typing import Dict, NoReturn, Union, Iterable

from infrastructure.errors import TestError
from infrastructure.session import Session


class Sessions:
    """
    Browser sessions
    """
    def __init__(self):
        """
        Constructor.
        """
        self._sessions: Dict[str, Session] = {}
        self._active_session: Union[Session, None] = None

    def add(self, session: Session) -> NoReturn:
        """
        Add session to registry.
        :param session: Session to add.
        """
        session_name = session.get_name()

        if session_name in self._sessions:
            raise TestError('Session with name "{}" already exists'.format(session_name))

        self._sessions[session_name] = session

        if self._active_session is None:
            self._active_session = session

    def remove(self, session: Session) -> NoReturn:
        """
        Remove session from registry.
        :param session: Session to remove.
        """
        self.remove_by_name(session.get_name())

    def remove_by_name(self, session_name: str) -> NoReturn:
        """
        Remove session from registry by name.
        :param session_name: Session name.
        """
        if session_name not in self._sessions:
            return

        session = self._sessions[session_name]

        del self._sessions[session_name]

        if self._active_session == session:
            if len(self._sessions) > 0:
                self._active_session = self._sessions[next(iter(self._sessions.keys()))]
            else:
                self._active_session = None

    def clear(self) -> NoReturn:
        """
        Remove all sessions
        :return:
        """
        self._sessions.clear()
        self._active_session = None

    def set_active_session(self, session: Session) -> NoReturn:
        """
        Set active session.
        :param session: Session.
        """
        self.set_active_session_by_name(session.get_name())

    def set_active_session_by_name(self, session_name: str) -> NoReturn:
        """
        Set active session by name.
        :param session_name: Session name.
        """
        if session_name not in self._sessions:
            raise TestError('Unknown session with name "{}"'.format(session_name))

        self._active_session = self._sessions[session_name]

    def exists(self, session_name: str) -> bool:
        """
        Check if session with name exists.
        :param session_name: Session name.
        :return: True - exists, False - missing
        """
        return session_name in self._sessions

    def get_session(self, session_name: str = None) -> Session:
        """
        Get session with name or default session.
        :param session_name: Session name.
        :return: Session.
        """
        if session_name is None:
            if self._active_session is None:
                raise TestError('There is no active sessions')
            return self._active_session

        if session_name not in self._sessions:
            raise TestError('Unknown session with name "{}"'.format(session_name))

        return self._sessions[session_name]

    def get_sessions(self) -> Iterable[Session]:
        """
        Get all sessions
        :return: Sessions
        """
        return self._sessions.values()

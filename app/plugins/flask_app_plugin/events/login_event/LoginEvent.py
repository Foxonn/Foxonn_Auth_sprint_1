from app.utils.message_bus import EventModel

__all__ = ['LoginEvent']


class LoginEvent(EventModel):
    login: str
    password: str
    fingerprint: bytes

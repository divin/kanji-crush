import reflex as rx


class User(rx.State):
    user_name: str = ""
    level: int = 0
    max_level: int = 0
    is_subscribed: bool = False

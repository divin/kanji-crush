import reflex as rx


class Settings(rx.State):
    min_level: int = 1
    max_level: int = 20
    is_random: bool = True
    is_open: bool = False

    @rx.event
    def set_level(self, value: list[int]) -> None:
        self.min_level = value[0]
        self.max_level = value[1]

    @rx.event
    def toggle_drawer(self):
        self.is_open = not self.is_open

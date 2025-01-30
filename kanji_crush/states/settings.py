import os

import reflex as rx


class Settings(rx.State):
    min_level: int = 1
    max_level: int = 20
    is_random: bool = True
    is_open: bool = True
    api_token: str = ""
    is_not_valid: bool = True

    @rx.event
    def set_level(self, value: list[int]) -> None:
        self.min_level = value[0]
        self.max_level = value[1]

    @rx.event
    def toggle_drawer(self):
        self.is_open = not self.is_open

    @rx.event
    async def validate_api_token(self):
        from kanji_crush.states.game import Game
        from kanji_crush.states.user import User
        from kanji_crush.states.wanikani import Wanikani

        game = await self.get_state(Game)

        if self.api_token == "":
            await game.reset_game()
            self.is_not_valid = True
            yield rx.toast.error(
                "Please provide a WaniKani API token 🙅",
                duration=5000,
                position="bottom-right",
            )
            return

        user = await self.get_state(User)
        wanikani = await self.get_state(Wanikani)

        if not os.path.exists("assets/kanjis.json"):
            api_token = os.environ.get("WANIKANI_API_TOKEN", None)

            if api_token is None:
                raise ValueError("Please provide a WaniKani API token.")

            wanikani.get_similar_looking_kanjis(api_token=api_token)

        await wanikani.set_user_details(api_token=self.api_token)

        if not user.is_subscribed:
            self.is_not_valid = True
            yield rx.toast.error("Please subscribe to WaniKani first 🙇", duration=5000)
            return

        yield rx.toast.success("API token is valid 👌", duration=5000)

        self.min_level = 1
        self.max_level = user.level
        self.is_not_valid = False

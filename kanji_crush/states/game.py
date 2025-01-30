import numpy as np
import reflex as rx

from .kanjis import Kanjis
from .settings import Settings
from .statistics import Statistics


class Game(rx.State):
    score: int = 0
    is_started: bool = False
    is_finished: bool = False

    current_index: int = 0
    number_of_kanjis: int = 0

    current_kanji: str = ""
    current_meanings: str = ""
    current_kanji_level: int = 0
    current_options: list[str] = []
    current_selection: list[dict[str, int | list[str | int]]] = []

    @rx.event
    async def reset_game(self) -> None:
        self.current_index = 0
        self.number_of_kanjis = 0
        self.is_started = False
        self.is_finished = False
        self.current_kanji = ""
        self.current_meanings = ""
        self.current_options = []
        self.current_selection = []

    @rx.event
    async def start_game(self) -> None:
        kanjis = await self.get_state(Kanjis)
        statistics = await self.get_state(Statistics)
        settings = await self.get_state(Settings)

        if settings.is_not_valid:
            yield rx.toast.error("Please provide a valid API token 🙅", duration=5000)
            return

        # Reset game
        self.current_index = 0
        self.number_of_kanjis = 0
        self.is_started = False
        self.is_finished = False
        self.current_kanji = ""
        self.current_meanings = ""
        self.current_options = []
        self.current_selection = []
        statistics.reset_statistics()

        # Start game
        self.current_selection = await kanjis.get_selection()

        statistics.number_of_kanjis_left = len(self.current_selection)
        statistics.number_of_total_kanjis = len(self.current_selection)

        self.number_of_kanjis = len(self.current_selection)
        self.next_kanji()
        self.is_started = True

    @rx.event
    async def restart_with_failed(self) -> None:
        kanjis = await self.get_state(Kanjis)
        statistics = await self.get_state(Statistics)

        # Restart game
        self.current_selection = await kanjis.get_failed_selection()

        if self.current_selection == []:
            self.is_started = False
            self.is_finished = True
            yield rx.toast.info("No failed kanjis found! 🎉", duration=3000)
            return

        # Reset game
        self.current_index = 0
        self.number_of_kanjis = 0
        self.is_started = False
        self.is_finished = False
        self.current_kanji = ""
        self.current_meanings = ""
        self.current_options = []

        # Reset statistics
        statistics.reset_statistics()

        statistics.number_of_kanjis_left = len(self.current_selection)
        statistics.number_of_total_kanjis = len(self.current_selection)

        self.number_of_kanjis = len(self.current_selection)
        self.next_kanji()
        self.is_started = True

    def next_kanji(self) -> None:
        self.current_kanji = self.current_selection[self.current_index]["kanji"]
        self.current_meanings = ", ".join(
            self.current_selection[self.current_index]["meanings"]
        )
        self.current_kanji_level = self.current_selection[self.current_index]["level"]
        self.current_options = self.current_selection[self.current_index][
            "visually_similar_kanjis"
        ] + [self.current_kanji]
        np.random.shuffle(self.current_options)

    @rx.event
    async def check_answer(self, selected_kanji: str, duration: int = 1000) -> None:
        statistics = await self.get_state(Statistics)
        statistics.set_kanji(
            kanji=self.current_kanji,
            level=self.current_kanji_level,
            meanings=self.current_meanings,
            is_identified=selected_kanji == self.current_kanji,
        )

        if selected_kanji == self.current_kanji:
            if self.current_index == self.number_of_kanjis - 1:
                self.is_started = False
                self.is_finished = True
                self.current_index = self.number_of_kanjis
                yield rx.toast.success("Game finished! 🎉", duration=duration)
            else:
                self.current_index += 1
                self.next_kanji()
                yield rx.toast.success("Correct! 👍", duration=duration)
        else:
            yield rx.toast.error("Incorrect! 👎", duration=duration)

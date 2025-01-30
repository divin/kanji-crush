import os

import pandas as pd
import reflex as rx


class Kanjis(rx.State):
    kanjis: pd.DataFrame | None = None

    async def get_selection(self) -> list[dict[str, int | list[str | int]]]:
        from kanji_crush.states.settings import Settings
        from kanji_crush.states.wanikani import Wanikani

        settings = await self.get_state(Settings)
        wanikani = await self.get_state(Wanikani)

        if self.kanjis is None and os.path.exists("assets/kanjis.json"):
            self.kanjis = pd.read_json("assets/kanjis.json")
        else:
            api_token = os.environ.get("WANIKANI_API_TOKEN", None)

            if api_token is None:
                raise ValueError("Please provide a WaniKani API token.")

            wanikani.get_similar_looking_kanjis(api_token=api_token)

        # Select levels
        is_level = (settings.min_level <= self.kanjis.level) & (
            self.kanjis.level <= settings.max_level
        )

        # Select only kanjis which have similar looking kanjis
        has_similar_looking_kanjis = self.kanjis.visually_similar_kanjis.notnull()

        # Get selection
        selection = self.kanjis.loc[is_level & has_similar_looking_kanjis, :]

        # Randomize selection
        if settings.is_random:
            selection = selection.sample(frac=1, ignore_index=True)

        return selection.to_dict(orient="records")

    async def get_failed_selection(self) -> list[dict[str, int | list[str | int]]]:
        from kanji_crush.states.settings import Settings
        from kanji_crush.states.statistics import Statistics

        settings = await self.get_state(Settings)
        statistics = await self.get_state(Statistics)

        # Get failed kanjis
        failed_kanjis = [
            key
            for key, values in statistics.kanjis.items()
            if values["number_of_tries"] > 0
        ]

        if failed_kanjis == []:
            return []

        # Select levels
        is_level = (settings.min_level <= self.kanjis.level) & (
            self.kanjis.level <= settings.max_level
        )

        # Select only kanjis which have similar looking kanjis
        has_similar_looking_kanjis = self.kanjis.visually_similar_kanjis.notnull()

        # Select only failed kanjis
        is_failed = self.kanjis.kanji.isin(failed_kanjis)

        # Get selection
        selection = self.kanjis.loc[
            is_level & has_similar_looking_kanjis & is_failed, :
        ]

        # Randomize selection
        if settings.is_random:
            selection = selection.sample(frac=1, ignore_index=True)

        return selection.to_dict(orient="records")

import io

import pandas as pd
import reflex as rx


class Statistics(rx.State):
    """
    Statistics about the current game.
    """

    number_of_kanjis_left: int = 0
    number_of_total_kanjis: int = 0

    kanjis: dict[str, dict[str, str | int]] = {}

    def reset_statistics(self) -> None:
        self.kanjis = {}
        self.number_of_kanjis_left = 0
        self.number_of_total_kanjis = 0

    @rx.var(cache=False)
    def current_accuracy(self) -> int:
        return (
            int(
                100
                * self.number_of_correct_answers
                / (self.number_of_total_kanjis - self.number_of_kanjis_left)
            )
            if (self.number_of_total_kanjis - self.number_of_kanjis_left) > 0
            else 100
        )

    @rx.var(cache=False)
    def kanjis_data(self) -> pd.DataFrame:
        if self.kanjis == {}:
            return pd.DataFrame()

        kanjis_data = pd.DataFrame(self.kanjis).T.reset_index()
        kanjis_data = kanjis_data.rename(
            columns={
                "index": "Kanji",
                "number_of_tries": "Number of Tries",
                "level": "Level",
                "meanings": "Meanings",
            }
        )
        kanjis_data = kanjis_data.drop(columns=["is_identified"], errors="ignore")
        return kanjis_data

    @rx.event
    def download_kanjis_csv(self) -> None:
        # file_name = "kanjis.csv"
        # self.kanjis_data.to_csv(file_name, index=False, sep=";")
        buffer = io.StringIO()
        self.kanjis_data.to_csv(buffer, index=False, sep=";")
        csv_string = buffer.getvalue()
        buffer.close()
        return rx.download(data=csv_string, filename="kanjis.csv")

    def set_kanji(
        self, kanji: str, level: int, meanings: list[str], is_identified: bool
    ) -> None:
        if is_identified:
            if kanji not in self.kanjis:
                self.kanjis[kanji] = {
                    "is_identified": True,
                    "number_of_tries": 0,
                    "level": level,
                    "meanings": meanings,
                }
                self.number_of_kanjis_left -= 1
            else:
                self.kanjis[kanji]["is_identified"] = True
                self.number_of_kanjis_left -= 1
        else:
            if kanji not in self.kanjis:
                self.kanjis[kanji] = {
                    "is_identified": False,
                    "number_of_tries": 1,
                    "level": level,
                    "meanings": meanings,
                }
            else:
                self.kanjis[kanji]["number_of_tries"] += 1

    @rx.var(cache=False)
    def number_of_incorrect_answers(self) -> int:
        return sum(
            [
                values["is_identified"] and values["number_of_tries"] > 0
                for values in self.kanjis.values()
            ]
        )

    @rx.var(cache=False)
    def number_of_correct_answers(self) -> int:
        return sum(
            [
                values["is_identified"] and values["number_of_tries"] == 0
                for values in self.kanjis.values()
            ]
        )

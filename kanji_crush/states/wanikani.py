import numpy as np
import pandas as pd
import reflex as rx
import requests


class Wanikani(rx.State):
    def get_headers(self, api_token: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {api_token}",
            "Wanikani-Revision": "20170710",
        }

    async def set_user_details(self, api_token: str) -> None:
        from kanji_crush.states.user import User

        user = await self.get_state(User)
        headers = self.get_headers(api_token=api_token)

        url = "https://api.wanikani.com/v2/user"
        response = requests.get(url, headers=headers).json()

        user.set_user_name(response["data"]["username"])
        user.set_level(response["data"]["level"])
        user.set_max_level(response["data"]["subscription"]["max_level_granted"])
        user.set_is_subscribed(response["data"]["subscription"]["active"])

    def get_similar_looking_kanjis(self, api_token: str) -> None:
        headers = self.get_headers(api_token=api_token)

        kanjis = {}
        next_url = "https://api.wanikani.com/v2/subjects"
        while next_url:
            response = requests.get(next_url, headers=headers).json()
            for subject in response["data"]:
                if subject["object"] == "kanji":
                    id = subject["id"]
                    kanji = {
                        "level": subject["data"]["level"],
                        "slug": subject["data"]["slug"],
                        "visually_similar_subject_ids": subject["data"][
                            "visually_similar_subject_ids"
                        ],
                        "meanings": [
                            meaning["meaning"]
                            for meaning in subject["data"]["meanings"]
                        ],
                    }
                    kanjis[id] = kanji

            next_url = response["pages"].get("next_url")

        for id in kanjis.keys():
            visually_similar_subject_ids = kanjis[id]["visually_similar_subject_ids"]

            if visually_similar_subject_ids == []:
                continue

            visually_similar_kanjis = []
            for visually_similar_subject_id in visually_similar_subject_ids:
                kanji = kanjis[visually_similar_subject_id]["slug"]
                visually_similar_kanjis.append(kanji)

            kanjis[id]["visually_similar_kanjis"] = visually_similar_kanjis

        df = pd.DataFrame(kanjis).T.reset_index()
        df.columns = [
            "subject_id",
            "level",
            "kanji",
            "visually_similar_subject_ids",
            "meanings",
            "visually_similar_kanjis",
        ]
        df.loc[:, "visually_similar_subject_ids"] = (
            df.visually_similar_subject_ids.apply(lambda x: x if x != [] else np.nan)
        )
        df.loc[:, "visually_similar_kanjis"] = df.visually_similar_kanjis.apply(
            lambda x: x if x != [] else np.nan
        )
        df.to_json("assets/kanjis.json", index=False)

import numpy as np
import pandas as pd
import requests


def read_markdown_file(file: str) -> str:
    """Read a markdown file and return its content.

    Args:
        file (str): The path to the markdown file.

    Returns:
        str: The content of the markdown file.
    """
    with open(file=file, mode="r") as markdown_file:
        return markdown_file.read()


def get_similar_looking_kanjis(api_token: str) -> None:
    headers = {"Authorization": f"Bearer {api_token}", "Wanikani-Revision": "20170710"}

    kanjis = {}
    next_url = "https://api.wanikani.com/v2/subjects"
    while next_url:
        response = requests.get(next_url, headers=headers).json()
        for subject in response["data"]:
            if subject["object"] == "kanji":
                # print(subject)
                id = subject["id"]
                kanji = {
                    "level": subject["data"]["level"],
                    "slug": subject["data"]["slug"],
                    "visually_similar_subject_ids": subject["data"][
                        "visually_similar_subject_ids"
                    ],
                    "meanings": [
                        meaning["meaning"] for meaning in subject["data"]["meanings"]
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
    df.loc[:, "visually_similar_subject_ids"] = df.visually_similar_subject_ids.apply(
        lambda x: x if x != [] else np.nan
    )
    df.loc[:, "visually_similar_kanjis"] = df.visually_similar_kanjis.apply(
        lambda x: x if x != [] else np.nan
    )
    df.to_json("assets/kanjis.json", index=False)

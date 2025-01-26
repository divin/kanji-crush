from typing import Any

import reflex as rx


def get_description(**props: dict[str, Any]) -> rx.Component:
    return rx.text(
        "Master similar-looking kanji characters through this engaging practice game.",
        font_size="1em",
        padding="0.25em",
        text_align="center",
        **props,
    )

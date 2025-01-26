from typing import Any

import reflex as rx

from kanji_crush.components import get_footer


def body(components: list[rx.Component], **props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        *components,
        direction="column",
        justify_content="flex-start",
        # align_items="center",
        max_width="100svw",
        min_height="100svh",
        **props,
    )


def main(components: list[rx.Component], **props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        *components,
        gap="1.0rem",
        direction="column",
        justify_content="center",
        align_items="center",
        width="100%",
        height="100%",
        max_width="1280px",
        **props,
    )


def header(title: str, **props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.heading(title, size="8"),
        # rx.color_mode.button(position="top-right"),
        direction="row",
        justify_content="left",
        align_items="left",
        gap="1.0em",
        **props,
    )


def default_layout(title: str, components: list[rx.Component]) -> rx.Component:
    return body(
        [
            main(
                [
                    header(title=title),
                    *components,
                    get_footer(),
                ]
            )
        ]
    )

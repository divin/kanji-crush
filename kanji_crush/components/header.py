from typing import Any

import reflex as rx

from kanji_crush.states import Game, Settings


def _get_level_selection(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.text(
            f"Kanjis from Wanikani level {Settings.min_level} to {Settings.max_level}",
            font_size="1em",
        ),
        rx.slider(
            default_value=[Settings.min_level, Settings.max_level],
            min=1,
            max=60,
            size="3",
            step=1,
            on_change=Settings.set_level,
        ),
        direction="column",
        gap="0.5em",
        width="100%",
        **props,
    )


def _get_random(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.text("Shuffle Kanjis", font_size="1em"),
        rx.switch(checked=Settings.is_random, on_change=Settings.set_is_random),
        direction="row",
        align="center",
        justify="between",
        gap="1em",
        width="100%",
        **props,
    )


def _get_support_link(text: str, href: str, **props: dict[str, Any]) -> rx.Component:
    return rx.link(
        rx.button(
            text,
            font_size="1em",
            padding="0.5em",
            width="100%",
            height="100%",
            weight="bold",
            text_align="center",
        ),
        href=href,
        is_external=True,
        # background_color="#2e6960",
        # border_radius="0.5em",
        **props,
    )


def _get_support_links(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        _get_support_link(
            "Support on Ko-fi ❤️",
            "https://ko-fi.com/divin",
            flex="1 1 50%",
        ),
        _get_support_link(
            "Support on GitHub ❤️",
            "https://github.com/sponsors/divin",
            flex="1 1 50%",
        ),
        direction="row",
        gap="1em",
        width="100%",
        **props,
    )


def _get_reset_button(**props: dict[str, Any]) -> rx.Component:
    return rx.button(
        rx.html('<i class="fas fa-power-off"></i>'),
        "Reset",
        on_click=Game.reset_game,
        font_size="1em",
        width="100%",
        **props,
    )


def get_menu(**props: dict[str, Any]) -> rx.Component:
    return rx.drawer.root(
        rx.drawer.trigger(
            rx.button(
                rx.html('<i class="fas fa-bars"></i>'),
                width="100%",
                height="100%",
                padding="0.5em",
                font_size="1.5em",
                flex="1 0 20%",
                variant="ghost",
                color="#eeeeee",
                on_click=Settings.toggle_drawer,
                # _hover={"background_color": "white"},
            )
        ),
        rx.drawer.overlay(z_index="5"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.flex(
                    _get_level_selection(),
                    _get_random(),
                    _get_reset_button(),
                    rx.text("Support this App", font_size="1em"),
                    _get_support_links(),
                    rx.drawer.close(
                        rx.button(
                            "Close",
                            on_click=Settings.toggle_drawer,
                            flex="0 1 10%",
                            width="100%",
                        )
                    ),
                    align_items="start",
                    gap="1em",
                    padding="0.5em",
                    direction="column",
                    width="100%",
                ),
                height="100%",
                width="70%",
                max_width="256px",
                padding="1em",
                background_color="#232a26",
            ),
        ),
        open=Settings.is_open,
        direction="left",
        dismissible=False,
    )


def get_header(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.link(
            rx.heading("Kanji Crush", size="8", text_align="left"),
            href="/",
            flex="1 1 80%",
            _hover={"text_decoration": "none"},
        ),
        get_menu(),
        padding="0.5em",
        align="center",
        **props,
    )


def get_header_without_menu(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.link(
            rx.heading("Kanji Crush", size="8", text_align="left"),
            href="/",
            flex="1 1 100%",
            _hover={"text_decoration": "none"},
        ),
        padding="0.5em",
        align="center",
        **props,
    )

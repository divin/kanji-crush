from typing import Any

import reflex as rx

from kanji_crush.states.game import Game
from kanji_crush.states.settings import Settings
from kanji_crush.states.user import User


def _get_api_token_input(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.text("1) WaniKani API token", font_size="1em"),
        rx.input(
            placeholder="WaniKani API token",
            value=Settings.api_token,
            on_change=Settings.set_api_token,
            type="password",
            auto_focus=True,
        ),
        rx.button(
            "Validate",
            on_click=Settings.validate_api_token,
            font_size="1em",
            width="100%",
        ),
        direction="column",
        gap="0.5em",
        width="100%",
        **props,
    )


def _get_level_selection(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.text(
            f"2) Kanjis from WaniKani level {Settings.min_level} to {Settings.max_level}",
            font_size="1em",
        ),
        rx.slider(
            default_value=[Settings.min_level, Settings.max_level],
            min=1,
            max=User.max_level,
            size="1",
            step=1,
            on_change=Settings.set_level,
            disabled=Settings.is_not_valid,
            # width="90%",
        ),
        direction="column",
        gap="1em",
        width="100%",
        **props,
    )


def _get_random(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.text("3) Shuffle Kanjis", font_size="1em"),
        rx.switch(
            checked=Settings.is_random,
            on_change=Settings.set_is_random,
            disabled=Settings.is_not_valid,
        ),
        direction="row",
        align="center",
        justify="between",
        gap="1em",
        width="100%",
        **props,
    )


def _get_reset_button(**props: dict[str, Any]) -> rx.Component:
    return rx.button(
        rx.html('<i class="fas fa-save"></i>'),
        "Save",
        on_click=Game.reset_game,
        font_size="1em",
        width="100%",
        disabled=Settings.is_not_valid,
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
            )
        ),
        rx.drawer.overlay(z_index="5"),
        rx.drawer.portal(
            rx.drawer.content(
                rx.flex(
                    rx.text("Settings", font_size="1.5em", weight="bold"),
                    rx.text(
                        "To use this app, you need to provide a WaniKani API token. See the reason and details ",
                        rx.link(
                            "here",
                            href="https://github.com/divin/kanji-crush?tab=readme-ov-file#limitations",
                            is_external=True,
                            underline="always",
                        ),
                        ".",
                    ),
                    _get_api_token_input(),
                    _get_level_selection(),
                    _get_random(),
                    rx.flex(
                        rx.drawer.close(
                            rx.button(
                                rx.html('<i class="fas fa-window-close"></i>'),
                                "Close",
                                font_size="1em",
                                on_click=Settings.toggle_drawer,
                                flex="1 1 50%",
                                width="100%",
                                disabled=Settings.is_not_valid,
                            )
                        ),
                        _get_reset_button(flex="1 1 50%"),
                        gap="1em",
                        direction="row",
                        flex="0 1 10%",
                    ),
                    rx.text(
                        "Issues? Feedback? Feature requests? Or just want to say hi? Feel free to open an issue on ",
                        rx.link(
                            "GitHub",
                            href="https://github.com/divin/kanji-crush/issues",
                            is_external=True,
                            underline="always",
                        ),
                        " or ",
                        rx.link(
                            "contact me",
                            href="mailto:hello@kanji-crush.com",
                            underline="always",
                        ),
                        ".",
                        font_size="0.75em",
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

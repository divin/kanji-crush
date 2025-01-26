from typing import Any

import reflex as rx

from kanji_crush.states import Game, Statistics


def _create_kanji_button(kanji: str) -> rx.Component:
    """Creates a button component with a kanji character.

    Parameters
    ----------
    kanji : str
        The kanji character to display on the button

    Returns
    -------
    rx.Component
        A button component with the kanji character and click handler
    """
    return rx.button(
        kanji,
        on_click=Game.check_answer(kanji),
        font_size="2.0em",
        padding="1em",
    )


def _create_stats_display(**props: dict[str, Any]) -> rx.Component:
    """Creates a statistics display component.

    This function creates a flex container displaying various game statistics including:
    - Current accuracy percentage
    - Number of correct answers
    - Number of incorrect answers
    - Number of remaining kanjis

    Returns
    -------
    rx.Component
        A flex container component with statistics text elements
    """
    return rx.flex(
        rx.text(f"👍 {Statistics.current_accuracy}%"),
        rx.text(f"✅ {Statistics.number_of_correct_answers}"),
        rx.text(f"❎ {Statistics.number_of_incorrect_answers}"),
        rx.text(f"🗂️ {Statistics.number_of_kanjis_left}"),
        gap="1em",
        justify="between",
        direction="row",
        **props,
    )


def _create_progress_section(**props: dict[str, Any]) -> rx.Component:
    """Creates a progress section component.

    This function creates a flex container with a progress bar and statistics display.
    The progress bar shows the current progress through the kanji game, while the
    statistics display shows various game metrics.

    Returns
    -------
    rx.Component
        A flex container component containing a progress bar and statistics display
    """
    return rx.flex(
        rx.progress(
            value=Game.current_index,
            max=Game.number_of_kanjis,
            size="3",
            color_scheme="green",
            flex="0 1 30%",
        ),
        _create_stats_display(flex="0 1 70%"),
        gap="0.5em",
        direction="column",
        **props,
    )


def _create_meaning_section(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.text("Meaning:", weight="bold"),
        rx.text(Game.current_meanings),
        gap="1em",
        direction="row",
        justify="center",
        **props,
    )


def _create_options_section(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.foreach(
            Game.current_options,
            _create_kanji_button,
        ),
        wrap="wrap",
        gap="0.5em",
        justify="center",
        padding="0.5em",
        **props,
    )


def _get_game(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        _create_progress_section(
            flex="0 1 5%",
        ),
        _create_meaning_section(
            flex="0 1 10%",
        ),
        _create_options_section(
            flex="1 0 85%",
        ),
        gap="1em",
        direction="column",
        padding="0.5em",
        **props,
    )


def _get_start_button(**props: dict[str, Any]) -> rx.Component:
    return rx.center(
        rx.button(
            rx.html('<i class="fas fa-play"></i>'),
            on_click=Game.start_game,
            font_size="2em",
            padding="1em",
        ),
        padding="0.5em",
        **props,
    )


def _create_download_button(**props: dict[str, Any]) -> rx.Component:
    return rx.button(
        rx.html('<i class="fas fa-download"></i>'),
        "Download Summary Table",
        on_click=Statistics.download_kanjis_csv,
        **props,
    )


def _create_restart_all_button(**props: dict[str, Any]) -> rx.Component:
    return rx.button(
        rx.html('<i class="fas fa-undo"></i>'),
        "Restart with current selection",
        on_click=Game.start_game,
        **props,
    )


def _create_restart_failed_button(**props: dict[str, Any]) -> rx.Component:
    return rx.button(
        rx.html('<i class="fas fa-undo"></i>'),
        "Restart with failed Kanjis",
        on_click=Game.restart_with_failed,
        **props,
    )


def _create_data_table(**props: dict[str, Any]) -> rx.Component:
    return rx.data_table(
        data=Statistics.kanjis_data,
        pagination=True,
        search=False,
        sort=True,
        **props,
    )


def _get_summary(**props: dict[str, Any]) -> rx.Component:
    return rx.flex(
        rx.flex(
            _create_progress_section(flex="0 1 10%", min_width="256px"),
            _create_download_button(flex="0 1 10%", min_width="256px"),
            # _create_restart_all_button(flex="0 1 10%", min_width="256px"),
            _create_restart_failed_button(flex="0 1 10%", min_width="256px"),
            direction="column",
            justify="center",
            align="center",
            gap="1em",
            width="100%",
            max_height="512px",
        ),
        gap="1em",
        width="100%",
        height="100%",
        padding="0.5em",
        justify="center",
        **props,
    )


def _get_game_over(**props: dict[str, Any]) -> rx.Component:
    return rx.cond(
        condition=Game.is_finished,
        c1=_get_summary(**props),
        c2=_get_start_button(**props),
    )


def get_game(**props: dict[str, Any]) -> rx.Component:
    return rx.cond(
        condition=Game.is_started, c1=_get_game(**props), c2=_get_game_over(**props)
    )

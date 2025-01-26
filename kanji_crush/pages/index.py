import reflex as rx

from kanji_crush.components.description import get_description
from kanji_crush.components.footer import get_footer
from kanji_crush.components.game import get_game
from kanji_crush.components.header import get_header


def index() -> rx.Component:
    return rx.container(
        rx.flex(
            get_header(
                flex="0 1 5%",
            ),
            get_description(
                flex="0 1 5%",
            ),
            get_game(
                flex="1 1 85%",
            ),
            get_footer(
                gap="0.75em",
                padding="1em",
                flex="0 1 5%",
            ),
            gap="0.75em",
            direction="column",
            width="100%",
            max_width="960px",
            height="100%",
            min_height="100svh",
        ),
        padding="0.5em",
        max_width="100svw",
        min_height="100svh",
    )

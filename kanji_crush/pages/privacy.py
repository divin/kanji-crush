import reflex as rx

from kanji_crush.components.footer import get_footer
from kanji_crush.components.header import get_header_without_menu
from kanji_crush.utilities import read_markdown_file


def privacy() -> rx.Component:
    content = read_markdown_file("content/privacy.md")
    return rx.container(
        rx.flex(
            get_header_without_menu(
                flex="0 1 5%",
            ),
            rx.markdown(
                content, text_align="justify", margin="1.0rem", padding="1.0rem"
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

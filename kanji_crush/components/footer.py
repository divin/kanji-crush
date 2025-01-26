from datetime import date
from typing import Any

import reflex as rx


def _get_site_end(seperator: str = "|", **props: Any) -> rx.Component:
    flex_props = {
        "gap": "0.5em",
        "direction": "row",
        "justify": "center",
        "align_items": "center",
        "align_content": "stretch",
    }
    return rx.center(
        rx.flex(
            rx.link(f"{date.today().strftime('%Y')} © Divin Gavran", href="/"),
            seperator,
            rx.link("Imprint", href="/imprint"),
            seperator,
            rx.link("Privacy Policy", href="/privacy"),
            **flex_props,
        ),
        **props,
    )


def get_footer(**props: Any) -> rx.Component:
    return rx.center(
        _get_site_end(font_size="0.85em"),
        **props,
    )

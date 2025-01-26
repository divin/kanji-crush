import reflex as rx

from kanji_crush.pages import imprint, index, privacy

style = {
    "color": "#eeeeee",
    "font_size": "1.0em",
    "font_family": "Lato",
    "font_weight": "400",
    "a": {
        "color": "#eeeeee",
    },
    "a:hover": {"color": "#2e6960"},
    "background_color": "#0a0c0b",
}

stylesheets = [
    "/css/reset.css",
    "/css/default.css",
    "/css/lato.css",
    "/css/fontawesome.css",
]

theme = rx.theme(
    color_mode="dark",
    appearance="dark",
    radius="medium",
    accent_color="green",
)

app = rx.App(
    theme=theme,
    style=style,
    stylesheets=stylesheets,
)

app.add_page(index, title="Kanji Crush", route="/")
app.add_page(privacy, title="Privacy", route="/privacy")
app.add_page(imprint, title="Imprint", route="/imprint")

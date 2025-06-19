import reflex as rx
from app.components.cards import form_card
from app.components.input import (btn_icon, btn_text_icon, field_style,
                                  form_header, std_input)
from app.components.selects import player_select
from app.states.upload import UploadState
from app.templates import template


def files_badge(file) -> rx.Component:
    return rx.badge(
        rx.hstack(
            rx.icon("file-text", size=18, stroke_width=1.5),
            rx.text(rx.text.strong(file), size="6"),
            align="center",
            spacing="2",
        ),
        variant="soft",
        high_contrast=True,
    )


def player_selection(player_n):
    return rx.hstack(
        rx.cond(
            UploadState.unknowns[player_n - 1],
            rx.select(
                ["Sconosciuto"],
                value="Sconosciuto",
                disabled=True,
                **field_style | {"width": "88%"},
            ),
            player_select(
                UploadState,
                f"Giocatore {player_n}",
                field_style | {"width": "88%"},
                field_style | {"width": "88%"},
            ),
        ),
        btn_icon(
            rx.cond(UploadState.unknowns[player_n - 1], "user-plus", "user-x"),
            on_click=lambda: UploadState.toggle_player(player_n - 1),
            type="button",
            variant="soft",
        ),
        align="center",
        width="100%",
    )


def form_upload() -> rx.Component:
    return rx.vstack(
        form_card(
            rx.flex(
                form_header(
                    "chart-pie",
                    "Upload delle statistiche",
                    (
                        "Carica i file ",
                        rx.code("stats.json"),
                        " e ",
                        rx.code("insights.json"),
                        " per visualizzare l'analisi della partita",
                    ),
                ),
                rx.divider(),
                rx.form(
                    rx.vstack(
                        std_input(
                            "file-text",
                            "File Statistiche",
                            rx.upload(
                                rx.vstack(
                                    btn_text_icon(
                                        "pointer",
                                        "Seleziona file",
                                        text_size="4",
                                        icon_w=2,
                                        variant="soft",
                                        spacing="2",
                                    ),
                                    rx.text(
                                        "Trascina i file o clicca per selezionare ",
                                        rx.text.strong("le statistiche"),
                                        " da inviare",
                                    ),
                                    rx.callout(
                                        "Il sistema accetta solo file di tipo JSON",
                                        icon="info",
                                        size="1",
                                        variant="surface",
                                    ),
                                    align="center",
                                ),
                                id="upload-form",
                                multiple=True,
                                accept={"application/json": [".json"]},
                                padding="2em",
                                width="100%",
                            ),
                        ),
                        rx.cond(
                            rx.selected_files("upload-form"),
                            rx.hstack(
                                rx.foreach(
                                    rx.selected_files("upload-form"), files_badge
                                ),
                                rx.button(
                                    rx.icon("x", size=16, stroke_width=1.5),
                                    on_click=rx.clear_selected_files("upload-form"),
                                    color_scheme="tomato",
                                    variant="outline",
                                ),
                                align="center",
                                justify="center",
                                width="80%",
                            ),
                        ),
                        btn_text_icon(
                            "cloud-upload",
                            "Carica file",
                            text_size="4",
                            on_click=[
                                UploadState.upload(
                                    rx.upload_files(
                                        upload_id="upload-form",
                                        on_upload_progress=UploadState.upload_progress,
                                    ),
                                ),
                                UploadState.clear_file,
                            ],
                            disabled=rx.cond(
                                rx.selected_files("upload-form"), False, True
                            ),
                            **field_style,
                        ),
                        rx.cond(
                            UploadState.progress > 0,
                            rx.progress(value=UploadState.progress, max=100),
                        ),
                        spacing="5",
                        align="center",
                    ),
                    reset_on_submit=True,
                    width="100%",
                ),
                width="100%",
                spacing="4",
                flex_direction="column",
            )
        ),
        spacing="5",
        width="100%",
    )


def form_name() -> rx.Component:
    return rx.vstack(
        form_card(
            rx.flex(
                form_header(
                    "chart-pie",
                    "Upload delle statistiche",
                    (
                        "Aggiorni i dati della partita con ",
                        rx.code("nome"),
                        " e ",
                        rx.code("giocatori"),
                    ),
                ),
                rx.divider(),
                rx.form(
                    rx.vstack(
                        std_input(
                            "trophy",
                            "Nome della Partita",
                            rx.input(
                                placeholder="Nome della partita",
                                name="name",
                                **field_style,
                            ),
                        ),
                        std_input(
                            "calendar",
                            "Data della Partita",
                            rx.hstack(
                                rx.input(type="date", name="date", **field_style),
                                rx.input(type="time", name="time", **field_style),
                                width="100%",
                            ),
                        ),
                        rx.hstack(
                            std_input(
                                "users",
                                "Squadra 1",
                                rx.vstack(
                                    player_selection(1),
                                    rx.cond(
                                        UploadState.players_n == 4, player_selection(2)
                                    ),
                                    width="100%",
                                ),
                            ),
                            rx.text("VS", size="7"),
                            std_input(
                                "users",
                                "Squadra 2",
                                rx.vstack(
                                    player_selection(3),
                                    rx.cond(
                                        UploadState.players_n == 4, player_selection(4)
                                    ),
                                    width="100%",
                                ),
                            ),
                            spacing="3",
                            align="center",
                            justify_content=["center", "center", "justify"],
                            width="100%",
                        ),
                        btn_text_icon(
                            "circle-plus",
                            "Inserisci dati",
                            type="submit",
                            **field_style,
                        ),
                        rx.divider(),
                        rx.text(
                            "Se ",
                            rx.text.strong("non"),
                            " trovi il giocatore, aggiungilo",
                        ),
                        rx.hstack(
                            rx.input(
                                placeholder="Nome del Giocatore",
                                value=UploadState.player_name,
                                on_change=UploadState.set_player_name,
                                **field_style,
                            ),
                            rx.input(
                                placeholder="Cognome del giocatore",
                                value=UploadState.player_surname,
                                on_change=UploadState.set_player_surname,
                                **field_style,
                            ),
                            btn_icon(
                                "circle-plus",
                                on_click=UploadState.add_player,
                                type="button",
                                variant="soft",
                            ),
                            width="100%",
                            align="center",
                        ),
                        spacing="5",
                        align="center",
                    ),
                    on_submit=UploadState.submit,
                    width="100%",
                ),
                width="100%",
                spacing="4",
                flex_direction="column",
            )
        ),
        spacing="5",
        width="100%",
    )


@template(
    route="/upload",
    title="Upload",
    on_load=UploadState.on_load,
)
def home_page() -> rx.Component:
    return rx.cond(UploadState.uploaded, form_name(), form_upload())

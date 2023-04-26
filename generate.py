import dash_bootstrap_components as dbc

from dash import html, dcc


def parse_img(img):
    res = html.Div(
        [
            html.Img(
                src=img,
                style={
                    "height": "4.5cm",
                    "width": "4.5cm",
                },
            ),
        ],
        id="content-style"
    )
    return res


def transfer_img(img):
    res = dbc.Container(
        [
            dbc.Row(
                dcc.Graph(
                    figure=img,
                    style={
                        "height": "9.5cm",
                    }
                ),
                align="center",
            )
        ],
        id="result",
        style={
            "margin": "auto",
        }
    )
    return res

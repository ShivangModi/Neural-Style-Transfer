import dash_bootstrap_components as dbc
from dash import html, dcc

symbol = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

# img
logo = html.Img(src=symbol, height="35px")

# NavbarBrand
navbar_brand = dbc.NavbarBrand(
    "Image Style Transfer",
    className="ms-3",
    style={
        "font-size": "20px",
    },
)

# logo
header_contains = dbc.Row(
    [
        dbc.Col(
            [
                logo,
                navbar_brand,
            ],
        ),
    ],
    align="center",
    className="g-0",
)

# card header
card_header = dbc.CardHeader(
    [
        html.A(
            header_contains,
            href='/',
            style={
                "textDecoration": "none",
            },
        ),
    ],
)

# carousel
carousel = dbc.Carousel(
    items=[
        {
            "key": "1",
            "src": "https://images.plot.ly/logo/new-branding/plotly-logomark.png",
            "header": "With header ",
            "caption": "and caption",
        },
        {
            "key": "2",
            "src": "https://images.plot.ly/logo/new-branding/plotly-logomark.png",
            "header": "With header only",
            "caption": "",
        },
        {
            "key": "3",
            "src": "https://images.plot.ly/logo/new-branding/plotly-logomark.png",
            "header": "",
            "caption": "This slide has a caption only",
        },
    ],
    variant="dark",
    className="carousel-fade",
    style={
        "color": "black",
    }
)

# card_carousel
card_carousel = dbc.Card(
    [
        dbc.CardBody(
            [
                carousel,
            ],
            # style={
            #     "padding": "15px",
            #     "align": "center",
            # }
        ),
    ],
    style={
        "height": "825px",
    }
)

# tab
tab = dbc.Tabs(
    [
        dbc.Tab(label="Fast Style Transfer", tab_id="fast-style", tab_style={"marginLeft": "auto"}),
        dbc.Tab(label="Custom Style Transfer", tab_id="custom-style"),
    ],
    id="card-tabs",
    active_tab="fast-style",
)

# upload content img
upload_content = dbc.Card(
    [
        dbc.CardHeader(
            [
                dcc.Upload(
                    [
                        html.Div(
                            [
                                "Content: ",
                                html.A("select image"),
                            ],
                        ),
                    ],
                    id="upload-content",
                    style={
                        'lineHeight': '25px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '2px',
                    },
                ),
            ],
        ),
        dbc.CardBody(
            id="output-uploaded-content",
            style={
                "height": "5cm",
                "margin-left": "auto",
                "margin-right": "auto",
                "padding": "10px",
            }
        ),
    ],
)

# upload style img
upload_style = dbc.Card(
    [
        dbc.CardHeader(
            [
                dcc.Upload(
                    [
                        html.Div(
                            [
                                "Style: ",
                                html.A("select image"),
                            ],
                        ),
                    ],
                    id="upload-style",
                    style={
                        'lineHeight': '25px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'textAlign': 'center',
                        'margin': '2px',
                    },
                ),
            ],
        ),
        dbc.CardBody(
            id="output-uploaded-style",
            style={
                "height": "5cm",
                "margin-left": "auto",
                "margin-right": "auto",
                "padding": "10px",
            }
        ),
    ],
)

# result of style transfer
result = dbc.Card(
    [
        dbc.CardHeader(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("⍺:", style={"margin-right": "15px", "font-size": "20px"}),
                                dcc.Input(type="number", min=1, max=10, step=1, placeholder="1-11", size="md", id="alpha",
                                          style={"margin-right": "15px", "font-size": "15px", "width": "100px",
                                                 'background-color': 'rgba(0,0,0,0.0)', 'border-color': 'white'}),
                                dbc.Label("ℬ:", style={"margin-right": "15px", "font-size": "20px"}),
                                dcc.Input(type="number", min=0.01, max=0.1, step=0.01, placeholder="0.001-1", size="md",
                                          id="beta",
                                          style={"font-size": "15px", "width": "100px",
                                                 'background-color': 'rgba(0,0,0,0.0)', 'border-color': 'white'}),
                            ],
                            id="custom",
                        ),
                        dbc.Col(
                            dbc.Button("Transfer", id="transfer-btn", size="sm", color="primary")
                        ),
                    ]
                )
            ],
            id="result-header",
        ),
        dbc.CardBody(
            id="result-body",
            style={
                "height": "11cm",
            }
        ),
    ],
)

# card_image
card_image = dbc.Card(
    [
        dbc.CardHeader(tab),
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(upload_content),
                        dbc.Col(upload_style),
                    ],
                    style={
                        "margin-bottom": "15px",
                    }
                ),
                dbc.Row(
                    [
                        dbc.Col(result),
                    ],
                ),
            ],
            style={
                "padding": "15px",
            }
        ),
    ],
    style={
        "height": "825px",
    }
)

# card body
card_body = dbc.CardBody(
    [
        dbc.Row(
            [
                dbc.Col(card_carousel),
                dbc.Col(card_image),
            ],
        ),
    ],

)

# main_layout
main_layout = dbc.Card(
    [
        card_header,
        card_body,
    ],
    style={
        "margin": "25px",
        "height": "25cm",
        # "height": "100vh",
    },
)

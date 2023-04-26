import dash
import dash_bootstrap_components as dbc
import plotly.express as px

from dash import Input, Output, State

from components import main_layout
from generate import parse_img, transfer_img
from FastStyleTransfer import FastStyleTransfer
from CustomStyleTransfer import CustomStyleTransfer

# Initializing dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.QUARTZ,
    ],
    title="Image Style Transfer",
)

app.layout = main_layout


@app.callback(
    Output('output-uploaded-content', 'children'),
    Input('upload-content', 'contents'),
)
@app.callback(
    Output('output-uploaded-style', 'children'),
    Input('upload-style', 'contents'),
)
def update_output(img):
    if img is not None:
        return parse_img(img)


@app.callback(
    Output('custom', 'style'),
    Input('card-tabs', 'active_tab')
)
def render_header(tab):
    if tab == "fast-style":
        return {"display": "none"}
    elif tab == "custom-style":
        return {"display": "block"}


@app.callback(
    Output('result-body', 'children'),
    [
        Input('transfer-btn', 'n_clicks'),
        Input('alpha', 'value'),
        Input('beta', 'value')
    ],
    [
        State('upload-content', 'contents'),
        State('upload-style', 'contents'),
        State('card-tabs', 'active_tab')
    ]
)
def update_result(transfer, alpha, beta, content, style, tab):
    # fetching context to determine which button triggered callback
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if transfer and trigger == "transfer-btn":
        if content and style:
            if tab == 'fast-style':
                fst = FastStyleTransfer()
                img = fst.predict(content, style)
                fig = px.imshow(img)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=0, b=0, l=0, r=0),
                    xaxis=dict(
                        showgrid=False,
                        showticklabels=False,
                        linewidth=0
                    ),
                    yaxis=dict(
                        showgrid=False,
                        showticklabels=False,
                        linewidth=0
                    ),
                    hovermode=False
                )
                return transfer_img(fig)
            if tab == 'custom-style':
                cst = CustomStyleTransfer(content, style, alpha, beta)
                fig = None
                for n in range(cst.epochs):
                    for m in range(cst.batch):
                        cst.train_step()
                        fig = cst.tensor_to_image()
                fig = px.imshow(fig)
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    margin=dict(t=0, b=0, l=0, r=0),
                    xaxis=dict(
                        showgrid=False,
                        showticklabels=False,
                        linewidth=0
                    ),
                    yaxis=dict(
                        showgrid=False,
                        showticklabels=False,
                        linewidth=0
                    ),
                    hovermode=False
                )
                return transfer_img(fig)
        else:
            no = 1
            if (not content) and (not style):
                no = 'both'
            msg = f'You have not uploaded {no} image!!!'
            alert = dbc.Alert(
                msg,
                id="alert-fade",
                color="primary",
                dismissable=True
            )
            return alert


if __name__ == '__main__':
    app.run_server(debug=True)

from dash import Dash, dcc, html
from map import get_map_figure
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    className='d-flex flex-column justify-content-center align-items-center',
    children=[
    html.Div(children='International Students in Europe'),
    html.Div([
        dcc.Graph(
            figure=get_map_figure(),
            style={"width": "100%", "height": "100%"}
        )
    ])
])

if __name__ == '__main__':
    app.run(debug=True)
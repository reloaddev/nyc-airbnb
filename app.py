from dash import Dash, dcc, html, Input, Output
from map import get_map_figure
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container(
    className='d-flex flex-column justify-content-center align-items-center',
    children=[
    html.Div(children='International Students in Europe'),
    html.Div([
        dcc.Graph(
            id='map-graph',
            figure=get_map_figure(),
            style={"width": "100%", "height": "100%"}
        )
    ])
])

@app.callback(
    Output('map-graph', 'figure'),
    Input('map-graph', 'hoverData')
)
def highlight_country(hoverData):
    if hoverData is not None:
        country_id = hoverData['points'][0]['location']
    else:
        country_id = None
    return get_map_figure(highlighted_country=country_id)

if __name__ == '__main__':
    app.run(debug=True)
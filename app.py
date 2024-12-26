import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

from components.area_select import create_area_select
from components.map import create_map
from components.neighbourhood_distribution import get_nyc_neighbourhood_distribution
from components.price_distribution import get_nyc_price_distribution
from components.price_rating import update_price_rating_scatter
from data import df

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dcc.Store(id="app-state", data="neighborhood_view"),
        dbc.Row([
            dbc.Col(html.H1("New York Airbnb Data Analysis"), width=9),
            dbc.Col(create_area_select(), width=3),
        ], style={"margin": "2rem"}),
        dbc.Row([
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id="interactive-map",
                        figure=create_map(),
                    ),
                ]),
                html.Div([
                    dcc.Graph(
                        id="price-rating-line-chart",
                        figure=update_price_rating_scatter("New York City"),
                    )
                ])
            ], width=6),
            dbc.Col([
                html.Div([
                    dcc.Graph(
                        id="interactive-pie-chart",
                        figure=get_nyc_neighbourhood_distribution(),
                    )
                ]),
                html.Div([
                    dcc.Graph(
                        id="violin-plot",
                        figure=get_nyc_price_distribution(df)
                    ),
                ])
            ], width=6)
        ])
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

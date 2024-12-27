import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

from components.area_select import create_area_select
from components.map import create_map
from components.neighbourhood_distribution import get_nyc_neighbourhood_distribution
from components.price_distribution import get_nyc_price_distribution
from components.price_rating import update_price_rating_scatter
from components.room_type_distribution import get_room_type_distribution_bar_chart
from data import df

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dcc.Store(id="app-state", data="neighborhood_view"),
        dbc.Row([
            dbc.Col(html.H1("New York Airbnb Data Analysis"), width=9),
            dbc.Col(create_area_select(), width=3),
        ], style={"margin": "2rem"}),
        dbc.Col([
            dbc.Row([
                html.Div([
                    dcc.Graph(
                        id="interactive-map",
                        figure=create_map(),
                    ),
                ], style={"width": "50%"}),
                html.Div([
                    dcc.Graph(
                        id="interactive-pie-chart",
                        figure=get_nyc_neighbourhood_distribution(),
                    )
                ], style={"width": "50%"}),
            ]),
            dbc.Row([
                html.Div([
                    dcc.Graph(
                        id="price-rating-line-chart",
                        figure=update_price_rating_scatter("New York City"),
                    )
                ], style={"width": "33%"}),
                html.Div([
                    dcc.Graph(
                        id="room-type-distro-chart",
                        figure=get_room_type_distribution_bar_chart("New York City"),
                    )
                ], style={"width": "33%"}),
                html.Div([
                    dcc.Graph(
                        id="violin-plot",
                        figure=get_nyc_price_distribution(df)
                    ),
                ], style={"width": "33%"})
            ])
        ], width=12),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)

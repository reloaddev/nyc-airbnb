import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

from components.area_select import create_area_select
from components.neighbourhood_distribution import create_pie_chart
from components.map import create_map
from components.price_distribution import create_violin_plot
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
                html.H3(
                    "Interactive Map",
                    style={"textAlign": "center"},
                ),
                html.Div([
                    dcc.Graph(
                        id="interactive-map",
                        figure=create_map(),
                    ),
                ])
            ], width=6),
            dbc.Col([
                html.H3(
                    "Interactive Pie Chart & Violin Plot Dashboard",
                    style={"textAlign": "center"},
                ),
                html.Div([
                    dcc.Graph(
                        id="interactive-pie-chart",
                        figure=create_pie_chart(),
                    )
                ]),
                html.Hr(),
                html.Div([
                    html.H3(
                        "Apartment Price Distribution",
                        style={"textAlign": "center"},
                    ),
                    dcc.Graph(
                        id="violin-plot",
                        figure=create_violin_plot(
                            df, "Overall Price Distribution", "Overall"
                        ),
                    ),
                ])
            ], width=6)
        ])
    ]
)


if __name__ == "__main__":
    app.run_server(debug=True)

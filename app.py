from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
from data import df
from components.map import create_map
from components.district_distribution import create_pie_chart
from components.price_distribution import create_violin_plot

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


app.layout = html.Div(
    [
        dcc.Store(id="app-state", data="neighborhood_view"),
        dbc.Row(
            dbc.Col(
                html.H1(
                    "New York Airbnb Data Analysis",
                    style={
                        "textAlign": "center",
                        "margin": "20px",
                        "margin-bottom": "40px",
                    },
                ),
            )
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3(
                            "Interactive Map",
                            style={"textAlign": "center"},
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="interactive-map",
                                    figure=create_map(),
                                ),
                            ]
                        )
                    ]
                    
                    , width=6),
                dbc.Col(
                    [
                        html.H3(
                            "Interactive Pie Chart & Violin Plot Dashboard",
                            style={"textAlign": "center"},
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    id="interactive-pie-chart",
                                    figure=create_pie_chart(),
                                ),
                                html.Button(
                                    "Back",
                                    id="back-button",
                                    n_clicks=0,
                                    style={
                                        "display": "none"
                                    }
                                ),
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H3(
                                    "Apartment Price Distribution",
                                    style={"textAlign": "center"},
                                ),
                                dcc.Dropdown(
                                    id="neighbourhood-group-dropdown",
                                    options=[
                                        {"label": group, "value": group}
                                        for group in sorted(
                                            df["neighbourhood_group"].unique()
                                        )
                                    ],
                                    placeholder="Select a Neighbourhood Group",
                                    style={"width": "50%", "margin": "auto"},
                                ),
                                dcc.Graph(
                                    id="violin-plot",
                                    figure=create_violin_plot(
                                        df, "Overall Price Distribution", "Overall"
                                    ),
                                ),
                            ]
                        ),
                    ],
                    width=6,
                ),
            ]
        ),
    ]
)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

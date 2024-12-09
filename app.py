from dash import Dash, dcc, html
from data import df
from components.district_distribution import get_pie_chart
from components.price_distribution import create_violin_plot

app = Dash(__name__)


app.layout = html.Div([
    html.H1(
        "Interactive Pie Chart & Violin Plot Dashboard",
        style={'textAlign': 'center'}
    ),
    html.Div([
        dcc.Graph(
            id='interactive-pie-chart',
            figure=get_pie_chart()
        ),
        html.Button(
            'Back',
            id='back-button',
            n_clicks=0,
            style={'display': 'none'}  # Placeholder for future functionality
        )
    ]),
    html.Hr(),
    html.Div([
        html.H2(
            "Apartment Price Distribution",
            style={'textAlign': 'center'}
        ),
        dcc.Dropdown(
            id='neighbourhood-group-dropdown',
            options=[{'label': group, 'value': group} for group in sorted(df['neighbourhood_group'].unique())],
            placeholder="Select a Neighbourhood Group",
            style={'width': '50%', 'margin': 'auto'}
        ),
        dcc.Graph(
            id='violin-plot',
            figure=create_violin_plot(df, "Overall Price Distribution", "Overall")
        )
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

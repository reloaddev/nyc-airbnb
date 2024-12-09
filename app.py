import pandas as pd
import matplotlib.pyplot as plt
import pandas as pd
from data import df
from dash import Dash, dcc, html, Input, Output, State  # Added State to imports
import plotly.express as px
from config import color_mapping
from components.district_distribution import get_pie_chart

 
header = df.columns
 
# Remove outliers based on the Interquartile Range (IQR)
Q1 = df['price'].quantile(0.25)
Q3 = df['price'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
 
# Filter the dataset
filtered_df = df[(df['price'] >= lower_bound) & (df['price'] <= upper_bound)]
 
# Create the Dash app
app = Dash(__name__)
 
app.layout = html.Div([
    html.H1("Interactive Pie Chart & Violin Plot Dashboard", style={'textAlign': 'center'}),
    # Pie chart section
    html.Div([
        dcc.Graph(id='interactive-pie-chart', figure=get_pie_chart()),
        html.Button('Back', id='back-button', n_clicks=0, style={'display': 'none'})
    ]),
    html.Hr(),
    # Violin plot section
    html.Div([
        html.H2("Apartment Price Distribution", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='neighbourhood-group-dropdown',
            options=[{'label': group, 'value': group} for group in df['neighbourhood_group'].unique()],
            placeholder="Select a Neighbourhood Group",
            style={'width': '50%', 'margin': 'auto'}
        ),
        dcc.Graph(id='violin-plot')
    ])
])

 
@app.callback(
    Output('violin-plot', 'figure'),
    Input('neighbourhood-group-dropdown', 'value')
)
def update_violin_plot(selected_group):
    if selected_group:
        filtered_data = filtered_df[filtered_df['neighbourhood_group'] == selected_group]
        title = f"Price Distribution in {selected_group}"
    else:
        # When "Overall" is selected (no neighbourhood is selected), combine all data
        filtered_data = filtered_df
        title = "Overall Price Distribution"
        selected_group = 'Overall'  # Set the color to 'Overall' for the combined case
 
    # If "Overall" is selected, merge all data into a single violin plot
    if selected_group == 'Overall':
        fig = px.violin(
            filtered_data,
            x='price',  # Horizontal violin plot
            box=True,  # Include box plot within violin
            points=None,  # Remove scatter points
            title=title,
            labels={'price': 'Price per night'},
            hover_data=['neighbourhood', 'room_type'],
            color_discrete_sequence=[color_mapping['Overall']]  # Use unique color for overall
        )
    else:
        # When a specific neighbourhood group is selected, create individual violins
        fig = px.violin(
            filtered_data,
            x='price',  # Horizontal violin plot
            box=True,  # Include box plot within violin
            points=None,  # Remove scatter points
            title=title,
            labels={'price': 'Price per night'},
            hover_data=['neighbourhood', 'room_type'],
            color='neighbourhood_group',  # Apply color based on neighbourhood group
            color_discrete_map=color_mapping  # Apply custom color mapping
        )
 
    # Remove wallpaper and set the background to white
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray'
        ),
        yaxis=dict(
            showgrid=True,       
            gridcolor='lightgray'
        )  
    )

    return fig
 

if __name__ == '__main__':
    app.run_server(debug=True)
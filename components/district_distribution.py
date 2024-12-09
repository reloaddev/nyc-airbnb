from dash import Input, Output, State, callback
import plotly.express as px
from data import df
from config import color_mapping


neighbourhood_group_data = df['neighbourhood_group'].value_counts().reset_index()
neighbourhood_group_data.columns = ['neighbourhood_group', 'listings_count']
neighbourhood_group_data['percentage'] = (neighbourhood_group_data['listings_count'] /
                                          neighbourhood_group_data['listings_count'].sum()) * 100

def create_pie_chart():
    pie_chart = px.pie(
        neighbourhood_group_data,
        names='neighbourhood_group',
        values='percentage',
        title="Percentage of Listings by Neighbourhood Group",
        hover_data=['listings_count'],
        labels={'percentage': '% Listings'},
        color='neighbourhood_group',
        color_discrete_map=color_mapping
    )
    pie_chart.update_traces(textposition='outside', textinfo='percent+label')  # Move percentage outside
    return pie_chart

@callback(
    [Output('interactive-pie-chart', 'figure'),  
     Output('back-button', 'style')],  
    [Input('interactive-pie-chart', 'clickData'),  
     Input('back-button', 'n_clicks')],  
    [State('interactive-pie-chart', 'figure')]  
)
def update_pie_chart(click_data, n_clicks, current_figure):
    # If the back button is clicked, reset to the initial pie chart
    if n_clicks > 0:
        fig = create_pie_chart()
        return fig, {'display': 'none'}
    if click_data:
        selected_group = click_data['points'][0]['label'] 
        filtered_data = df[df['neighbourhood_group'] == selected_group]
        room_type_data = filtered_data['room_type'].value_counts().reset_index()
        room_type_data.columns = ['room_type', 'count']
        room_type_data['percentage'] = (room_type_data['count'] /
                                        room_type_data['count'].sum()) * 100
        fig = px.pie(
            room_type_data,
            names='room_type',
            values='percentage',
            title=f"Percentage of Room Types in {selected_group}",
            hover_data=['count'],
            labels={'percentage': '% Room Types'},
            color='room_type',
            color_discrete_map=color_mapping
        )
        fig.update_traces(textposition='outside', textinfo='percent+label')
        return fig, {'display': 'inline-block'}
    return current_figure, {'display': 'none'}

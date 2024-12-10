from dash import Input, Output, State, callback
import plotly.express as px
from data import df
from config import color_mapping


neighbourhood_group_data = df['neighbourhood_group'].value_counts().reset_index()
neighbourhood_group_data.columns = ['neighbourhood_group', 'calculated_host_listings_count']
neighbourhood_group_data['percentage'] = (neighbourhood_group_data['calculated_host_listings_count'] /
                                          neighbourhood_group_data['calculated_host_listings_count'].sum()) * 100


def create_pie_chart():
    pie_chart = px.pie(
        neighbourhood_group_data,
        names='neighbourhood_group',
        values='percentage',
        title="Percentage of Listings by Neighbourhood Group",
        hover_data=['calculated_host_listings_count'],
        labels={'percentage': '% Listings'},
        color='neighbourhood_group',
        color_discrete_map=color_mapping
    )
    pie_chart.update_traces(textposition='outside', textinfo='percent+label')
    return pie_chart


@callback(
    [Output('interactive-pie-chart', 'figure'),  
     Output('back-button', 'style'),
     Output('back-button', 'n_clicks'),
     Output('app-state', 'data')],  
    [Input('interactive-pie-chart', 'clickData'),
     Input('back-button', 'n_clicks')],
    [State('app-state', 'data')]
)
def update_pie_chart(click_data, n_clicks, app_state):
    # Reset to the main pie chart if the back button is clicked
    if app_state == 'room_type_view' and n_clicks > 0:
        return create_pie_chart(), {'display': 'none'}, 0, 'neighborhood_view' # 0 for resetting click count of the back button

    # Drill down into room types when a pie slice is clicked
    if app_state == 'neighborhood_view' and click_data:
        selected_group = click_data['points'][0]['label']  # Extract selected neighborhood group
        filtered_data = df[df['neighbourhood_group'] == selected_group]

        # Prepare data for room type breakdown
        room_type_data = filtered_data['room_type'].value_counts().reset_index()
        room_type_data.columns = ['room_type', 'count']
        room_type_data['percentage'] = (room_type_data['count'] /
                                        room_type_data['count'].sum()) * 100

        # Create a detailed pie chart for room types
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
        return fig, {'display': 'inline-block'}, 0, 'room_type_view'

    # Default: return the current figure and hide the back button (fallback)
    return create_pie_chart(), {'display': 'none'}, 0, 'neighborhood_view'

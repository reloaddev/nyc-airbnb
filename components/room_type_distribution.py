from dash import Input, Output, callback
import plotly.express as px

from config import color_mapping_nyc
from data import df
from util.filters import filter_by_neighbourhood_group

df_copy = df.copy()

@callback(
    Output('room-type-distro-chart', 'figure'),
    Input('area-select', 'value')
)
def get_room_type_distribution_bar_chart(selected_area):
    filtered_data = filter_by_neighbourhood_group(df_copy, neighbourhood_group=selected_area, threshold=0.03)
    bar_color = color_mapping_nyc.get(selected_area, "#6a5acd")
    bar_chart = px.bar(
        filtered_data,
        x="room_type",
        title=f"Distribution of room types",
        color_discrete_sequence=[bar_color]
    )
    bar_chart.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        xaxis_title="Room Type",
        yaxis_title="Count"
    )
    return bar_chart
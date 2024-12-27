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
    aggregated_data = filtered_data.groupby("room_type").size().reset_index(name="count")
    bar_color = color_mapping_nyc.get(selected_area, "#6a5acd")
    bar_chart = px.bar(
        aggregated_data,
        x="room_type",
        y="count",
        title=f"Distribution of room types"
    )
    bar_chart.update_traces(marker_color=bar_color, marker_line_color=bar_color, opacity=0.6)
    bar_chart.update_layout(
        showlegend=False,
        plot_bgcolor="white",
        xaxis_title="Room Type",
        yaxis_title="Count"
    )
    return bar_chart
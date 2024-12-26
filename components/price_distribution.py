import plotly.express as px
from dash import Input, Output, callback

from config import color_mapping
from data import df
from util.filters import filter_outliers

filtered_df = filter_outliers(df, 'price')


def create_violin_plot(data, title, color_key):
    return px.violin(
        data,
        x="price",
        box=True,
        points=None,
        title=title,
        labels={"price": "Price per night"},
        hover_data=["neighbourhood", "room_type"],
        color='neighbourhood_group' if color_key != "Overall" else None,
        color_discrete_sequence=[color_mapping["Overall"]] if color_key == "Overall" else None,
        color_discrete_map=color_mapping if color_key != "Overall" else None,
    )


@callback(
    Output('violin-plot', 'figure'),
    Input('area-select', 'value')
)
def update_violin_plot(selected_group):
    if selected_group == "New York City":
        filtered_data = filtered_df
        title = "Overall Price Distribution"
    else:
        selected_group = 'New York City'
        filtered_data = filtered_df[filtered_df['neighbourhood_group'] == selected_group]
        title = f"Price Distribution in {selected_group}"
    fig = create_violin_plot(filtered_data, title, selected_group)
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray')
    )
    return fig

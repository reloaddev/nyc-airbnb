import plotly.express as px
from dash import Input, Output, callback

from config import get_colors_for_neighborhood_group
from data import df
from util.filters import filter_outliers

filtered_df = filter_outliers(df, 'price')


def get_nyc_price_distribution(data):
    return px.violin(
        data,
        x="price",
        box=True,
        points=None,
        title='Distribution of prices',
        labels={"price": "Price per night in USD"},
        hover_data=["neighbourhood", "room_type"],
        color='neighbourhood_group',
        color_discrete_map=get_colors_for_neighborhood_group('New York City')
    )


@callback(
    Output('violin-plot', 'figure'),
    Input('area-select', 'value')
)
def get_neighbourhood_group_price_distribution(selected_group):
    if selected_group == "New York City":
        filtered_data = filtered_df
    else:
        filtered_data = filtered_df[filtered_df['neighbourhood_group'] == selected_group]
    fig = get_nyc_price_distribution(filtered_data)
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        width=700,
        height=450,
        margin=dict(t=50, b=50, l=50, r=50),
        showlegend=False
    )
    return fig

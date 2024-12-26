import plotly.express as px
from dash import Input, Output, callback

from data import df
from util.filters import filter_outliers

filtered_df = filter_outliers(df, 'price')


def get_nyc_price_distribution(data, title, color_key):
    return px.violin(
        data,
        x="price",
        box=True,
        points=None,
        title=title,
        labels={"price": "Price per night"},
        hover_data=["neighbourhood", "room_type"],
        color='neighbourhood_group' if color_key != "Overall" else None
    )


@callback(
    Output('violin-plot', 'figure'),
    Input('area-select', 'value')
)
def get_neighbourhood_group_price_distribution(selected_group):
    if selected_group == "New York City":
        filtered_data = filtered_df
        title = "Overall Price Distribution"
    else:
        filtered_data = filtered_df[filtered_df['neighbourhood_group'] == selected_group]
        title = f"Price Distribution in {selected_group}"
    fig = get_nyc_price_distribution(filtered_data, title, selected_group)
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        width=700,
        height=450,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    return fig

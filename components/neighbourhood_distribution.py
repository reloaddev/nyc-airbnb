import plotly.express as px
from dash import Input, Output, callback

from config import color_mapping_bronx, get_colors_for_neighborhood_group
from data import df
from util.filters import filter_by_neighbourhood_group


def get_nyc_neighbourhood_distribution():
    filtered_data = df.copy()
    total_count = len(filtered_data)
    filtered_data['group_count'] = filtered_data.groupby('neighbourhood_group')['neighbourhood_group'].transform('count')
    filtered_data['group_percentage'] = (filtered_data['group_count'] / total_count) * 100

    sunburst_chart = px.sunburst(
        filtered_data,
        names='neighbourhood_group',
        title="Distribution of apartments",
        path=['neighbourhood_group', 'neighbourhood'],
        color='neighbourhood_group',
        color_discrete_map=get_colors_for_neighborhood_group('New York City'),
        custom_data=['group_count', 'group_percentage', 'neighbourhood_group'],
    )
    sunburst_chart.update_traces(
        hovertemplate=(
            "<b>%{customdata[2]}</b><br>"
            "Count: %{customdata[0]}<br>"  # Group count
            "Percentage: %{customdata[1]:.2f}%<extra></extra>"
        ))
    sunburst_chart.update_layout(
        width=700,
        height=450,
        margin=dict(t=50, b=50, l=50, r=50),
        showlegend=False
    )
    return sunburst_chart


@callback(
    Output('interactive-pie-chart', 'figure'),
    Input('area-select', 'value')
)
def get_group_neighbourhood_distribution(selected_area):
    if selected_area == "New York City":
        return get_nyc_neighbourhood_distribution()
    filtered_data = df.copy()
    filtered_data = filter_by_neighbourhood_group(df=filtered_data, neighbourhood_group=selected_area, threshold=0.03)
    filtered_data.loc[:, 'absolute_count'] = filtered_data.groupby('neighbourhood')['neighbourhood'].transform('count')

    pie_chart = px.pie(
        filtered_data,
        names='neighbourhood',
        title=f"Distribution of apartments",
        hover_data=['absolute_count'],
        color='neighbourhood',
        color_discrete_map=get_colors_for_neighborhood_group(selected_area)
    )
    pie_chart.update_traces(
        textinfo='label',
        textposition='inside',
        hovertemplate='<b>%{label}</b><br>Count: %{customdata[0]}<br>Percentage: %{percent:.2%}<extra></extra>',
        customdata=filtered_data[['absolute_count']]
    )
    pie_chart.update_layout(
        width=700,
        height=450,
        margin=dict(t=50, b=50, l=50, r=50),
        showlegend=False
    )
    return pie_chart

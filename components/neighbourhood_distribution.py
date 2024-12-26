import plotly.express as px
from dash import Input, Output, callback

from config import color_mapping
from data import df
from util.filters import filter_by_neighbourhood_group


def get_nyc_neighbourhood_distribution():
    filtered_data = df.copy()
    pie_chart = px.sunburst(
        filtered_data,
        names='neighbourhood_group',
        title="Distribution of apartments by neighbourhood group and neighbourhood",
        path=['neighbourhood_group', 'neighbourhood'],
        color='neighbourhood_group',
        color_discrete_map=color_mapping
    )
    pie_chart.update_layout(
        width=900,
        height=600,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    return pie_chart


@callback(
    Output('interactive-pie-chart', 'figure'),
    Input('area-select', 'value')
)
def get_group_neighbourhood_distribution(selected_area):
    if selected_area == "New York City":
        return get_nyc_neighbourhood_distribution()
    filtered_data = filter_by_neighbourhood_group(df=df, neighbourhood_group=selected_area, threshold=0.03)
    filtered_data.loc[:, 'absolute_count'] = filtered_data.groupby('neighbourhood')['neighbourhood'].transform('count')

    pie_chart = px.pie(
        filtered_data,
        names='neighbourhood',
        title=f"Distribution of apartments by neighbourhood group and neighbourhood in {selected_area}",
        hover_data=['absolute_count'],
        color='neighbourhood',
        color_discrete_map=color_mapping
    )
    pie_chart.update_traces(
        hovertemplate='<b>%{label}</b><br>Absolute Count: %{customdata[0]}<extra></extra>',
        customdata=filtered_data[['absolute_count']]
    )
    return pie_chart

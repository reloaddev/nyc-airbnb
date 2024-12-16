import plotly.express as px
from dash import Input, Output, callback

from config import color_mapping
from data import df
from util.filters import filter_by_neighbourhood_group


def create_pie_chart():
    filtered_data = df.copy()
    filtered_data.loc[:, 'percentage'] = (
            filtered_data
            .groupby('neighbourhood_group')['neighbourhood_group']
            .transform('count') / len(filtered_data)
    )
    filtered_data.loc[:, 'absolute_count'] = (
        filtered_data
        .groupby('neighbourhood_group')['neighbourhood_group']
        .transform('count')
    )
    pie_chart = px.pie(
        filtered_data,
        names='neighbourhood_group',
        title="Percentage of listings by neighbourhood group",
        hover_data=['absolute_count'],
        color='neighbourhood_group',
        color_discrete_map=color_mapping
    )
    pie_chart.update_traces(
        hovertemplate='<b>%{label}</b><br>Absolute Count: %{customdata[0]}<extra></extra>',
        customdata=filtered_data[['absolute_count']]
    )
    return pie_chart


@callback(
    Output('interactive-pie-chart', 'figure'),
    Input('area-select', 'value')
)
def update_pie_chart(selected_area):
    if selected_area == "New York City":
        return create_pie_chart()
    filtered_data = filter_by_neighbourhood_group(df=df, neighbourhood_group=selected_area, threshold=0.03)
    filtered_data.loc[:, 'absolute_count'] = filtered_data.groupby('neighbourhood')['neighbourhood'].transform('count')

    pie_chart = px.pie(
        filtered_data,
        names='neighbourhood',
        title=f"Percentage of listings in {selected_area} by neighbourhood sub group",
        hover_data=['absolute_count'],
        color='neighbourhood',
        color_discrete_map=color_mapping
    )
    pie_chart.update_traces(
        hovertemplate='<b>%{label}</b><br>Absolute Count: %{customdata[0]}<extra></extra>',
        customdata=filtered_data[['absolute_count']]
    )
    return pie_chart

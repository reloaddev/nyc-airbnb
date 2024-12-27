import plotly.express as px
from dash import Input, Output, callback
from geopandas import GeoDataFrame
from shapely.geometry import Point

from config import get_colors_for_neighborhood_group
from data import df
from util.filters import filter_by_neighbourhood_group

df_copy = df.copy()
geometry = [Point(xy) for xy in zip(df_copy.longitude, df.latitude)]
gdf = GeoDataFrame(df_copy, crs="EPSG:4326", geometry=geometry)


def create_map():
    created_map = px.scatter_map(
        gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        title='Apartment locations',
        color='neighbourhood_group',
        color_discrete_map=get_colors_for_neighborhood_group('New York City'),
        size_max=50,
        zoom=9,
        custom_data=['neighbourhood_group', 'neighbourhood']
    )
    created_map.update_traces(
        hovertemplate=(
            "Neighborhood Group: %{customdata[0]}<br>"  # Group count
            "Neighborhood: %{customdata[1]}<br>"
        ))
    created_map.update_layout(
        width=700,
        height=450,
        margin=dict(t=50, b=50, l=50, r=50),
        showlegend=False
    )
    return created_map


@callback(
    Output('interactive-map', 'figure'),
    Input('area-select', 'value')
)
def update_map(selected_area):
    if selected_area == "New York City":
        return create_map()
    filtered_data = filter_by_neighbourhood_group(df=gdf, neighbourhood_group=selected_area, threshold=0.03)

    created_map = px.scatter_map(
        filtered_data,
        lat=filtered_data.geometry.y,
        lon=filtered_data.geometry.x,
        title=f"Apartment locations in {selected_area}",
        color='neighbourhood',
        color_discrete_map=get_colors_for_neighborhood_group(selected_area),
        size_max=50,
        zoom=11
    )
    created_map.update_layout(
        width=700,
        height=450,
        margin=dict(t=50, b=50, l=50, r=50),
        showlegend=False
    )
    return created_map

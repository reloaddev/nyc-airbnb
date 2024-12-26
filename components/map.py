import plotly.express as px
from dash import Input, Output, callback
from geopandas import GeoDataFrame
from shapely.geometry import Point

from data import df
from util.filters import filter_by_neighbourhood_group

geometry = [Point(xy) for xy in zip(df.longitude, df.latitude)]
df = df.drop(['longitude', 'latitude'], axis=1)
gdf = GeoDataFrame(df, crs="EPSG:4326", geometry=geometry)


def create_map():
    created_map = px.scatter_map(
        gdf,
        lat=gdf.geometry.y,
        lon=gdf.geometry.x,
        title="Apartment locations in New York City",
        color='neighbourhood_group',
        size_max=50,
        zoom=9
    )
    created_map.update_layout(
        width=700,
        height=450,
        margin=dict(t=50, b=50, l=50, r=50)
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
        size_max=50,
        zoom=11
    )
    created_map.update_layout(
        width=700,
        height=450,
        margin=dict(t=50, b=50, l=50, r=50)
    )
    return created_map
